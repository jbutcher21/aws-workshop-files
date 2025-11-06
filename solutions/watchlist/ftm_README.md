# FTM (FollowTheMoney) to Senzing JSON Mapper

## Overview

This mapper transforms FollowTheMoney (FTM) format data into Senzing JSON format for entity resolution. The FTM data contains persons, companies, and their relationships (sanctions, ownership, directorship) represented as separate records in a JSONL file.

**Source Format:** JSONL (FollowTheMoney schema)
**Target Format:** Senzing JSON (JSONL output)
**Entities Mapped:** 2 (Person, Company)
**Total Source Records:** 73 (33 Person, 6 Company, 17 Sanction, 8 Ownership, 6 Directorship, 3 Identifier)
**Target Records:** 39 (33 Person + 6 Company)

## Key Features

- **Entity Resolution:** Maps Person and Company entities with full identifying features
- **Relationship Handling:** Converts FTM relationship records into Senzing REL_POINTER/REL_ANCHOR format
- **Identifier Merging:** Merges separate identifier records (SSN, Driver's License) onto person entities
- **Sanction Metadata:** Includes sanction information as payload attributes for risk assessment
- **Validated Output:** All mappings validated against Senzing entity specification using lint_senzing_json.py

## Data Source Codes

| Entity Type | DATA_SOURCE Code | Description |
|-------------|------------------|-------------|
| Person | SANCTIONS | Persons from sanctions/watchlist data (ids: sanctions-person-*) |
| Company | CORP_FILINGS | Companies from corporate filings (ids: corp-filings-org-*) |

## Mapped Features

### Person Entity (SANCTIONS)
**Identifying Features:**
- NAME (parsed: FIRST/LAST/MIDDLE or full name)
- DATE_OF_BIRTH
- ADDRESS (full text)
- EMAIL
- PHONE
- NATIONALITY
- GENDER
- SSN (merged from identifier records)
- DRIVERS_LICENSE + STATE (merged from identifier records)

**Relationships:**
- REL_POINTER for ownership (person → company, role: OWNER_OF)
- REL_POINTER for directorship (person → company, role: PRINCIPAL_OF or PRESIDENT_OF)
- REL_ANCHOR (target of relationships)

**Payload Attributes:**
- PROGRAM (e.g., "SANCTIONS")
- AUTHORITY (e.g., "Sanctions Authority")
- REASON (e.g., "Category: Fraud")
- LISTING_DATE (sanction listing date)
- STATUS (e.g., "Active", "Current", "Inactive")

### Company Entity (CORP_FILINGS)
**Identifying Features:**
- NAME_ORG (current and former names with NAME_TYPE)
- ADDRESS (BUSINESS type)
- REGISTRATION_COUNTRY (jurisdiction)

**Relationships:**
- REL_POINTER for ownership (company → company, role: OWNER_OF)
- REL_ANCHOR (target of ownership/directorship relationships)

## Usage

### Running the Mapper

**Basic usage:**
```bash
python3 ftm_mapper.py input.jsonl output.jsonl
```

**Input directory:**
```bash
python3 ftm_mapper.py /path/to/ftm/files/ output.jsonl
```

**Test with sample records:**
```bash
python3 ftm_mapper.py input.jsonl output.jsonl --sample 10
```

### Command-Line Arguments

- `input`: Path to FTM JSONL file or directory
- `output`: Path to output Senzing JSONL file
- `--sample N`: Process only first N records (for testing)

### Validating Output

After running the mapper, validate the output structure:

```bash
python3 tools/sz_json_analyzer.py output.jsonl
```

**Note:** `sz_json_analyzer.py` is the production validation tool that provides:
- Statistics on records, entities, and features
- Feature usage analysis
- JSONL structure validation

This is different from `lint_senzing_json.py`, which was used during mapping development to validate sample records.

## Testing

### Development Testing (Small Sample)

Test with a small sample to verify the mapping logic:

```bash
# Process first 5 records
python3 ftm_mapper.py input.jsonl test_output.jsonl --sample 5

# Validate structure
python3 tools/sz_json_analyzer.py test_output.jsonl
```

### Production Run

Once validated, process the full dataset:

```bash
python3 ftm_mapper.py ftm_data.jsonl senzing_output.jsonl
```

## Mapping Details

For complete mapping specifications, including:
- Field-by-field disposition (Feature/Payload/Ignore)
- Transformation logic
- Confidence scores
- Crosswalk mappings
- Sample JSON for each entity

See: **ftm_mapper.md**

## Architecture Notes

### Relationship Resolution Strategy

The FTM format stores relationships as separate records. The mapper:

1. **First Pass:** Collect all Person and Company master entities
2. **Second Pass:** Process relationship records (Sanction, Ownership, Directorship, Identifier)
3. **Merge:** Attach relationship data to master entities:
   - Sanctions → payload attributes on Person/Company
   - Identifiers → features on Person
   - Ownership/Directorship → REL_POINTER on source entity
4. **Output:** Emit merged Person and Company records with all relationships

### Record ID Strategy

- **Person/Company:** Use existing FTM `id` field as RECORD_ID
- **REL_ANCHOR/REL_POINTER:** Use DATA_SOURCE + RECORD_ID for domain/key pairs

### Cross-DATA_SOURCE Relationships

Relationships may cross DATA_SOURCE boundaries:
- Person (SANCTIONS) → Company (CORP_FILINGS): REL_POINTER_DOMAIN = "CORP_FILINGS"
- This is valid per Senzing spec

## Files

- `ftm_README.md` - This file
- `ftm_mapper.md` - Complete mapping specification (source of truth)
- `ftm_mapper.py` - Python mapper implementation
- `lint_senzing_json.py` - Development validation tool (in tools/ directory)
- `sz_json_analyzer.py` - Production validation tool (in tools/ directory)

## Support

For issues or questions about:
- Mapping decisions: See ftm_mapper.md
- Senzing specification: See reference/senzing_entity_specification.md
- Identifier/usage type mappings: See reference/identifier_crosswalk.json and reference/usage_type_crosswalk.json

---

**Generated by Senzing Mapping Assistant v4.0**
