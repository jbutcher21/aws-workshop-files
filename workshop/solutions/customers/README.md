# Customers to Senzing Mapping

## Overview

This mapping transforms customer records from CSV format into Senzing JSON format for entity resolution. The source contains both individual customers (PERSON) and organizational customers (ORGANIZATION).

## Source Data

**File:** `customers.csv`
**Format:** CSV
**Records:** 120 (114 individuals, 6 organizations)
**Fields:** 19

## Mapping Summary

- **DATA_SOURCE:** CUSTOMERS
- **Entities:** 1 (customers table - handles both PERSON and ORGANIZATION)
- **Features Mapped:** 15 Senzing features
- **Payload Attributes:** 4 operational fields
- **Identifier Types:** SSN, DRLIC (Driver's License), PASSPORT, NATIONAL_ID

## Field Mapping

### Features (for entity resolution)
- `customer_id` → RECORD_ID
- `customer_type` → RECORD_TYPE (I=PERSON, C=ORGANIZATION)
- `customer_name` → NAME (parsed for persons: Last, First Middle)
- `dob` → DATE_OF_BIRTH (standardized to YYYY-MM-DD)
- `gender` → GENDER
- `address` → ADDR_LINE1
- `city` → ADDR_CITY
- `state` → ADDR_STATE
- `zip_code` → ADDR_POSTAL_CODE
- `country` → ADDR_COUNTRY
- `phone` → PHONE_NUMBER
- `email` → EMAIL_ADDRESS
- `id_type` + `id_number` + `id_country` → Dynamic identifier (SSN/DRLIC/PASSPORT/NATIONAL_ID)

### Payload Attributes (operational data)
- `registration_date` → CUSTOMER_SINCE_DATE
- `account_status` → ACCOUNT_STATUS
- `account_balance` → ACCOUNT_BALANCE
- `customer_tier` → CUSTOMER_TIER

## Usage

### Run the Mapper

```bash
# Map all records
python3 customers_mapper.py customers.csv -o customers_senzing.jsonl

# Map sample (first 10 records)
python3 customers_mapper.py customers.csv -o sample.jsonl --sample 10

# Show progress for large files
python3 customers_mapper.py customers.csv -o customers_senzing.jsonl --progress
```

### Validate Output

```bash
# Lint the generated Senzing JSON
python3 ../senzing/reference/lint_senzing_json.py customers_senzing.jsonl
```

## Key Decisions

1. **CUSTOMER_SINCE_DATE vs REGISTRATION_DATE**: Used CUSTOMER_SINCE_DATE to avoid confusion with Senzing's REGISTRATION_DATE feature (which is for legal incorporation dates of organizations). Our field represents customer onboarding date.

2. **Name Parsing**: For PERSON records, customer_name format is "Last, First Middle" which is parsed into NAME_LAST, NAME_FIRST, NAME_MIDDLE components. For ORGANIZATION records, the name is mapped directly to NAME_ORG.

3. **Dynamic Identifiers**: The id_type field determines which Senzing identifier feature to use:
   - SSN → SSN_NUMBER
   - DRIVERS_LICENSE → DRIVERS_LICENSE_NUMBER + DRIVERS_LICENSE_STATE
   - PASSPORT → PASSPORT_NUMBER + PASSPORT_COUNTRY
   - NATIONAL_ID → NATIONAL_ID_NUMBER + NATIONAL_ID_COUNTRY

4. **Date Standardization**: Birth dates and customer since dates are standardized to YYYY-MM-DD format.

## Testing

```bash
# Run with sample flag to test
python3 customers_mapper.py customers.csv -o test_output.jsonl --sample 5

# Verify output
python3 ../senzing/reference/lint_senzing_json.py test_output.jsonl

# Check record count
wc -l test_output.jsonl
```

## Notes

- All 120 customer records are mapped (no records skipped)
- Mixed record types (PERSON and ORGANIZATION) are handled in single output
- Only 36 of 120 records have identification numbers (30%)
- Address components may be partial or missing for some records
- Phone and email fields are optional (21% and 37.5% populated respectively)

## Support

For questions about the mapping specification, see `customers_mapper.md`.

For Senzing entity specification details, see `../senzing/reference/senzing_entity_specification.md`.
