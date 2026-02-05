# LegacyEvolve Protocol (LEP) v2.0 - Python SDK

**The reference implementation of the LegacyEvolve Protocol in Python.**

---

## Overview

This directory contains the complete Python implementation of the LegacyEvolve Protocol (LEP) v2.0, including:

- **Core Protocol**: JSON-RPC 2.0 transport layer and data models
- **Base Adapter**: Abstract base class for building LEP adapters
- **Example Adapter**: A working example demonstrating the protocol
- **Test Suite**: Comprehensive tests proving the implementation works

## Project Structure

```
src/
├── lep_py/                    # Main LEP Python package
│   ├── core/                  # Core protocol implementation
│   │   └── jsonrpc.py        # JSON-RPC 2.0 handler
│   ├── models/                # Data models
│   │   └── protocol.py       # LEP protocol data structures
│   ├── adapter/               # Adapter implementations
│   │   ├── base_adapter.py   # Abstract base class
│   │   └── example_adapter.py # Example customer database adapter
│   ├── client/                # Client library (future)
│   └── utils/                 # Utility functions
└── test_adapter.py            # Test script
```

## Quick Start

### 1. Run the Example

```bash
cd src/
python3 test_adapter.py
```

This will run a complete demonstration of the LEP protocol, including:
- Session initialization
- Skill discovery
- Read operations
- Human-in-the-loop approval
- Write operations with approval tokens
- Audit trail retrieval

### 2. Build Your Own Adapter

To create your own LEP adapter for a legacy system:

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
    
    def get_skills(self) -> List[Skill]:
        """Define the skills your adapter provides."""
        return [
            Skill(
                name="myReadSkill",
                description="Read data from legacy system",
                parameters={"param1": {"type": "string", "required": True}},
                returns={"type": "object"},
                operation_type=OperationType.READ
            ),
            Skill(
                name="myWriteSkill",
                description="Write data to legacy system",
                parameters={"param1": {"type": "string", "required": True}},
                returns={"type": "object"},
                operation_type=OperationType.WRITE
            )
        ]
    
    async def get_resource_impl(self, resource_name: str, parameters: Dict[str, Any]) -> Any:
        """Implement how to read data from your legacy system."""
        # Your implementation here
        pass
    
    async def call_skill_impl(self, skill_name: str, parameters: Dict[str, Any]) -> Any:
        """Implement how to execute skills on your legacy system."""
        # Your implementation here
        pass
    
    async def request_human_approval(
        self,
        skill_name: str,
        parameters: Dict[str, Any],
        reason: str,
        estimated_impact: Dict[str, Any]
    ) -> ApprovalState:
        """Implement how to request approval from a human operator."""
        # In production, this would integrate with your approval UI
        # For testing, you can auto-approve:
        return ApprovalState.APPROVED
```

## Key Features

### 1. Security-First Design

- **Cryptographic Approval Tokens**: All write operations require a time-limited, cryptographically secure token
- **5-Minute Token Expiry**: Tokens automatically expire to prevent replay attacks
- **Exact Parameter Matching**: Tokens are bound to specific operations and parameters

### 2. Complete Auditability

- **Immutable Audit Trail**: Every operation is logged with timestamp, user, and result
- **Decision Tracking**: All approval decisions are linked to their execution
- **Full Transparency**: Audit trail can be retrieved at any time

### 3. Human-in-the-Loop

- **Mandatory Approval**: Write operations cannot proceed without human approval
- **Rich Context**: Approval requests include reason and estimated impact
- **Flexible UI Integration**: Approval mechanism can be integrated with any UI

### 4. Industry Standards

- **JSON-RPC 2.0**: Uses the industry-standard JSON-RPC 2.0 protocol
- **Standard Error Codes**: HTTP-style error codes for easy debugging
- **Capability Negotiation**: Client and server exchange capabilities during initialization

## Protocol Methods

### Session Management

- `session/initialize`: Initialize a new LEP session
- `session/shutdown`: Gracefully shut down the session

### Legacy System Operations

- `legacy/listSkills`: Discover available skills
- `legacy/getResource`: Read data (no approval needed)
- `legacy/callSkill`: Execute a skill (requires approval token)

### Security & Auditing

- `security/requestApproval`: Request human approval for a write operation
- `security/getAuditTrail`: Retrieve the audit trail

## Example: Complete Workflow

```python
import asyncio
import json
from lep_py.adapter.example_adapter import CustomerDatabaseAdapter

async def example_workflow():
    adapter = CustomerDatabaseAdapter()
    
    # 1. Initialize session
    init_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "session/initialize",
        "params": {
            "client_name": "My AI Agent",
            "client_version": "1.0.0",
            "supported_lep_versions": ["2.0"],
            "client_capabilities": {"notifications": True}
        },
        "id": 1
    })
    response = await adapter.handle_request(init_request)
    print(f"Initialized: {response}")
    
    # 2. List available skills
    list_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/listSkills",
        "params": {},
        "id": 2
    })
    response = await adapter.handle_request(list_request)
    print(f"Skills: {response}")
    
    # 3. Read data (no approval needed)
    read_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/getResource",
        "params": {
            "resource_name": "customer",
            "parameters": {"customer_id": "CUST001"}
        },
        "id": 3
    })
    response = await adapter.handle_request(read_request)
    print(f"Customer data: {response}")
    
    # 4. Request approval for write operation
    approval_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "security/requestApproval",
        "params": {
            "skill_name": "updateCustomerBalance",
            "parameters": {"customer_id": "CUST001", "new_balance": 60000.00},
            "reason": "Customer requested credit increase",
            "estimated_impact": {"description": "Balance will increase by $10,000"}
        },
        "id": 4
    })
    response = await adapter.handle_request(approval_request)
    response_data = json.loads(response)
    approval_token = response_data["result"]["approval_token"]
    print(f"Approval granted: {approval_token}")
    
    # 5. Execute write operation with approval token
    write_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/callSkill",
        "params": {
            "skill_name": "updateCustomerBalance",
            "parameters": {"customer_id": "CUST001", "new_balance": 60000.00},
            "approval_token": approval_token
        },
        "id": 5
    })
    response = await adapter.handle_request(write_request)
    print(f"Write result: {response}")
    
    # 6. Get audit trail
    audit_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "security/getAuditTrail",
        "params": {},
        "id": 6
    })
    response = await adapter.handle_request(audit_request)
    print(f"Audit trail: {response}")

asyncio.run(example_workflow())
```

## Next Steps

1. **Build Your Adapter**: Extend `BaseLEPAdapter` for your legacy system
2. **Integrate with AI**: Connect your adapter to an AI agent (Manus, Claude, etc.)
3. **Add UI**: Build an approval interface for human operators
4. **Deploy**: Run your adapter in production with proper security

## Contributing

This is an open-source Digital Public Good. Contributions are welcome!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

---

**Built with ❤️ for the public good**  
*Evolve, Don't Replace*
