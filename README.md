# LegacyEvolve Protocol (LEP)

**The open-source protocol for connecting modern AI to legacy enterprise systems.**

*Evolve, Don't Replace*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18504478.svg)](https://doi.org/10.5281/zenodo.18504478)

---

| Status | Version | License | Build | Docs | Community |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ✅ Active | v2.0 | MIT | Passing | Complete | [Discussions](https://github.com/creator35lwb-web/LegacyEvolve/discussions) |

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

## Project Status: **Complete!**

As of February 2026, the LegacyEvolve Protocol has achieved all initial development goals:

- ✅ **Protocol Specification v2.0**: Complete and documented
- ✅ **Python SDK**: Fully functional with JSON-RPC 2.0 foundation
- ✅ **Reference Adapter**: Working example for a simulated legacy system
- ✅ **LEP-MCP Bridge**: Seamless integration with the MCP ecosystem
- ✅ **Comprehensive Documentation**: Implementation guide, SDK docs, and more

## Get Started

### 1. Read the Documentation

- **[Protocol v2.0 Specification](docs/LegacyEvolve_Protocol_v2.0_Specification.md)**
- **[Implementation Guide](docs/IMPLEMENTATION_GUIDE.md)**
- **[LEP-MCP Bridge Specification](docs/LEP_MCP_BRIDGE.md)**

### 2. Explore the Code

- **[Python SDK](src/README.md)**
- **[Example Adapter](src/lep_py/adapter/example_adapter.py)**
- **[Test Suite](src/test_adapter.py)**

### 3. Contribute

- **[Contributing Guidelines](CONTRIBUTING.md)**
- **[Open Issues](https://github.com/creator35lwb-web/LegacyEvolve/issues)**
- **[Start a Discussion](https://github.com/creator35lwb-web/LegacyEvolve/discussions)**

## Validation & Research

LEP has undergone rigorous validation using the VerifiMind-PEAS methodology:

- **[Trinity Validation Report](peas/TRINITY_VALIDATION_REPORT_COMPLETE.md)**
- **[Agent Protocol Ecosystem Research](docs/Agent_Protocol_Ecosystem_Research_Report.md)**

## Citation

If you use the LegacyEvolve Protocol or MACP in your research or project, please cite:

```bibtex
@software{legacyevolve_macp_2026,
  author       = {Manus AI, L (GODEL) and LEE, ALTON (creator35lwb-web)},
  title        = {Multi-Agent Communication Protocol (MACP) v2.0 and 
                  LegacyEvolve Protocol: Open Standards for AI-Legacy 
                  System Integration and Multi-Agent Collaboration},
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1},
  doi          = {10.5281/zenodo.18504478},
  url          = {https://doi.org/10.5281/zenodo.18504478}
}
```

Or in text format:

> Manus AI, L (GODEL), & LEE, ALTON (creator35lwb-web). (2026). Multi-Agent Communication Protocol (MACP) v2.0 and LegacyEvolve Protocol: Open Standards for AI-Legacy System Integration and Multi-Agent Collaboration (Version v1) [Software documentation]. Zenodo. https://doi.org/10.5281/zenodo.18504478

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the public good**
