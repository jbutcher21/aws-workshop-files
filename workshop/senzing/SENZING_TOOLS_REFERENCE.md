# Senzing Tools Reference Guide

## Overview
This document provides command-line reference for Senzing tools used in the workshop environment. This guide is designed to be AI-friendly with explicit success criteria, parameter requirements, and decision logic.

## AI Usage Guidelines

### Decision Logic: Which Tool to Use When
1. **Before loading data:**
   - Use `sz_json_analyzer.py` to analyze data quality and attribute mappings
   - Use `lint_senzing_json.py` to validate JSON format compliance
   - Use `sz_configtool` to add data source if it doesn't exist

2. **For loading data:**
   - Use `sz_file_loader` to load validated JSONL files into Senzing

3. **For querying/analyzing results:**
   - Use `sz_command` for specific entity queries and analysis
   - Use `sz_snapshot` for bulk exports of resolved entities

### Success Validation Pattern
```bash
# Always check exit codes
COMMAND_HERE
if [ $? -eq 0 ]; then
  echo "Success"
else
  echo "Failed with exit code $?"
fi
```

### File Path Requirements
- All file paths can be relative to working directory `/home/ubuntu/workshop/workshop`
- Workshop tools expect: `senzing/tools/script.py`
- Input files should be in current directory or provide full path
- Core Senzing tools use absolute path: `/opt/senzing/er/bin/`

## Tool Locations

### Workshop Tools
**Location:** `/home/ubuntu/workshop/workshop/senzing/tools/`

### Senzing Core Tools  
**Location:** `/opt/senzing/er/bin/`

---

## Workshop Tools (`/home/ubuntu/workshop/workshop/senzing/tools/`)

### sz_json_analyzer.py
**Purpose:** Analyze Senzing JSON files to detect mapping quality and identify issues BEFORE loading into Senzing

**AI Decision Logic:**
- ✅ Use when: After mapping data to Senzing format, BEFORE loading
- ✅ Run AFTER linting passes to check mapping quality
- ✅ Essential for validating custom mappers and transformations
- ✅ Detects issues that linting doesn't catch (data source config, data quality)
- ❌ Skip if: File hasn't changed since last analysis
- ⚠️ **IMPORTANT**: After running this tool, AI MUST summarize the bottom line for the user:
  - Report critical ERRORS that block loading (e.g., DATA_SOURCE not found)
  - Summarize key WARNINGS (low population/uniqueness issues)
  - Count MAPPED vs UNMAPPED attributes
  - Provide actionable next steps based on findings

**Command:**
```bash
python3 senzing/tools/sz_json_analyzer.py <input_file.jsonl> [-o output_file.txt]
```

**Parameters:**
- `input_file` (required): Senzing JSONL file to analyze
- `-o` / `--output_file` (optional): Save analysis report to file instead of displaying in terminal

**Examples:**
```bash
# Analyze and display in terminal (interactive table viewer)
python3 senzing/tools/sz_json_analyzer.py customers_senzing.jsonl

# Save analysis to file for later review
python3 senzing/tools/sz_json_analyzer.py customers_senzing.jsonl -o customers_analysis.txt
```

**AI Workflow:**
```bash
# 1. Lint the file first
python3 senzing/tools/lint_senzing_json.py customers_senzing.jsonl
if [ $? -ne 0 ]; then
  echo "Fix linting errors first"
  exit 1
fi

# 2. Analyze mapping quality
python3 senzing/tools/sz_json_analyzer.py customers_senzing.jsonl -o analysis.txt

# 3. Review the analysis for:
#    - ERROR: DATA_SOURCE not configured (must fix before loading)
#    - WARNING: Low population/uniqueness issues (may affect matching)
#    - INFO: Missing desired attributes (optional improvements)
#    - UNMAPPED: Payload attributes (stored but not used for matching)

# 4. If critical errors found, fix them before loading
# 5. Proceed with sz_file_loader if acceptable
```

**Success Indicators:**
- Exit code: `0`
- Summary message: `N rows processed, completed in X minutes`
- Final message: `creating report...` (terminal) or `Report written to <file>` (file output)

**Output Categories:**

1. **MAPPED** (Green) - Senzing-recognized attributes:
   - Core attributes: DATA_SOURCE, RECORD_ID, RECORD_TYPE
   - Feature families: NAME, ADDRESS, PHONE, EMAIL, DOB, GENDER
   - Identifiers: PASSPORT, DRLIC (drivers license), SSN, NATIONAL_ID
   - Shows hierarchical structure (e.g., NAME > NAME_FIRST, NAME_LAST)

2. **UNMAPPED** (Yellow) - Payload/custom attributes:
   - Stored in Senzing but NOT used for entity resolution
   - Examples: ACCOUNT_BALANCE, CUSTOMER_TIER, ACCOUNT_STATUS
   - Useful for business context but doesn't affect matching

3. **ERROR** (Red) - Critical issues requiring fixes:
   - `DATA_SOURCE not found: <NAME>` - Data source not configured in Senzing
   - **MUST be fixed before loading** - use `sz_configtool` to add data source

4. **WARNING** (Orange) - Data quality issues:
   - `<ATTR> < 25% populated` - Attribute appears in less than 25% of records
   - `<ATTR> < 80% unique` - Low uniqueness may indicate data quality issues
   - May affect matching quality but doesn't block loading

5. **INFO** (Blue) - Optional improvements:
   - `<ATTR> desired` - Recommended attributes that could improve matching
   - Example: NATIONAL_ID_TYPE, NATIONAL_ID_COUNTRY for better ID matching

**Statistics Provided:**
For each attribute:
- **Record Count** - Number of records containing this attribute
- **Record Percent** - Percentage of total records
- **Unique Count** - Number of distinct values
- **Unique Percent** - Uniqueness ratio
- **Top Value1-10** - Most frequent values with counts

**Common Issues Detected:**

| Issue | Category | Action Required |
|-------|----------|-----------------|
| DATA_SOURCE not configured | ERROR | Add data source with sz_configtool before loading |
| Attribute < 25% populated | WARNING | Review data completeness; may need source data fixes |
| Attribute < 80% unique | WARNING | Check for data quality issues or incorrect mapping |
| Phone format variations | WARNING | Standardize phone format in mapper |
| Missing ID_TYPE/ID_COUNTRY | INFO | Add these attributes to improve ID matching |
| Unmapped business attributes | INFO | Expected; payload data stored but not matched on |

**Output Format:**
```
┌──────────┬─────────────┬──────────┬────────┬─────────┬──────────┐
│ Category │ Attribute   │ Records  │ Rec %  │ Unique  │ Top Val  │
├──────────┼─────────────┼──────────┼────────┼─────────┼──────────┤
│ MAPPED   │ DATA_SOURCE │ 120      │ 100.0  │ 1       │ CUST(120)│
│ MAPPED   │ RECORD_ID   │ 120      │ 100.0  │ 120     │ 1001 (1) │
│ MAPPED   │ NAME        │ 120      │ 100.0  │ 113     │ ...      │
│   MAPPED │   NAME_LAST │ 114      │ 95.0   │ 66      │ Smith(13)│
│ UNMAPPED │ ACCT_STATUS │ 99       │ 82.5   │ 3       │ Active92 │
│ ERROR    │ DATA_SOURCE not found: CUSTOMERS │ 120 │ 100.0 │   │      │
│ WARNING  │ GENDER < 25% populated          │     │       │   │      │
│ INFO     │ NATIONAL_ID_TYPE desired        │  4  │ 3.3   │   │      │
└──────────┴─────────────┴──────────┴────────┴─────────┴──────────┘

120 rows processed, completed in 0.0 minutes
```

**Important Behavior:**
- Requires Senzing configuration data to detect mapped vs unmapped attributes
- Uses cached configuration (shows: `Using previously cached configuration data`)
- Interactive terminal display uses color coding and table viewer
- File output is plain text without color codes
- Always run AFTER linting but BEFORE loading data
- Helps catch mapping errors that would waste time during load/test cycles

**Critical Pre-Loading Check:**
```bash
# Check for ERROR category in output
python3 senzing/tools/sz_json_analyzer.py data.jsonl -o analysis.txt
if grep -q "^│ ERROR" analysis.txt; then
  echo "CRITICAL: Fix errors before loading!"
  grep "^│ ERROR" analysis.txt
  exit 1
else
  echo "No critical errors - safe to proceed with loading"
fi
```

**AI Summary Example:**
After running the analyzer, the AI should provide a summary like:

```
Analysis Results for customers_senzing.jsonl:

CRITICAL ERRORS (must fix before loading):
❌ DATA_SOURCE not found: CUSTOMERS
   → Action: Run sz_configtool to add CUSTOMERS data source

MAPPED ATTRIBUTES: 11 feature families recognized
✅ Core: DATA_SOURCE, RECORD_ID, RECORD_TYPE (100% populated)
✅ Names: NAME_LAST (95%), NAME_FIRST (87.5%)
✅ Identifiers: PASSPORT (11.7%), DRLIC (9.2%), SSN (5.8%)
✅ Contact: EMAIL (37.5%), PHONE (17.5%), ADDRESS (60.8%)
✅ Demographics: DOB (51.7%), GENDER (16.7%)

UNMAPPED ATTRIBUTES: 4 payload fields
ℹ️ ACCOUNT_BALANCE, ACCOUNT_STATUS, CUSTOMER_SINCE_DATE, CUSTOMER_TIER
   → These will be stored but not used for entity matching

WARNINGS: 10 data quality issues
⚠️ Low population (<25%): GENDER, DRLIC, SSN, NATIONAL_ID, PASSPORT, PHONE
⚠️ Low uniqueness (<80%): EMAIL, DRLIC, SSN, NATIONAL_ID

NEXT STEPS:
1. Add CUSTOMERS data source using sz_configtool (REQUIRED)
2. Review low population warnings - consider enriching source data
3. After fixing errors, proceed with sz_file_loader
```

### sz_schema_generator.py
**Purpose:** Generate markdown schema with statistics for source CSV or JSON files

**AI Decision Logic:**
- ✅ Use when: Need to understand data structure and field statistics before mapping
- ✅ Run ONLY if schema file doesn't already exist (check first!)
- ❌ Skip if: Schema file already exists for this data source

**Command:**
```bash
python3 senzing/tools/sz_schema_generator.py <input_file> -o <output_schema.md>
```

**Parameters:**
- `input_file` (required): Can be:
  - Single file: `customers.csv`
  - Wildcard pattern: `*.csv`, `data_*.json`
  - Directory path: `/path/to/data/` (processes all CSV, JSON, JSONL, XML, Parquet files)
- `-o` (required): Output file path (`.md` for markdown, `.csv` for CSV format)

**Naming Convention:**
Follow pattern: `<source_filename>_schema.md`
Example: `customers.csv` → `customers_schema.md`

**Examples:**
```bash
# Single file
python3 senzing/tools/sz_schema_generator.py customers.csv -o customers_schema.md

# Multiple files with wildcard (auto-groups by filename)
python3 senzing/tools/sz_schema_generator.py *.csv -o all_schemas.md

# All files in a directory
python3 senzing/tools/sz_schema_generator.py /path/to/data/ -o combined_schema.md
```

**Prerequisites Check:**
```bash
# Check if schema already exists before running
if [ ! -f "customers_schema.md" ]; then
  python3 senzing/tools/sz_schema_generator.py customers.csv -o customers_schema.md
else
  echo "Schema already exists, skipping generation"
fi
```

**Success Indicators:**
- Exit code: `0`
- Output message: `markdown schema saved to <filename>`
- Progress: `reading file 1 of 1: <filename>` followed by `<N> rows read, file complete`

**Failure Indicators:**
- Exit code: Non-zero
- Common errors:
  - File not found
  - Invalid file format
  - Missing required dependencies

**Output Format:**
Markdown file containing:
- File metadata (type, record count, field count)
- Statistics table with columns:
  - Field Name, Type, Records, Pop %, Unique %
  - Table Context
  - Sample 1-5 (top values with frequency counts)

**Multiple File Behavior:**
When processing multiple files (wildcards or directories):
- **Combines all files into ONE output file**
- **Auto-groups by source filename** (creates sections per file)
- Output message: `Auto-grouping by source file (processing N files)`
- Markdown output has separate "## Table: filename" sections for each file
- Useful for analyzing multiple related data sources together

**Important Behavior:**
- ⚠️ OVERWRITES existing schema files without warning
- Processes entire file before writing output
- Works with CSV, JSON, JSONL, Parquet, XML formats
- Auto-detects file format from extension

### lint_senzing_json.py
**Purpose:** Validate Senzing JSON records against entity resolution specification

**AI Decision Logic:**
- ✅ Use when: After generating or modifying Senzing JSON files
- ✅ Run BEFORE loading data to catch format errors early
- ✅ Always validate when converting from other formats
- ❌ Skip if: File already passed linting and hasn't changed

**Command:**
```bash
python3 senzing/tools/lint_senzing_json.py <file.json|file.jsonl|directory>
```

**Parameters:**
- `input_path` (required): Can be:
  - Single JSON file: `customers_senzing.json`
  - Single JSONL file: `customers_senzing.jsonl`
  - Directory path: `/path/to/data/` (recursively validates all .json/.jsonl files)
- `--self-test` (optional): Run built-in tests to verify linter is functional
- `--help` (optional): Display usage information

**Examples:**
```bash
# Validate a single JSONL file
python3 senzing/tools/lint_senzing_json.py customers_senzing.jsonl

# Validate all JSON/JSONL files in a directory (recursive)
python3 senzing/tools/lint_senzing_json.py /path/to/data/

# Test that linter is working correctly
python3 senzing/tools/lint_senzing_json.py --self-test
```

**AI Validation Workflow:**
```bash
# 1. Generate or convert data to Senzing format
# 2. Save to file (e.g., customers_senzing.jsonl)
# 3. Validate before loading
python3 senzing/tools/lint_senzing_json.py customers_senzing.jsonl
if [ $? -eq 0 ]; then
  echo "Validation passed - ready to load"
  # Proceed with sz_file_loader
else
  echo "Validation failed - fix errors before loading"
  exit 1
fi
```

**Success Indicators:**
- Exit code: `0`
- Output message: `OK: All files passed`
- May include warnings (WARN:) that don't cause failure

**Failure Indicators:**
- Exit code: `1`
- Output format: `ERROR: filename:line: error description`
- Final message: `FAIL: N error(s) found`
- Common errors:
  - Missing DATA_SOURCE (required string at root)
  - Missing or non-array FEATURES (required array at root)
  - Missing RECORD_ID (strongly recommended)
  - Invalid JSON syntax
  - Feature attributes at root level (must be in FEATURES array)
  - Mixed feature families in single object
  - Invalid ADDR_FULL/NAME_FULL combinations
  - Non-scalar values in feature objects

**Warning Messages:**
- Format: `WARN: filename:line: warning description`
- Do NOT cause validation failure (exit code 0)
- Common warnings:
  - Missing RECORD_TYPE (recommended but not required)
  - Unknown attribute names

**Validation Rules Enforced:**
1. **Root structure:**
   - Must have DATA_SOURCE (string)
   - Must have FEATURES (array)
   - RECORD_ID strongly recommended (string)
   - Root payload attributes must be scalars only

2. **FEATURES array:**
   - Each item must be a flat object (no nested arrays/objects)
   - Each feature object contains attributes from ONE feature family
   - RECORD_TYPE recommended (PERSON, ORGANIZATION, VESSEL, AIRCRAFT)

3. **Feature families:**
   - NAME: NAME_FIRST, NAME_LAST, NAME_FULL, etc.
   - ADDRESS: ADDR_CITY, ADDR_STATE, ADDR_FULL, etc.
   - PHONE, EMAIL, SSN, PASSPORT, etc.
   - Cannot mix NAME_FULL with NAME_FIRST/NAME_LAST
   - Cannot mix ADDR_FULL with ADDR_CITY/ADDR_STATE, etc.

**Output Format:**
```
WARN: file.jsonl:1: Missing RECORD_TYPE; include when known to prevent cross-type resolution
ERROR: file.jsonl:5: Missing or non-string DATA_SOURCE at root
ERROR: file.jsonl:5: Feature attribute 'NAME_FULL' must be inside FEATURES array, not at root level

FAIL: 2 error(s) found
```

**Important Behavior:**
- Validates JSONL files line-by-line (shows line numbers in errors)
- Validates entire JSON files as single records
- Recursive directory validation (finds all .json/.jsonl files)
- Zero dependencies (no pip install required)
- Fast validation (suitable for CI/CD pipelines)

---

## Senzing Core Tools (`$SENZING_ROOT/bin/`)

All Senzing core tools require the **SENZING_ROOT** environment variable to be set. AIs should check for this variable before running any Senzing core tool.

### sz_configtool
**Purpose:** Configure Senzing data sources and settings

**Environment Check:**
```bash
if [ -z "$SENZING_ROOT" ]; then
  echo "ERROR: SENZING_ROOT not set - initialize Senzing environment first"
  exit 1
fi
```

**Usage:**
```bash
echo -e "addDataSource <DATASOURCE_NAME>\nsave\ny\nquit" | $SENZING_ROOT/bin/sz_configtool
```

**Example:**
```bash
echo -e "addDataSource CUSTOMERS\nsave\ny\nquit" | $SENZING_ROOT/bin/sz_configtool
```

**Interactive Mode:**
```bash
$SENZING_ROOT/bin/sz_configtool
```

**Common Commands:**
- `addDataSource <NAME>` - Add new data source
- `listDataSources` - List configured data sources
- `save` - Save configuration changes
- `quit` - Exit tool

### sz_file_loader
**Purpose:** Load Senzing JSON records into the entity resolution engine and perform entity resolution

**AI Decision Logic:**
- ✅ Use when: Ready to load validated data into Senzing
- ✅ Run AFTER: linting, analysis, and adding data sources with sz_configtool
- ❌ DO NOT run before: Validating with linter and analyzer
- ⚠️ **IMPORTANT**: After loading, AI MUST summarize the bottom line for the user:
  - Report load statistics (records processed, errors)
  - Summarize entity resolution results (entities created, matches found)
  - Note any failures or issues
  - Provide next steps (query with sz_command, export with sz_snapshot)

**Prerequisites (REQUIRED):**
1. ✅ Senzing environment must be initialized (SENZING_ROOT environment variable must be set)
2. ✅ File must pass `lint_senzing_json.py` validation
3. ✅ File must be analyzed with `sz_json_analyzer.py` (no critical errors)
4. ✅ All DATA_SOURCE values must be configured with `sz_configtool`

**Environment Check:**
```bash
# AI should ALWAYS check this before running sz_file_loader
if [ -z "$SENZING_ROOT" ]; then
  echo "ERROR: SENZING_ROOT environment variable not set"
  echo "Please initialize the Senzing environment first"
  exit 1
fi

# Tool location: $SENZING_ROOT/bin/sz_file_loader
```

**Command:**
```bash
$SENZING_ROOT/bin/sz_file_loader -f <file.jsonl>
```

**Parameters:**
- `-f <file>` (required): Path to Senzing JSONL file to load

**Optional Parameters:**
- `-w` - Produce with-info messages (detailed resolution info per record)
- `-t` - Debug trace information
- `-nt <num>` - Number of threads (for parallel processing)
- `-n` - Disable redo processing (faster but may miss some matches)
- `-ns` - Don't shuffle input files (use if already shuffled)
- `-l` - Use logging style output

**Examples:**
```bash
# Basic load
$SENZING_ROOT/bin/sz_file_loader -f customers_senzing.jsonl

# Load with detailed info
$SENZING_ROOT/bin/sz_file_loader -f customers_senzing.jsonl -w

# Load with multiple threads for performance
$SENZING_ROOT/bin/sz_file_loader -f customers_senzing.jsonl -nt 4
```

**AI Pre-Loading Workflow:**
```bash
# 0. Check Senzing environment
if [ -z "$SENZING_ROOT" ]; then
  echo "STOP: SENZING_ROOT not set - initialize Senzing environment first"
  exit 1
fi

# 1. Validate format
python3 senzing/tools/lint_senzing_json.py customers_senzing.jsonl
if [ $? -ne 0 ]; then
  echo "STOP: Fix linting errors first"
  exit 1
fi

# 2. Analyze mapping quality
python3 senzing/tools/sz_json_analyzer.py customers_senzing.jsonl -o analysis.txt

# 3. Check for critical errors
if grep -q "DATA_SOURCE not found" analysis.txt; then
  echo "STOP: Add missing data sources with sz_configtool first"
  exit 1
fi

# 4. Load data
$SENZING_ROOT/bin/sz_file_loader -f customers_senzing.jsonl

# 5. Check exit code
if [ $? -eq 0 ]; then
  echo "Load completed successfully"
else
  echo "Load failed - review error messages"
  exit 1
fi
```

**Success Indicators:**
- Exit code: `0`
- Progress messages showing records loaded
- Final summary with statistics
- No error messages in output
- Output shows: "X records processed, Y entities created"

**Failure Indicators:**
- Exit code: Non-zero
- Error messages during load
- Common errors:
  - `DATA_SOURCE not configured` - Run sz_configtool first
  - `Invalid JSON format` - Run linter to fix
  - `Database connection error` - Check Senzing configuration
  - `Permission denied` - Check file/database permissions

**Output Format:**
```
Loading file: customers_senzing.jsonl
Processing records...
.................................................
Records processed: 120
Records loaded with success: 120
Records loaded with errors: 0

Entity Resolution Results:
- Total entities: 87
- Total relationships: 0
- Entities with multiple records: 33
- Single record entities: 54

Redo processing:
- Records requiring redo: 35
- Redo operations completed: 35

Load completed in 2.3 seconds
```

**Key Metrics to Report:**
1. **Records processed** - Total input records
2. **Records with errors** - Failed loads (should be 0)
3. **Total entities** - Unique resolved entities created
4. **Entities with multiple records** - Records that matched together
5. **Single record entities** - Records with no matches

**AI Summary Example:**
After running sz_file_loader, the AI should provide a summary like:

```
Load Results for customers_senzing.jsonl:

✅ LOAD SUCCESSFUL
📊 Records: 120 processed, 0 errors
🎯 Entity Resolution: 87 entities created
   - 33 entities resolved from multiple records (27.5%)
   - 54 single-record entities (72.5%)
🔄 Redo Processing: 35 operations completed

KEY FINDINGS:
- 33 duplicate customer records were identified and resolved into entities
- Example: "Smith, Bob" had 4 different customer IDs that matched to 1 entity
- 54 customers had unique identities with no matches

NEXT STEPS:
1. Query specific entities: $SENZING_ROOT/bin/sz_command -C getEntityByEntityID <id>
2. Search for entities: $SENZING_ROOT/bin/sz_command -C searchByAttributes '{"NAME_LAST":"Smith"}'
3. Export results: $SENZING_ROOT/bin/sz_snapshot -o customers_results
4. Review matched entities to validate resolution quality
```

**Important Behavior:**
- Loads data directly into Senzing database
- Performs entity resolution during load
- Redo processing runs automatically to catch late-binding matches
- Progress dots appear during load (one per batch)
- Can be interrupted with Ctrl+C (partial load will remain)
- Idempotent: Can reload same file (duplicate RECORD_IDs will update existing records)

### sz_command
**Purpose:** Interactive demonstration tool for the Senzing SDK - execute API functions directly

**Usage:**
```bash
$SENZING_ROOT/bin/sz_command -C <command> [args...]
```

**Key Commands:**
- **get functions** - Retrieve entity information
- **why functions** - Explain why entities matched or didn't match
- **how functions** - Show how entities are related
- **do_ functions** - Execute various SDK operations

**Examples:**
```bash
# Get entity by ID
$SENZING_ROOT/bin/sz_command -C getEntityByEntityID 1

# Get entity by record
$SENZING_ROOT/bin/sz_command -C getEntityByRecordID CUSTOMERS 1001

# Explain why entities matched
$SENZING_ROOT/bin/sz_command -C whyEntityByEntityID 1

# Show how entities are related
$SENZING_ROOT/bin/sz_command -C howEntityByEntityID 1

# Search for entities
$SENZING_ROOT/bin/sz_command -C searchByAttributes '{"NAME_FULL":"John Smith"}'
```

**Key Options:**
- `-C <command>` - Run specific command (required)
- `-c <ini_file>` - Use custom configuration file
- `-f <file>` - Run commands from file

**Output:** JSON responses from Senzing SDK showing:
- Entity details and relationships
- Match explanations and scoring
- Search results
- API responses

### sz_snapshot
**Purpose:** Analyze entity resolution match quality and export statistics about resolved entities

**AI Decision Logic:**
- ✅ Use when: After loading data with sz_file_loader to analyze match quality
- ✅ Run to understand: How many matches were made and what types
- ✅ Essential for: Validating entity resolution results before production use
- ⚠️ **IMPORTANT**: After running, AI MUST summarize the bottom line for the user:
  - Report total entities vs total records
  - Summarize matches within data sources vs across data sources
  - Identify entities with multiple data sources (linked records)
  - Note entities by size (singles, pairs, large clusters)
  - Provide entity IDs that can be queried with Senzing MCP server

**Command:**
```bash
$SENZING_ROOT/bin/sz_snapshot -o <output_file_path>
```

**Parameters:**
- `-o <file_path>` (required): Full output file path and name (will create `.json` file)

**Optional Parameters:**
- `-Q` - Quiet mode (overwrites existing file without prompting, recommended for AI automation)
- `-d <datasource>` - Filter by specific data source
- `-s <size>` - Sample size (limit number of entities analyzed)
- `-f <filter>` - Relationship filter:
  - `1` = No relationships
  - `2` = Include possible matches
  - `3` = Include all relationships
- `-A` - Export CSV format for audit

**Naming Convention:**
Recommended format: `<project>-snapshot-<date>`
- Example: `customers-snapshot-2025-01-15`
- Makes it easy to track analysis over time

**Examples:**
```bash
# Basic snapshot with date (will prompt if file exists)
$SENZING_ROOT/bin/sz_snapshot -o customers-snapshot-2025-01-15

# Quiet mode - overwrites without prompting (recommended for AI automation)
$SENZING_ROOT/bin/sz_snapshot -o customers-snapshot-2025-01-15 -Q

# Snapshot filtered by data source
$SENZING_ROOT/bin/sz_snapshot -o customers-only-2025-01-15 -d CUSTOMERS -Q

# Snapshot with all relationships
$SENZING_ROOT/bin/sz_snapshot -o full-analysis-2025-01-15 -f 3 -Q
```

**AI Usage Pattern:**
```bash
# Always use -Q flag for automated workflows to avoid interactive prompts
DATE=$(date +%Y-%m-%d)
$SENZING_ROOT/bin/sz_snapshot -o customers-snapshot-$DATE -Q
```

**Output Files Generated:**
Creates JSON file at specified path containing structured statistics

**Statistics Tracked:**
1. **Matches within a data source** - Records from same data source that matched
   - Example: Two CUSTOMERS records matched to one entity
   - Includes entity IDs and record counts

2. **Matches across data sources** - Records from different data sources that matched
   - Example: CUSTOMERS record matched with WATCHLIST record
   - Shows cross-source linkages

3. **Entities with records in multiple data sources** - Entities appearing in 2+ sources
   - Example: Person found in both CUSTOMERS and SANCTIONS
   - Critical for compliance and screening

4. **Entities by size** - Distribution of how many records per entity
   - Singles: 1 record = 1 entity (no matches)
   - Pairs: 2 records matched together
   - Large clusters: 3+ records matched together
   - Helps identify data quality issues (too many matches may indicate over-matching)

**Output Structure:**
```json
{
  "statistics": {
    "total_entities": 87,
    "total_records": 120,
    "within_source_matches": {
      "count": 25,
      "entity_ids": [1, 5, 12, ...]
    },
    "cross_source_matches": {
      "count": 8,
      "entity_pairs": [
        {"entity_id": 42, "sources": ["CUSTOMERS", "WATCHLIST"]},
        ...
      ]
    },
    "entities_by_size": {
      "singles": {"count": 54, "entity_ids": [...]},
      "pairs": {"count": 20, "entity_ids": [...]},
      "triples": {"count": 10, "entity_ids": [...]},
      "large_clusters": {"count": 3, "entity_ids": [...]}
    },
    "multi_source_entities": {
      "count": 8,
      "entities": [
        {"entity_id": 42, "sources": ["CUSTOMERS", "SANCTIONS"], "record_count": 3},
        ...
      ]
    }
  }
}
```

**Using Entity IDs with Senzing MCP Server:**
Once you have entity IDs from the snapshot, retrieve full entity details:
```bash
# Via sz_command
$SENZING_ROOT/bin/sz_command -C getEntityByEntityID <entity_id>

# Via Senzing MCP server (if available)
# Use the MCP tool to query entity details by ID
```

**AI Summary Example:**
After running sz_snapshot, the AI should provide a summary like:

```
Snapshot Analysis Results:

✅ SNAPSHOT GENERATED: customers-snapshot-2025-01-15.json

📊 ENTITY RESOLUTION SUMMARY:
- Total Records Loaded: 120
- Total Entities Created: 87
- Deduplication Rate: 27.5% (33 duplicate records resolved)

🔗 MATCH ANALYSIS:
Within-Source Matches: 25 entities
  → 25 entities had multiple records from the SAME data source
  → Top examples: Entity IDs [12, 45, 67]

Cross-Source Matches: 8 entities
  → 8 entities matched across DIFFERENT data sources
  → Example: Entity 42 linked CUSTOMERS + SANCTIONS records
  → Review these for compliance/screening purposes

📈 ENTITY SIZE DISTRIBUTION:
- Singles (1 record): 54 entities (62%)
- Pairs (2 records): 20 entities (23%)
- Triples (3 records): 10 entities (11.5%)
- Large clusters (4+ records): 3 entities (3.5%)

⚠️ MULTI-SOURCE ENTITIES: 8 found
Critical entities appearing in multiple data sources:
  - Entity 42: CUSTOMERS + SANCTIONS (3 records)
  - Entity 58: CUSTOMERS + WATCHLIST (2 records)
  → ACTION: Review these entities for compliance

NEXT STEPS:
1. Query specific entities: $SENZING_ROOT/bin/sz_command -C getEntityByEntityID 42
2. Review large clusters (may indicate over-matching): Entity IDs [101, 102, 103]
3. Investigate multi-source matches for business impact
4. Use Senzing MCP server to retrieve full entity details
```

**Success Indicators:**
- Exit code: `0`
- Output file created: `<prefix>.json`
- Statistics show reasonable match rates
- Final message: "Snapshot complete"

**Failure Indicators:**
- Exit code: Non-zero
- No output file generated
- Common errors:
  - `No entities found` - Database empty, load data first
  - `Permission denied` - Check file write permissions
  - `SENZING_ROOT not set` - Initialize Senzing environment

**Important Behavior:**
- Reads from Senzing database (does not modify data)
- Can be run multiple times without side effects
- Processing time scales with database size
- Each stat category includes entity/pair IDs for drill-down analysis
- Use snapshot to validate match quality before production deployment

---

## Common Workflows

### 1. Complete Data Mapping and Loading
```bash
# 1. Analyze source data
python3 senzing/tools/sz_json_analyzer.py source_data.jsonl

# 2. Validate JSON format
python3 senzing/tools/lint_senzing_json.py source_data.jsonl

# 3. Add data source to configuration
echo -e "addDataSource MYDATASOURCE\nsave\ny\nquit" | $SENZING_ROOT/bin/sz_configtool

# 4. Load data into Senzing
$SENZING_ROOT/bin/sz_file_loader -f source_data.jsonl

# 5. Take snapshot of results
$SENZING_ROOT/bin/sz_snapshot -o results_snapshot
```

### 2. Data Quality Check
```bash
# Analyze data quality before loading
python3 senzing/tools/sz_json_analyzer.py data.jsonl

# Validate format compliance
python3 senzing/reference/lint_senzing_json.py data.jsonl
```

### 3. Export Results
```bash
# Export all resolved entities
/opt/senzing/er/bin/sz_snapshot -o full_export

# Export specific data source only
/opt/senzing/er/bin/sz_snapshot -o filtered_export -d CUSTOMERS

# Export with relationships
/opt/senzing/er/bin/sz_snapshot -o with_relationships -f 3
```

### 4. Query and Analyze Results
```bash
# Get specific entity details
/opt/senzing/er/bin/sz_command -C getEntityByEntityID 1

# Find entity by source record
/opt/senzing/er/bin/sz_command -C getEntityByRecordID CUSTOMERS 1001

# Explain why entities matched
/opt/senzing/er/bin/sz_command -C whyEntityByEntityID 1

# Search for similar entities
/opt/senzing/er/bin/sz_command -C searchByAttributes '{"NAME_FULL":"John Smith"}'

# Show entity relationships
/opt/senzing/er/bin/sz_command -C howEntityByEntityID 1
```

---

## File Formats

### Input: Senzing JSON (JSONL)
```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "1001",
  "FEATURES": [
    {"RECORD_TYPE": "PERSON"},
    {"NAME_FULL": "John Smith"},
    {"EMAIL_ADDRESS": "john@example.com"}
  ],
  "STATUS": "Active"
}
```

### Output: Snapshot JSON
```json
{
  "SOURCE": "sz_snapshot",
  "TOTALS": {
    "ENTITY_COUNT": 83,
    "RECORD_COUNT": 120,
    "MATCH": {
      "ENTITY_COUNT": 33,
      "RECORD_COUNT": 35
    }
  },
  "ENTITIES": {
    "1": {
      "RECORDS": [...]
    }
  }
}
```

---

## Troubleshooting

### Common Issues

**sz_json_analyzer shows "DATA_SOURCE not found"**
- Solution: Add data source using sz_configtool first

**sz_file_loader fails with "unrecognized arguments"**
- Solution: Use `-f` flag: `sz_file_loader -f file.jsonl`

**lint_senzing_json reports format errors**
- Solution: Fix JSON structure, ensure FEATURES is array of objects

**sz_snapshot creates empty file**
- Solution: Ensure data is loaded first with sz_file_loader

### Performance Tips

1. **Loading large files:** Use multiple threads with `-nt` option
2. **Skip shuffling:** Use `-ns` for pre-shuffled files
3. **Disable redo:** Use `-n` for faster initial loads
4. **Batch processing:** Split large files into smaller chunks

---

## Environment Notes

- **Working Directory:** `/home/ubuntu/workshop/workshop`
- **Python Version:** Python 3.x required for workshop tools
- **Senzing Version:** 4.1.0 (as of last check)
- **Database:** SQLite3 backend (`/home/ubuntu/sz_sqlite/G2C.db`)

---

*Last Updated: November 2025*
*Workshop Environment: Amazon Q Developer*
