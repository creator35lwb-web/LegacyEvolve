# Agent Protocol Ecosystem Map
## Comprehensive Landscape Analysis (February 2026)

**Research Date:** February 5, 2026  
**Researcher:** Manus AI (CTO, LegacyEvolve Protocol)  
**Purpose:** Map the complete agent protocol ecosystem and identify LEP's strategic positioning

---

## Executive Summary

The agent protocol ecosystem is rapidly evolving with **15+ competing protocols** emerging since 2024. The landscape can be organized along two key dimensions:

1. **Context-Oriented vs. Inter-Agent**: Whether protocols connect agents to external resources or enable agent-to-agent communication
2. **General-Purpose vs. Domain-Specific**: Whether protocols serve broad use cases or optimize for specific domains

**Key Finding:** Only **3 protocols have achieved significant adoption** (MCP: 100K+ stars, A2A: 20K+ stars, AG-UI: 4K+ stars). The rest are experimental (<1K stars).

**LEP's Position:** LEP is a **context-oriented, domain-specific protocol** for legacy system modernization—a unique niche with no direct competitors.

---

## Part 1: Protocol Classification Framework

### Dimension 1: Context-Oriented vs. Inter-Agent

**Context-Oriented Protocols:**
- Enable agents to connect with external resources (databases, APIs, tools, services)
- Standardize how agents acquire context and invoke capabilities beyond their core LLM
- Act as a bridge between AI and existing systems

**Examples:** MCP, ACP (Agent Client Protocol), LEP (LegacyEvolve Protocol)

**Inter-Agent Protocols:**
- Facilitate communication between multiple agents
- Enable collaboration, task delegation, and distributed problem-solving
- Define how agents discover each other, negotiate capabilities, and coordinate workflows

**Examples:** A2A, ANP, AComP, AITP

### Dimension 2: General-Purpose vs. Domain-Specific

**General-Purpose Protocols:**
- Support broad use cases across industries and applications
- Provide universal interfaces that work with diverse agent types
- Prioritize flexibility and wide adoption over specialized optimization

**Examples:** MCP, A2A, ANP

**Domain-Specific Protocols:**
- Optimized for particular environments or use cases
- Sacrifice broad compatibility for deep functionality in target domain
- Examples: AG-UI (agent-to-UI), ACP (agent-to-editor), LEP (agent-to-legacy-system)

---

## Part 2: The Top 3 Production-Ready Protocols

### 1. Model Context Protocol (MCP) ⭐⭐⭐⭐⭐

**Developer:** Anthropic  
**GitHub Stars:** 100K+  
**Status:** Production, most adopted protocol  
**Type:** Context-Oriented, General-Purpose

**Purpose:**
Universal protocol for connecting LLM agents to external resources through a client-server architecture.

**Key Features:**
- JSON-RPC 2.0 for standardized tool invocation and data access
- Decouples sensitive operations from LLM responses
- Unified interface for integrating databases, APIs, and services across different LLM providers
- 100+ community-built MCP servers

**Strengths:**
- ✅ Anthropic-backed (credibility and resources)
- ✅ Largest ecosystem (100+ servers)
- ✅ Production-proven (Claude Desktop, Cline, etc.)
- ✅ Clear documentation and examples

**Weaknesses:**
- ⚠️ Does not focus on agent-to-agent communication
- ⚠️ Lacks strong async support (to be addressed)
- ⚠️ No registry, authorization, or reputation system yet
- ⚠️ Highly duplicative of other protocols

**LEP Relationship:** LEP can interoperate with MCP via LEP-MCP bridge

---

### 2. Agent2Agent (A2A) ⭐⭐⭐⭐

**Developer:** Google  
**GitHub Stars:** 20K+  
**Status:** Production, enterprise-focused  
**Type:** Inter-Agent, General-Purpose

**Purpose:**
Protocol for complex agent collaboration using HTTP(S), JSON-RPC 2.0, and Server-Sent Events.

**Key Features:**
- Async-first architecture with task management
- Multimodal support (text, images, audio, video)
- Built-in enterprise security features
- Capability discovery and user experience negotiation
- Agents collaborate without sharing internal implementation details

**Strengths:**
- ✅ Google-backed (enterprise credibility)
- ✅ Strong async support for long-running agent interactions
- ✅ Enterprise security features
- ✅ Multimodal support

**Weaknesses:**
- ⚠️ Smaller ecosystem than MCP
- ⚠️ More complex than MCP (higher learning curve)
- ⚠️ Less community adoption

**LEP Relationship:** LEP could enable A2A agents to access legacy systems

---

### 3. AG-UI Protocol ⭐⭐⭐

**Developer:** Community-driven  
**GitHub Stars:** 4K+  
**Status:** Production, UI-focused  
**Type:** Context-Oriented, Domain-Specific

**Purpose:**
Lightweight, event-driven protocol standardizing AI agent connections to front-end applications through streaming HTTP interfaces.

**Key Features:**
- 16 typed event categories (lifecycle, messages, tool calls, state management)
- Server-Sent Events and binary protocol support
- Bidirectional state synchronization using JSON Patch deltas
- Real-time UI updates
- Human-in-the-loop workflows through Observable-based agent execution model

**Strengths:**
- ✅ Focused on agent-to-UI communication
- ✅ Real-time updates and streaming
- ✅ Human-in-the-loop support

**Weaknesses:**
- ⚠️ Smaller ecosystem than MCP/A2A
- ⚠️ Domain-specific (UI only)

**LEP Relationship:** LEP could use AG-UI for human approval interfaces

---

## Part 3: Emerging Protocols (1K-10K Stars)

### agents.json ⭐

**Developer:** Community-driven  
**GitHub Stars:** 1K+  
**Type:** Context-Oriented, Domain-Specific (Web)

**Purpose:**
OpenAPI-based specification for making websites AI-agent compatible through machine-readable contracts.

**Key Features:**
- Hosted at `/.well-known/agents.json`
- Defines flows (multi-step API sequences) and data dependencies
- Enables agents to discover and interact with web services
- No custom prompt engineering or integration work needed

**Strengths:**
- ✅ Simple and lightweight
- ✅ Web-native (uses existing web standards)
- ✅ Easy to adopt for websites

**Weaknesses:**
- ⚠️ Web-only (not applicable to other domains)
- ⚠️ Limited adoption so far

**LEP Relationship:** Not directly applicable (LEP is for legacy systems, not websites)

---

### Agent Protocol ⭐

**Developer:** AI Engineer Foundation  
**GitHub Stars:** 1K+  
**Type:** Inter-Agent, General-Purpose

**Purpose:**
Framework-agnostic standard for agent lifecycle management using RESTful APIs and OpenAPI v3.

**Key Features:**
- Core abstractions: Runs (task execution), Threads (multi-turn interactions), Store (persistent memory)
- Enables control consoles to manage heterogeneous agents across diverse systems
- Standardized operations

**Strengths:**
- ✅ Framework-agnostic
- ✅ Clear lifecycle management

**Weaknesses:**
- ⚠️ Limited adoption
- ⚠️ Overlaps with other protocols

**LEP Relationship:** LEP could adopt similar lifecycle management concepts

---

## Part 4: Experimental Protocols (<1K Stars)

### Agent Network Protocol (ANP)

**Developer:** Open-source community  
**Type:** Inter-Agent, General-Purpose

**Purpose:**
Open-source protocol for cross-domain agent communication using W3C DID standards for decentralized identity.

**Key Features:**
- Three layers: identity/encryption, meta-protocol negotiation, application protocols
- Agent discovery and interaction
- Designed to create an "Internet of Agents"
- Native machine-to-machine interfaces (not human-centric)

**Strengths:**
- ✅ Decentralized identity (W3C DID)
- ✅ Vision of "Internet of Agents"

**Weaknesses:**
- ⚠️ Experimental (no significant adoption)
- ⚠️ Complex architecture

**LEP Relationship:** LEP could adopt decentralized identity concepts for adapter certification

---

### Agent Interaction & Transaction Protocol (AITP)

**Developer:** NEAR Foundation  
**Type:** Inter-Agent, Domain-Specific (Blockchain)

**Purpose:**
Blockchain-based protocol for secure agent communication across trust boundaries.

**Key Features:**
- Autonomous negotiation and value exchange
- Structured capabilities and thread-based communication
- Cross-organizational agent interactions
- Built-in identity verification and transaction capabilities
- Cost negotiation (competing agents bid to solve problems)

**Strengths:**
- ✅ Blockchain-based security
- ✅ Value exchange and cost negotiation

**Weaknesses:**
- ⚠️ Blockchain dependency (complexity and cost)
- ⚠️ Limited adoption

**LEP Relationship:** LEP could adopt cost negotiation concepts for adapter marketplace

---

### Summoner Protocol (SPTL)

**Developer:** Summoner team  
**Type:** Inter-Agent, General-Purpose

**Purpose:**
Modular runtime and SDK for building and coordinating autonomous agents across networks.

**Key Features:**
- Python client, Rust relay server, optional desktop UI
- Self-issued cryptographic identities
- Encrypted relay routing
- Behavior-based reputation for trust
- Native micropayments (ERC-20 compatible)
- Modular SDK extensions for composable agent systems

**Strengths:**
- ✅ Decentralized, peer-to-peer (alternative to hub-based systems like MCP/A2A)
- ✅ Reputation system
- ✅ Micropayments

**Weaknesses:**
- ⚠️ Experimental
- ⚠️ Complex architecture

**LEP Relationship:** LEP could adopt reputation system for adapter certification

---

### Agent Connect Protocol (AConP)

**Developer:** Cisco/LangChain  
**Type:** Inter-Agent, General-Purpose

**Purpose:**
Specification defining standard APIs for agent invocation and configuration using OpenAPI and JSON.

**Key Features:**
- Endpoints for agent lifecycle management (run, interrupt, resume)
- Thread-based interactions
- Distributed registry for global agent discovery
- Agent distribution mechanisms (download and execute agents locally)

**Strengths:**
- ✅ Cisco/LangChain backing
- ✅ Agent discovery registry

**Weaknesses:**
- ⚠️ Limited adoption
- ⚠️ Overlaps with other protocols

**LEP Relationship:** LEP could adopt agent discovery concepts for adapter registry

---

### Agent Communication Protocol (AComP)

**Developer:** IBM / Linux Foundation  
**Type:** Inter-Agent, General-Purpose

**Purpose:**
Open protocol for agent interoperability using standardized RESTful APIs that support all modalities, async/sync communication, and streaming interactions.

**Key Features:**
- BeeAI as reference implementation
- Seamless agent replacement
- Multi-agent collaboration
- Cross-platform integration
- Offline discovery
- Mimetype-based content handling
- Works with any framework

**Strengths:**
- ✅ IBM / Linux Foundation backing
- ✅ Reference implementation (BeeAI)

**Weaknesses:**
- ⚠️ Limited adoption
- ⚠️ Overlaps with other protocols

**LEP Relationship:** LEP could adopt mimetype-based content handling

---

## Part 5: Domain-Specific Protocols

### Agent Client Protocol (ACP) ⭐⭐

**Developer:** Community-driven (Zed, JetBrains, GitHub)  
**Type:** Context-Oriented, Domain-Specific (Code Editors)

**Purpose:**
Open standard for connecting AI coding agents to code editors/IDEs.

**Key Features:**
- JSON-RPC 2.0 for reliable communication
- Connects via stdio (local) or HTTP (remote)
- Standardized methods for file access, terminal execution, permissions
- Streams agent plans, reasoning, and tool calls via session updates
- Re-uses MCP JSON representations where possible

**Strengths:**
- ✅ Focused domain (code editors)
- ✅ Zed, JetBrains, GitHub support
- ✅ Re-uses MCP patterns (interoperability)

**Weaknesses:**
- ⚠️ Domain-specific (editors only)
- ⚠️ Smaller ecosystem than MCP

**LEP Relationship:** **Closest analog to LEP!** Both are context-oriented, domain-specific protocols using JSON-RPC 2.0. LEP can learn from ACP's design patterns.

---

### LegacyEvolve Protocol (LEP) ⭐ (NEW!)

**Developer:** Open-source community (Digital Public Good)  
**Type:** Context-Oriented, Domain-Specific (Legacy Systems)

**Purpose:**
Open protocol for connecting AI agents to legacy systems (COBOL mainframes, AS/400, old ERPs).

**Key Features:**
- JSON-RPC 2.0 for reliable communication
- TLS 1.3 for security
- Standardized methods for skill discovery, resource access, skill execution
- Mandatory human-in-the-loop approval for write operations
- Mandatory audit logging
- Adapter certification framework

**Strengths:**
- ✅ Unique niche (legacy systems)
- ✅ No direct competitors
- ✅ Rigorous security model (stricter than MCP/ACP)
- ✅ Digital Public Good positioning

**Weaknesses:**
- ⚠️ Pre-implementation (no code yet)
- ⚠️ No ecosystem yet

**Strategic Position:** LEP fills a critical gap in the agent protocol ecosystem—no other protocol addresses legacy system modernization.

---

## Part 6: Protocol Ecosystem Visualization

### The Agent Protocol Landscape (2D Map)

```
                        General-Purpose
                              ▲
                              │
                              │
                    ┌─────────┼─────────┐
                    │   MCP   │   A2A   │
                    │ (100K⭐) │ (20K⭐)  │
                    │         │         │
                    │  ANP    │ AComP   │
                    │         │  AITP   │
                    │         │ Summoner│
Context-Oriented ◄──┼─────────┼─────────┼──► Inter-Agent
                    │         │         │
                    │  ACP    │ AG-UI   │
                    │  LEP    │ (4K⭐)   │
                    │         │         │
                    │agents.  │ Agent   │
                    │json     │Protocol │
                    └─────────┼─────────┘
                              │
                              │
                              ▼
                        Domain-Specific
```

### LEP's Strategic Position

**Quadrant:** Context-Oriented + Domain-Specific (Lower-Left)

**Neighbors:**
- **ACP** (agent-to-editor): Closest analog, same quadrant
- **agents.json** (agent-to-website): Same quadrant, different domain
- **MCP** (agent-to-context): Adjacent quadrant, general-purpose

**Unique Value Proposition:**
LEP is the **only protocol** focused on legacy system modernization. This is a **blue ocean** opportunity.

---

## Part 7: Adoption Metrics and Trends

### GitHub Stars (Proxy for Adoption)

| Protocol | Stars | Status | Trend |
|----------|-------|--------|-------|
| MCP | 100K+ | Production | ↗️ Rapid growth |
| A2A | 20K+ | Production | ↗️ Steady growth |
| AG-UI | 4K+ | Production | ↗️ Growing |
| agents.json | 1K+ | Emerging | → Stable |
| Agent Protocol | 1K+ | Emerging | → Stable |
| ACP | <1K | Emerging | ↗️ Growing |
| LEP | 0 (pre-launch) | Concept | 🚀 Launch pending |
| All others | <1K | Experimental | → Stable or declining |

### Key Insights:

1. **Winner-Take-Most Dynamics:** MCP has 5x more stars than A2A, 25x more than AG-UI. The ecosystem is consolidating around a few winners.

2. **Corporate Backing Matters:** MCP (Anthropic), A2A (Google), AComP (IBM) have more traction than community-driven protocols.

3. **Domain-Specific Protocols Can Succeed:** ACP and AG-UI are growing despite being domain-specific, because they solve focused problems well.

4. **Timing is Critical:** MCP launched in Nov 2024 and captured the market. Late entrants struggle unless they have unique value.

**Implication for LEP:** LEP has a **unique value proposition** (legacy systems) and **no direct competitors**. If launched with strong execution, LEP can capture its niche.

---

## Part 8: Interoperability Matrix

### Which Protocols Can Work Together?

| Protocol 1 | Protocol 2 | Interoperability | Use Case |
|------------|------------|------------------|----------|
| MCP | ACP | ✅ High | ACP re-uses MCP JSON representations |
| MCP | LEP | ✅ High | LEP can expose MCP interface (LEP-MCP bridge) |
| A2A | LEP | ✅ Medium | A2A agents can invoke LEP adapters |
| ACP | LEP | ✅ Medium | ACP agents can use LEP for legacy data |
| AG-UI | LEP | ✅ High | AG-UI can provide human approval UI for LEP |
| MCP | A2A | ⚠️ Low | Different purposes (context vs. inter-agent) |
| ANP | LEP | ⚠️ Low | Different architectures (decentralized vs. client-server) |

### Key Insight:

**LEP has high interoperability potential** with MCP, ACP, and AG-UI because:
1. All use JSON-RPC 2.0
2. All are context-oriented (or have context-oriented features)
3. LEP can act as a "data provider" for other protocols

---

## Part 9: Strategic Recommendations for LEP

### 1. Position LEP as "MCP for Legacy Systems" ⭐⭐⭐

**Why:** Leverages MCP's credibility and familiarity

**How:**
- Use similar language and concepts as MCP
- Reference MCP in LEP documentation
- Build LEP-MCP bridge early

**Benefit:** Easier to explain, faster adoption

---

### 2. Build LEP-MCP Bridge as First Interoperability Project ⭐⭐⭐

**Why:** MCP has the largest ecosystem (100K+ stars)

**How:**
- Create translation layer: MCP `tools/call` → LEP `legacy/callSkill`
- Publish as open-source project
- Demonstrate LEP adapter working with Claude Desktop

**Benefit:** Instant access to MCP ecosystem

---

### 3. Collaborate with ACP Community ⭐⭐

**Why:** ACP is the closest analog to LEP (same quadrant)

**How:**
- Reach out to ACP maintainers (Zed, JetBrains, GitHub)
- Propose shared standards (permission model, error codes)
- Co-develop interoperability layer

**Benefit:** Shared learning, cross-promotion

---

### 4. Adopt MCP/ACP Best Practices ⭐⭐⭐

**Why:** Don't reinvent the wheel, leverage proven patterns

**What:**
- Explicit initialization and capability negotiation (from ACP)
- 4-kind permission model (from ACP)
- Notification support (from ACP)
- Security principles (from MCP)

**Benefit:** Better protocol design, faster implementation

---

### 5. Join Agent Protocol Community Discussions ⭐⭐

**Why:** Network effects, visibility, collaboration opportunities

**How:**
- Participate in MCP Discord/GitHub
- Participate in ACP discussions
- Present LEP at agent protocol conferences/meetups

**Benefit:** Community support, early adopters, partnerships

---

### 6. Differentiate on Security and Governance ⭐⭐⭐

**Why:** Legacy systems require stricter security than code editors or general tools

**How:**
- Emphasize mandatory human-in-the-loop
- Emphasize mandatory audit logging
- Emphasize adapter certification
- Emphasize scope restrictions (prohibited applications)

**Benefit:** Trust and credibility for enterprise adoption

---

### 7. Target Enterprise Early Adopters ⭐⭐⭐

**Why:** Enterprises have legacy systems and budget

**How:**
- Identify 3-5 pilot organizations (banks, insurance, manufacturing)
- Offer free consulting and adapter development
- Build case studies and testimonials

**Benefit:** Proof points, revenue, ecosystem growth

---

## Part 10: Conclusion

### Key Takeaways

1. ✅ **The agent protocol ecosystem is forming NOW**
   - 15+ protocols competing
   - Only 3 have achieved significant adoption (MCP, A2A, AG-UI)
   - Winner-take-most dynamics

2. ✅ **LEP has a unique strategic position**
   - Context-oriented, domain-specific (legacy systems)
   - No direct competitors
   - Blue ocean opportunity

3. ✅ **JSON-RPC 2.0 is the industry standard**
   - MCP, A2A, ACP, LEP all use JSON-RPC 2.0
   - LEP's choice is validated

4. ✅ **Interoperability is achievable and valuable**
   - LEP can work with MCP, ACP, AG-UI
   - LEP-MCP bridge should be first priority
   - Shared standards (permission model, error codes) are possible

5. ✅ **Timing and execution are critical**
   - MCP captured the market by being first and well-executed
   - LEP needs to move fast and execute well
   - Corporate backing helps but isn't required (ACP is community-driven)

6. ✅ **Domain-specific protocols can succeed**
   - ACP (editors) and AG-UI (UI) are growing despite being domain-specific
   - LEP (legacy systems) can succeed with focused execution

### Next Steps for LEP

**Immediate (This Week):**
1. Update LEP documentation to reference MCP and ACP
2. Reach out to Philipp Schmid (ACP) and Anthropic (MCP) communities
3. Draft LEP-MCP bridge specification

**Short-Term (Next Month):**
4. Build LEP-MCP bridge proof-of-concept
5. Demonstrate LEP adapter working with Claude Desktop
6. Present LEP at agent protocol community meetings

**Long-Term (Next Quarter):**
7. Recruit 3-5 pilot organizations
8. Build first production adapter (banking or insurance)
9. Publish case studies and testimonials

---

**The agent protocol ecosystem is the next frontier of AI infrastructure. LEP has a unique opportunity to be a founding member and shape the future of legacy system modernization.**

---

**Document Version:** 1.0  
**Last Updated:** February 5, 2026  
**Status:** Ready for Implementation
