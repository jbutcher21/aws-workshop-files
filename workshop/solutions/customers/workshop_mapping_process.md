# Workshop: Mapping Customer Data to Senzing Format

## Module 4: Hands-On Mapping Exercise

### Task: Map customers.csv to Senzing JSON format

---

## Step 1: Understand the Source Data

**Current State:**
- File: `workspace/customers/customers.csv`
- Records: 120 customers (114 individuals, 6 companies)
- Fields: 19 fields total

**Field Structure:**
```
customer_id, customer_name, customer_type, gender, dob,
address, city, state, zip_code, country, phone, email,
id_type, id_number, id_country, registration_date,
account_status, account_balance, customer_tier
```

**Key Observations:**
- customer_type: "I" (Individual) or "C" (Company)
- customer_name: Format is "Last, First Middle" for individuals, or company name for companies
- id_type: SSN, DRIVERS_LICENSE, PASSPORT, NATIONAL_ID (only 30% have IDs)
- Dates in various formats (need standardization)
- Mix of parsed and full addresses

---

## Step 2: Review Senzing Entity Specification

**Reference Materials:**
- Location: `workshop/senzing/reference/senzing_entity_specification.md`
- Key concepts to understand:
  - Entities (PERSON vs ORGANIZATION)
  - Features (NAME, ADDRESS, PHONE, etc.)
  - Attributes (individual fields within features)
  - Usage Types (PRIMARY, HOME, MOBILE, etc.)
  - Payload attributes (non-matching fields like STATUS, dates, amounts)

**High-Priority Features for Mapping:**
1. RECORD_TYPE - Distinguish PERSON vs ORGANIZATION
2. NAME - Person names (parsed) or organization names
3. DOB - Date of birth for persons
4. ADDRESS - Physical addresses
5. PHONE - Telephone numbers
6. EMAIL - Email addresses
7. Identifiers - SSN, DRLIC, PASSPORT, NATIONAL_ID

---

## Step 3: AI-Assisted Mapping Prompts

### Prompt 1: Initial Analysis
```
I need to map a customer CSV file to Senzing JSON format.

Source file: workspace/customers/customers.csv
Schema documentation: workspace/solutions/customers/customers_schema.md
Target format: Senzing JSON (see senzing/reference/senzing_entity_specification.md)

Please analyze the source schema and suggest a mapping strategy for:
1. RECORD_TYPE (customer_type: I=PERSON, C=ORGANIZATION)
2. NAME features (customer_name field needs parsing for persons)
3. DATE_OF_BIRTH (dob field - various formats)
4. ADDRESS (combination of address, city, state, zip_code, country)
5. PHONE and EMAIL
6. Identifiers (id_type, id_number, id_country)
7. Payload attributes (registration_date, account_status, account_balance, customer_tier)
```

---

## Prompts to Accumulate:

### Current Session Prompts:

**User:** "ok lets go back to the customers.csv file. Next thing we need to do is map it."

**User:** "for this next part I want you to start capturing the process for workshop. you should start accumulating the prompts as well, ok?"

**User:** "I will do the video later, but capture this for now to see how it goes, ok>"

**Assistant:** "Absolutely! I'll continue documenting everything as we go through the mapping process. This will become the demo script for your video."

**User:** "please load the mapping assistant prompt from the senzing folder"

**Assistant:** "Loaded: `workshop/senzing/prompts/senzing_mapping_assistant.md` - This is the Senzing Mapping Assistant v4 prompt that guides the 5-stage mapping workflow."

**User:** "yes"

**Assistant:** "Starting the Senzing Mapping Assistant workflow..."

---

## IMPORTANT NOTE:

**Assistant should have asked:** "Which file or schema would you like to map?"

**User would provide:** "customers.csv" or "workspace/customers/customers.csv" or "the customers schema"

**In the workshop video, emphasize:**
- The AI needs YOU to tell it what to map
- You can provide a file path, schema document, or description
- This is the starting point for the mapping conversation

---

**User:** "note: you should have had to ask me what file or schema I wanted to map. And yes, proceed"

**Assistant:** [Stage 2 Complete - Inventory extracted, 19 fields identified]

**Assistant:** [Stage 3 Planning - Asked for DATA_SOURCE code]

**User:** "CUSTOMERS"

**Assistant:** [Stage 3 Complete - DATA_SOURCE set to CUSTOMERS, ready for mapping]

**User:** "YES"

**Assistant:** [Starting Stage 4 - Field-by-field mapping...]

**Assistant:** [Presented complete mapping table for all 19 fields - all high confidence 1.0]

**User:** "yes"

**Assistant:** [Generating sample JSON records...]

**Assistant:** [Generated samples, ran linter, discovered payload vs feature distinction, corrected JSON - PASSED]

**User:** "Should that be the senzing feature registration date? Tell me why you think so."

**Assistant:** [Explained reasoning - spec says REGISTRATION_DATE is for org incorporation dates, but our data is customer signup dates for both persons and orgs. Asked clarification: A) Legal incorporation or B) Customer registration?]

**User:** "B"

**Assistant:** "Perfect! Then registration_date should be PAYLOAD, not a Senzing feature. It represents when they became a customer (operational data), not when an organization was legally incorporated (identifying feature)."

**Assistant:** [Tested with linter - ERROR: REGISTRATION_DATE conflicts with Senzing feature name]

**Assistant:** [Offered two options: 1) Rename to CUSTOMER_REGISTRATION_DATE (payload), or 2) Keep as REGISTRATION_DATE feature]

**User:** "1"

**Assistant:** "Excellent choice! We'll map registration_date → CUSTOMER_REGISTRATION_DATE (payload attribute). This avoids the naming conflict and clearly indicates it's customer relationship data."

**Assistant:** [Tested with linter - PASSED with CUSTOMER_REGISTRATION_DATE]

**User:** "I think the senzing parser will still see this as REGISTRATION_DATE because you can prefix a usage_type at the root level. Please rename that field to CUSTOMER_SINCE_DATE"

**Assistant:** "Excellent catch! You're right - the parser could interpret CUSTOMER_REGISTRATION_DATE as CUSTOMER (usage type) + REGISTRATION_DATE (feature). CUSTOMER_SINCE_DATE is much clearer and won't be misinterpreted."

**Assistant:** [Tested with linter - PASSED with CUSTOMER_SINCE_DATE]

**User:** "YES"

**Assistant:** [Proceeding to Stage 5 - Generating outputs...]

**Assistant:** [Generated 3 files: README.md, customers_mapper.md, customers_mapper.py]

**Assistant:** [Ran full mapper on 120 records - ALL PASSED linter validation]

**User:** "Ok I also want you to run the sz_json_analyzer to see what senzing recognizes. I want to see the result"

**Assistant:** [Ran sz_json_analyzer.py on the mapped output]

## Senzing Analysis Results

**Key Findings from sz_json_analyzer:**

### MAPPED Features (Senzing Recognized):
- ✅ **DATA_SOURCE**: CUSTOMERS (120 records)
- ✅ **RECORD_ID**: 120 records, 100% unique
- ✅ **RECORD_TYPE**: PERSON (114), ORGANIZATION (6)
- ✅ **NAME**: 120 records, 94.2% unique
  - NAME_ORG: 6 organizations
  - NAME_LAST: 114 persons (66 unique)
  - NAME_FIRST: 105 records (76 unique)
  - NAME_MIDDLE: 9 records
- ✅ **DOB**: 62 records (51.7%), 34 unique dates
- ✅ **GENDER**: 20 records (16.7%)
- ✅ **ADDRESS**: 73 records (60.8%)
  - ADDR_LINE1: 73 records
  - ADDR_CITY: 38 records
  - ADDR_STATE: 34 records
  - ADDR_POSTAL_CODE: 37 records
  - ADDR_COUNTRY: 6 records
- ✅ **PHONE**: 21 records (17.5%)
- ✅ **EMAIL**: 45 records (37.5%)
- ✅ **Identifiers:**
  - PASSPORT: 14 records (11.7%)
  - DRLIC: 11 records (9.2%)
  - SSN: 7 records (5.8%)
  - NATIONAL_ID: 4 records (3.3%)

### UNMAPPED (Payload Attributes):
- **ACCOUNT_BALANCE**: 90 records (75%)
- **ACCOUNT_STATUS**: 99 records (82.5%)
- **CUSTOMER_SINCE_DATE**: 99 records (82.5%)
- **CUSTOMER_TIER**: 9 records (7.5%)

### Errors & Warnings:
- ⚠️ **ERROR**: DATA_SOURCE "CUSTOMERS" not found in Senzing config (expected - would need to be added to config)
- ⚠️ **WARNINGS**: Low population for some identifiers (<25%) - this is expected for real-world data

**Interpretation:**
- All features correctly recognized by Senzing
- Payload attributes properly excluded from matching (shown as UNMAPPED)
- Warnings are normal for sparse optional fields
- Ready for loading into Senzing!

---

## Next Steps: Loading and Exploring the Data

**User:** "ok, so while I cant do this now, the next steps will be to register the data source with sz_configtool. to load the jsonl file with sz_file_loader, to take a snapshot with sz_snapshot and to explore it with sz_explorer. (these are all tools installed with the senzing sdk). I will be asking the AI to run these programs for me. Then we will move on to do this whole process for the ftm watchlist"

### Module 5: Load and Validate (To be demonstrated)

**Step 1: Register the DATA_SOURCE**
```bash
# Use sz_configtool to add "CUSTOMERS" data source to Senzing config
# This resolves the "DATA_SOURCE not found" error
```

**Step 2: Load the mapped data**
```bash
# Use sz_file_loader to load customers_senzing.jsonl into Senzing
sz_file_loader -f customers_senzing.jsonl
```

**Step 3: Take a snapshot**
```bash
# Use sz_snapshot to create a point-in-time view of entities
sz_snapshot -o customers_snapshot.json
```

**Step 4: Explore the results**
```bash
# Use sz_explorer to interactively explore resolved entities
sz_explorer
```

**What to look for:**
- How many entities resolved from 120 records?
- Did the 3 "Mooney Susan" records resolve to 1 entity?
- Which features contributed to entity resolution?
- Are duplicate customers correctly identified?

### Then: Repeat for Watchlist FTM Data

After validating the customers mapping, the same process will be repeated for:
- **Source:** workspace/watchlist/ftm.jsonl (70 FTM entities)
- **Challenge:** More complex structure (nested properties, relationships)
- **Goal:** Map FTM format → Senzing JSON format
- **Include:** Sanction, Ownership, Directorship relationships

---

## Mapping Assistant Workflow Overview

The Senzing Mapping Assistant follows a 5-stage process:

1. **STAGE 1: INIT** - Load reference files and verify they're available
2. **STAGE 2: INVENTORY** - Extract all source fields, build complete inventory
3. **STAGE 3: PLANNING** - Identify entities, determine DATA_SOURCE codes
4. **STAGE 4: MAPPING** - Map each field to Senzing features or payload, generate JSON
5. **STAGE 5: OUTPUTS** - Generate README, mapping spec, and Python mapper

**Key Principles:**
- NO guessing - always ask when uncertain
- EVERY field must be dispositioned (Feature/Payload/Ignore)
- Validate with linter before approval
- One question at a time for low-confidence items

---

## Next Steps:
1. Create mapping script with AI assistance
2. Handle name parsing for individuals (Last, First Middle format)
3. Standardize date formats
4. Map identifier types to Senzing features
5. Test mapping on sample records
6. Validate output against Senzing spec

---

## Notes:
- This is the hands-on portion where students learn to map real-world data
- Emphasize iterative refinement with AI assistance
- Students should reference the entity specification throughout
- Use the schema files as reference for understanding source data structure
