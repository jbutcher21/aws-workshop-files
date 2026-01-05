# Senzing MCP Server Reference

This document describes the Senzing MCP Server for AI assistants with Model Context Protocol (MCP) support. The server provides read-only access to Senzing entity resolution results.

**Repository:** https://github.com/jbutcher21/senzing-mcp-server

---

## When to Use

The MCP server is for **post-loading analysis** — after data has been mapped, loaded, and resolved by Senzing. It enables AI assistants to:

- Search and retrieve resolved entities
- Explore entity relationships and networks
- Understand WHY entities matched (matching explanation)
- Understand HOW entities resolved (resolution mechanics)

**Not for:** Data mapping, loading, or configuration. Use the CLI tools in [SENZING_TOOLS_REFERENCE.md](SENZING_TOOLS_REFERENCE.md) for those tasks.

---

## Workflow Context

```
1. Generate schema     → sz_schema_generator.py
2. Analyze schema      → Review output
3. Map to Senzing JSON → senzing_mapping_assistant.md (prompt)
4. Validate mapping    → lint_senzing_json.py, sz_json_analyzer.py
5. Configure sources   → sz_configtool
6. Load data           → sz_file_loader
7. Analyze results     → sz_snapshot + MCP Server ← YOU ARE HERE
```

The MCP server complements `sz_snapshot` for step 7. Snapshot provides statistics; MCP server enables interactive exploration.

---

## Available Tools

| Tool | Purpose |
|------|---------|
| `search_entities` | Find entities by name, address, phone, email, identifiers |
| `get_entity` | Retrieve full entity details by entity ID |
| `get_record` | Look up a specific source record |
| `find_path` | Discover connection path between two entities |
| `find_network` | Map entity network up to 3 degrees of separation |
| `why_entity` | Explain why records resolved together |
| `how_entity` | Show resolution mechanics for an entity |

---

## Setup

### Requirements

- Python 3.10+
- Senzing SDK v4
- Configured Senzing database with loaded data
- Claude Desktop (or other MCP-compatible client)

### Installation

```bash
git clone https://github.com/jbutcher21/senzing-mcp-server.git
cd senzing-mcp-server
pip install -r requirements.txt
chmod +x launch_senzing_mcp.sh
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "senzing": {
      "command": "/path/to/senzing-mcp-server/launch_senzing_mcp.sh",
      "env": {
        "SENZING_ENGINE_CONFIGURATION_JSON": "{...}",
        "LD_LIBRARY_PATH": "/opt/senzing/er/lib",
        "PYTHONPATH": "/opt/senzing/er/sdk/python"
      }
    }
  }
}
```

See the [MCP server repository](https://github.com/jbutcher21/senzing-mcp-server) for full configuration details.

---

## Example Queries

Once connected, ask natural language questions:

- "Search for entities with the name 'John Smith'"
- "Get details for entity 12345"
- "Find the path between entity 100 and entity 200"
- "Why did records from CUSTOMERS and WATCHLIST resolve together for entity 500?"
- "Show me the network around entity 1001"

---

## Response Formatting

The MCP server repository includes `RESPONSE_FORMATTING.md` with guidance for presenting results clearly. Reference this file in your conversation or project instructions for better output formatting.
