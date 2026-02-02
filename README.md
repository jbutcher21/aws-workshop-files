# Senzing Entity Resolution Workshop

Transform source data into Senzing JSON format, load it, and analyze entity resolution results. This repository contains reference materials, Python validation tools, and two hands-on exercises.

**Note:** Workshop course instructions are in a separate repository. This contains the technical files for exercises.

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
│   ├── senzing_tools_reference.md        # Tool documentation
│   └── senzing_mcp_reference.md          # MCP server usage
├── solutions/                            # Reference implementations
│   ├── customers/                        # mapper.md, mapper.py, schema.md
│   └── watchlist/                        # mapper.md, mapper.py, schema.md
└── workspace/                            # Source data for exercises
    ├── customers/customers.csv
    └── watchlist/ftm.jsonl
```

## Key Documents

- **`senzing/senzing_tools_reference.md`** — Describes all tools and when to use them
- **`senzing/prompts/senzing_mapping_assistant.md`** — Guides you through the mapping process
- **`senzing/senzing_mcp_reference.md`** — How to use the MCP server to ask questions about resolved entities

## Workflow

This repository supports a proven method for mapping source systems to Senzing:

1. **Explore Senzing** — Understand the entity resolution environment
2. **Generate Schema** — Analyze source data structure
3. **Map with Assistant** — 5-stage AI-guided process (Init, Inventory, Planning, Mapping, Outputs)
4. **Validate Mapping** — Lint and analyze output quality
5. **Load Data** — Import into Senzing
6. **Analyze Resolved Data** — Run snapshot, explore with MCP server
7. **Key Takeaways** — Review learnings

## Prerequisites

- **Python 3.x** — standard library only
- **Senzing** — pre-configured in workshop environment
- **IDE with AI assistant** — for AI-assisted mapping workflow
- **MCP server** (optional) — test with "Get entity 1"

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

## Resources

- [Senzing Entity Resolution Workshop](TBD) — Workshop instructions and slides
- [Senzing MCP Server](https://github.com/jbutcher21/senzing-mcp-server) — MCP server for entity exploration
- [Senzing Documentation](https://docs.senzing.com)
- [FollowTheMoney Format](https://followthemoney.tech) (for watchlist exercise)
