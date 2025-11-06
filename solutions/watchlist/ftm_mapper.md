# FTM to Senzing JSON - Complete Mapping Specification

**Version:** 1.0
**Date:** 2025-11-05
**Source:** FollowTheMoney (FTM) JSONL format
**Target:** Senzing JSON format
**Mapping Assistant:** v4.0

---

## Table of Contents

1. [Overview](#overview)
2. [Source Schema Analysis](#source-schema-analysis)
3. [Entity Planning](#entity-planning)
4. [Entity 1: Person](#entity-1-person)
5. [Entity 2: Company](#entity-2-company)
6. [Crosswalk Mappings](#crosswalk-mappings)
7. [Sample JSON](#sample-json)
8. [Validation Results](#validation-results)

---

## Overview

This document is the complete mapping specification for transforming FTM format data into Senzing JSON. It serves as the source of truth for all mapping decisions.

**Key Characteristics:**
- **Source Format:** JSONL with nested property lists
- **Entity Types:** Person, Company (master entities); Sanction, Ownership, Directorship, Identifier (relationship records)
- **Total Records:** 73 source records → 39 target records (merging relationships into masters)
- **Relationships:** Explicit relationships mapped using REL_POINTER/REL_ANCHOR

---

## Source Schema Analysis

### Schema Types

| Schema | Count | Purpose |
|--------|-------|---------|
| Person | 33 | Master entity - individuals |
| Company | 6 | Master entity - organizations |
| Sanction | 17 | Relationship - sanction metadata for persons/companies |
| Ownership | 8 | Relationship - owner → asset links |
| Directorship | 6 | Relationship - director → organization links |
| Identifier | 3 | Relationship - identifier details for persons |
| **Total** | **73** | |

### Field Structure

FTM uses a consistent structure:
```json
{
  "id": "unique-identifier",
  "schema": "Person|Company|Sanction|Ownership|Directorship",
  "properties": {
    "fieldName": [{"fieldName": "value"}],
    ...
  }
}
```

**Key observations:**
- All properties are arrays with single-element objects
- Field name is duplicated (key and nested key)
- Relationships stored as separate records, not embedded

---

## Entity Planning

### Master Entities

**Decision:** Map Person and Company as separate master entities with distinct DATA_SOURCE codes.

| Entity | DATA_SOURCE | Count | RECORD_TYPE |
|--------|-------------|-------|-------------|
| Person | SANCTIONS | 33 | PERSON |
| Company | CORP_FILINGS | 6 | ORGANIZATION |

**Rationale:**
- IDs naturally partition: "sanctions-person-*" vs "corp-filings-org-*"
- Separate DATA_SOURCE codes allow different governance/refresh cycles
- Clear lineage traceability

### Relationship Handling

**Sanction Records:**
- **Approach:** Payload attributes (not relationships)
- **Rationale:** Sanctions describe entity properties, not links to other entities
- **Mapping:** program, authority, reason, listingDate, status → root-level payload attributes

**Ownership Records:**
- **Approach:** REL_POINTER (owner → asset)
- **Role:** OWNER_OF
- **REL_POINTER on:** Owner entity (person or company)
- **REL_ANCHOR on:** Asset entity (company)

**Directorship Records:**
- **Approach:** REL_POINTER (director → organization)
- **Role:** PRINCIPAL_OF (for "Principal"), PRESIDENT_OF (for "President")
- **REL_POINTER on:** Director entity (person)
- **REL_ANCHOR on:** Organization entity (company)

**Identifier Records:**
- **Approach:** Flatten/merge onto Person entities as identifier features
- **Mapping:** type + number + country → SSN_NUMBER or DRIVERS_LICENSE_NUMBER + DRIVERS_LICENSE_STATE

### RECORD_ID Strategy

**Source has unique IDs:** Use existing `id` field as RECORD_ID (no hashing required).

---

## Entity 1: Person

**DATA_SOURCE:** SANCTIONS
**RECORD_TYPE:** PERSON
**Source Schema:** Person (33 records) + merged Sanction (17) + Identifier (3) + Ownership/Directorship relationships

### Complete Field Mapping

| # | Source Field | Disposition | Senzing Attribute | Transform | Confidence | Reference |
|---|--------------|-------------|-------------------|-----------|------------|-----------|
| 1 | id | Feature | RECORD_ID | Use as-is | 1.0 | [Spec §RECORD_ID] |
| 2 | schema | Ignore | - | Not mapped | 1.0 | - |
| 3 | properties.firstName[].firstName | Feature | NAME_FIRST | Extract from list, trim | 1.0 | [Spec §Feature: NAME: "NAME_FIRST"] |
| 4 | properties.lastName[].lastName | Feature | NAME_LAST | Extract from list, trim | 1.0 | [Spec §Feature: NAME: "NAME_LAST"] |
| 5 | properties.middleName[].middleName | Feature | NAME_MIDDLE | Extract from list, trim | 1.0 | [Spec §Feature: NAME: "NAME_MIDDLE"] |
| 6 | properties.name[].name | Feature | NAME_FULL | Extract from list when firstName/lastName not available | 0.95 | [Spec §Feature: NAME: "NAME_FULL"] |
| 7 | properties.birthDate[].birthDate | Feature | DATE_OF_BIRTH | Extract from list, format YYYY-MM-DD | 1.0 | [Spec §Feature: DOB: "DATE_OF_BIRTH"] |
| 8 | properties.address[].address | Feature | ADDR_FULL | Extract from list | 1.0 | [Spec §Feature: ADDRESS: "ADDR_FULL"] |
| 9 | properties.email[].email | Feature | EMAIL_ADDRESS | Extract from list, lowercase | 1.0 | [Spec §Feature: EMAIL: "EMAIL_ADDRESS"] |
| 10 | properties.gender[].gender | Feature | GENDER | Extract from list | 1.0 | [Spec §Feature: GENDER: "GENDER"] |
| 11 | properties.phone[].phone | Feature | PHONE_NUMBER | Extract from list | 1.0 | [Spec §Feature: PHONE: "PHONE_NUMBER"] |
| 12 | properties.nationality[].nationality | Feature | NATIONALITY | Extract from list | 1.0 | [Spec §Feature: NATIONALITY: "NATIONALITY"] |
| 13 | **Merged from Identifier records** | | | | | |
| 14 | properties.type="SSN" + number | Feature | SSN_NUMBER | Merge identifier record onto person | 1.0 | [Spec §Feature: SSN]; [Crosswalk: SSN] |
| 15 | properties.type="DRIVERS_LICENSE" + number + country | Feature | DRIVERS_LICENSE_NUMBER + DRIVERS_LICENSE_STATE | Merge identifier record onto person; map country to STATE | 0.90 | [Spec §Feature: DRLIC]; [Crosswalk: DRLIC] |
| 16 | **Merged from Sanction records** | | | | | |
| 17 | properties.program[].program | Payload | PROGRAM | Root-level payload attribute | 0.85 | [Spec §Payload Attributes] |
| 18 | properties.authority[].authority | Payload | AUTHORITY | Root-level payload attribute | 0.85 | [Spec §Payload Attributes] |
| 19 | properties.reason[].reason | Payload | REASON | Root-level payload attribute | 0.85 | [Spec §Payload Attributes] |
| 20 | properties.listingDate[].listingDate | Payload | LISTING_DATE | Root-level payload attribute | 0.85 | [Spec §Payload Attributes] |
| 21 | properties.status[].status | Payload | STATUS | Root-level payload attribute | 0.90 | [Spec §Payload Attributes: "STATUS"] |
| 22 | **Relationships** | | | | | |
| 23 | Ownership: properties.owner = person.id | Feature | REL_POINTER | owner→asset, role=OWNER_OF | 1.0 | [Spec §REL_POINTER] |
| 24 | Directorship: properties.director = person.id | Feature | REL_POINTER | director→org, role from properties.role | 0.95 | [Spec §REL_POINTER] |
| 25 | When person is relationship target | Feature | REL_ANCHOR | One anchor per person | 1.0 | [Spec §REL_ANCHOR] |
| 26 | Constant | Feature | RECORD_TYPE | Set to "PERSON" | 1.0 | [Spec §FEATURE: RECORD_TYPE] |

### Name Handling Logic

**Rule:** Prefer parsed name components when available; fall back to full name.

```python
if firstName or lastName:
    # Create NAME feature with parsed components
    name_feature = {
        "NAME_FIRST": firstName,
        "NAME_LAST": lastName,
        "NAME_MIDDLE": middleName  # if present
    }
elif name:
    # Use full name
    name_feature = {"NAME_FULL": name}
```

### Identifier Merging Logic

Identifier records have:
- `properties.holder` → person ID
- `properties.type` → identifier type (SSN, DRIVERS_LICENSE)
- `properties.number` → identifier value
- `properties.country` → issuing country/state

**Merge process:**
1. Build lookup map: holder ID → identifier details
2. When processing person, check if identifiers exist
3. Add identifier features to person's FEATURES array

### Relationship Pointer Logic

**Ownership:**
- When `Ownership.owner` = person.id AND `Ownership.asset` exists
- Add to person: `{"REL_POINTER_DOMAIN": "CORP_FILINGS", "REL_POINTER_KEY": asset_id, "REL_POINTER_ROLE": "OWNER_OF"}`

**Directorship:**
- When `Directorship.director` = person.id AND `Directorship.organization` exists
- Map role: "Principal" → "PRINCIPAL_OF", "President" → "PRESIDENT_OF"
- Add to person: `{"REL_POINTER_DOMAIN": "CORP_FILINGS", "REL_POINTER_KEY": org_id, "REL_POINTER_ROLE": role}`

---

## Entity 2: Company

**DATA_SOURCE:** CORP_FILINGS
**RECORD_TYPE:** ORGANIZATION
**Source Schema:** Company (6 records) + relationships

### Complete Field Mapping

| # | Source Field | Disposition | Senzing Attribute | Transform | Confidence | Reference |
|---|--------------|-------------|-------------------|-----------|------------|-----------|
| 1 | id | Feature | RECORD_ID | Use as-is | 1.0 | [Spec §RECORD_ID] |
| 2 | schema | Ignore | - | Not mapped | 1.0 | - |
| 3 | properties.name[].name | Feature | NAME_ORG | Extract from list | 1.0 | [Spec §Feature: NAME: "NAME_ORG"] |
| 4 | properties.address[].address | Feature | ADDR_FULL + ADDR_TYPE=BUSINESS | Extract from list, mark as BUSINESS | 1.0 | [Spec §Feature: ADDRESS: "ADDR_FULL"]; [Spec §Mapping Usage Types] |
| 5 | properties.jurisdiction[].jurisdiction | Feature | REGISTRATION_COUNTRY | Extract from list | 0.90 | [Spec §Feature: REGISTRATION_COUNTRY] |
| 6 | properties.previousName[].previousName | Feature | NAME_ORG + NAME_TYPE=FORMER | Extract from list, mark as FORMER | 0.95 | [Spec §Feature: NAME]; [Usage Type Crosswalk: FORMER] |
| 7 | **Relationships** | | | | | |
| 8 | Ownership: properties.owner = company.id | Feature | REL_POINTER | owner→asset, role=OWNER_OF | 1.0 | [Spec §REL_POINTER] |
| 9 | All companies (relationship targets) | Feature | REL_ANCHOR | One anchor per company | 1.0 | [Spec §REL_ANCHOR] |
| 10 | Constant | Feature | RECORD_TYPE | Set to "ORGANIZATION" | 1.0 | [Spec §FEATURE: RECORD_TYPE] |

### Name Handling Logic

**Current Name:**
```python
name_feature = {"NAME_TYPE": "PRIMARY", "NAME_ORG": name}
```

**Previous Names:**
```python
for prev_name in previousNames:
    name_feature = {"NAME_TYPE": "FORMER", "NAME_ORG": prev_name}
```

### Address Logic

All company addresses marked as BUSINESS type (adds weight per Senzing spec):
```python
addr_feature = {"ADDR_TYPE": "BUSINESS", "ADDR_FULL": address}
```

---

## Crosswalk Mappings

### Identifier Type Crosswalk

**Applied mappings:**

| Source Type | Canonical | Senzing Feature | Attributes |
|-------------|-----------|-----------------|------------|
| SSN | SSN | SSN | SSN_NUMBER |
| DRIVERS_LICENSE | DRLIC | DRLIC | DRIVERS_LICENSE_NUMBER, DRIVERS_LICENSE_STATE |

**Source:** identifier_crosswalk.json

**Notes:**
- DRIVERS_LICENSE mapped via alias "DRIVERS_LICENSE_NUMBER" → DRLIC
- Country field ("US") mapped to DRIVERS_LICENSE_STATE

### Usage Type Crosswalk

**Applied mappings:**

| Feature | Source Type | Canonical | Special Meaning |
|---------|-------------|-----------|-----------------|
| NAME | (previousName) | FORMER | No |
| ADDRESS | (company address) | BUSINESS | Yes (adds weight for orgs) |

**Source:** usage_type_crosswalk.json

**Notes:**
- BUSINESS address type has special meaning for organizations (increases weight on physical location)
- FORMER name type is reference only

### Directorship Role Mapping

**Custom mapping (not in crosswalk):**

| Source Role | Senzing REL_POINTER_ROLE |
|-------------|--------------------------|
| Principal | PRINCIPAL_OF |
| President | PRESIDENT_OF |

**Rationale:** Per Senzing spec examples for person→organization relationships

---

## Sample JSON

### Person Sample 1: Full Features with Identifiers and Sanction

```json
{
  "DATA_SOURCE": "SANCTIONS",
  "RECORD_ID": "sanctions-person-1006",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Robert", "NAME_LAST": "Smith" },
    { "DATE_OF_BIRTH": "1973-12-11" },
    { "ADDR_FULL": "123 Main St, Las Vegas" },
    { "EMAIL_ADDRESS": "robert.smith@email.com" },
    { "PHONE_NUMBER": "800-111-1234" },
    { "NATIONALITY": "Pakistan" },
    { "SSN_NUMBER": "294-66-9999" },
    { "DRIVERS_LICENSE_NUMBER": "112233", "DRIVERS_LICENSE_STATE": "US" },
    { "REL_ANCHOR_DOMAIN": "SANCTIONS", "REL_ANCHOR_KEY": "sanctions-person-1006" }
  ],
  "PROGRAM": "SANCTIONS",
  "AUTHORITY": "Sanctions Authority",
  "REASON": "Category: Fraud",
  "LISTING_DATE": "2019-03-05",
  "STATUS": "Active"
}
```

### Person Sample 2: Full Name Only

```json
{
  "DATA_SOURCE": "SANCTIONS",
  "RECORD_ID": "sanctions-person-1007",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FULL": "John Smith" },
    { "DATE_OF_BIRTH": "1980-01-07" },
    { "ADDR_FULL": "638 Downey St, Salem, OR" },
    { "EMAIL_ADDRESS": "msentosa@fmail.com" },
    { "PHONE_NUMBER": "+92 42-7925774" },
    { "REL_ANCHOR_DOMAIN": "SANCTIONS", "REL_ANCHOR_KEY": "sanctions-person-1007" }
  ],
  "PROGRAM": "SANCTIONS",
  "AUTHORITY": "Sanctions Authority",
  "REASON": "Category: Sanctioned",
  "LISTING_DATE": "2015-05-07",
  "STATUS": "Current"
}
```

### Person Sample 3: With Directorship Relationship

```json
{
  "DATA_SOURCE": "SANCTIONS",
  "RECORD_ID": "corp-filings-person-2051",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Patricia", "NAME_LAST": "Smith" },
    { "REL_POINTER_DOMAIN": "CORP_FILINGS", "REL_POINTER_KEY": "corp-filings-org-2071", "REL_POINTER_ROLE": "PRINCIPAL_OF" },
    { "REL_ANCHOR_DOMAIN": "SANCTIONS", "REL_ANCHOR_KEY": "corp-filings-person-2051" }
  ]
}
```

### Company Sample 1: With Previous Name

```json
{
  "DATA_SOURCE": "CORP_FILINGS",
  "RECORD_ID": "corp-filings-org-2011",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_TYPE": "PRIMARY", "NAME_ORG": "Acme Corporation" },
    { "NAME_TYPE": "FORMER", "NAME_ORG": "Universal Exports" },
    { "ADDR_TYPE": "BUSINESS", "ADDR_FULL": "100 Market St, Boston, MA 02109" },
    { "REGISTRATION_COUNTRY": "Singapore" },
    { "REL_ANCHOR_DOMAIN": "CORP_FILINGS", "REL_ANCHOR_KEY": "corp-filings-org-2011" }
  ]
}
```

### Company Sample 2: As Owner (Relationship)

```json
{
  "DATA_SOURCE": "CORP_FILINGS",
  "RECORD_ID": "corp-filings-org-2074",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_ORG": "Holding Company LLC" },
    { "ADDR_TYPE": "BUSINESS", "ADDR_FULL": "Fieldstrasse 10, FL-2198 Triesen, Lichtenstein" },
    { "REGISTRATION_COUNTRY": "Germany" },
    { "REL_POINTER_DOMAIN": "CORP_FILINGS", "REL_POINTER_KEY": "corp-filings-org-2011", "REL_POINTER_ROLE": "OWNER_OF" },
    { "REL_ANCHOR_DOMAIN": "CORP_FILINGS", "REL_ANCHOR_KEY": "corp-filings-org-2074" }
  ]
}
```

### Company Sample 3: Minimal (Target Only)

```json
{
  "DATA_SOURCE": "CORP_FILINGS",
  "RECORD_ID": "corp-filings-org-2071",
  "FEATURES": [
    { "RECORD_TYPE": "ORGANIZATION" },
    { "NAME_ORG": "Tech Services Inc" },
    { "ADDR_TYPE": "BUSINESS", "ADDR_FULL": "3212 W. 32nd St Palm Harbor, FL 60527" },
    { "REL_ANCHOR_DOMAIN": "CORP_FILINGS", "REL_ANCHOR_KEY": "corp-filings-org-2071" }
  ]
}
```

---

## Validation Results

### Linter Tests

**Tool:** lint_senzing_json.py
**Date:** 2025-11-05

**Person Samples:** ✅ PASSED (3 samples, 0 errors)
**Company Samples:** ✅ PASSED (3 samples, 0 errors)

**Test files:**
- `/tmp/ftm_person_samples.jsonl`
- `/tmp/ftm_company_samples.jsonl`

**All samples validated against:**
- Root structure (DATA_SOURCE, RECORD_ID, FEATURES required)
- Feature families (no mixing of attributes across families)
- Relationship rules (REL_ANCHOR max 1 per record, no mixing ANCHOR/POINTER)
- Name rules (no mixing NAME_FULL with parsed components)
- Address rules (no mixing ADDR_FULL with parsed components)

---

## Implementation Notes

### Processing Order

1. **Load all records** into memory by schema type
2. **Build lookup maps:**
   - Sanctions: entity ID → sanction metadata
   - Identifiers: holder ID → identifier details
   - Ownership: owner ID → list of assets
   - Directorship: director ID → list of organizations
3. **Process Person entities:**
   - Merge sanction metadata (if exists)
   - Merge identifier records (if exist)
   - Add REL_POINTER for ownership relationships
   - Add REL_POINTER for directorship relationships
   - Add REL_ANCHOR (all persons are potential targets)
4. **Process Company entities:**
   - Add REL_POINTER for ownership relationships (company as owner)
   - Add REL_ANCHOR (all companies are relationship targets)
5. **Output:** Write merged JSONL

### Edge Cases Handled

1. **Missing firstName/lastName:** Fall back to properties.name as NAME_FULL
2. **Multiple addresses:** Create separate ADDR_FULL features for each
3. **Cross-DATA_SOURCE relationships:** Person (SANCTIONS) can point to Company (CORP_FILINGS)
4. **Empty property lists:** Check list length before extracting
5. **Missing sanction metadata:** Not all persons may be sanctioned; skip payload attributes if not present

---

**End of Mapping Specification**

---

**Generated by Senzing Mapping Assistant v4.0**
**Validated:** All mappings ≥0.80 confidence, all samples passed linter
