# FTM (Follow The Money) Mapper

Maps Follow The Money format data to Senzing JSON for entity resolution.

## Overview

This mapper processes FTM format data containing persons, companies, sanctions, identifications, and corporate relationships from both watchlist and corporate registry sources.

## Usage

### Basic Usage
```bash
python3 ftm_mapper.py workspace/watchlist/ftm.jsonl output.jsonl
```

### Testing with Sample
```bash
python3 ftm_mapper.py workspace/watchlist/ftm.jsonl output.jsonl --sample 10
```

## Validation

### Structure Validation
```bash
python3 senzing/tools/lint_senzing_json.py output.jsonl
```

### Quality Analysis
```bash
python3 senzing/tools/sz_json_analyzer.py output.jsonl -o analysis.md
```

The analyzer provides statistics, feature usage, and validates the JSONL structure. Review the analysis.md file for comprehensive quality metrics.

## Data Sources

- **WATCHLIST**: Sanctions persons and related data
- **CORPORATE_REGISTRY**: Corporate entities, persons, and relationships

## Entity Types

- **Person**: 33 records (from both watchlist and corporate registry)
- **Company**: 6 records (corporate registry only)

## Features Mapped

### Person Features
- Names (parsed when available, full names as fallback)
- Addresses, birth dates, contact info
- Identifiers (SSN, Driver's License, National IDs, Tax IDs)
- Relationships (directorship, ownership)
- Sanctions data (as payload attributes)

### Company Features
- Organization names (current and previous)
- Business addresses
- Phone numbers
- Identifiers (UEN, EIN, VAT, LEI, GSTIN)
- Corporate relationships (ownership, directorship targets)

## Relationships

- **Directorship**: Person → Company (Principal, President roles)
- **Ownership**: Person/Company → Company (with percentage)

## Testing

The mapper includes comprehensive error handling and progress display. Use `--sample N` for testing with subsets.

## Dependencies

Python 3 standard library only - no external dependencies required.