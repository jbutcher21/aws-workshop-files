# Senzing Entity Resolution Workshop

Transform source data into Senzing JSON format, load it, and analyze entity resolution results. This repository contains reference materials, Python validation tools, and two hands-on exercises.

**Note:** Workshop course instructions are in a separate repository. This contains the technical files for exercises.

## Exercises

### Exercise 1: Customer Data

**Source:** `workspace/customers/customers.csv` (120 records: 114 persons, 6 organizations)

**Complexity:** Introductory — AI agent leads the workflow

**Learning Focus:**
- Name parsing (Last, First Middle → NAME_FIRST, NAME_LAST)
- Identifier type handling (SSN, Driver's License, Passport, National ID)
- Mixed entity types (PERSON and ORGANIZATION in same file)
- Payload attributes (operational data)

**Expected Outcome:** ~78 entities (35% compression)

**Solution:** `solutions/customers/`

---

### Exercise 2: Watchlist Data

**Source:** `workspace/watchlist/ftm.jsonl` (73 FTM records: persons, companies, relationships)

**Complexity:** Advanced — you direct the AI, applying Exercise 1 learnings

**Learning Focus:**
- Complex relationship handling (sanctions, ownership, directorship)
- REL_ANCHOR/REL_POINTER linking between entities
- Merging relationship records onto master entities
- Cross-DATA_SOURCE relationships

**Expected Outcome:** ~92 entities (42% compression). Look for cross-source matches.

**Solution:** `solutions/watchlist/`

## Repository Structure

```
.
├── senzing/                              # Core workshop materials
│   ├── prompts/
│   │   └── senzing_mapping_assistant.md  # AI mapping assistant (5-stage workflow)
│   ├── reference/
│   │   ├── senzing_entity_specification.md  # Master JSON specification
│   │   ├── senzing_mapping_examples.md      # Mapping patterns
│   │   └── identifier_crosswalk.json        # Identifier type mappings
│   ├── tools/                            # Python utilities (stdlib only)
│   │   ├── sz_schema_generator.py        # Generate schema from source data
│   │   ├── lint_senzing_json.py          # Validate JSON structure
│   │   └── sz_json_analyzer.py           # Analyze mapping quality
│   └── senzing_tools_reference.md        # Complete tool documentation
├── solutions/                            # Reference implementations
│   ├── customers/                        # mapper.md, mapper.py, schema.md
│   └── watchlist/                        # mapper.md, mapper.py, schema.md
└── workspace/                            # Source data for exercises
    ├── customers/customers.csv
    └── watchlist/ftm.jsonl
```

## Tools

All Python tools use standard library only — no pip install needed.

### Schema Generator
Analyze source data structure at the start of mapping:
```bash
python3 senzing/tools/sz_schema_generator.py input.csv -o schema.md
```

### Linter (Development)
Validate Senzing JSON structure during development:
```bash
python3 senzing/tools/lint_senzing_json.py output.jsonl
python3 senzing/tools/lint_senzing_json.py --self-test  # verify linter works
```

### Analyzer (Production)
Check full output before loading:
```bash
python3 senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md
```

### Senzing Core Tools
Requires Senzing SDK: `sz_configtool`, `sz_file_loader`, `sz_snapshot`

## Prerequisites

- **Python 3.x** — standard library only
- **Senzing** — pre-configured in workshop environment
- **IDE with AI assistant** — for AI-assisted mapping workflow
- **MCP server** (optional) — test with "Get entity 1"

## Resources

**Reference Files:**
- `senzing/reference/senzing_entity_specification.md` — Master Senzing JSON specification
- `senzing/prompts/senzing_mapping_assistant.md` — AI mapping workflow guide
- `senzing/senzing_tools_reference.md` — Complete tool documentation

**External:**
- [Senzing Documentation](https://docs.senzing.com)
- [FollowTheMoney Format](https://followthemoney.tech) (for watchlist exercise)
