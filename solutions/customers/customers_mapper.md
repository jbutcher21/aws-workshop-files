# Customers Mapping Specification

**Version:** 1.0
**Date:** 2025-11-02
**Source:** customers.csv (120 records)
**Target:** Senzing JSON format
**DATA_SOURCE:** CUSTOMERS

---

## Source Schema

| # | Field | Type | Pop % | Unique % | Sample Values |
|---|-------|------|-------|----------|---------------|
| 1 | customer_id | str | 100.0% | 100.0% | 1001, 1002, 1003, 1004, 1005 |
| 2 | customer_name | str | 100.0% | 94.2% | Mooney, Susan (3), Kusha, Mary (2) |
| 3 | customer_type | str | 100.0% | 1.7% | I (114), C (6) |
| 4 | gender | str | 16.7% | 30.0% | M (5), F (5), Male (3), Female (3) |
| 5 | dob | str | 53.3% | 60.9% | 1/7/80, 3/12/87, 4/12/82 |
| 6 | address | str | 60.8% | 67.1% | 1304 Poppy Hills Dr |
| 7 | city | str | 31.7% | 36.8% | Elmwood Park, Sacramento |
| 8 | state | str | 28.3% | 23.5% | CA, NV, OH, IL |
| 9 | zip_code | str | 30.8% | 35.1% | 95823, 95865, 43004 |
| 10 | country | str | 5.0% | 66.7% | Germany, Singapore, CAN |
| 11 | phone | str | 17.5% | 76.2% | 702-919-1300, 512-353-8633 |
| 12 | email | str | 37.5% | 28.9% | info@ca-state.gov |
| 13 | id_type | str | 30.0% | 11.1% | PASSPORT, DRIVERS_LICENSE, SSN, NATIONAL_ID |
| 14 | id_number | str | 30.0% | 55.6% | 483290175, 293-90-9090 |
| 15 | id_country | str | 29.2% | 40.0% | US, CA, MN, USA, OR |
| 16 | registration_date | str | 82.5% | 44.4% | 1/31/18, 1/2/18, 1/7/18 |
| 17 | account_status | str | 82.5% | 3.0% | Active (92), Inactive (5) |
| 18 | account_balance | str | 75.0% | 10.0% | 100, 200, 300, 400, 500 |
| 19 | customer_tier | str | 7.5% | 33.3% | Platinum (4), Silver (3), Gold (2) |

---

## Complete Field Mapping

| # | Source Field | Disposition | Target | Instructions | Confidence |
|---|--------------|-------------|--------|--------------|------------|
| 1 | customer_id | Feature | RECORD_ID | Map directly as unique identifier | 1.0 |
| 2 | customer_name | Feature | NAME | Parse for PERSON: "Last, First Middle" → NAME_LAST, NAME_FIRST, NAME_MIDDLE; For ORGANIZATION: NAME_ORG | 1.0 |
| 3 | customer_type | Feature | RECORD_TYPE | Map: I→PERSON, C→ORGANIZATION | 1.0 |
| 4 | gender | Feature | GENDER | Map directly | 1.0 |
| 5 | dob | Feature | DATE_OF_BIRTH | Parse to YYYY-MM-DD format | 1.0 |
| 6 | address | Feature | ADDR_LINE1 | Map directly | 1.0 |
| 7 | city | Feature | ADDR_CITY | Map directly | 1.0 |
| 8 | state | Feature | ADDR_STATE | Map directly | 1.0 |
| 9 | zip_code | Feature | ADDR_POSTAL_CODE | Map directly | 1.0 |
| 10 | country | Feature | ADDR_COUNTRY | Map directly | 1.0 |
| 11 | phone | Feature | PHONE_NUMBER | Map directly | 1.0 |
| 12 | email | Feature | EMAIL_ADDRESS | Map directly | 1.0 |
| 13 | id_type | Feature | (selector) | Determines identifier feature to use | 1.0 |
| 14 | id_number | Feature | (dynamic) | Maps to SSN_NUMBER, DRIVERS_LICENSE_NUMBER, PASSPORT_NUMBER, or NATIONAL_ID_NUMBER based on id_type | 1.0 |
| 15 | id_country | Feature | (dynamic) | Maps to DRIVERS_LICENSE_STATE, PASSPORT_COUNTRY, or NATIONAL_ID_COUNTRY based on id_type | 1.0 |
| 16 | registration_date | Payload | CUSTOMER_SINCE_DATE | Parse to YYYY-MM-DD format | 1.0 |
| 17 | account_status | Payload | ACCOUNT_STATUS | Map directly | 1.0 |
| 18 | account_balance | Payload | ACCOUNT_BALANCE | Map directly | 1.0 |
| 19 | customer_tier | Payload | CUSTOMER_TIER | Map directly (empty string if missing) | 1.0 |

---

## Identifier Type Mappings

These mappings are applied via the identifier_crosswalk.json:

| id_type Value | Senzing Feature | Attributes Required | Notes |
|---------------|-----------------|---------------------|-------|
| SSN | SSN | SSN_NUMBER | US Social Security Number |
| DRIVERS_LICENSE | DRLIC | DRIVERS_LICENSE_NUMBER, DRIVERS_LICENSE_STATE | Include issuing state from id_country |
| PASSPORT | PASSPORT | PASSPORT_NUMBER, PASSPORT_COUNTRY | Include issuing country from id_country |
| NATIONAL_ID | NATIONAL_ID | NATIONAL_ID_NUMBER, NATIONAL_ID_COUNTRY | Include issuing country from id_country |

---

## Name Parsing Logic

### For PERSON records (customer_type = 'I'):

Input format: "Last, First Middle"

**Examples:**
- "Smith, Robert" → NAME_LAST="Smith", NAME_FIRST="Robert"
- "Smith, Bob J" → NAME_LAST="Smith", NAME_FIRST="Bob", NAME_MIDDLE="J"
- "Kusha, Mary" → NAME_LAST="Kusha", NAME_FIRST="Mary"

**Algorithm:**
1. Split on comma: [last_part, first_part]
2. Strip whitespace from both parts
3. Split first_part on spaces: [first, ...middle_parts]
4. NAME_LAST = last_part
5. NAME_FIRST = first word
6. NAME_MIDDLE = remaining words (if any)
7. Always include NAME_TYPE="PRIMARY"

### For ORGANIZATION records (customer_type = 'C'):

Input: Full organization name as-is

**Examples:**
- "Hajah Mamunah (Jln Pisang)" → NAME_ORG="Hajah Mamunah (Jln Pisang)"
- "Mullenkrants Autoworks" → NAME_ORG="Mullenkrants Autoworks"

**Algorithm:**
1. Use customer_name directly as NAME_ORG
2. Always include NAME_TYPE="PRIMARY"

---

## Date Standardization

### Input Formats Observed:
- M/D/YY → "1/7/80"
- M/D/YYYY → "12/11/1978"
- MM/DD/YYYY → "10/27/76"
- D-MMM-YY → "24-May-11"
- YYYY-MM-DD → "1993-09-14" (already standardized)

### Target Format: YYYY-MM-DD

**Parse Logic:**
```python
def parse_date(date_str):
    if not date_str:
        return None
    # Try MM/DD/YYYY
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    except: pass
    # Try M/D/YY
    try:
        return datetime.strptime(date_str, '%m/%d/%y').strftime('%Y-%m-%d')
    except: pass
    # Try D-MMM-YY
    try:
        return datetime.strptime(date_str, '%d-%b-%y').strftime('%Y-%m-%d')
    except: pass
    # Already YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    # If can't parse, return original
    return date_str
```

---

## Sample Output JSON

### Example 1: PERSON with Parsed Address and Driver's License

```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "1005",
  "CUSTOMER_SINCE_DATE": "2019-07-16",
  "ACCOUNT_STATUS": "Active",
  "ACCOUNT_BALANCE": "500",
  "CUSTOMER_TIER": "",
  "FEATURES": [
    {
      "RECORD_TYPE": "PERSON"
    },
    {
      "NAME_TYPE": "PRIMARY",
      "NAME_LAST": "Smith",
      "NAME_FIRST": "Robbie"
    },
    {
      "ADDR_LINE1": "123 E Main St",
      "ADDR_CITY": "Henderson",
      "ADDR_STATE": "NV",
      "ADDR_POSTAL_CODE": "89132"
    },
    {
      "DRIVERS_LICENSE_NUMBER": "112233",
      "DRIVERS_LICENSE_STATE": "NV"
    }
  ]
}
```

### Example 2: PERSON with Passport and Full Address

```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "1069",
  "CUSTOMER_SINCE_DATE": "2018-01-26",
  "ACCOUNT_BALANCE": "100",
  "ACCOUNT_STATUS": "",
  "CUSTOMER_TIER": "",
  "FEATURES": [
    {
      "RECORD_TYPE": "PERSON"
    },
    {
      "NAME_TYPE": "PRIMARY",
      "NAME_LAST": "Wang",
      "NAME_FIRST": "Jie"
    },
    {
      "DATE_OF_BIRTH": "1993-09-14"
    },
    {
      "GENDER": "Male"
    },
    {
      "ADDR_LINE1": "12 Constitution Street"
    },
    {
      "PASSPORT_NUMBER": "832721",
      "PASSPORT_COUNTRY": "Hong Kong"
    }
  ]
}
```

### Example 3: ORGANIZATION

```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "2011",
  "CUSTOMER_SINCE_DATE": "2018-01-31",
  "ACCOUNT_STATUS": "Inactive",
  "ACCOUNT_BALANCE": "",
  "CUSTOMER_TIER": "Platinum",
  "FEATURES": [
    {
      "RECORD_TYPE": "ORGANIZATION"
    },
    {
      "NAME_TYPE": "PRIMARY",
      "NAME_ORG": "Hajah Mamunah (Jln Pisang)"
    },
    {
      "ADDR_LINE1": "#01-11, HillV2, 4 Hillview Rise, 667979"
    }
  ]
}
```

### Example 4: PERSON with Email and Phone

```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "1009",
  "CUSTOMER_SINCE_DATE": "2018-01-07",
  "ACCOUNT_STATUS": "Active",
  "ACCOUNT_BALANCE": "600",
  "CUSTOMER_TIER": "",
  "FEATURES": [
    {
      "RECORD_TYPE": "PERSON"
    },
    {
      "NAME_TYPE": "PRIMARY",
      "NAME_LAST": "Kusha",
      "NAME_FIRST": "Edward"
    },
    {
      "DATE_OF_BIRTH": "1970-03-01"
    },
    {
      "ADDR_LINE1": "1304 Poppy Hills Dr",
      "ADDR_CITY": "Blacklick",
      "ADDR_STATE": "OH",
      "ADDR_POSTAL_CODE": "43004"
    },
    {
      "EMAIL_ADDRESS": "Kusha123@hmail.com"
    },
    {
      "PHONE_NUMBER": "294-66-9999"
    },
    {
      "SSN_NUMBER": "294-66-9999"
    }
  ]
}
```

---

## Implementation Rules

1. **Empty Fields**: Omit feature objects entirely if all attributes within that feature are empty. For payload attributes, use empty string "" if missing.

2. **Feature Grouping**: Group related attributes together in single feature object (e.g., all ADDRESS components in one object).

3. **Record Type Logic**:
   - If customer_type = 'I' → RECORD_TYPE = "PERSON", use NAME_LAST/NAME_FIRST/NAME_MIDDLE
   - If customer_type = 'C' → RECORD_TYPE = "ORGANIZATION", use NAME_ORG
   - If customer_type missing → skip record or default to PERSON (configurable)

4. **Identifier Handling**: Only include identifier feature if all three fields present (id_type, id_number, id_country). For SSN, id_country is optional.

5. **Date Handling**: If date parsing fails, use original value or omit field (configurable).

---

## Statistics

- **Total Records:** 120
- **PERSON:** 114 (95%)
- **ORGANIZATION:** 6 (5%)
- **With Identifiers:** 36 (30%)
  - SSN: 7 records
  - DRIVERS_LICENSE: 11 records
  - PASSPORT: 14 records
  - NATIONAL_ID: 4 records
- **With Address:** 73 (60.8%)
- **With Phone:** 21 (17.5%)
- **With Email:** 45 (37.5%)
- **With DOB:** 64 (53.3%)

---

## Validation

All generated JSON must pass the Senzing linter:

```bash
python3 ../senzing/reference/lint_senzing_json.py output.jsonl
```

Expected: `OK: All files passed`

---

**End of Mapping Specification**
