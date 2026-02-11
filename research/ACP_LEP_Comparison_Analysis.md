# Agent Client Protocol (ACP) vs LegacyEvolve Protocol (LEP)
## Comprehensive Comparison and Design Analysis

**Research Date:** February 5, 2026  
**Researcher:** Manus AI (CTO, LegacyEvolve Protocol)  
**Purpose:** Detailed comparison of ACP and LEP to identify best practices and improvement opportunities

---

## Executive Summary

The Agent Client Protocol (ACP) and LegacyEvolve Protocol (LEP) are both JSON-RPC 2.0-based protocols for agent-system communication, but serve different domains. ACP connects AI coding agents to code editors/IDEs, while LEP connects AI agents to legacy systems. Despite different purposes, they share remarkable architectural similarities and can learn from each other.

**Key Finding:** ACP validates LEP's core design decisions (JSON-RPC 2.0, permission mechanisms, capability negotiation) while revealing opportunities for LEP to adopt industry best practices.

---

## Part 1: Side-by-Side Protocol Comparison

### 1.1 Foundation & Architecture

| Aspect | ACP | LEP | Analysis |
|--------|-----|-----|----------|
| **Protocol Base** | JSON-RPC 2.0 | JSON-RPC 2.0 | ✅ Both use industry standard |
| **Message Types** | Methods + Notifications | Methods only (currently) | ⚠️ LEP should add notifications |
| **Connection Model** | Stateful sessions | Stateful connections | ✅ Both stateful |
| **Transport** | stdio (local), HTTP/WebSocket (remote) | TLS 1.3 (all scenarios) | Different but appropriate for domains |
| **Initialization** | Explicit `initialize` method | Implicit in connection | ⚠️ LEP should add explicit initialization |
| **Capability Negotiation** | During initialization | Not specified | ⚠️ LEP needs capability negotiation |

**Recommendation:** LEP should adopt ACP's explicit initialization and capability negotiation pattern.

---

### 1.2 Core Methods Comparison

#### Agent-Side Methods (What Agents Implement)

| ACP Method | LEP Equivalent | Similarity | Notes |
|------------|----------------|------------|-------|
| `initialize` | *(missing)* | N/A | LEP needs this |
| `authenticate` | *(implicit in TLS)* | Partial | LEP could make explicit |
| `session/new` | *(implicit)* | N/A | LEP could add session management |
| `session/prompt` | `legacy/callSkill` | High | Similar purpose: execute operation |
| `session/load` | *(missing)* | N/A | Optional for LEP |
| `session/set_mode` | *(missing)* | N/A | Not applicable to LEP |

**Key Insight:** ACP has richer session management. LEP could benefit from explicit session lifecycle.

#### Client-Side Methods (What Clients Implement)

| ACP Method | LEP Equivalent | Similarity | Notes |
|------------|----------------|------------|-------|
| `session/request_permission` | `security/requestApproval` | **Very High** ⭐ | Core similarity! |
| `fs/read_text_file` | `legacy/getResource` | High | Similar purpose: read data |
| `fs/write_text_file` | `legacy/executeSkill` (write) | High | Similar purpose: write data |
| `terminal/create` | *(not applicable)* | N/A | ACP-specific |
| `terminal/output` | *(not applicable)* | N/A | ACP-specific |
| `terminal/release` | *(not applicable)* | N/A | ACP-specific |
| `terminal/wait_for_exit` | *(not applicable)* | N/A | ACP-specific |
| `terminal/kill` | *(not applicable)* | N/A | ACP-specific |

**Key Insight:** Permission mechanism is the **core parallel** between ACP and LEP.

#### Notifications

| ACP Notification | LEP Equivalent | Similarity | Notes |
|------------------|----------------|------------|-------|
| `session/update` | *(missing)* | N/A | LEP should add for real-time updates |
| `session/cancel` | *(missing)* | N/A | LEP should add for cancellation |

**Recommendation:** LEP should add notification support for:
1. Real-time progress updates (`legacy/update`)
2. Operation cancellation (`legacy/cancel`)
3. Audit log streaming (`security/auditUpdate`)

---

### 1.3 Permission Mechanisms (Deep Dive)

This is the **most critical comparison** because both protocols recognize permission/approval as fundamental.

#### ACP Permission Model

**Method:** `session/request_permission`

**Request Structure:**
```json
{
  "method": "session/request_permission",
  "params": {
    "sessionId": "sess_abc123def456",
    "toolCall": {
      "toolCallId": "call_001",
      "title": "Reading configuration file",
      "kind": "read",
      "status": "pending"
    },
    "options": [
      {
        "optionId": "allow-once",
        "name": "Allow once",
        "kind": "allow_once"
      },
      {
        "optionId": "allow-always",
        "name": "Allow always",
        "kind": "allow_always"
      },
      {
        "optionId": "reject-once",
        "name": "Reject",
        "kind": "reject_once"
      },
      {
        "optionId": "reject-always",
        "name": "Reject always",
        "kind": "reject_always"
      }
    ]
  }
}
```

**Response Structure:**
```json
{
  "result": {
    "outcome": {
      "outcome": "selected",
      "optionId": "allow-once"
    }
  }
}
```

**Permission Options (4 Kinds):**
1. `allow_once` - Allow this operation only this time
2. `allow_always` - Allow this operation and remember the choice
3. `reject_once` - Reject this operation only this time
4. `reject_always` - Reject this operation and remember the choice

**Automatic Handling:**
> "Clients MAY automatically allow or reject permission requests according to the user settings."

**Cancellation:**
If prompt turn is cancelled, client responds with:
```json
{
  "outcome": {
    "outcome": "cancelled"
  }
}
```

---

#### LEP Permission Model (Current)

**Method:** `security/requestApproval`

**Request Structure (Conceptual):**
```json
{
  "method": "security/requestApproval",
  "params": {
    "operation": "executeSkill",
    "skillName": "updateAccountBalance",
    "parameters": {
      "accountId": "12345",
      "newBalance": 1000.00
    },
    "reason": "AI agent requested account balance update"
  }
}
```

**Response Structure (Conceptual):**
```json
{
  "result": {
    "approved": true,
    "approvalToken": "tok_xyz789abc",
    "expiresAt": "2026-02-05T12:00:00Z"
  }
}
```

**Permission Options:**
- Binary: Approve or Reject
- Token-based: Approval token must be included in subsequent operation

**Automatic Handling:**
- Supported (configurable policies)

**Timeout:**
- Approval token expires after configured time

---

#### Comparison: ACP vs LEP Permission

| Aspect | ACP | LEP | Winner |
|--------|-----|-----|--------|
| **Granularity** | Per tool call | Per operation | Tie |
| **Options** | 4 kinds (once/always, allow/reject) | Binary (approve/reject) | **ACP** ⭐ |
| **Token/ID** | `optionId` for tracking | `approvalToken` for validation | **LEP** ⭐ |
| **Remember Choice** | Built-in (`allow_always`/`reject_always`) | Policy-based (future) | **ACP** ⭐ |
| **Cancellation** | Explicit `cancelled` outcome | Timeout-based | **ACP** ⭐ |
| **Automatic Mode** | Supported (MAY) | Supported (configurable) | Tie |
| **Security** | User settings control | Cryptographic token validation | **LEP** ⭐ |
| **Scope** | Optional (MAY request) | Mandatory for writes (MUST request) | **LEP** ⭐ |

**Key Insights:**

1. ✅ **ACP's 4-kind permission model is superior for UX**
   - Users can say "always allow this" or "never allow this"
   - Reduces permission fatigue
   - More flexible than binary approve/reject

2. ✅ **LEP's approval token is superior for security**
   - Cryptographic validation prevents replay attacks
   - Time-limited tokens reduce risk window
   - Explicit token passing makes audit trail clearer

3. ✅ **Best of both worlds:** LEP should adopt ACP's 4-kind model + keep approval tokens

**Recommendation:** Enhance LEP's `security/requestApproval` to support:
```json
{
  "method": "security/requestApproval",
  "params": {
    "operation": "executeSkill",
    "skillName": "updateAccountBalance",
    "parameters": {...},
    "reason": "AI agent requested account balance update",
    "options": [
      {
        "optionId": "approve-once",
        "name": "Approve once",
        "kind": "approve_once"
      },
      {
        "optionId": "approve-always-skill",
        "name": "Always approve this skill",
        "kind": "approve_always"
      },
      {
        "optionId": "reject-once",
        "name": "Reject",
        "kind": "reject_once"
      },
      {
        "optionId": "reject-always-skill",
        "name": "Never allow this skill",
        "kind": "reject_always"
      }
    ]
  }
}
```

Response includes both `outcome` and `approvalToken`:
```json
{
  "result": {
    "outcome": {
      "outcome": "selected",
      "optionId": "approve-once"
    },
    "approvalToken": "tok_xyz789abc",
    "expiresAt": "2026-02-05T12:00:00Z"
  }
}
```

---

### 1.4 Error Handling

| Aspect | ACP | LEP | Analysis |
|--------|-----|-----|----------|
| **Error Format** | Standard JSON-RPC 2.0 | Standard JSON-RPC 2.0 | ✅ Both follow standard |
| **Error Structure** | `error` object with `code` and `message` | Same | ✅ Aligned |
| **Success Response** | `result` field | Same | ✅ Aligned |
| **Notification Errors** | Never receive responses | Not applicable (no notifications yet) | LEP should follow ACP pattern |

**Recommendation:** LEP should document standard error codes similar to HTTP status codes:
- 400-series: Client errors (invalid request, unauthorized, etc.)
- 500-series: Server errors (adapter failure, legacy system error, etc.)

---

### 1.5 Content Types

#### ACP Content Types

1. **Regular Content:** Text, images, resources
2. **Diffs:** File modifications (oldText → newText)
   ```json
   {
     "type": "diff",
     "path": "/home/user/project/src/config.json",
     "oldText": "{\n  \"debug\": false\n}",
     "newText": "{\n  \"debug\": true\n}"
   }
   ```
3. **Terminals:** Live terminal output

#### LEP Content Types (Current)

1. **Resources:** Data from legacy systems
2. **Skill Results:** Execution results

**Gap:** LEP doesn't have a "diff" concept for showing before/after changes.

**Recommendation:** LEP should add diff support for write operations:
```json
{
  "type": "diff",
  "resource": "CUSTOMER.ACCOUNT.DB",
  "recordId": "12345",
  "field": "balance",
  "oldValue": 500.00,
  "newValue": 1000.00
}
```

This would help users understand exactly what changed in the legacy system.

---

### 1.6 Tool Call Lifecycle vs Skill Execution Lifecycle

#### ACP Tool Call Lifecycle

1. **Creating:** Agent reports tool call via `session/update` (status: `pending`)
2. **Requesting Permission:** Agent calls `session/request_permission` (optional)
3. **Updating:** Agent sends progress updates via `session/update` (status: `in_progress`)
4. **Completing:** Agent sends final update (status: `completed` or `failed`)

**Statuses:**
- `pending` - Tool call hasn't started (awaiting approval or input streaming)
- `in_progress` - Tool call is currently running
- `completed` - Tool call completed successfully
- `failed` - Tool call failed with an error

#### LEP Skill Execution Lifecycle (Current)

1. **Listing:** Agent calls `legacy/listSkills` to discover available operations
2. **Requesting Approval:** Agent calls `security/requestApproval` (for writes)
3. **Executing:** Agent calls `legacy/executeSkill` with approval token
4. **Auditing:** Agent calls `security/getAuditTrail` to retrieve audit log

**Gap:** LEP doesn't have real-time progress updates during execution.

**Recommendation:** LEP should add `legacy/update` notification for real-time progress:
```json
{
  "method": "legacy/update",
  "params": {
    "executionId": "exec_001",
    "status": "in_progress",
    "progress": {
      "current": 50,
      "total": 100,
      "message": "Processing records 50/100..."
    }
  }
}
```

---

### 1.7 Security Models

#### ACP Security Principles (from MCP)

1. **User Consent and Control**
   - Users must explicitly consent to and understand all data access
   - Users retain control over what data is shared
   - Clear UIs for reviewing and authorizing activities

2. **Data Privacy**
   - Hosts must obtain explicit user consent before exposing user data
   - Hosts must not transmit resource data elsewhere without consent
   - User data protected with appropriate access controls

3. **Tool Safety**
   - Tools represent arbitrary code execution
   - Tool descriptions are UNTRUSTED unless from trusted server
   - Hosts must obtain explicit user consent before invoking any tool

4. **LLM Sampling Controls**
   - Users must explicitly approve any LLM sampling requests
   - Protocol intentionally limits server visibility into prompts

#### LEP Security Principles (from Trinity Validation)

1. **Human-in-the-Loop (Mandatory)**
   - All write operations require explicit human approval
   - Approval tokens with cryptographic validation
   - Time-limited tokens to reduce risk window

2. **Audit Logging (Mandatory)**
   - All operations logged with timestamp, user, operation, data accessed
   - Log integrity protection (HMAC signing)
   - Audit trail accessible via `security/getAuditTrail`

3. **Data Minimization (Mandatory)**
   - Purpose declaration for all data access
   - Scope limitation parameters
   - Only necessary data accessed

4. **Adapter Certification (Mandatory)**
   - Independent security audits
   - Ethics review board approval
   - Tiered security controls (Tier 1-4)

5. **Scope Restrictions (Mandatory)**
   - Prohibited applications (weapons, mass surveillance)
   - Restricted applications (critical infrastructure)
   - Conditional applications (banking, insurance)

**Comparison:**

| Principle | ACP/MCP | LEP | Analysis |
|-----------|---------|-----|----------|
| User Consent | ✅ Required | ✅ Required (human-in-the-loop) | Both have this |
| Data Privacy | ✅ Required | ✅ Required (data minimization) | Both have this |
| Tool/Skill Safety | ✅ Untrusted descriptions | ✅ Certification required | LEP is stricter |
| Audit Logging | ⚠️ Not specified | ✅ Mandatory | LEP is stricter |
| Scope Restrictions | ⚠️ Not specified | ✅ Mandatory (prohibited apps) | LEP is stricter |

**Key Insight:** LEP has a **stricter security model** than ACP because legacy systems are higher risk than code editors.

**Recommendation:** LEP should adopt ACP/MCP's principle of "untrusted descriptions":
- Adapter skill descriptions should be treated as untrusted unless adapter is certified
- UI should indicate certification status
- Warnings for uncertified adapters

---

## Part 2: JSON-RPC 2.0 Pattern Analysis

### 2.1 Why JSON-RPC 2.0?

Both ACP and LEP chose JSON-RPC 2.0. Why is this the industry standard for agent protocols?

**Advantages:**

1. ✅ **Simple and Lightweight**
   - Easy to implement in any language
   - Minimal overhead
   - Human-readable JSON format

2. ✅ **Request-Response Pattern**
   - Clear request-response pairs
   - Easy error handling
   - Supports both synchronous and asynchronous operations

3. ✅ **Extensible**
   - Custom methods easy to add
   - Custom parameters supported
   - Backward compatibility

4. ✅ **Proven in Production**
   - Language Server Protocol (LSP) uses JSON-RPC 2.0
   - Model Context Protocol (MCP) uses JSON-RPC 2.0
   - Debug Adapter Protocol (DAP) uses JSON-RPC 2.0
   - Now ACP and LEP use JSON-RPC 2.0

5. ✅ **Tooling and Libraries**
   - JSON-RPC 2.0 libraries available in all major languages
   - Testing tools available
   - Debugging tools available

**Disadvantages:**

1. ⚠️ **No Built-in Streaming**
   - JSON-RPC 2.0 is request-response only
   - Streaming requires notifications or custom extensions
   - ACP solves this with `session/update` notifications

2. ⚠️ **No Built-in Authentication**
   - JSON-RPC 2.0 has no authentication mechanism
   - Must be layered on top (TLS, OAuth, etc.)
   - ACP has explicit `authenticate` method
   - LEP uses TLS 1.3

3. ⚠️ **Limited Error Semantics**
   - Only `code` and `message` in error object
   - No standard error codes (unlike HTTP)
   - Protocols must define their own error codes

**Conclusion:** JSON-RPC 2.0 is the right choice for both ACP and LEP. Its simplicity, extensibility, and proven track record make it ideal for agent protocols.

---

### 2.2 Methods vs Notifications

**Methods:**
- Request-response pairs
- Expect a result or error
- Synchronous or asynchronous

**Notifications:**
- One-way messages
- Don't expect a response
- Used for events, updates, cancellations

**ACP Usage:**

- **Methods:** `initialize`, `authenticate`, `session/new`, `session/prompt`, `session/request_permission`, `fs/read_text_file`, `fs/write_text_file`, etc.
- **Notifications:** `session/update`, `session/cancel`

**LEP Usage (Current):**

- **Methods:** `legacy/listSkills`, `legacy/getResource`, `legacy/callSkill`, `security/requestApproval`, `security/getAuditTrail`
- **Notifications:** *(none currently)*

**Recommendation:** LEP should add notifications for:
1. `legacy/update` - Real-time progress updates during skill execution
2. `legacy/cancel` - Cancel ongoing skill execution
3. `security/auditUpdate` - Real-time audit log streaming

---

### 2.3 Capability Negotiation Pattern

**ACP Pattern:**

During `initialize`, client and agent exchange capabilities:

**Client → Agent:**
```json
{
  "method": "initialize",
  "params": {
    "protocolVersion": "1.0.0",
    "clientInfo": {
      "name": "Zed",
      "version": "0.1.0"
    },
    "capabilities": {
      "fs": {
        "readTextFile": true,
        "writeTextFile": true
      },
      "terminal": true
    }
  }
}
```

**Agent → Client:**
```json
{
  "result": {
    "protocolVersion": "1.0.0",
    "agentInfo": {
      "name": "Claude Code",
      "version": "1.0.0"
    },
    "capabilities": {
      "loadSession": true,
      "modes": ["auto", "manual"]
    }
  }
}
```

Now both sides know what the other supports!

**LEP Should Adopt This:**

**Client → Adapter:**
```json
{
  "method": "initialize",
  "params": {
    "protocolVersion": "1.0.0",
    "clientInfo": {
      "name": "LangChain",
      "version": "0.1.0"
    },
    "capabilities": {
      "approval": {
        "humanInTheLoop": true,
        "automaticApproval": false
      },
      "audit": {
        "logging": true,
        "streaming": false
      }
    }
  }
}
```

**Adapter → Client:**
```json
{
  "result": {
    "protocolVersion": "1.0.0",
    "adapterInfo": {
      "name": "Banking Mainframe Adapter",
      "version": "1.0.0",
      "certified": true,
      "certificationLevel": "Tier 1"
    },
    "capabilities": {
      "operations": {
        "read": true,
        "write": true,
        "transaction": false
      },
      "dataMinimization": true,
      "realTimeUpdates": false
    }
  }
}
```

**Benefits:**
1. Client knows what adapter supports (read-only? write? transactions?)
2. Adapter knows what client supports (automatic approval? audit streaming?)
3. Both can adapt behavior accordingly
4. Graceful degradation if features not supported
5. Future extensibility without breaking changes

---

## Part 3: Key Recommendations for LEP

Based on this comprehensive comparison, here are the top recommendations for enhancing LEP:

### Priority 1: Add Explicit Initialization and Capability Negotiation ⭐⭐⭐

**Why:** Industry standard pattern (ACP, MCP, LSP all have this)

**What:** Add `initialize` method to LEP

**Example:**
```json
// Client → Adapter
{
  "method": "initialize",
  "params": {
    "protocolVersion": "1.0.0",
    "clientInfo": {...},
    "capabilities": {...}
  }
}

// Adapter → Client
{
  "result": {
    "protocolVersion": "1.0.0",
    "adapterInfo": {...},
    "capabilities": {...}
  }
}
```

**Impact:** High - Enables extensibility and interoperability

---

### Priority 2: Enhance Permission Mechanism with ACP's 4-Kind Model ⭐⭐⭐

**Why:** Better UX, reduces permission fatigue, more flexible

**What:** Add `approve_always` and `reject_always` options to `security/requestApproval`

**Example:**
```json
{
  "method": "security/requestApproval",
  "params": {
    "operation": "executeSkill",
    "skillName": "updateAccountBalance",
    "parameters": {...},
    "options": [
      {"optionId": "approve-once", "kind": "approve_once"},
      {"optionId": "approve-always-skill", "kind": "approve_always"},
      {"optionId": "reject-once", "kind": "reject_once"},
      {"optionId": "reject-always-skill", "kind": "reject_always"}
    ]
  }
}
```

**Impact:** High - Significantly improves user experience

---

### Priority 3: Add Notification Support for Real-Time Updates ⭐⭐

**Why:** Users need to see progress during long-running operations

**What:** Add `legacy/update` notification

**Example:**
```json
{
  "method": "legacy/update",
  "params": {
    "executionId": "exec_001",
    "status": "in_progress",
    "progress": {
      "current": 50,
      "total": 100,
      "message": "Processing records 50/100..."
    }
  }
}
```

**Impact:** Medium - Improves UX for long-running operations

---

### Priority 4: Add Diff Support for Write Operations ⭐⭐

**Why:** Users need to see exactly what changed in legacy system

**What:** Add diff content type to skill execution results

**Example:**
```json
{
  "type": "diff",
  "resource": "CUSTOMER.ACCOUNT.DB",
  "recordId": "12345",
  "field": "balance",
  "oldValue": 500.00,
  "newValue": 1000.00
}
```

**Impact:** Medium - Improves transparency and trust

---

### Priority 5: Add Cancellation Support ⭐

**Why:** Users need ability to cancel long-running operations

**What:** Add `legacy/cancel` notification

**Example:**
```json
{
  "method": "legacy/cancel",
  "params": {
    "executionId": "exec_001"
  }
}
```

**Impact:** Low - Nice to have, not critical for MVP

---

### Priority 6: Document Standard Error Codes ⭐

**Why:** Consistent error handling across adapters

**What:** Define standard error codes similar to HTTP status codes

**Example:**
- 400: Invalid request
- 401: Unauthorized
- 403: Forbidden (approval denied)
- 404: Skill not found
- 500: Adapter internal error
- 502: Legacy system error
- 503: Legacy system unavailable

**Impact:** Low - Improves developer experience

---

## Part 4: Interoperability Opportunities

### 4.1 LEP Adapter as MCP Server

**Concept:** A LEP adapter could expose an MCP server interface

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client (Claude Desktop)              │
└──────────────────────┬──────────────────────────────────────┘
                       │ MCP Protocol
                       │ (tools/call, resources/read)
┌──────────────────────▼──────────────────────────────────────┐
│              LEP-MCP Bridge (Translation Layer)             │
│  - Translates MCP tools/call → LEP legacy/callSkill        │
│  - Translates MCP resources/read → LEP legacy/getResource  │
│  - Handles permission mapping                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ LEP Protocol
┌──────────────────────▼──────────────────────────────────────┐
│              LEP Adapter (Banking Mainframe)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Legacy System (COBOL Mainframe)            │
└─────────────────────────────────────────────────────────────┘
```

**Use Case:**
- Claude Desktop user wants to query banking mainframe
- LEP adapter exposes MCP interface
- Claude Desktop sees mainframe as MCP server
- User can use natural language to query legacy system

**Benefits:**
- Instant access to MCP ecosystem (Claude Desktop, Cline, etc.)
- No need to build custom integrations
- Leverages existing MCP tooling

**Implementation Complexity:** Medium

---

### 4.2 ACP Agent Using LEP

**Concept:** An ACP-compatible agent (Claude Code, Gemini CLI) could use LEP to access legacy systems

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Code Editor (Zed, JetBrains)             │
└──────────────────────┬──────────────────────────────────────┘
                       │ ACP Protocol
┌──────────────────────▼──────────────────────────────────────┐
│              ACP Agent (Claude Code, Gemini CLI)            │
└──────────────────────┬──────────────────────────────────────┘
                       │ LEP Protocol
┌──────────────────────▼──────────────────────────────────────┐
│              LEP Adapter (Banking Mainframe)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Legacy System (COBOL Mainframe)            │
└─────────────────────────────────────────────────────────────┘
```

**Use Case:**
- Developer using Claude Code in Zed editor
- Needs to query production mainframe to debug issue
- Claude Code connects to LEP adapter
- Developer gets real-time data from legacy system in editor

**Benefits:**
- Developers can access legacy systems without leaving editor
- AI agents can use production data for better assistance
- Bridges modern dev tools with legacy systems

**Implementation Complexity:** Low (ACP agents can already call external APIs)

---

### 4.3 Unified Permission Framework

**Concept:** Cross-protocol permission standard that works across MCP, ACP, and LEP

**Shared Permission Schema:**
```json
{
  "method": "permission/request",
  "params": {
    "protocol": "LEP",
    "operation": {
      "type": "write",
      "target": "CUSTOMER.ACCOUNT.DB",
      "action": "updateAccountBalance",
      "parameters": {...}
    },
    "options": [
      {"optionId": "allow-once", "kind": "allow_once"},
      {"optionId": "allow-always", "kind": "allow_always"},
      {"optionId": "reject-once", "kind": "reject_once"},
      {"optionId": "reject-always", "kind": "reject_always"}
    ]
  }
}
```

**Benefits:**
- Shared UI components for permission dialogs
- Consistent user experience across protocols
- Lower implementation cost for tool builders

**Implementation Complexity:** High (requires coordination across protocol communities)

---

## Part 5: Conclusion

### Key Takeaways

1. ✅ **ACP validates LEP's core design decisions**
   - JSON-RPC 2.0 is the right choice
   - Permission mechanisms are fundamental
   - Stateful connections are appropriate

2. ✅ **LEP can learn from ACP's best practices**
   - Explicit initialization and capability negotiation
   - 4-kind permission model (once/always, allow/reject)
   - Notification support for real-time updates
   - Diff support for showing changes

3. ✅ **LEP has stricter security than ACP (appropriately)**
   - Mandatory human-in-the-loop for writes
   - Mandatory audit logging
   - Adapter certification required
   - Scope restrictions (prohibited applications)
   - This is correct because legacy systems are higher risk

4. ✅ **Interoperability is achievable**
   - LEP adapters can expose MCP interfaces
   - ACP agents can use LEP adapters
   - Unified permission framework is possible

5. ✅ **LEP is well-positioned in the agent protocol ecosystem**
   - Complements MCP (context/tools) and ACP (editors)
   - Fills a critical gap (legacy systems)
   - Can leverage existing ecosystems

### Next Steps for LEP

**Immediate (MVP Phase):**
1. Add `initialize` method with capability negotiation
2. Enhance `security/requestApproval` with 4-kind permission model
3. Document standard error codes

**Short-Term (Post-MVP):**
4. Add `legacy/update` notification for real-time progress
5. Add diff support for write operations
6. Add `legacy/cancel` notification

**Long-Term (Scaling Phase):**
7. Build LEP-MCP bridge for MCP ecosystem access
8. Propose unified permission framework to protocol communities
9. Collaborate with ACP and MCP on shared standards

---

**The agent protocol ecosystem is forming NOW. LEP has a unique opportunity to be a founding member and shape the future of agent-system communication.**

---

**Document Version:** 1.0  
**Last Updated:** February 5, 2026  
**Status:** Ready for Implementation
