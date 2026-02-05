# LegacyEvolve Protocol (LEP) v2.0 - Implementation Guide

**A step-by-step guide to building and deploying LEP adapters for legacy systems.**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Understanding the Architecture](#understanding-the-architecture)
4. [Building Your First Adapter](#building-your-first-adapter)
5. [Security Best Practices](#security-best-practices)
6. [Testing and Validation](#testing-and-validation)
7. [Deployment Considerations](#deployment-considerations)
8. [Advanced Topics](#advanced-topics)

---

## 1. Introduction

The LegacyEvolve Protocol (LEP) is designed to bridge the gap between modern AI agents and legacy enterprise systems. This guide will walk you through the process of building a production-ready LEP adapter for your specific legacy system.

### What You'll Learn

- How to extend the `BaseLEPAdapter` class
- How to implement read and write operations securely
- How to integrate with your approval workflow
- How to test and validate your adapter
- How to deploy your adapter in production

---

## 2. Prerequisites

### Technical Requirements

- **Python 3.11+**: The LEP SDK is built with Python 3.11
- **Async/Await Knowledge**: LEP uses async Python extensively
- **Legacy System Access**: You need programmatic access to your legacy system
- **JSON-RPC 2.0 Understanding**: Basic familiarity with JSON-RPC is helpful

### Knowledge Requirements

- Understanding of your legacy system's data model
- Knowledge of your organization's approval workflows
- Familiarity with security best practices

---

## 3. Understanding the Architecture

### The Four Layers

```
┌─────────────────────────────────────────────────────────┐
│                    AI Agent Host                        │
│              (Manus, Claude, Custom Agent)              │
└────────────────────┬────────────────────────────────────┘
                     │ JSON-RPC 2.0
                     │ over TLS 1.3+
┌────────────────────▼────────────────────────────────────┐
│                    LEP Client                           │
│         (Manages connection, handles responses)         │
└────────────────────┬────────────────────────────────────┘
                     │ JSON-RPC 2.0
                     │ (Local or Remote)
┌────────────────────▼────────────────────────────────────┐
│                    LEP Adapter                          │
│    (Your custom code - extends BaseLEPAdapter)          │
│  - Translates LEP methods to legacy system calls        │
│  - Enforces security (approval tokens, audit log)       │
│  - Manages session state                                │
└────────────────────┬────────────────────────────────────┘
                     │ Legacy Protocol
                     │ (COBOL, SQL, File I/O, etc.)
┌────────────────────▼────────────────────────────────────┐
│                  Legacy System                          │
│         (Mainframe, ERP, Custom Application)            │
└─────────────────────────────────────────────────────────┘
```

### Key Concepts

1. **Skills**: Functions your adapter exposes (e.g., "getCustomerInfo", "updateBalance")
2. **Resources**: Data entities your adapter can read (e.g., "customer", "account")
3. **Approval Tokens**: Cryptographic tokens that authorize write operations
4. **Audit Trail**: Immutable log of all operations

---

## 4. Building Your First Adapter

### Step 1: Create Your Adapter Class

```python
from lep_py.adapter.base_adapter import BaseLEPAdapter
from lep_py.models.protocol import Skill, OperationType, ApprovalState
from typing import Any, Dict, List

class MyLegacyAdapter(BaseLEPAdapter):
    def __init__(self):
        super().__init__(
            adapter_name="MyLegacyAdapter",
            adapter_version="1.0.0"
        )
        # Initialize your legacy system connection here
        self.legacy_connection = self._connect_to_legacy()
    
    def _connect_to_legacy(self):
        """Establish connection to your legacy system."""
        # Your connection logic here
        pass
```

### Step 2: Define Your Skills

Skills are the operations your adapter can perform. Each skill must specify:
- **Name**: Unique identifier
- **Description**: Human-readable explanation
- **Parameters**: Input schema
- **Returns**: Output schema
- **Operation Type**: `READ` or `WRITE`

```python
def get_skills(self) -> List[Skill]:
    return [
        # Read operation (no approval needed)
        Skill(
            name="getAccountBalance",
            description="Retrieve the current balance for an account",
            parameters={
                "account_id": {
                    "type": "string",
                    "required": True,
                    "description": "The account identifier"
                }
            },
            returns={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string"},
                    "balance": {"type": "number"},
                    "currency": {"type": "string"}
                }
            },
            operation_type=OperationType.READ
        ),
        
        # Write operation (requires approval)
        Skill(
            name="transferFunds",
            description="Transfer funds between two accounts",
            parameters={
                "from_account": {
                    "type": "string",
                    "required": True
                },
                "to_account": {
                    "type": "string",
                    "required": True
                },
                "amount": {
                    "type": "number",
                    "required": True,
                    "minimum": 0.01
                }
            },
            returns={
                "type": "object",
                "properties": {
                    "transaction_id": {"type": "string"},
                    "status": {"type": "string"}
                }
            },
            operation_type=OperationType.WRITE
        )
    ]
```

### Step 3: Implement Read Operations

Read operations don't require approval and are used for data retrieval.

```python
async def get_resource_impl(self, resource_name: str, parameters: Dict[str, Any]) -> Any:
    """Implement resource retrieval from your legacy system."""
    
    if resource_name == "account":
        account_id = parameters.get("account_id")
        
        # Query your legacy system
        result = await self._query_legacy_system(
            f"SELECT * FROM ACCOUNTS WHERE ID = '{account_id}'"
        )
        
        return {
            "account_id": result["ID"],
            "balance": result["BALANCE"],
            "currency": result["CURRENCY"],
            "status": result["STATUS"]
        }
    
    elif resource_name == "transaction":
        transaction_id = parameters.get("transaction_id")
        
        # Query your legacy system
        result = await self._query_legacy_system(
            f"SELECT * FROM TRANSACTIONS WHERE ID = '{transaction_id}'"
        )
        
        return {
            "transaction_id": result["ID"],
            "from_account": result["FROM_ACCT"],
            "to_account": result["TO_ACCT"],
            "amount": result["AMOUNT"],
            "timestamp": result["TIMESTAMP"]
        }
    
    else:
        raise Exception(f"Unknown resource: {resource_name}")

async def _query_legacy_system(self, query: str) -> Dict[str, Any]:
    """Execute a query on your legacy system."""
    # Your legacy system query logic here
    pass
```

### Step 4: Implement Write Operations

Write operations modify data and **MUST** be protected by approval tokens.

```python
async def call_skill_impl(self, skill_name: str, parameters: Dict[str, Any]) -> Any:
    """Implement skill execution on your legacy system."""
    
    if skill_name == "getAccountBalance":
        # This is actually a read operation, but can be called as a skill
        account_id = parameters.get("account_id")
        result = await self._query_legacy_system(
            f"SELECT BALANCE FROM ACCOUNTS WHERE ID = '{account_id}'"
        )
        return {"balance": result["BALANCE"]}
    
    elif skill_name == "transferFunds":
        from_account = parameters.get("from_account")
        to_account = parameters.get("to_account")
        amount = parameters.get("amount")
        
        # Execute the transfer on your legacy system
        transaction_id = await self._execute_legacy_transaction(
            from_account, to_account, amount
        )
        
        return {
            "transaction_id": transaction_id,
            "status": "completed"
        }
    
    else:
        raise Exception(f"Unknown skill: {skill_name}")

async def _execute_legacy_transaction(
    self, from_account: str, to_account: str, amount: float
) -> str:
    """Execute a transaction on your legacy system."""
    # Your legacy system transaction logic here
    # This should be atomic and include rollback capability
    pass
```

### Step 5: Implement Approval Workflow

This is where you integrate with your organization's approval process.

```python
async def request_human_approval(
    self,
    skill_name: str,
    parameters: Dict[str, Any],
    reason: str,
    estimated_impact: Dict[str, Any]
) -> ApprovalState:
    """Request approval from a human operator."""
    
    # Option 1: Console-based approval (for testing)
    print(f"\n{'='*60}")
    print(f"APPROVAL REQUEST")
    print(f"{'='*60}")
    print(f"Skill: {skill_name}")
    print(f"Parameters: {json.dumps(parameters, indent=2)}")
    print(f"Reason: {reason}")
    print(f"Impact: {json.dumps(estimated_impact, indent=2)}")
    print(f"{'='*60}")
    
    response = input("Approve? (yes/no): ").strip().lower()
    return ApprovalState.APPROVED if response == "yes" else ApprovalState.REJECTED
    
    # Option 2: Web-based approval UI
    # approval_id = await self.approval_service.create_request(
    #     skill_name, parameters, reason, estimated_impact
    # )
    # state = await self.approval_service.wait_for_decision(approval_id)
    # return state
    
    # Option 3: Slack/Teams notification
    # await self.notification_service.send_approval_request(
    #     channel="#approvals",
    #     skill_name=skill_name,
    #     parameters=parameters,
    #     reason=reason
    # )
    # state = await self.notification_service.wait_for_response()
    # return state
```

---

## 5. Security Best Practices

### 1. Input Validation

**Always validate and sanitize inputs before passing them to your legacy system.**

```python
def _validate_account_id(self, account_id: str) -> bool:
    """Validate account ID format."""
    # Example: Account IDs must be 10 digits
    if not account_id.isdigit() or len(account_id) != 10:
        raise ValueError(f"Invalid account ID format: {account_id}")
    return True

def _sanitize_sql_input(self, input_str: str) -> str:
    """Sanitize input to prevent SQL injection."""
    # Use parameterized queries instead of string concatenation
    # This is just an example - use your database library's parameterization
    return input_str.replace("'", "''")
```

### 2. Least Privilege

**Your adapter should only have the minimum necessary permissions on the legacy system.**

- Create a dedicated service account for the adapter
- Grant only the specific permissions needed for each skill
- Use read-only credentials for read operations

### 3. Secure Token Storage

**Never log or persist approval tokens.**

```python
# ❌ BAD: Logging approval tokens
logger.info(f"Executing skill with token: {approval_token}")

# ✅ GOOD: Log without exposing tokens
logger.info(f"Executing skill with token: {approval_token[:8]}...")
```

### 4. Audit Trail Integrity

**Ensure your audit trail cannot be tampered with.**

```python
def _log_audit_event(self, event_type: str, ...):
    """Log an event to the audit trail."""
    event = AuditEvent(...)
    
    # Option 1: Append-only file
    with open("/var/log/lep/audit.log", "a") as f:
        f.write(json.dumps(event.__dict__) + "\n")
    
    # Option 2: Centralized SIEM
    await self.siem_client.send_event(event)
    
    # Option 3: Blockchain (for maximum immutability)
    await self.blockchain_client.append_block(event)
```

---

## 6. Testing and Validation

### Unit Tests

Test each method in isolation:

```python
import pytest
from my_adapter import MyLegacyAdapter

@pytest.mark.asyncio
async def test_get_account_balance():
    adapter = MyLegacyAdapter()
    
    result = await adapter.get_resource_impl(
        "account",
        {"account_id": "1234567890"}
    )
    
    assert result["account_id"] == "1234567890"
    assert "balance" in result
    assert isinstance(result["balance"], (int, float))

@pytest.mark.asyncio
async def test_transfer_funds_requires_approval():
    adapter = MyLegacyAdapter()
    
    # Attempt to transfer without approval token should fail
    with pytest.raises(Exception, match="Invalid or expired approval token"):
        await adapter._handle_call_skill({
            "skill_name": "transferFunds",
            "parameters": {
                "from_account": "1234567890",
                "to_account": "0987654321",
                "amount": 100.00
            },
            "approval_token": "invalid_token"
        })
```

### Integration Tests

Test the full JSON-RPC flow:

```python
@pytest.mark.asyncio
async def test_full_approval_workflow():
    adapter = MyLegacyAdapter()
    
    # 1. Initialize
    init_response = await adapter.handle_request(json.dumps({
        "jsonrpc": "2.0",
        "method": "session/initialize",
        "params": {...},
        "id": 1
    }))
    assert "result" in json.loads(init_response)
    
    # 2. Request approval
    approval_response = await adapter.handle_request(json.dumps({
        "jsonrpc": "2.0",
        "method": "security/requestApproval",
        "params": {...},
        "id": 2
    }))
    approval_data = json.loads(approval_response)
    assert approval_data["result"]["state"] == "approved"
    token = approval_data["result"]["approval_token"]
    
    # 3. Execute with token
    exec_response = await adapter.handle_request(json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/callSkill",
        "params": {"approval_token": token, ...},
        "id": 3
    }))
    assert "result" in json.loads(exec_response)
```

---

## 7. Deployment Considerations

### Production Checklist

- [ ] **Security Audit**: Have your adapter reviewed by a security expert
- [ ] **Load Testing**: Ensure your adapter can handle expected traffic
- [ ] **Monitoring**: Set up alerts for errors and performance issues
- [ ] **Backup**: Ensure audit logs are backed up regularly
- [ ] **Documentation**: Document all skills and their parameters
- [ ] **Runbook**: Create an operations runbook for common issues

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Load Balancer                          │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐     ┌────────▼────────┐
│  LEP Adapter    │     │  LEP Adapter    │
│  Instance 1     │     │  Instance 2     │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   Legacy System       │
         │  (Connection Pool)    │
         └───────────────────────┘
```

---

## 8. Advanced Topics

### Custom Capabilities

Extend the base capabilities to advertise adapter-specific features:

```python
def __init__(self):
    super().__init__(...)
    self.capabilities.diff_support = True  # Enable diff support
    self.capabilities.cancellation = True  # Enable skill cancellation
```

### Progress Notifications

For long-running skills, send progress updates:

```python
async def call_skill_impl(self, skill_name: str, parameters: Dict[str, Any]) -> Any:
    if skill_name == "bulkImport":
        total_records = parameters.get("total_records")
        
        for i, record in enumerate(records):
            # Process record
            await self._import_record(record)
            
            # Send progress update
            if self.capabilities.notifications:
                await self._send_notification("legacy/update", {
                    "skill_name": skill_name,
                    "progress_percentage": (i + 1) / total_records * 100,
                    "status_message": f"Processed {i + 1} of {total_records} records"
                })
        
        return {"status": "completed", "records_imported": total_records}
```

### Skill Cancellation

Allow long-running skills to be cancelled:

```python
async def call_skill_impl(self, skill_name: str, parameters: Dict[str, Any]) -> Any:
    if skill_name == "longRunningJob":
        self.cancellation_requested = False
        
        for i in range(1000):
            if self.cancellation_requested:
                return {"status": "cancelled", "progress": i}
            
            # Do work
            await self._process_item(i)
        
        return {"status": "completed"}

async def _handle_cancel_notification(self, params: Dict[str, Any]):
    """Handle legacy/cancel notification."""
    skill_name = params.get("skill_name")
    if skill_name == "longRunningJob":
        self.cancellation_requested = True
```

---

## Conclusion

You now have a complete understanding of how to build, test, and deploy a production-ready LEP adapter. Remember:

1. **Security First**: Always validate inputs and enforce approval for writes
2. **Test Thoroughly**: Unit tests, integration tests, and security audits
3. **Monitor Everything**: Audit logs, performance metrics, error rates
4. **Document Well**: Your future self (and your team) will thank you

For more examples and community support, visit the [LegacyEvolve GitHub repository](https://github.com/creator35lwb-web/LegacyEvolve).

---

**Built with ❤️ for the public good**  
*Evolve, Don't Replace*
