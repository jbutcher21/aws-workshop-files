#!/usr/bin/env python3
"""
FTM to Senzing JSON Mapper

Transforms FollowTheMoney (FTM) format data into Senzing JSON format.

Usage:
    python3 ftm_mapper.py input.jsonl output.jsonl
    python3 ftm_mapper.py input_dir/ output.jsonl
    python3 ftm_mapper.py input.jsonl output.jsonl --sample 10

Arguments:
    input: Path to FTM JSONL file or directory
    output: Path to output Senzing JSONL file
    --sample N: Process only first N records (for testing)
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional
from collections import defaultdict


# Hard-coded DATA_SOURCE values
DATA_SOURCE_PERSON = "SANCTIONS"
DATA_SOURCE_COMPANY = "CORP_FILINGS"


def extract_property_value(properties: Dict, key: str) -> Optional[str]:
    """Extract single value from FTM property list structure."""
    if key not in properties:
        return None
    prop_list = properties[key]
    if not isinstance(prop_list, list) or len(prop_list) == 0:
        return None
    item = prop_list[0]
    # Handle both simple string arrays and object arrays
    if isinstance(item, str):
        return item
    elif isinstance(item, dict):
        return item.get(key)
    return None


def extract_property_values(properties: Dict, key: str) -> List[str]:
    """Extract all values from FTM property list structure."""
    if key not in properties:
        return []
    prop_list = properties[key]
    if not isinstance(prop_list, list):
        return []
    values = []
    for item in prop_list:
        # Handle both simple string arrays and object arrays
        if isinstance(item, str):
            values.append(item)
        elif isinstance(item, dict) and key in item:
            values.append(item[key])
    return values


def map_person(record: Dict, sanction_map: Dict, identifier_map: Dict,
               ownership_map: Dict, directorship_map: Dict) -> Dict:
    """Map FTM Person record to Senzing JSON."""
    record_id = record.get("id")
    properties = record.get("properties", {})

    features = []

    # RECORD_TYPE
    features.append({"RECORD_TYPE": "PERSON"})

    # NAME - prefer parsed components, fall back to full name
    first_name = extract_property_value(properties, "firstName")
    last_name = extract_property_value(properties, "lastName")
    middle_name = extract_property_value(properties, "middleName")

    if first_name or last_name:
        name_feature = {}
        if first_name:
            name_feature["NAME_FIRST"] = first_name.strip()
        if last_name:
            name_feature["NAME_LAST"] = last_name.strip()
        if middle_name:
            name_feature["NAME_MIDDLE"] = middle_name.strip()
        features.append(name_feature)
    else:
        # Fall back to full name
        full_name = extract_property_value(properties, "name")
        if full_name:
            features.append({"NAME_FULL": full_name.strip()})

    # DATE_OF_BIRTH
    dob = extract_property_value(properties, "birthDate")
    if dob:
        features.append({"DATE_OF_BIRTH": dob})

    # ADDRESS (can be multiple)
    addresses = extract_property_values(properties, "address")
    for addr in addresses:
        features.append({"ADDR_FULL": addr})

    # EMAIL
    emails = extract_property_values(properties, "email")
    for email in emails:
        features.append({"EMAIL_ADDRESS": email.lower()})

    # PHONE
    phones = extract_property_values(properties, "phone")
    for phone in phones:
        features.append({"PHONE_NUMBER": phone})

    # GENDER
    gender = extract_property_value(properties, "gender")
    if gender:
        features.append({"GENDER": gender})

    # NATIONALITY
    nationalities = extract_property_values(properties, "nationality")
    for nationality in nationalities:
        features.append({"NATIONALITY": nationality})

    # IDENTIFIERS (merged from identifier records)
    if record_id in identifier_map:
        for identifier in identifier_map[record_id]:
            id_type = identifier.get("type")
            id_number = identifier.get("number")
            id_country = identifier.get("country")

            if id_type == "SSN" and id_number:
                features.append({"SSN_NUMBER": id_number})
            elif id_type == "DRIVERS_LICENSE" and id_number:
                drlic_feature = {"DRIVERS_LICENSE_NUMBER": id_number}
                if id_country:
                    drlic_feature["DRIVERS_LICENSE_STATE"] = id_country
                features.append(drlic_feature)

    # RELATIONSHIPS - Ownership (person as owner)
    if record_id in ownership_map:
        for asset_id in ownership_map[record_id]:
            features.append({
                "REL_POINTER_DOMAIN": DATA_SOURCE_COMPANY,
                "REL_POINTER_KEY": asset_id,
                "REL_POINTER_ROLE": "OWNER_OF"
            })

    # RELATIONSHIPS - Directorship (person as director)
    if record_id in directorship_map:
        for org_id, role in directorship_map[record_id]:
            # Map role
            if role == "Principal":
                mapped_role = "PRINCIPAL_OF"
            elif role == "President":
                mapped_role = "PRESIDENT_OF"
            else:
                mapped_role = "DIRECTOR_OF"  # fallback

            features.append({
                "REL_POINTER_DOMAIN": DATA_SOURCE_COMPANY,
                "REL_POINTER_KEY": org_id,
                "REL_POINTER_ROLE": mapped_role
            })

    # REL_ANCHOR (all persons are potential targets)
    features.append({
        "REL_ANCHOR_DOMAIN": DATA_SOURCE_PERSON,
        "REL_ANCHOR_KEY": record_id
    })

    # Build output record
    output = {
        "DATA_SOURCE": DATA_SOURCE_PERSON,
        "RECORD_ID": record_id,
        "FEATURES": features
    }

    # PAYLOAD - Sanction metadata (if exists)
    if record_id in sanction_map:
        sanction = sanction_map[record_id]
        if "program" in sanction:
            output["PROGRAM"] = sanction["program"]
        if "authority" in sanction:
            output["AUTHORITY"] = sanction["authority"]
        if "reason" in sanction:
            output["REASON"] = sanction["reason"]
        if "listingDate" in sanction:
            output["LISTING_DATE"] = sanction["listingDate"]
        if "status" in sanction:
            output["STATUS"] = sanction["status"]

    return output


def map_company(record: Dict, ownership_map: Dict) -> Dict:
    """Map FTM Company record to Senzing JSON."""
    record_id = record.get("id")
    properties = record.get("properties", {})

    features = []

    # RECORD_TYPE
    features.append({"RECORD_TYPE": "ORGANIZATION"})

    # NAME - current (PRIMARY)
    name = extract_property_value(properties, "name")
    if name:
        features.append({
            "NAME_TYPE": "PRIMARY",
            "NAME_ORG": name.strip()
        })

    # NAME - previous (FORMER)
    previous_names = extract_property_values(properties, "previousName")
    for prev_name in previous_names:
        features.append({
            "NAME_TYPE": "FORMER",
            "NAME_ORG": prev_name.strip()
        })

    # ADDRESS (BUSINESS type for organizations)
    addresses = extract_property_values(properties, "address")
    for addr in addresses:
        features.append({
            "ADDR_TYPE": "BUSINESS",
            "ADDR_FULL": addr
        })

    # REGISTRATION_COUNTRY (jurisdiction)
    jurisdiction = extract_property_value(properties, "jurisdiction")
    if jurisdiction:
        features.append({"REGISTRATION_COUNTRY": jurisdiction})

    # RELATIONSHIPS - Ownership (company as owner)
    if record_id in ownership_map:
        for asset_id in ownership_map[record_id]:
            features.append({
                "REL_POINTER_DOMAIN": DATA_SOURCE_COMPANY,
                "REL_POINTER_KEY": asset_id,
                "REL_POINTER_ROLE": "OWNER_OF"
            })

    # REL_ANCHOR (all companies are relationship targets)
    features.append({
        "REL_ANCHOR_DOMAIN": DATA_SOURCE_COMPANY,
        "REL_ANCHOR_KEY": record_id
    })

    # Build output record
    output = {
        "DATA_SOURCE": DATA_SOURCE_COMPANY,
        "RECORD_ID": record_id,
        "FEATURES": features
    }

    return output


def build_sanction_map(sanction_records: List[Dict]) -> Dict:
    """Build map of entity_id -> sanction metadata."""
    sanction_map = {}

    for record in sanction_records:
        properties = record.get("properties", {})
        entity_id = extract_property_value(properties, "entity")

        if not entity_id:
            continue

        sanction_data = {}

        program = extract_property_value(properties, "program")
        if program:
            sanction_data["program"] = program

        authority = extract_property_value(properties, "authority")
        if authority:
            sanction_data["authority"] = authority

        reason = extract_property_value(properties, "reason")
        if reason:
            sanction_data["reason"] = reason

        listing_date = extract_property_value(properties, "listingDate")
        if listing_date:
            sanction_data["listingDate"] = listing_date

        status = extract_property_value(properties, "status")
        if status:
            sanction_data["status"] = status

        sanction_map[entity_id] = sanction_data

    return sanction_map


def build_identifier_map(identifier_records: List[Dict]) -> Dict:
    """Build map of holder_id -> list of identifier details."""
    identifier_map = defaultdict(list)

    for record in identifier_records:
        properties = record.get("properties", {})
        holder_id = extract_property_value(properties, "holder")

        if not holder_id:
            continue

        identifier_data = {}

        id_type = extract_property_value(properties, "type")
        if id_type:
            identifier_data["type"] = id_type

        id_number = extract_property_value(properties, "number")
        if id_number:
            identifier_data["number"] = id_number

        id_country = extract_property_value(properties, "country")
        if id_country:
            identifier_data["country"] = id_country

        identifier_map[holder_id].append(identifier_data)

    return identifier_map


def build_ownership_map(ownership_records: List[Dict]) -> Dict:
    """Build map of owner_id -> list of asset_ids."""
    ownership_map = defaultdict(list)

    for record in ownership_records:
        properties = record.get("properties", {})
        owner_id = extract_property_value(properties, "owner")
        asset_id = extract_property_value(properties, "asset")

        if owner_id and asset_id:
            ownership_map[owner_id].append(asset_id)

    return ownership_map


def build_directorship_map(directorship_records: List[Dict]) -> Dict:
    """Build map of director_id -> list of (organization_id, role) tuples."""
    directorship_map = defaultdict(list)

    for record in directorship_records:
        properties = record.get("properties", {})
        director_id = extract_property_value(properties, "director")
        org_id = extract_property_value(properties, "organization")
        role = extract_property_value(properties, "role")

        if director_id and org_id:
            directorship_map[director_id].append((org_id, role))

    return directorship_map


def load_ftm_records(input_path: str, sample_limit: Optional[int] = None) -> List[Dict]:
    """Load FTM JSONL records from file or directory."""
    records = []

    if os.path.isdir(input_path):
        # Process all .jsonl files in directory
        for filename in sorted(os.listdir(input_path)):
            if filename.endswith('.jsonl'):
                filepath = os.path.join(input_path, filename)
                records.extend(load_jsonl_file(filepath, sample_limit))
                if sample_limit and len(records) >= sample_limit:
                    break
    else:
        # Single file
        records = load_jsonl_file(input_path, sample_limit)

    return records


def load_jsonl_file(filepath: str, sample_limit: Optional[int] = None) -> List[Dict]:
    """Load records from a single JSONL file."""
    records = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
                records.append(record)

                if sample_limit and len(records) >= sample_limit:
                    break
            except json.JSONDecodeError as e:
                print(f"WARNING: Invalid JSON at {filepath}:{line_num}: {e}", file=sys.stderr)
                continue

    return records


def partition_records(records: List[Dict]) -> Dict[str, List[Dict]]:
    """Partition FTM records by schema type."""
    partitioned = defaultdict(list)

    for record in records:
        schema = record.get("schema")
        if schema:
            partitioned[schema].append(record)

    return partitioned


def map_ftm_to_senzing(records: List[Dict]) -> List[Dict]:
    """Map FTM records to Senzing JSON format."""
    # Partition by schema type
    partitioned = partition_records(records)

    person_records = partitioned.get("Person", [])
    company_records = partitioned.get("Company", [])
    sanction_records = partitioned.get("Sanction", [])
    ownership_records = partitioned.get("Ownership", [])
    directorship_records = partitioned.get("Directorship", [])

    # Detect identifier records (no explicit schema, have holder/number/type)
    identifier_records = []
    for record in records:
        props = record.get("properties", {})
        if "holder" in props and "number" in props and "type" in props:
            identifier_records.append(record)

    # Build lookup maps
    sanction_map = build_sanction_map(sanction_records)
    identifier_map = build_identifier_map(identifier_records)
    ownership_map = build_ownership_map(ownership_records)
    directorship_map = build_directorship_map(directorship_records)

    # Map entities
    output_records = []

    # Map persons
    for person in person_records:
        mapped = map_person(person, sanction_map, identifier_map,
                          ownership_map, directorship_map)
        output_records.append(mapped)

    # Map companies
    for company in company_records:
        mapped = map_company(company, ownership_map)
        output_records.append(mapped)

    return output_records


def write_senzing_jsonl(records: List[Dict], output_path: str) -> None:
    """Write Senzing JSON records to JSONL file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record) + '\n')


def main(args: List[str]) -> int:
    """Main entry point."""
    if len(args) < 3:
        print(__doc__)
        return 2

    input_path = args[1]
    output_path = args[2]

    sample_limit = None
    if len(args) >= 5 and args[3] == '--sample':
        try:
            sample_limit = int(args[4])
        except ValueError:
            print(f"ERROR: Invalid sample limit: {args[4]}", file=sys.stderr)
            return 2

    # Validate input
    if not os.path.exists(input_path):
        print(f"ERROR: Input path not found: {input_path}", file=sys.stderr)
        return 1

    print(f"Loading FTM records from: {input_path}")
    if sample_limit:
        print(f"Sample limit: {sample_limit} records")

    # Load records
    try:
        ftm_records = load_ftm_records(input_path, sample_limit)
    except Exception as e:
        print(f"ERROR: Failed to load records: {e}", file=sys.stderr)
        return 1

    print(f"Loaded {len(ftm_records)} FTM records")

    # Map to Senzing format
    print("Mapping to Senzing JSON format...")
    senzing_records = map_ftm_to_senzing(ftm_records)

    print(f"Mapped {len(senzing_records)} Senzing records")

    # Write output
    print(f"Writing output to: {output_path}")
    try:
        write_senzing_jsonl(senzing_records, output_path)
    except Exception as e:
        print(f"ERROR: Failed to write output: {e}", file=sys.stderr)
        return 1

    print(f"✅ Complete! Wrote {len(senzing_records)} records to {output_path}")
    print(f"\nValidate output with: python3 tools/sz_json_analyzer.py {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
