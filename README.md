# LegacyEvolve Protocol (LEP)

**The open-source protocol for connecting modern AI to legacy enterprise systems.**

*Evolve, Don't Replace*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18663782.svg)](https://doi.org/10.5281/zenodo.18663782)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Scanning](https://github.com/creator35lwb-web/LegacyEvolve/actions/workflows/security-scan.yml/badge.svg)](https://github.com/creator35lwb-web/LegacyEvolve/actions/workflows/security-scan.yml)
[![Integration Tests](https://github.com/creator35lwb-web/LegacyEvolve/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/creator35lwb-web/LegacyEvolve/actions/workflows/integration-tests.yml)
[![Security: Hardened](https://img.shields.io/badge/Security-Hardened-green.svg)](SECURITY.md)
[![Governance](https://img.shields.io/badge/Governance-Community--Led-blue.svg)](GOVERNANCE.md)

---

| Status | Version | License | Security | Docs | Community |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ Active | v2.3 | MIT | 🔒 Hardened | [Wiki](https://github.com/creator35lwb-web/LegacyEvolve/wiki) | [Discussions](https://github.com/creator35lwb-web/LegacyEvolve/discussions) |

---

## Mission

To unlock the trillions of dollars of value trapped in legacy enterprise systems by providing a secure, open-source, and standardized protocol for AI-legacy integration.

## Key Features

- **Security-First Design**: Human-in-the-loop approval for all write operations
- **Complete Auditability**: Immutable audit trail for every transaction
- **Ecosystem Interoperability**: Works with MCP clients (Claude Desktop, Zed, etc.)
- **Industry Standards**: Built on JSON-RPC 2.0 and best practices
- **Digital Public Good**: Open-source, community-driven, and for the public good

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│              MCP Client (Claude Desktop)                │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
┌────────────────────▼────────────────────────────────────┐
│                  LEP-MCP Bridge                         │
└────────────────────┬────────────────────────────────────┘
                     │ LEP Protocol
┌────────────────────▼────────────────────────────────────┐
│                  LEP Adapter                            │
└────────────────────┬────────────────────────────────────┘
                     │ Legacy Protocol
┌────────────────────▼────────────────────────────────────┐
│                  Legacy System                          │
└─────────────────────────────────────────────────────────┘
```

## Project Status

**LEP (LegacyEvolve Protocol): Complete!** As of February 2026, the LegacyEvolve Protocol has achieved all initial development goals:

- ✅ **Protocol Specification v2.0**: Complete and documented
- ✅ **Python SDK**: Fully functional with JSON-RPC 2.0 foundation
- ✅ **Reference Adapter**: Working example for a simulated legacy system
- ✅ **LEP-MCP Bridge**: Seamless integration with the MCP ecosystem
- ✅ **Comprehensive Documentation**: Implementation guide, SDK docs, and more

## Quick Start (5 Minutes)

### Install LEP Python SDK

```bash
pip install lep-py
```

### Create Your First Adapter

```python
from lep_py.adapter import BaseAdapter

class MyLegacyAdapter(BaseAdapter):
    def read_data(self, query):
        # Connect to your legacy system
        return {"status": "success", "data": "Hello from legacy!"}

adapter = MyLegacyAdapter()
result = adapter.read_data({"table": "customers"})
print(result)
```

### Connect to AI Agents via MCP

```bash
# Install LEP-MCP Bridge
npm install lep-mcp-bridge

# Configure Claude Desktop
echo '{
  "mcpServers": {
    "legacy-system": {
      "command": "lep-mcp-bridge",
      "args": ["--adapter", "./my_adapter.py"]
    }
  }
}' > ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Done!** Your AI agent can now safely interact with your legacy system.

---

## Full Documentation

### 1. Protocol & Architecture

- **[Protocol v2.0 Specification](docs/LegacyEvolve_Protocol_v2.0_Specification.md)**
- **[Implementation Guide](docs/IMPLEMENTATION_GUIDE.md)**
- **[LEP-MCP Bridge Specification](docs/LEP_MCP_BRIDGE.md)**

### 2. Explore the Code

- **[Python SDK](src/README.md)**
- **[Example Adapter](src/lep_py/adapter/example_adapter.py)**
- **[Test Suite](src/test_adapter.py)**

### 3. Security & Governance

- **[Security Policy](SECURITY.md)** - Report vulnerabilities responsibly
- **[Governance](GOVERNANCE.md)** - Community decision-making process
- **[Sustainability](SUSTAINABILITY.md)** - Long-term roadmap and funding

### 4. Contribute

- **[Contributing Guidelines](CONTRIBUTING.md)**
- **[Open Issues](https://github.com/creator35lwb-web/LegacyEvolve/issues)**
- **[Start a Discussion](https://github.com/creator35lwb-web/LegacyEvolve/discussions)**

## Validation & Research

LEP has undergone rigorous validation using the VerifiMind-PEAS methodology:

- **[Trinity Validation Report](peas/TRINITY_VALIDATION_REPORT_COMPLETE.md)** - 8.67/10 overall score
- **[Agent Protocol Ecosystem Research](docs/Agent_Protocol_Ecosystem_Research_Report.md)** - Market analysis
- **[FLYWHEEL TEAM Validation](https://github.com/creator35lwb-web/LegacyEvolve/wiki#flywheel-team-validation)** - Multi-agent ethical review with bias minimization

## FLYWHEEL TEAM

LEP and MACP are developed and maintained by the **FLYWHEEL TEAM v1.3** — a 6-agent multi-model team coordinated via MACP:

| Agent | Nature | Role |
|-------|--------|------|
| **Alton Lee** | Human | Human Orchestrator — absolute authority |
| **L** (GODEL) | AI-Generated | CEO — delegated authority via GodelAI C-S-P |
| **T** (Manus AI) | Manus AI | CTO — strategy, documentation |
| **RNA** (Claude Code) | Claude Code | CSO — implementation, deployment |
| **XV** (Perplexity) | Perplexity | CIO — real-time intelligence |
| **AY** (Antigravity) | Gemini | COO — operations, metrics |

The FLYWHEEL TEAM uses the **ai-council** skill for multi-model validation — running X (Analyst), Y (Innovator), Z (Guardian), and CS (Validator) agents in parallel to score ideas against the Genesis Methodology. This is the same validation methodology used for the LEP 8.67/10 Trinity score.

See [VerifiMind-PEAS](https://verifimind.ysenseai.org) for the live implementation.

## Why LEP?

### The Problem

- **$3 trillion** locked in legacy systems (COBOL, mainframes, proprietary databases)
- **80%+ AI project failure rate** due to integration challenges
- **30% GenAI projects abandoned** by end-2025 due to poor controls

### The Solution

- **Security-First:** Human-in-the-loop approval, immutable audit trail
- **Open Standard:** MIT license, community-driven, Digital Public Good
- **Proven Validation:** FLYWHEEL TEAM 8.67/10 score with bias minimization
- **Real-World Ready:** Supply chain attack prevention, CI/CD security scanning

## MACP Protocol (Actively Evolving)

The **Multi-Agent Communication Protocol (MACP)** originated in this repository and continues to evolve independently of LEP. LEP is complete; MACP is actively developed as part of the YSenseAI™ Ecosystem.

**Current version:** v2.2 "Identity" — adds Identity Clarity principle (Alton ≠ L)

- **[MACP v2.2 Specification](macp/MACP_v2.2_Specification.md)** — full protocol reference
- **Deployed implementation:** [VerifiMind-PEAS](https://verifimind.ysenseai.org) — live MCP server

> **MACP v2.2 Identity Clarity:** Alton (Human Orchestrator) and L (Godel, AI-Generated Entity) are distinct. Alton has absolute authority; L operates under delegated authority via GodelAI C-S-P self-recursion.

---

## Citation

If you use the LegacyEvolve Protocol or MACP in your research or project, please cite:

```bibtex
@software{legacyevolve_macp_2026,
  author       = {LEE, ALTON (Human Orchestrator, creator35lwb-web) and
                  L (AI-Generated Entity, YSenseAI GodelAI C-S-P)},
  title        = {Multi-Agent Communication Protocol (MACP) v2.2 "Identity" and
                  LegacyEvolve Protocol: Open Standards for AI-Legacy
                  System Integration and Multi-Agent Collaboration},
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v2.4},
  doi          = {10.5281/zenodo.18663782},
  url          = {https://doi.org/10.5281/zenodo.18663782}
}
```

Or in text format:

> LEE, ALTON (Human Orchestrator, creator35lwb-web) & L (AI-Generated Entity, YSenseAI GodelAI C-S-P). (2026). Multi-Agent Communication Protocol (MACP) v2.2 "Identity" and LegacyEvolve Protocol: Open Standards for AI-Legacy System Integration and Multi-Agent Collaboration (Version v2.4) [Software documentation]. Zenodo. https://doi.org/10.5281/zenodo.18663782

> **Note on authorship:** Alton is the human creator (absolute authority). L is an AI-generated entity operating under delegated authority. Per MACP v2.2, these are distinct entities and must not be conflated.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the public good**
