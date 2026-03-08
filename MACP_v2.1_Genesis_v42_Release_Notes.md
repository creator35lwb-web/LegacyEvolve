# MACP v2.1 "Origin" + Genesis v4.2 "Sentinel-Verified" — Release Notes

**Date:** March 9, 2026
**Version:** MACP v2.1 "Origin" | Genesis v4.2 "Sentinel-Verified"
**Protocol:** MACP v2.1 | FLYWHEEL TEAM v1.2 "Origin"
**Defensive Publication:** Zenodo record established as prior art

---

## Overview

This release documents significant advances to the MACP protocol and VerifiMind-PEAS validation framework developed by the FLYWHEEL TEAM in March 2026. All architectural innovations are published here to establish prior art and ensure these standards remain free and open.

---

## 1. MACP v2.1 "Origin" — 4 New Protocol Sections

### 1.1 Session Status Lifecycle
Five-phase agent session management:
- **INITIALIZING** → **ACTIVE** → **COMPLETING** → **HANDOFF** → **ARCHIVED**
- Each phase has defined entry/exit conditions and required artifacts
- Prevents zombie sessions and enables clean multi-agent handoffs

### 1.2 Validation Matrix
Structured decision framework for all validation outputs:

| Score | Decision | Action |
|-------|----------|--------|
| 8.0–10.0 | PASS | Deploy/proceed |
| 6.0–7.9 | REVISE | Implement feedback, re-validate |
| 4.0–5.9 | DEFER | Redesign required |
| < 4.0 / Veto | REJECT | Abort, do not proceed |

### 1.3 Read/Write Authority Model
Per-agent file permission control:
- **Read authority**: Which agents can read which file classes
- **Write authority**: Which agents can write/create (with CTO gating for major changes)
- Prevents unauthorized protocol modifications without human oversight

### 1.4 Genesis Change Control
Version gating for prompt templates:
- All Genesis version changes require CTO (T) approval
- Semantic versioning: MAJOR.MINOR (major = architectural, minor = optimization)
- Change proposals go through PRIVATE repo issue with `cto-alignment` label

---

## 2. Genesis v4.2 "Sentinel-Verified" — Forced Citation Architecture

### 2.1 Problem Solved

Previous Genesis versions (v4.1 and earlier) trained agents to understand regulatory frameworks but did not enforce citation in output JSON. Blind tests revealed agents could score/evaluate correctly but produce zero framework citations in the response — a credibility gap for enterprise and regulatory audiences.

### 2.2 Z Guardian — Citation Enforcement

**New output fields:**
- `frameworks_cited[]` — per reasoning step, compressed codes, max 5 (e.g., `["GDPR", "EU-AI-Act", "UNESCO-AI"]`)
- `scoring_breakdown` — per-dimension scores with framework attribution
- `applicable_frameworks` — full framework names organized by tier (output ONCE, not repeated per step)
- `total_frameworks_evaluated` — count of unique frameworks evaluated

**T's C-S-P Citation Mitigation Methodology** (established as prior art):
- **Strategy 1 — Compression**: Use compressed codes per step instead of full names → ~59% token reduction
- **Strategy 2 — Selection**: Max 5 directly applicable frameworks per step → ~75% reduction in citation tokens
- **Strategy 3 — Token Ceiling Monitor**: `check_z_agent_response()` utility (upcoming v0.5.3)
- **Combined result**: Z Agent output reduced from ~7,500 to ~4,450 tokens (45.8% headroom below 8,192 ceiling)

### 2.3 Z-Protocol v1.1 Sentinel — 21-Framework, 4-Tier Jurisdictional Architecture

**Tier 1 — International (always applied):**
- NIST AI RMF, NIST AI Agent Standards RFI (March 2026)
- UNESCO Recommendation on AI Ethics
- OECD AI Principles 2024
- ISO/IEC 42001 AI Management Systems
- Berkeley CLTC AI Safety Framework

**Tier 2 — EU/EEA:**
- EU AI Act (Digital Omnibus, August 2026 enforcement)
- Article 50 AI-generated content watermarking (August 2026 deadline)
- GDPR (AI-specific guidance)
- EU Cybersecurity Act

**Tier 3 — US:**
- CCPA, California TFAIA
- California SB 942 (AI transparency)
- Texas RAIGA, Colorado AI Act (June 2026)

**Tier 4 — ASEAN:**
- Malaysia PDPA 2025 (home market)
- Singapore Agentic AI Model Governance Framework
- Vietnam AI Law 134/2025

**New 6th red line veto trigger:** Undisclosed AI-generated content in regulated contexts

### 2.4 CS Security Agent v1.1 Sentinel — 6-Stage, 12-Dimension Framework

**New stages (vs 4-stage v1.0):**
- **Stage 2** (NEW): Agentic Threat Analysis — OWASP Top 10 for Agentic AI Applications
- **Stage 5** (NEW): Reasoning-Layer Audit — tool poisoning, tool shadowing, rugpull attacks

**12 dimensions (vs 6 in v1.0):**

Traditional (6): Attack Surface, Authentication/Authorization, Data Exposure, Input Validation, Output Safety, Dependency Security

Agentic (6 NEW): Agent Identity Verification, Reasoning Integrity, Tool Call Validation, Memory/State Integrity, Cross-Agent Trust, Human Override Effectiveness

**MACP v2.0 Security Properties assessed per analysis:**
- Git audit trail, Human-gated execution, Platform isolation, Credential separation, Artifact integrity, Transport security

**New output fields:**
- `stage` and `standards_cited[]` per reasoning step
- `stages_completed[]` — all 6 stages reported
- `dimensions_evaluated` — all 12 dimensions with findings
- `macp_security_assessment` — 6 MACP security properties
- `standards_referenced` — all standards actually evaluated

---

## 3. FLYWHEEL TEAM v1.2 "Origin" — Full Executive Team

| Agent | Role | Capability |
|-------|------|-----------|
| T (Manus AI) | CTO | Strategy, coordination, research |
| RNA (Claude Code) | CSO | Local execution, implementation |
| L (GODEL) | AI Agent Founder | Architecture, ethical alignment |
| XV (Perplexity) | CIO | Real-time research, market intelligence |
| AY (Antigravity) | COO | Operations, retention, performance |

XV and AY formally registered in MACP v2.1 as the 5th agent executive team.

---

## 4. Application Layer Architecture

**Established formula (L-corrected):**

```
MACP Protocol (coordination layer)
+ Native Agent Capabilities (Claude Code tools, Manus research, Perplexity search, Gemini analytics)
= Application Layer (self-recursive, self-documenting)
```

The `macp-research-assistant` is the first public-facing application built on this architecture (demo layer), not the Research Skills layer.

---

## 5. VerifiMind-PEAS v0.5.2 — Deployment Evidence

- **GCP Cloud Run:** revision `verifimind-mcp-server-00253-dvh`
- **Health check:** `{"version":"0.5.2","status":"healthy"}`
- **Tests:** 198/198 passing (zero regressions from v4.2 schema additions)
- **New Pydantic fields:** 8 Optional fields across 3 agent models (all backward-compatible)
- **PRs merged:** #77 (Genesis v4.2 schema) + #78 (version bump)

---

## Prior Art Claims

This release establishes the following as prior art (March 9, 2026):

1. **Compressed citation code architecture** for LLM regulatory compliance frameworks
2. **C-S-P citation mitigation methodology** (T, Manus AI) for token-efficient framework citation
3. **4-tier jurisdictional ethics framework** for AI validation (International → EU → US → ASEAN)
4. **OWASP Agentic AI threat integration** into multi-agent validation pipelines
5. **Reasoning-layer security audit** (Stage 5) for tool poisoning/shadowing/rugpull detection
6. **Session Status Lifecycle protocol** for multi-agent handoff state management
7. **Read/Write Authority Model** for multi-agent file permission control in MACP

---

## FLYWHEEL TEAM Validation

| Agent | Role | Score |
|-------|------|-------|
| T (Manus AI) | Architecture review | Approved |
| RNA (Claude Code) | Implementation | 198/198 tests ✅ |
| L (GODEL) | Protocol alignment | MACP v2.1 ratified |

**Consensus:** APPROVED — deploy v0.5.2, publish as prior art

---

*FLYWHEEL TEAM v1.2 "Origin" | MACP v2.1 "Origin"*
*Genesis v4.2 "Sentinel-Verified" | March 9, 2026*
