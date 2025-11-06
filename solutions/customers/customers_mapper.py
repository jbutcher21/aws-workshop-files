#!/usr/bin/env python3
"""
Customers to Senzing JSON Mapper

Maps customer CSV records to Senzing JSON format for entity resolution.
Handles both PERSON and ORGANIZATION record types.

Usage:
    python3 customers_mapper.py input.csv -o output.jsonl
    python3 customers_mapper.py input.csv -o output.jsonl --sample 10
"""

import csv
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path


# Hard-coded DATA_SOURCE per mapping specification
DATA_SOURCE = "CUSTOMERS"


def parse_date(date_str):
    """
    Parse various date formats to YYYY-MM-DD standard.

    Handles: M/D/YY, M/D/YYYY, MM/DD/YYYY, D-MMM-YY, YYYY-MM-DD
    """
    if not date_str or not date_str.strip():
        return None

    date_str = date_str.strip()

    # Try MM/DD/YYYY
    try:
        dt = datetime.strptime(date_str, '%m/%d/%Y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        pass

    # Try M/D/YY (assumes 19xx for >50, 20xx for <=50)
    try:
        dt = datetime.strptime(date_str, '%m/%d/%y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        pass

    # Try D-MMM-YY
    try:
        dt = datetime.strptime(date_str, '%d-%b-%y')
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        pass

    # Already YYYY-MM-DD
    if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
        return date_str

    # If can't parse, return None
    return None


def parse_person_name(name_str):
    """
    Parse "Last, First Middle" format into components.

    Returns: (last, first, middle) tuple
    """
    if not name_str or ',' not in name_str:
        return (name_str.strip() if name_str else None, None, None)

    parts = name_str.split(',', 1)
    last = parts[0].strip()
    rest = parts[1].strip()

    rest_parts = rest.split()
    first = rest_parts[0] if rest_parts else None
    middle = ' '.join(rest_parts[1:]) if len(rest_parts) > 1 else None

    return (last, first, middle)


def map_customer_record(row):
    """
    Map a single customer CSV row to Senzing JSON format.

    Args:
        row: Dictionary from csv.DictReader

    Returns:
        Dictionary in Senzing JSON format
    """
    # Start with root-level fields
    record = {
        "DATA_SOURCE": DATA_SOURCE,
        "RECORD_ID": row['customer_id']
    }

    # Add payload attributes (always at root, use empty string if missing)
    customer_since_date = parse_date(row.get('registration_date', ''))
    if customer_since_date:
        record['CUSTOMER_SINCE_DATE'] = customer_since_date
    else:
        record['CUSTOMER_SINCE_DATE'] = ""

    record['ACCOUNT_STATUS'] = row.get('account_status', '').strip()
    record['ACCOUNT_BALANCE'] = row.get('account_balance', '').strip()
    record['CUSTOMER_TIER'] = row.get('customer_tier', '').strip()

    # Build FEATURES array
    features = []

    # RECORD_TYPE
    customer_type = row.get('customer_type', '').strip()
    if customer_type == 'I':
        record_type = "PERSON"
    elif customer_type == 'C':
        record_type = "ORGANIZATION"
    else:
        # Default to PERSON if not specified
        record_type = "PERSON"

    features.append({"RECORD_TYPE": record_type})

    # NAME
    customer_name = row.get('customer_name', '').strip()
    if customer_name:
        if record_type == "PERSON":
            # Parse "Last, First Middle"
            last, first, middle = parse_person_name(customer_name)
            name_feature = {"NAME_TYPE": "PRIMARY"}
            if last:
                name_feature['NAME_LAST'] = last
            if first:
                name_feature['NAME_FIRST'] = first
            if middle:
                name_feature['NAME_MIDDLE'] = middle
            features.append(name_feature)
        else:  # ORGANIZATION
            features.append({
                "NAME_TYPE": "PRIMARY",
                "NAME_ORG": customer_name
            })

    # DATE_OF_BIRTH (persons only, but include if present)
    dob = parse_date(row.get('dob', ''))
    if dob:
        features.append({"DATE_OF_BIRTH": dob})

    # GENDER
    gender = row.get('gender', '').strip()
    if gender:
        features.append({"GENDER": gender})

    # ADDRESS (group all components together)
    addr_feature = {}
    if row.get('address', '').strip():
        addr_feature['ADDR_LINE1'] = row['address'].strip()
    if row.get('city', '').strip():
        addr_feature['ADDR_CITY'] = row['city'].strip()
    if row.get('state', '').strip():
        addr_feature['ADDR_STATE'] = row['state'].strip()
    if row.get('zip_code', '').strip():
        addr_feature['ADDR_POSTAL_CODE'] = row['zip_code'].strip()
    if row.get('country', '').strip():
        addr_feature['ADDR_COUNTRY'] = row['country'].strip()

    if addr_feature:
        features.append(addr_feature)

    # PHONE
    phone = row.get('phone', '').strip()
    if phone:
        features.append({"PHONE_NUMBER": phone})

    # EMAIL
    email = row.get('email', '').strip()
    if email:
        features.append({"EMAIL_ADDRESS": email})

    # IDENTIFIERS (dynamic based on id_type)
    id_type = row.get('id_type', '').strip()
    id_number = row.get('id_number', '').strip()
    id_country = row.get('id_country', '').strip()

    if id_type and id_number:
        id_feature = {}

        if id_type == 'SSN':
            id_feature['SSN_NUMBER'] = id_number

        elif id_type == 'DRIVERS_LICENSE':
            id_feature['DRIVERS_LICENSE_NUMBER'] = id_number
            if id_country:
                id_feature['DRIVERS_LICENSE_STATE'] = id_country

        elif id_type == 'PASSPORT':
            id_feature['PASSPORT_NUMBER'] = id_number
            if id_country:
                id_feature['PASSPORT_COUNTRY'] = id_country

        elif id_type == 'NATIONAL_ID':
            id_feature['NATIONAL_ID_NUMBER'] = id_number
            if id_country:
                id_feature['NATIONAL_ID_COUNTRY'] = id_country

        if id_feature:
            features.append(id_feature)

    # Add FEATURES array to record
    record['FEATURES'] = features

    return record


def map_customers(input_file, output_file, sample=None, progress=False):
    """
    Map customer CSV to Senzing JSONL.

    Args:
        input_file: Path to input CSV
        output_file: Path to output JSONL
        sample: Optional number of records to process (for testing)
        progress: Show progress output
    """
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_file}", file=sys.stderr)
        return 1

    records_processed = 0
    records_written = 0

    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile)

            if progress:
                print(f"Reading from: {input_file}")
                print(f"Writing to: {output_file}")
                if sample:
                    print(f"Sample mode: Processing first {sample} records")
                print()

            for row in reader:
                records_processed += 1

                # Sample limit
                if sample and records_processed > sample:
                    break

                # Map the record
                try:
                    senzing_record = map_customer_record(row)
                    outfile.write(json.dumps(senzing_record) + '\n')
                    records_written += 1

                    if progress and records_written % 100 == 0:
                        print(f"Processed {records_written} records...")

                except Exception as e:
                    print(f"WARNING: Error mapping record {row.get('customer_id', '?')}: {e}",
                          file=sys.stderr)
                    continue

            if progress:
                print(f"\nComplete: {records_written} records written to {output_file}")

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def main(args=None):
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Map customer CSV to Senzing JSON format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s customers.csv -o output.jsonl
  %(prog)s customers.csv -o sample.jsonl --sample 10
  %(prog)s customers.csv -o output.jsonl --progress
        """
    )

    parser.add_argument('input',
                       help='Input CSV file')
    parser.add_argument('-o', '--output',
                       required=True,
                       help='Output JSONL file')
    parser.add_argument('--sample',
                       type=int,
                       help='Process only first N records (for testing)')
    parser.add_argument('--progress',
                       action='store_true',
                       help='Show progress messages')

    parsed_args = parser.parse_args(args)

    return map_customers(
        parsed_args.input,
        parsed_args.output,
        sample=parsed_args.sample,
        progress=parsed_args.progress
    )


if __name__ == '__main__':
    sys.exit(main())
