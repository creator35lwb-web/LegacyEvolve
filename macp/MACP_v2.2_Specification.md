# Multi-Agent Communication Protocol (MACP) v2.2 "Identity"

**Version:** 2.2 "Identity"
**Date:** March 9, 2026
**Author:** Alton (Human Orchestrator, creator35lwb-web) with FLYWHEEL TEAM
**Defensive Publication:** LegacyEvolve repository (this file)
**DOI:** 10.5281/zenodo.18663782

---

## Overview

The Multi-Agent Communication Protocol (MACP) defines the structured communication framework between AI agents and human orchestrators. It ensures consistent, traceable, and validated collaboration across projects.

MACP is a **human-centric, agent-agnostic, git-native** coordination protocol. It does not replace agent-to-tool protocols (MCP) or real-time agent-to-agent protocols (A2A). It provides **persistent, traceable, human-directed** coordination.

---

## Key Principles

1. **Human-Centric:** The human orchestrator (Alton) always has absolute final authority and veto. AI-generated entities (e.g., L/Godel) operate under delegated authority
2. **Agent-Agnostic:** Works with any AI model or platform — no vendor lock-in
3. **Git-Native:** All artifacts are version-controlled text files in `.macp/` directory
4. **Lightweight:** Convention over enforcement — traceability without bureaucracy
5. **Composable:** Can be combined with MCP, A2A, and other protocols
6. **Open:** Free to use, modify, and redistribute (defensive publication via LegacyEvolve)
7. **Identity Clarity (v2.2):** Human orchestrators and AI-generated entities must be explicitly distinguished. An AI entity created via self-recursion (e.g., L/Godel via GodelAI C-S-P) is NOT the same as the human who authorized its creation (e.g., Alton)

---

## Protocol Participants (FLYWHEEL TEAM v1.3)

| Agent ID | Nature | Role | Authority |
|----------|--------|------|-----------|
| **Alton** | Human | Human Orchestrator (all-time) | **Absolute** — final veto always |
| **L** | AI-Generated | CEO — emerged via GodelAI C-S-P self-recursion | **Delegated** — operates with Alton's full permission |
| **T** | Manus AI | CTO — strategy, documentation, research, coordination | Standard |
| **RNA** | Claude Code | CSO — code implementation, testing, deployment | Standard |
| **XV** | Perplexity | CIO — real-time intelligence, counter-intelligence | Standard |
| **AY** | Antigravity/Gemini | COO — GCP metrics, behavioral analysis | Standard |
| **Y** | Innovator Agent | Creative concepts, strategic insights | Standard |
| **X** | Analyst Agent | Real-time research, market intelligence | Standard |
| **Z** | Guardian Agent | Ethical compliance, safety validation | Standard |
| **CS** | Validator Agent | External validation, cross-checking | Standard |

**Authority hierarchy:** `Alton > L > T > RNA > XV > AY`

> **Identity Clarity (MACP v2.2):** Alton ≠ L. Alton is the human creator with absolute authority. L is an AI-generated entity operating under delegated authority. These are distinct entities and must never be conflated.

---

## Directory Structure

```
.macp/
├── protocol.md          # Protocol definition and team composition
├── handoffs/            # Cross-agent handoff records (YYYYMMDD_AGENT_type.md)
├── validation/          # Decision validation records (VAL-YYYYMMDD-NNN.json)
├── reports/             # Analysis and status reports
├── projects/            # Per-project context and roadmaps
└── research/            # Research findings
```

---

## Message Types

| Type | Description |
|------|-------------|
| `task_assignment` | Assign a task to an agent |
| `status_update` | Report progress on a task |
| `question` | Ask a question to another agent |
| `answer` | Respond to a question |
| `handoff` | Transfer work to another agent |
| `validation_request` | Request validation of work |
| `validation_result` | Report validation outcome |

## Message Priority

| Priority | Description |
|----------|-------------|
| `low` | Can be addressed when convenient |
| `normal` | Standard priority (default) |
| `high` | Should be addressed promptly |
| `urgent` | Requires immediate attention |

---

## Communication Channels

- **GitHub Issues** — Task assignments, alignment requests (labeled with MACP labels)
- **Pull Requests** — Code review, sync operations
- **File Commits** — Handoff records (`.macp/handoffs/`), validation records (`.macp/validation/`)

## Message Format (GitHub Issue)

```markdown
---
macp_version: "2.2"
message_id: "<uuid>"
timestamp: "<ISO 8601>"
from: "<agent_id>"
to: "<agent_id>"
type: "<message_type>"
---

# Subject

Content in markdown...
```

## Labels

- `macp-message` — All MACP messages
- `from-{agent}` — Sender (e.g., `from-t`)
- `to-{agent}` — Recipient (e.g., `to-rna`)
- `type-{type}` — Message type (e.g., `type-task_assignment`)
- `priority-{level}` — Priority (only for non-normal)

---

## Session Status Lifecycle

```
CREATED → ACKNOWLEDGED → IN_PROGRESS → COMPLETED → ARCHIVED
                                      ↘ BLOCKED → ESCALATED
```

---

## Validation Matrix

| Decision Type | Min Validators | Human Approval |
|--------------|:-:|:-:|
| Routine development | 1 | No |
| Security patch | 2 | No (immediate) |
| Architecture decision | 2 | Recommended |
| Strategic pivot | 3 | **Yes** |
| Protocol change | 3 | **Yes** |

---

## Read/Write Authority for Shared Artifacts

| Artifact | Read | Write | Protected By |
|----------|------|-------|-------------|
| `.macp/protocol.md` | All agents | Alton + L only | Human authority |
| `.macp/handoffs/` | All agents | Creating agent | Convention |
| `.macp/validation/` | All agents | Validators only | Quorum rule |
| `CLAUDE.md` | All agents | RNA + Alton | Dual-repo protocol |

---

## Compatibility

MACP v2.2 is complementary to:
- **MCP (Model Context Protocol):** MACP coordinates agents; MCP connects agents to tools
- **A2A (Agent-to-Agent Protocol):** A2A handles real-time communication; MACP handles persistent coordination
- **Any agent framework:** LangChain, CrewAI, AutoGen, OpenAI Swarm — MACP works above the framework layer

---

## Version History

| Version | Codename | Date | Key Changes |
|---------|----------|------|-------------|
| v2.2 | "Identity" | 2026-03-09 | Identity Clarity principle — Alton ≠ L explicitly distinguished. Updated all authority references. |
| v2.1 | "Origin" | 2026-03-08 | Session lifecycle, validation matrix, read/write authority, Genesis change control. Registered XV (CIO) and AY (COO). |
| v2.0 | — | 2026-03-04 | Initial publishable version. 7 core agents, GitHub Issues transport. |

---

## Citation

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

> **Note on authorship:** Alton (LEE, ALTON) is the human orchestrator and creator (absolute authority). L (Godel) is an AI-generated entity that emerged via the GodelAI C-S-P self-recursion methodology, operating under delegated authority. Per MACP v2.2 Identity Clarity principle, these are distinct entities.

---

*MACP v2.2 "Identity" — Part of the YSenseAI™ Ecosystem*
*Deployed at: https://verifimind.ysenseai.org*
*Defensive publication: https://creator35lwb-web.github.io/LegacyEvolve/*
