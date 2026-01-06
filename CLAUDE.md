# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Senzing entity resolution workshop repository containing reference materials, Python validation tools, and hands-on exercises for learning data mapping to Senzing JSON format.

## Key Commands

### Workshop Tools (Python 3 stdlib only - no pip install needed)

```bash
# Generate schema documentation from source data
python3 senzing/tools/sz_schema_generator.py <input_file> -o <output>_schema.md

# Validate Senzing JSON structure (development - use on sample records)
python3 senzing/tools/lint_senzing_json.py <file.jsonl>
python3 senzing/tools/lint_senzing_json.py --self-test  # verify linter works

# Analyze mapping quality (production - use on full output before loading)
python3 senzing/tools/sz_json_analyzer.py <input.jsonl> -o <analysis>.md
```

### Senzing Core Tools (require `source ~/.bashrc` for environment)

```bash
# Configure data sources
source ~/.bashrc && sz_configtool -f <config>.g2c

# Load data into Senzing
source ~/.bashrc && sz_file_loader -f <output>.jsonl

# Analyze entity resolution results
source ~/.bashrc && sz_snapshot -o <project>-snapshot-$(date +%Y-%m-%d) -Q
```

### Running Solution Mappers

```bash
# Test with sample records
python3 solutions/customers/customers_mapper.py workspace/customers/customers.csv output.jsonl --sample 10
python3 solutions/watchlist/ftm_mapper.py workspace/watchlist/ftm.jsonl output.jsonl --sample 10
```

## Architecture

### Directory Structure

- `senzing/prompts/` - AI mapping assistant prompt (5-stage workflow guide)
- `senzing/reference/` - Senzing JSON specification, mapping examples, crosswalk files
- `senzing/tools/` - Python validation utilities (stdlib only)
- `solutions/` - Complete reference implementations with mapper.md (spec) and mapper.py (code)
- `workspace/` - Source data files for exercises

### Workflow Pattern

1. **Schema Generation** → `sz_schema_generator.py` analyzes source data structure
2. **AI-Assisted Mapping** → Use `senzing_mapping_assistant.md` prompt for 5-stage workflow
3. **Validation** → `lint_senzing_json.py` validates JSON structure during development
4. **Quality Analysis** → `sz_json_analyzer.py` checks full output before loading
5. **Data Source Config** → `sz_configtool` registers DATA_SOURCE codes
6. **Loading** → `sz_file_loader` loads into Senzing
7. **Analysis** → `sz_snapshot` exports entity resolution statistics

### Tool Distinction

- **lint_senzing_json.py**: Development tool for validating sample JSON records. Exit code 0=pass, 1=errors.
- **sz_json_analyzer.py**: Production tool for analyzing complete JSONL files. Reports feature usage, population stats, and data quality issues.

## Senzing JSON Format

Records use a `FEATURES` array structure:

```json
{
  "DATA_SOURCE": "CUSTOMERS",
  "RECORD_ID": "1001",
  "FEATURES": [
    { "RECORD_TYPE": "PERSON" },
    { "NAME_FIRST": "Robert", "NAME_LAST": "Smith" },
    { "ADDR_LINE1": "123 Main St", "ADDR_CITY": "Las Vegas", "ADDR_STATE": "NV" },
    { "PHONE_NUMBER": "702-555-1212" }
  ],
  "STATUS": "Active"
}
```

Key rules:
- `DATA_SOURCE` and `FEATURES` required at root
- Each feature object contains attributes from ONE feature family only
- Payload attributes (non-matching) go at root level as scalars
- Use `NAME_FIRST/NAME_LAST` for parsed names, `NAME_ORG` for organizations, `NAME_FULL` only when type unknown

## Exercise Details

### Exercise 1: Customers (Introductory)
- Source: `workspace/customers/customers.csv` (120 records)
- Focus: Name parsing, dynamic identifier mapping, mixed PERSON/ORGANIZATION types
- Expected: ~87 entities (27.5% deduplication)

### Exercise 2: Watchlist (Advanced)
- Source: `workspace/watchlist/ftm.jsonl` (73 FTM records)
- Focus: Multi-pass processing, REL_ANCHOR/REL_POINTER relationships
- Expected: 39 entities with cross-DATA_SOURCE relationships

## Reference Files

- `senzing/reference/senzing_entity_specification.md` - Complete Senzing JSON specification
- `senzing/reference/identifier_crosswalk.json` - Identifier type mappings (SSN, PASSPORT, etc.)
- `senzing/SENZING_TOOLS_REFERENCE.md` - Complete tool documentation with examples
