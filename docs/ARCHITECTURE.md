# LegacyEvolve Protocol (LEP): Architecture Specification

**Version:** 0.1.0 (Draft)

This document provides the technical architecture and protocol specification for the LegacyEvolve Protocol (LEP). It is intended for developers who want to build LEP adapters or integrate LEP into AI agent hosts.

---

## 1. Core Philosophy: Evolve, Don't Replace

LEP is founded on the principle that not all legacy systems need to be replaced. Many are stable, reliable, and deeply embedded in business processes. LEP provides a pathway to **evolve** these systems by augmenting them with modern AI capabilities, rather than undertaking risky and expensive replacement projects.

---

## 2. Architectural Overview

LEP follows a client-server model, inspired by the Model Context Protocol (MCP). The key participants are:

-   **AI Agent Host:** The AI application that needs to interact with a legacy system.
-   **LEP Client:** A component within the AI Agent Host that implements the client-side of the LEP protocol.
-   **LEP Adapter:** A standalone service that acts as a bridge between the LEP Client and the legacy system. This is the core of the protocol.
-   **Legacy System:** The target system to be evolved.

<p align="center">
  <img src="assets/diagrams/LegacyEvolve-Architecture.png" alt="LegacyEvolve Protocol Architecture" width="800"/>
</p>

### 2.1. The LEP Adapter

The LEP Adapter is the heart of the protocol. It is responsible for:

1.  **Protocol Translation:** Translating JSON-RPC messages from the LEP Client into the native protocol of the legacy system (e.g., 3270 data streams for a mainframe, file I/O, proprietary API calls).
2.  **Skill Discovery:** Exposing the capabilities of the legacy system as a set of "skills" that the AI agent can discover and invoke.
3.  **State Management:** Maintaining session state with the legacy system.
4.  **Security Enforcement:** Implementing the security policies defined by the protocol (authentication, authorization, logging).
5.  **Sandboxing:** Executing operations in a safe, isolated environment.

---

## 3. Protocol Specification

LEP uses **JSON-RPC 2.0** over a secure transport (TLS 1.3) for all communication between the LEP Client and the LEP Adapter.

### 3.1. Core Primitives

LEP defines three core primitives, similar to MCP, but adapted for legacy systems:

1.  **`legacy/listSkills`**: Discovers the available skills (operations) that the adapter exposes for the legacy system.
    -   **Returns:** A list of skill definitions, including name, description, parameters, and whether it is a read or write operation.

2.  **`legacy/callSkill`**: Invokes a specific skill on the legacy system.
    -   **Parameters:** `skillName`, `parameters`, `humanApprovalToken` (for write operations).
    -   **Returns:** The result of the operation.

3.  **`legacy/getResource`**: Retrieves a data resource from the legacy system (e.g., a file, a screen scrape, a database record).
    -   **Parameters:** `resourceIdentifier`
    -   **Returns:** The requested resource.

### 3.2. Security Primitives (Mandatory)

Security is paramount in LEP. The following primitives are mandatory for all adapters:

1.  **`security/requestApproval`**: Requests human approval for a write operation.
    -   **Parameters:** `skillName`, `parameters`, `justification`
    -   **Returns:** A `humanApprovalToken` that can be used with `legacy/callSkill`.

2.  **`security/getAuditTrail`**: Retrieves the audit log for all operations.
    -   **Parameters:** `timeRange`, `filter`
    -   **Returns:** A list of audit log entries.

### 3.3. Example Workflow: Querying a Mainframe

1.  **AI Agent:** "I need to get the account balance for customer 12345."
2.  **LEP Client -> LEP Adapter:** `legacy/listSkills`
3.  **LEP Adapter -> LEP Client:** Returns `["getCustomerBalance", "updateCustomerAddress", ...]`
4.  **AI Agent:** Selects `getCustomerBalance` skill.
5.  **LEP Client -> LEP Adapter:** `legacy/callSkill("getCustomerBalance", { customerId: "12345" })`
6.  **LEP Adapter:**
    -   Connects to the mainframe via a 3270 terminal emulator.
    -   Navigates to the customer inquiry screen.
    -   Enters the customer ID.
    -   Scrapes the account balance from the screen.
    -   Disconnects from the mainframe.
7.  **LEP Adapter -> LEP Client:** Returns `{ "balance": 5432.10 }`
8.  **AI Agent:** "The account balance for customer 12345 is $5,432.10."

---

## 4. Building an LEP Adapter

Building an LEP Adapter requires expertise in both modern development practices and the target legacy system.

### 4.1. Adapter Development Kit (ADK)

A key part of the LegacyEvolve project will be to provide an **Adapter Development Kit (ADK)** in multiple languages (Python, Java, Go) that provides:

-   A boilerplate implementation of the LEP protocol.
-   Libraries for interacting with common legacy systems (e.g., 3270 emulators, file parsers).
-   A testing framework for validating adapter compliance.
-   Security best practices and reference implementations.

### 4.2. Certification Program

To ensure the security and reliability of the ecosystem, a **certification program** will be established for LEP adapters. Certified adapters will be verified to correctly implement all mandatory security controls.

---

## 5. Roadmap

### Phase 1: Protocol Definition (Current)
-   [x] VerifiMind-PEAS Trinity Validation
-   [x] Initial Architecture Design
-   [ ] Formal Protocol Specification (v1.0)
-   [ ] Open Community Review

### Phase 2: Reference Implementation
-   [ ] Develop Adapter Development Kit (ADK) for Python
-   [ ] Build a reference adapter for a common legacy system (e.g., a public-facing mainframe)
-   [ ] Build a reference LEP Client for a popular AI agent host

### Phase 3: Ecosystem Growth
-   [ ] Launch Adapter Certification Program
-   [ ] Partner with legacy system vendors
-   [ ] Foster a community of adapter developers

---

## 6. Conclusion

The LegacyEvolve Protocol represents a pragmatic and innovative approach to the legacy modernization problem. By creating a standardized bridge between AI and legacy systems, we can unlock the value trapped in decades of enterprise technology and accelerate the adoption of AI in the enterprise.
