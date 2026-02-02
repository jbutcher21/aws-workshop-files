# Senzing Entity Resolution Workshop

This repository contains materials for learning data mapping and entity resolution with Senzing: reference documentation, Python validation tools, hands-on exercises, and complete solution implementations.

**Note:** Workshop course instructions and presentation slides are in a separate repository.

## Workshop Workflow

Each exercise follows this 7-step process:

| Step | Description | Tool/Resource |
|------|-------------|---------------|
| 1 | Explore Senzing | (instructor guided) |
| 2 | Generate Schema | `sz_schema_generator.py` |
| 3 | Map with Assistant | `senzing_mapping_assistant.md` (5 stages) |
| 4 | Validate Mapping | `lint_senzing_json.py`, `sz_json_analyzer.py` |
| 5 | Load Data | `sz_configtool`, `sz_file_loader` |
| 6 | Analyze Results | `sz_snapshot` |
| 7 | Key Takeaways | (discussion) |

For complete tool documentation, see `senzing/SENZING_TOOLS_REFERENCE.md`.

## Repository Structure

```
.
├── senzing/
│   ├── prompts/
│   │   └── senzing_mapping_assistant.md    # AI mapping assistant (5-stage workflow)
│   ├── reference/
│   │   ├── senzing_entity_specification.md # Senzing JSON specification
│   │   ├── senzing_mapping_examples.md     # Mapping patterns
│   │   └── identifier_crosswalk.json       # Identifier type mappings
│   ├── tools/                              # Python utilities (stdlib only)
│   │   ├── sz_schema_generator.py
│   │   ├── lint_senzing_json.py
│   │   └── sz_json_analyzer.py
│   └── SENZING_TOOLS_REFERENCE.md          # Complete tool documentation
├── solutions/                               # Reference implementations
│   ├── customers/
│   └── watchlist/
└── workspace/                               # Exercise working directories
    ├── customers/
    └── watchlist/
```

## Exercises

### Exercise 1: Customer Data

**Source:** `workspace/customers/customers.csv` (120 records - persons and organizations)

**Learning Focus:**
- Name parsing and basic field mapping
- Dynamic identifier mapping (SSN, Driver's License, Passport)
- Mixed entity types (PERSON/ORGANIZATION)

**Solution:** `solutions/customers/`

### Exercise 2: Watchlist Data

**Source:** `workspace/watchlist/ftm.jsonl` (73 FTM records with relationships)

**Learning Focus:**
- Multi-pass processing for relationships
- REL_ANCHOR/REL_POINTER patterns
- Cross-DATA_SOURCE relationships

**Solution:** `solutions/watchlist/`

## Quick Start

Work with your AI agent throughout. The typical workflow:

**1. Analyze source data**
```bash
python3 senzing/tools/sz_schema_generator.py source.csv -o source_schema.md
```

**2-4. Map with AI assistance**
- Share `senzing/prompts/senzing_mapping_assistant.md` with your AI agent
- The 5-stage workflow guides you through mapping decisions

**5. Validate output**
```bash
python3 senzing/tools/lint_senzing_json.py output.jsonl
python3 senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md
```

**6. Load into Senzing**
```bash
source ~/.bashrc && sz_file_loader -f output.jsonl
```

**7. Analyze results**
```bash
source ~/.bashrc && sz_snapshot -o results -Q
```

## Key Resources

| Resource | Description |
|----------|-------------|
| `senzing/SENZING_TOOLS_REFERENCE.md` | Complete tool documentation with examples |
| `senzing/reference/senzing_entity_specification.md` | Senzing JSON format specification |
| `senzing/prompts/senzing_mapping_assistant.md` | AI mapping assistant prompt |
| `senzing/reference/identifier_crosswalk.json` | Identifier type mappings |

## Prerequisites

- **Python 3.x** - All tools use standard library only
- **Senzing** - Pre-configured in workshop environment
- **IDE with AI assistant** - For AI-assisted mapping workflow

## Additional Resources

- **Senzing Documentation:** https://docs.senzing.com
- **FollowTheMoney Format:** https://followthemoney.tech (for watchlist exercise)
