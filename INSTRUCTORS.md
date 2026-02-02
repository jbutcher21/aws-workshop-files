# Instructor Guide

This guide contains teaching tips, verification steps, and expected outcomes for workshop instructors.

## Pre-Workshop Setup

### Verify Repository Structure

```bash
# Check directory structure
tree -L 2 .

# Verify tools are executable
python3 senzing/tools/lint_senzing_json.py --self-test
```

### Test Solution Mappers

```bash
# Test customer mapper
python3 solutions/customers/customers_mapper.py workspace/customers/customers.csv test_output.jsonl --sample 10
python3 senzing/tools/lint_senzing_json.py test_output.jsonl

# Test watchlist mapper
python3 solutions/watchlist/ftm_mapper.py workspace/watchlist/ftm.jsonl test_output.jsonl --sample 10
python3 senzing/tools/lint_senzing_json.py test_output.jsonl
```

### Review AI Mapping Assistant

The AI mapping assistant (`senzing/prompts/senzing_mapping_assistant.md`) uses a 5-stage workflow with:
- Approval gates between stages
- Inventory integrity checks (prevents hallucinated fields)
- Interactive low-confidence field handling
- Built-in linter validation
- Generates README, spec, and mapper code

## Exercise Teaching Tips

### Exercise 1: Customer Data

| Aspect | Details |
|--------|---------|
| Source | `workspace/customers/customers.csv` - 120 records (114 persons, 6 organizations) |
| Complexity | Introductory |
| Expected Outcome | ~87 entities (27.5% deduplication) |

**Key Teaching Points:**
- **Start simple:** Use `--sample 10` to work with subset first
- **Name parsing:** Opportunity to discuss parsed vs full names (`NAME_FIRST/NAME_LAST` vs `NAME_FULL`)
- **Dynamic identifiers:** Teach the identifier classification workflow using `identifier_crosswalk.json`
- **Mixed types:** Show how `RECORD_TYPE` distinguishes PERSON from ORGANIZATION

### Exercise 2: Watchlist Data

| Aspect | Details |
|--------|---------|
| Source | `workspace/watchlist/ftm.jsonl` - 73 FTM records |
| Complexity | Advanced |
| Expected Outcome | 39 entities (33 persons + 6 companies) with relationships |

**Key Teaching Points:**
- **Build on Exercise 1:** Assumes understanding of basic mapping
- **Multi-pass processing:** First pass creates entities, second pass adds relationships
- **REL_ANCHOR/REL_POINTER:** Show how relationships link entities across DATA_SOURCEs
- **Cross-DATA_SOURCE:** Relationships from SANCTIONS to CORP_FILINGS demonstrate entity resolution across sources

**Focus Areas:**
- REL_ANCHOR/REL_POINTER patterns
- Merging relationship records onto master entities
- Cross-DATA_SOURCE relationships

## Common Questions

**Q: Why do we need both lint_senzing_json.py and sz_json_analyzer.py?**

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `lint_senzing_json.py` | Validates JSON structure | During development (sample records) |
| `sz_json_analyzer.py` | Analyzes data quality | Before loading (full datasets) |

**Q: Can solutions be modified?**

Yes! Encourage participants to extend or modify mappers. Good learning opportunities:
- Add new features
- Handle edge cases
- Optimize code

**Q: What if source data changes?**

- Re-run schema generator
- Mapping assistant handles iterative refinement
- Version control recommended for mapper specifications

## Verification Checklist

### Exercise 1: Customer Data

- [ ] Schema generated from customers.csv
- [ ] Mapper handles both PERSON and ORGANIZATION types
- [ ] Name parsing extracts first/middle/last correctly
- [ ] Identifiers mapped dynamically based on ID_TYPE field
- [ ] Linter passes with 0 errors
- [ ] Analyzer shows expected feature population
- [ ] ~87 entities after loading (27.5% deduplication)

### Exercise 2: Watchlist Data

- [ ] Schema generated from ftm.jsonl
- [ ] Multi-pass processing implemented
- [ ] REL_ANCHOR records created for entities
- [ ] REL_POINTER records link relationships
- [ ] Sanctions metadata preserved as payload
- [ ] Linter passes with 0 errors
- [ ] 39 entities with relationships after loading

## Workshop Flow Timing

The 7-step workflow applies to each exercise:

1. **Explore Senzing** - Instructor demonstrates Senzing Explorer
2. **Generate Schema** - Participants run sz_schema_generator.py
3. **Map with Assistant** - AI-guided 5-stage mapping process
4. **Validate Mapping** - Linter then analyzer
5. **Load Data** - Configure data source, load with sz_file_loader
6. **Analyze Results** - Run sz_snapshot, review entity counts
7. **Key Takeaways** - Discussion of results and patterns learned
