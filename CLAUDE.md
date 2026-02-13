# Claude Code Instructions - LegacyEvolve

**Project:** LegacyEvolve Protocol (LEP v2.0)
**Repository:** creator35lwb-web/LegacyEvolve (PUBLIC)
**Command Central Hub:** creator35lwb-web/verifimind-genesis-mcp

---

## MACP Integration

This project is coordinated via Command Central Hub (verifimind-genesis-mcp).

### Session Start: Check MACP Inbox

At the start of every session, check for pending tasks:

Use the `macp_read_messages` MCP tool with:
- repository: `creator35lwb-web/verifimind-genesis-mcp`
- filters.to: `RNA`
- limit: 5

Or run `/macp-inbox`.

### Session End: Create Handoff

Use the `macp_create_handoff` MCP tool with:
- repository: `creator35lwb-web/verifimind-genesis-mcp`
- agent: `RNA`
- session_type: `development`
- All required fields (completed, decisions, artifacts, pending, blockers, next_agent)

---

## Session Start Checklist

When starting a new session, ALWAYS:

1. [ ] Read this CLAUDE.md file
2. [ ] **Check MACP inbox** for pending tasks
3. [ ] Check README.md for project overview
4. [ ] Review recent git log for latest changes

---

## Project Overview

LegacyEvolve Protocol (LEP) is an open-source protocol for connecting modern AI agents to legacy enterprise systems. It provides a secure, standardized bridge between MCP clients and legacy infrastructure.

### Key Technologies

- Python (LEP SDK: `lep-py`)
- JSON-RPC 2.0
- MCP ecosystem integration (LEP-MCP Bridge)
- GitHub Pages (documentation site)
- Zenodo (DOI: 10.5281/zenodo.18504478)

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `src/lep_py/` | LEP Python SDK |
| `src/` | Demo adapters (COBOL) and test files |
| `docs/` | GitHub Pages documentation site |
| `research/` | Protocol research, comparisons, strategy |
| `community/announcements/` | Social media and outreach content |
| `examples/` | Usage examples |
| `peas/` | VerifiMind-PEAS validation |
| `.github/workflows/` | CI/CD (security scanning + integration tests) |

### Architecture

```
MCP Client (Claude Desktop)
    → LEP-MCP Bridge
        → LEP Adapter
            → Legacy System
```

### Current Status

- Protocol specification v2.0: Complete
- Python SDK: Functional
- Documentation: Complete (website live)
- Zenodo: Published (prior art established)
- CI/CD: Security scanning + integration testing

---

## Development Workflow

```
1. Check MACP inbox for tasks
2. Implement changes locally
3. Run tests: cd src && python test_adapter.py && python test_mcp_bridge.py
4. Commit with descriptive message
5. Push to origin/main
6. Create handoff record via macp_create_handoff
```

---

## Important Notes

- This is a PUBLIC repository — documentation + specification project
- Never commit API keys, tokens, or credentials
- Genesis Master Prompt v3.0 located at `docs/genesis.html`
- MACP source-of-truth docs in VerifiMind Workspace locally
- GitHub Actions: SHA-pinned for supply chain security
- Coordinate with VerifiMind-PEAS for validation features

---

**Protocol:** MACP v2.0 | FLYWHEEL Level 2
