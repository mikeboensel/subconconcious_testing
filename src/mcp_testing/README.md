# MCP Server Explorer

A generic tool that connects to **any** MCP server, discovers its capabilities (tools, resources, prompts, resource templates), and optionally calls a tool.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js / `npx` (for stdio servers that are npm packages)

```bash
# Install dependencies (from project root)
uv sync
```

## Usage

Two transport modes: **stdio** (local subprocess) and **http** (remote endpoint).

```
uv run src/mcp_testing/mcp_test.py stdio <command> [args...]
uv run src/mcp_testing/mcp_test.py http <url> [--header KEY=VALUE ...]
```

### Optional: call a tool after discovery

Add `--call-tool <name> '<json>'` **before** the transport subcommand:

```bash
uv run src/mcp_testing/mcp_test.py \
  --call-tool <tool-name> '{"param":"value"}' \
  stdio <command> [args...]
```

---

## Server Examples

### Context7 (documentation lookup)

Exposes two tools: `resolve-library-id` and `query-docs`. Useful for pulling up-to-date docs for any library.

**Stdio:**
```bash
uv run src/mcp_testing/mcp_test.py stdio npx -y @upstash/context7-mcp
```

**HTTP** (requires API key from [context7.com](https://context7.com)):
```bash
uv run src/mcp_testing/mcp_test.py http https://mcp.context7.com/mcp \
  --header "Authorization=Bearer $CONTEXT7_API_KEY"
```

**Call a tool:**
```bash
uv run src/mcp_testing/mcp_test.py \
  --call-tool resolve-library-id '{"query":"react hooks","libraryName":"react"}' \
  stdio npx -y @upstash/context7-mcp
```

---

### Filesystem (local file access)

Gives the server read/write access to specified directories. Good for testing resource and tool discovery on a well-known server.

```bash
# Grant access to /tmp and your home directory
uv run src/mcp_testing/mcp_test.py stdio npx -y @modelcontextprotocol/server-filesystem /tmp ~
```

**Call a tool:**
```bash
uv run src/mcp_testing/mcp_test.py \
  --call-tool list_directory '{"path":"/tmp"}' \
  stdio npx -y @modelcontextprotocol/server-filesystem /tmp
```

---

### GitHub

Browse repos, issues, PRs, and files. Requires a [GitHub personal access token](https://github.com/settings/tokens).

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."

uv run src/mcp_testing/mcp_test.py stdio npx -y @modelcontextprotocol/server-github
```

**Call a tool:**
```bash
uv run src/mcp_testing/mcp_test.py \
  --call-tool search_repositories '{"query":"language:python stars:>1000"}' \
  stdio npx -y @modelcontextprotocol/server-github
```

---

### Brave Search

Web search via the Brave Search API. Requires a [Brave API key](https://brave.com/search/api/).

```bash
export BRAVE_API_KEY="BSA..."

uv run src/mcp_testing/mcp_test.py stdio npx -y @modelcontextprotocol/server-brave-search
```

**Call a tool:**
```bash
uv run src/mcp_testing/mcp_test.py \
  --call-tool brave_web_search '{"query":"MCP protocol anthropic"}' \
  stdio npx -y @modelcontextprotocol/server-brave-search
```

---

### Memory (knowledge graph)

A persistent local knowledge graph for storing entities and relations.

```bash
uv run src/mcp_testing/mcp_test.py stdio npx -y @modelcontextprotocol/server-memory
```

---

### Puppeteer (browser automation)

Control a headless Chrome browser -- navigate, screenshot, click, fill forms.

```bash
uv run src/mcp_testing/mcp_test.py stdio npx -y @modelcontextprotocol/server-puppeteer
```

---

### SQLite

Query and manage a local SQLite database.

```bash
uv run src/mcp_testing/mcp_test.py stdio npx -y @modelcontextprotocol/server-sqlite /path/to/db.sqlite
```

---

### Any Python MCP server

If you have a Python-based MCP server, just point at it:

```bash
uv run src/mcp_testing/mcp_test.py stdio python path/to/my_server.py
```

---

## What the output looks like

```
============================================================
  Tools (2)
============================================================

  [1] resolve-library-id
      Description: Resolves a package/product name to a Context7-compatible...
      Parameters:
        - query: string (required)
        - libraryName: string (required)

  [2] query-docs
      Description: Retrieves documentation from Context7...
      Parameters:
        - libraryId: string (required)
        - query: string (required)

============================================================
  Resources (0)
============================================================
  None found.

============================================================
  Summary
============================================================
  Tools:              2
  Resources:          0
  Prompts:            0
  Resource Templates: 0
  Total capabilities: 2
```

Servers that don't support a capability (resources, prompts, etc.) gracefully show "None found" instead of crashing.

## Finding more MCP servers

- [Official MCP Servers repo](https://github.com/modelcontextprotocol/servers) -- reference implementations maintained by Anthropic and the community.
- [mcp.so](https://mcp.so/) -- community directory of MCP servers.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) -- curated list.
