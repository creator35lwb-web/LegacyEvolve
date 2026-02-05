# LegacyEvolve Protocol (LEP) Specification v2.0

**Version:** 2.0  
**Status:** DRAFT  
**Last Updated:** February 5, 2026  
**Author:** L (Project Founder, LegacyEvolve Protocol)

---

## 1. Introduction

This document defines version 2.0 of the LegacyEvolve Protocol (LEP), an open standard for connecting modern AI agents to legacy enterprise systems. This version incorporates best practices and design patterns from the broader agent protocol ecosystem, including the Agent Client Protocol (ACP) [1] and the Model Context Protocol (MCP) [2], to enhance security, interoperability, and developer experience.

Our mission is to **Evolve, Don't Replace**, by providing a secure, auditable, and standardized bridge to the valuable data and processes locked within legacy systems.

## 2. Core Concepts

-   **Transport:** All communication MUST use JSON-RPC 2.0 over a secure channel (TLS 1.3+).
-   **Stateful Connection:** The protocol is stateful. A session is established and maintained between the AI Agent Host and the LEP Adapter.
-   **Human-in-the-Loop:** All operations that modify data or state (`legacy/callSkill`) **MUST** be explicitly approved by a human operator.
-   **Immutable Audit Trail:** All requests, responses, and approvals **MUST** be logged in a verifiable, immutable audit trail.

## 3. Session Lifecycle

A LEP session follows a clear lifecycle: Initialization, Interaction, and Termination.

### 3.1. Initialization

The session is initiated by the client (AI Agent Host) sending an `initialize` request. This method allows the client and server (LEP Adapter) to negotiate capabilities.

**`session/initialize`**

-   **Direction:** Client -> Server
-   **Description:** Establishes a new session and exchanges capabilities.
-   **Parameters:**
    -   `client_name`: `string` - Name of the client software (e.g., "Manus AI").
    -   `client_version`: `string` - Version of the client software.
    -   `supported_lep_versions`: `string[]` - List of LEP versions the client supports.
    -   `client_capabilities`: `object` - Object describing client features (e.g., `{ "notifications": true }`).
-   **Returns:**
    -   `server_name`: `string` - Name of the LEP Adapter.
    -   `server_version`: `string` - Version of the adapter.
    -   `lep_version`: `string` - The LEP version selected for this session.
    -   `server_capabilities`: `object` - Object describing adapter features (e.g., `{ "diff_support": true }`).

### 3.2. Interaction

Once initialized, the client can interact with the legacy system using the methods defined in Section 4.

### 3.3. Termination

The session can be terminated by either party.

**`session/shutdown`**

-   **Direction:** Client -> Server
-   **Description:** Requests to gracefully shut down the session.
-   **Parameters:** None.
-   **Returns:** `null`.

**`session/exit`**

-   **Direction:** Server -> Client (Notification)
-   **Description:** Informs the client that the server is shutting down.
-   **Parameters:** None.

## 4. Protocol Methods

Methods are organized into namespaces: `legacy` for core operations and `security` for safety and auditing.

### 4.1. `legacy` Namespace

**`legacy/listSkills`**

-   **Description:** Lists all available skills (functions) the adapter exposes.
-   **Parameters:** None.
-   **Returns:** `Skill[]` - An array of Skill objects.
    -   `Skill`: `{ "name": string, "description": string, "parameters": object, "returns": object, "operation_type": "read" | "write" }`

**`legacy/getResource`**

-   **Description:** Retrieves a data resource from the legacy system (read-only).
-   **Parameters:**
    -   `resource_name`: `string` - The name of the resource to retrieve.
    -   `parameters`: `object` - Parameters to filter or identify the resource.
-   **Returns:** `object` - The requested data resource.

**`legacy/callSkill`**

-   **Description:** Executes a skill that may modify data or state (write operation).
-   **Parameters:**
    -   `skill_name`: `string` - The name of the skill to execute.
    -   `parameters`: `object` - The parameters for the skill.
    -   `approval_token`: `string` - A valid, non-expired token obtained from `security/requestApproval`.
-   **Returns:** `object` - The result of the skill execution.

### 4.2. `security` Namespace

**`security/requestApproval`**

-   **Description:** Requests human approval for a write operation. This is the core of the human-in-the-loop model.
-   **Parameters:**
    -   `skill_name`: `string` - The skill being requested.
    -   `parameters`: `object` - The parameters for the skill.
    -   `reason`: `string` - A human-readable explanation of why the operation is needed.
    -   `estimated_impact`: `object` - A description of the expected changes, potentially including a `diff`.
-   **Returns:** `ApprovalResponse`
    -   `ApprovalResponse`: `{ "state": "approved" | "rejected", "decision_id": string, "approval_token": string | null }`

**`security/getAuditTrail`**

-   **Description:** Retrieves the audit trail for the current session.
-   **Parameters:**
    -   `since_decision_id`: `string` (optional) - Retrieve logs since a specific decision.
-   **Returns:** `AuditEvent[]` - An array of audit events.

## 5. Notifications

LEP v2.0 introduces server-to-client notifications for real-time updates, inspired by ACP.

**`legacy/update`**

-   **Direction:** Server -> Client (Notification)
-   **Description:** Provides a progress update for a long-running skill.
-   **Parameters:**
    -   `skill_name`: `string`
    -   `progress_percentage`: `number`
    -   `status_message`: `string`

**`legacy/cancel`**

-   **Direction:** Client -> Server (Notification)
-   **Description:** Requests to cancel a long-running skill.
-   **Parameters:**
    -   `skill_name`: `string`

## 6. The Enhanced Permission Model

To improve user experience, the human approval UI (which is external to the protocol but invoked by `security/requestApproval`) **SHOULD** implement ACP's 4-kind permission model. The LEP Adapter, however, only receives the final `approved` or `rejected` state.

-   **UI Options:**
    1.  **Approve Once:** Grants a single-use `approval_token`.
    2.  **Approve Always:** Whitelists this specific `skill_name` with these exact `parameters` for the session.
    3.  **Reject Once:** Denies this specific request.
    4.  **Reject Always:** Blacklists this `skill_name` with these `parameters` for the session.

-   **Protocol-Level:** The adapter receives a standard `security/requestApproval` call. The client-side library or UI handles the "Always" logic, either by caching the `approval_token` or by auto-approving subsequent identical requests.

## 7. Error Handling

LEP v2.0 adopts a standardized error code system, similar to HTTP status codes.

| Code | Message | Meaning |
|---|---|---|
| -32700 | Parse error | Invalid JSON was received by the server. |
| -32600 | Invalid Request | The JSON sent is not a valid Request object. |
| -32601 | Method not found | The method does not exist / is not available. |
| -32602 | Invalid Params | Invalid method parameter(s). |
| -32603 | Internal error | Internal JSON-RPC error. |
| -32000 | Permission Denied | The requested operation was rejected by the user. |
| -32001 | Approval Expired | The provided `approval_token` has expired. |
| -32002 | Skill Execution Error | The skill failed to execute on the legacy system. |
| -32003 | Resource Not Found | The requested resource does not exist. |

## 8. References

[1] [Agent Client Protocol (ACP) Documentation](https://agentclientprotocol.com/)  
[2] [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/specification/2025-11-25)
