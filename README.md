# Senzing Entity Resolution Workshop

This repository contains all materials for learning data mapping and entity resolution with Senzing. You'll find reference materials, validation tools, workshop exercises with source data, and complete solution implementations.

**What's Included:**
- Reference documentation for Senzing JSON format
- Python tools for schema analysis, validation, and quality checking
- Two hands-on exercises (customer data and watchlist data)
- Complete solution implementations with mapper code
- AI mapping assistant prompt for guided development

**Note:** Workshop course instructions and presentation slides are in a separate repository. This repository contains the technical files you'll work with during exercises.

## First Steps (Start Here!)

You've just opened this folder in your IDE with your AI agent plugin open.  Here's what to do:

1. **Read this README** - Understand what's in this repository and how the workshop works
2. **Explore the `senzing/` directory** - This contains all the reference materials, tools, and prompts you'll use
3. **Ask your AI agent** - Your AI agent can help you understand the materials. Try asking:
   - "What's in the senzing/ directory?"
   - "Show me the Senzing entity specification"
   - "Explain what the AI mapping assistant does"
4. **Start Exercise 1** - Begin with the customer data exercise, then move on to the watchlist exercise

**Key Point:** Throughout this workshop, you'll work *with* your AI agent. The AI mapping assistant prompt is designed to help your agent guide you through the entire mapping process.

## Workshop Overview

In this workshop, you'll learn to transform source data into Senzing JSON format using AI-assisted mapping, then load and analyze entity resolution results. The workshop uses a structured 5-stage mapping workflow guided by an AI assistant.

### What You'll Learn

- Understand Senzing JSON entity specification and format
- Use schema analysis and validation tools
- Create data mappings with AI assistance
- Handle different data formats (CSV, JSONL)
- Work with relationships (REL_ANCHOR/REL_POINTER)
- Load data into Senzing and analyze entity resolution results

### Workshop Flow

1. **Introduction to Materials**
   - Overview of prompts, references, and tools in `senzing/`
   - Understanding the Senzing entity model
   - Introduction to the AI mapping assistant

2. **AI-Assisted Mapping Workflow**
   - Ask your AI agent to load the `senzing_mapping_assistant.md` prompt
   - Your AI agent guides you through a 5-stage mapping process:
     - Stage 1: Initialize (load references, verify tools)
     - Stage 2: Inventory (extract all source fields)
     - Stage 3: Planning (identify entities, determine DATA_SOURCE codes)
     - Stage 4: Mapping (decide how to handle each field)
     - Stage 5: Outputs (generate README, specification, mapper code)

3. **Complete Two Exercises**
   - Exercise 1: Customer data (simpler introduction)
   - Exercise 2: Watchlist data (advanced with relationships)
   - For each exercise, you'll:
     - Analyze source data with schema generator
     - Map to Senzing JSON format (AI-assisted)
     - Validate with linter
     - Analyze quality before loading
     - Load into Senzing
     - Review entity resolution results

## Workshop Exercises

### Exercise 1: Customer Data Mapping

**Source:** CSV file with 120 customer records (114 persons, 6 organizations)

**Complexity:** Introductory

**Learning Focus:**
- Basic field mapping (names, addresses, phones, emails)
- Name parsing (Last, First Middle → NAME_FIRST, NAME_LAST)
- Identifier type handling (SSN, Driver's License, Passport, National ID)
- Mixed entity types (PERSON and ORGANIZATION in same file)
- Payload attributes (operational data)

**Files:**
- Source data: `workspace/customers/customers.csv`
- Solution: `solutions/customers/`

### Exercise 2: Watchlist Data Mapping

**Source:** FTM (FollowTheMoney) JSONL with 73 records including persons, companies, and relationships

**Complexity:** Advanced

**Learning Focus:**
- Complex relationship handling (sanctions, ownership, directorship)
- Relationship linking between entities
- Merging relationship records onto master entities
- Cross-DATA_SOURCE relationships
- Sanction metadata as payload

**Files:**
- Source data: `workspace/watchlist/ftm.jsonl`
- Solution: `solutions/watchlist/`

## Repository Structure

```
.
├── senzing/                          # Core workshop materials
│   ├── prompts/
│   │   └── senzing_mapping_assistant.md    # AI mapping assistant prompt
│   ├── reference/
│   │   ├── senzing_entity_specification.md # Master specification
│   │   ├── senzing_mapping_examples.md     # Mapping patterns
│   │   └── identifier_crosswalk.json       # Identifier type mappings
│   ├── tools/                        # Python utilities (stdlib only)
│   │   ├── sz_schema_generator.py    # Generate schema from source data
│   │   ├── lint_senzing_json.py      # Validate JSON structure
│   │   ├── sz_json_analyzer.py       # Analyze mapping quality
│   │   └── sz_default_config.json    # Senzing configuration reference
│   └── senzing_tools_reference.md    # Complete tool documentation
├── solutions/                         # Complete solution implementations
│   ├── customers/
│   │   ├── README.md                 # Usage instructions
│   │   ├── customers_mapper.md       # Complete mapping specification
│   │   ├── customers_mapper.py       # Mapper implementation
│   │   ├── customers_schema.md       # Source data schema
│   │   └── customers_senzing.jsonl   # Sample output
│   └── watchlist/
│       ├── ftm_README.md             # Usage instructions
│       ├── ftm_mapper.md             # Complete mapping specification
│       ├── ftm_mapper.py             # Mapper implementation
│       ├── ftm_schema.md             # Source data schema
│       └── ftm_senzing.jsonl         # Sample output
└── workspace/                         # Source data and working directory
    ├── customers/
    │   └── customers.csv             # Source data
    └── watchlist/
        └── ftm.jsonl                 # Source data
```

## Senzing Directory Contents

### Prompts (`senzing/prompts/`)

**senzing_mapping_assistant.md** - AI mapping assistant prompt that guides through the complete mapping workflow:
- 5-stage structured process
- Built-in validation gates
- Interactive field disposition
- Guardrails to prevent hallucination

### Reference Materials (`senzing/reference/`)

**senzing_entity_specification.md** - Master specification document (detailed)
- Senzing JSON schema and validation rules
- Complete feature and attribute definitions
- Identifier classification workflow
- Relationship mapping guidance
- Source schema type handling (CSV, JSON, XML, Parquet, Graph)

**senzing_mapping_examples.md** - Practical mapping patterns and examples

**identifier_crosswalk.json** - Standard identifier type mappings
- Maps common codes to Senzing features (SSN, PASSPORT, NATIONAL_ID, TAX_ID, etc.)

### Tools (`senzing/tools/`)

All tools use **Python 3 standard library only** (no pip install required).

**sz_schema_generator.py** - Generate markdown schema from source data
```bash
python3 senzing/tools/sz_schema_generator.py input.csv -o schema.md
```
- Analyzes CSV, JSON, JSONL, Parquet, XML files
- Outputs field statistics and sample values
- Use at start of mapping process

**lint_senzing_json.py** - Validate Senzing JSON structure (development tool)
```bash
python3 senzing/tools/lint_senzing_json.py output.jsonl
```
- Validates JSON structure against specification
- Checks required fields and feature families
- Use during mapping development to validate samples
- Exit code 0 = pass, 1 = errors found

**sz_json_analyzer.py** - Analyze mapping quality (production tool)
```bash
python3 senzing/tools/sz_json_analyzer.py output.jsonl [-o report.txt]
```
- Analyzes feature usage, population, uniqueness
- Detects mapped vs unmapped attributes
- Identifies missing DATA_SOURCE configuration
- Reports data quality warnings
- Use AFTER linting, BEFORE loading into Senzing

### Tools Reference (`senzing/senzing_tools_reference.md`)

Comprehensive documentation for all workshop and Senzing core tools:
- Complete command-line reference with examples
- Decision logic for when to use each tool
- Success/failure indicators
- Common workflows
- Troubleshooting guidance

## Solutions Structure

Each solution directory contains five files:

1. **README.md** - Usage instructions and testing guidance
2. **`*_mapper.md`** - Complete mapping specification (source of truth)
   - Field-by-field disposition decisions
   - Transformation logic
   - Confidence scores
   - Sample JSON for each entity type
3. **`*_mapper.py`** - Working Python implementation
   - Standard library only (no dependencies)
   - Supports `--sample N` flag for testing
   - Import-able functions and CLI entry point
   - Progress display
4. **`*_schema.md`** - Source data schema (generated by sz_schema_generator.py)
5. **`*_senzing.jsonl`** - Sample Senzing JSON output

Solutions serve as:
- Reference implementations for participants
- Working code that can be executed and modified

## Prerequisites

### Workshop Environment

- **Python 3.x** - All tools use standard library only (no pip install needed)
- **Senzing** - Pre-configured in workshop environment
- **IDE with AI assistant plugin** - Required for AI-assisted mapping workflow

### Environment Variables

If using Senzing core tools (sz_file_loader, sz_snapshot):
```bash
export SENZING_ROOT=/opt/senzing/er
```

## Getting Started

### For Workshop Participants

You'll work *with your AI agent* throughout. The typical workflow for each exercise is:

**Step 1: Analyze source data**
Ask your AI agent to generate the schema for your source file.

**Step 2-4: Map with AI assistance (interactive)**
- Ask your AI agent to load `senzing/prompts/senzing_mapping_assistant.md`
- Your AI agent will guide you through the 5-stage mapping workflow
- Your AI agent will help generate your mapper code
- Ask questions anytime - your AI agent has access to all the reference materials

**Step 5: Validate and analyze**
Ask your AI agent to validate your output with the linter and run the analyzer.

**Step 6: Load into Senzing**
Ask your AI agent to load your data into Senzing.

**Step 7: Analyze resolution results**
Ask your AI agent to run a snapshot and interpret the results.

**Working Directories:**
- Complete your work in `workspace/customers/` and `workspace/watchlist/`
- Your AI agent can navigate these directories and create files for you
- Reference solutions are available in `solutions/` if you get stuck

## Key Resources

### Essential Reading

- **`senzing/reference/senzing_entity_specification.md`** - Master specification for Senzing JSON format (comprehensive reference)
- **`senzing/prompts/senzing_mapping_assistant.md`** - AI assistant prompt to share with your AI agent for guided mapping
- **`senzing/senzing_tools_reference.md`** - Complete documentation for all tools with examples

**Tip:** Ask your AI agent to read these files for you! For example:
- "Read the Senzing entity specification and explain the key concepts"
- "What does the mapping assistant prompt do?"
- "Show me how to use the linter tool"

### When You Need Help

- **Ask your AI agent first!** - Your AI agent has access to all the documentation and can help interpret errors
- **During exercises:** Your AI agent can refer to the Senzing entity specification for you
- **Validation errors:** Your AI agent can help fix JSON structure issues
- **Quality issues:** Your AI agent can interpret the analyzer report and suggest fixes
- **Solutions:** Available in `solutions/` if you get stuck or want to compare approaches

## Additional Resources

- **Senzing Documentation:** https://docs.senzing.com
- **FollowTheMoney Format:** https://followthemoney.tech (for watchlist exercise)

---

**Repository maintained for Senzing entity resolution workshops**
