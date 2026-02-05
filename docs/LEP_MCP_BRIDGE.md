# LEP-MCP Bridge Specification

**Enabling LegacyEvolve Protocol adapters to work with Model Context Protocol (MCP) clients.**

---

## Overview

The LEP-MCP Bridge is a translation layer that allows LEP adapters to be used as MCP servers, enabling seamless integration with the MCP ecosystem (Claude Desktop, Zed, JetBrains, etc.).

### Why This Matters

- **Ecosystem Integration**: LEP adapters can be used with any MCP-enabled application
- **Broader Adoption**: Developers can use familiar MCP tooling with LEP adapters
- **Interoperability**: Demonstrates LEP's commitment to open standards

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              MCP Client (Claude Desktop)                │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
                     │ (JSON-RPC 2.0)
┌────────────────────▼────────────────────────────────────┐
│                  LEP-MCP Bridge                         │
│  - Translates MCP methods to LEP methods               │
│  - Maps MCP primitives to LEP primitives               │
│  - Handles capability negotiation                      │
└────────────────────┬────────────────────────────────────┘
                     │ LEP Protocol
                     │ (JSON-RPC 2.0)
┌────────────────────▼────────────────────────────────────┐
│                  LEP Adapter                            │
│         (CustomerDatabase, Mainframe, etc.)             │
└────────────────────┬────────────────────────────────────┘
                     │ Legacy Protocol
┌────────────────────▼────────────────────────────────────┐
│                  Legacy System                          │
└─────────────────────────────────────────────────────────┘
```

---

## Protocol Mapping

### MCP → LEP Method Mapping

| MCP Method | LEP Method | Notes |
|------------|------------|-------|
| `initialize` | `session/initialize` | Direct mapping |
| `tools/list` | `legacy/listSkills` | MCP tools = LEP skills |
| `tools/call` | `security/requestApproval` + `legacy/callSkill` | Two-step process for writes |
| `resources/list` | Custom extension | LEP-specific |
| `resources/read` | `legacy/getResource` | Direct mapping |
| `prompts/list` | Not supported | LEP doesn't have prompts |
| `logging/setLevel` | Not supported | LEP uses audit trail |

### LEP → MCP Method Mapping

| LEP Method | MCP Method | Notes |
|------------|------------|-------|
| `session/initialize` | `initialize` | Direct mapping |
| `session/shutdown` | Connection close | MCP doesn't have explicit shutdown |
| `legacy/listSkills` | `tools/list` | LEP skills = MCP tools |
| `legacy/getResource` | `resources/read` | Direct mapping |
| `legacy/callSkill` | `tools/call` | Requires approval token |
| `security/requestApproval` | Custom notification | MCP doesn't have approval primitive |
| `security/getAuditTrail` | Custom notification | MCP doesn't have audit trail |

---

## Data Model Mapping

### LEP Skill → MCP Tool

**LEP Skill:**
```json
{
  "name": "updateCustomerBalance",
  "description": "Update a customer's account balance",
  "parameters": {
    "customer_id": {"type": "string", "required": true},
    "new_balance": {"type": "number", "required": true}
  },
  "returns": {"type": "object"},
  "operation_type": "write"
}
```

**MCP Tool:**
```json
{
  "name": "updateCustomerBalance",
  "description": "Update a customer's account balance (requires approval)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string"},
      "new_balance": {"type": "number"}
    },
    "required": ["customer_id", "new_balance"]
  }
}
```

### LEP Resource → MCP Resource

**LEP Resource:**
```json
{
  "resource_name": "customer",
  "parameters": {"customer_id": "CUST001"}
}
```

**MCP Resource:**
```json
{
  "uri": "lep://customer/CUST001",
  "name": "Customer CUST001",
  "mimeType": "application/json"
}
```

---

## Approval Flow Handling

MCP doesn't have a native approval primitive, so we handle it with notifications:

### Step 1: MCP Client Calls Tool

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "updateCustomerBalance",
    "arguments": {
      "customer_id": "CUST001",
      "new_balance": 60000.00
    }
  },
  "id": 1
}
```

### Step 2: Bridge Requests Approval from LEP Adapter

```json
{
  "jsonrpc": "2.0",
  "method": "security/requestApproval",
  "params": {
    "skill_name": "updateCustomerBalance",
    "parameters": {
      "customer_id": "CUST001",
      "new_balance": 60000.00
    },
    "reason": "MCP client requested operation",
    "estimated_impact": {
      "description": "Balance will change",
      "risk_level": "medium"
    }
  },
  "id": 1
}
```

### Step 3: LEP Adapter Returns Approval Token

```json
{
  "jsonrpc": "2.0",
  "result": {
    "state": "approved",
    "decision_id": "decision_1",
    "approval_token": "AaylJz7_rcWBTJ2gPLEhQHd5HtVFfeVFHswQBEZTGpA"
  },
  "id": 1
}
```

### Step 4: Bridge Calls LEP Skill with Token

```json
{
  "jsonrpc": "2.0",
  "method": "legacy/callSkill",
  "params": {
    "skill_name": "updateCustomerBalance",
    "parameters": {
      "customer_id": "CUST001",
      "new_balance": 60000.00
    },
    "approval_token": "AaylJz7_rcWBTJ2gPLEhQHd5HtVFfeVFHswQBEZTGpA"
  },
  "id": 2
}
```

### Step 5: Bridge Returns Result to MCP Client

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Balance updated successfully. Old balance: $50,000, New balance: $60,000"
      }
    ]
  },
  "id": 1
}
```

---

## Implementation

### Python Bridge Class

```python
from typing import Any, Dict, List
from lep_py.adapter.base_adapter import BaseLEPAdapter
from lep_py.core.jsonrpc import JSONRPCHandler

class LEPMCPBridge:
    """
    Bridge between LEP adapters and MCP clients.
    
    This class translates MCP protocol calls into LEP protocol calls,
    enabling LEP adapters to be used with MCP-enabled applications.
    """
    
    def __init__(self, lep_adapter: BaseLEPAdapter):
        self.lep_adapter = lep_adapter
        self.mcp_handler = JSONRPCHandler()
        self._register_mcp_methods()
    
    def _register_mcp_methods(self):
        """Register MCP protocol methods."""
        self.mcp_handler.register_method("initialize", self._handle_mcp_initialize)
        self.mcp_handler.register_method("tools/list", self._handle_mcp_tools_list)
        self.mcp_handler.register_method("tools/call", self._handle_mcp_tools_call)
        self.mcp_handler.register_method("resources/list", self._handle_mcp_resources_list)
        self.mcp_handler.register_method("resources/read", self._handle_mcp_resources_read)
    
    async def _handle_mcp_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request."""
        # Initialize LEP session
        lep_response = await self.lep_adapter._handle_initialize({
            "client_name": params.get("clientInfo", {}).get("name", "MCP Client"),
            "client_version": params.get("clientInfo", {}).get("version", "1.0.0"),
            "supported_lep_versions": ["2.0"],
            "client_capabilities": {
                "notifications": True,
                "diff_support": False,
                "cancellation": True
            }
        })
        
        # Return MCP-formatted response
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "logging": {}
            },
            "serverInfo": {
                "name": lep_response["server_name"],
                "version": lep_response["server_version"]
            }
        }
    
    async def _handle_mcp_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tools/list request."""
        # Get LEP skills
        lep_skills = await self.lep_adapter._handle_list_skills({})
        
        # Convert to MCP tools
        mcp_tools = []
        for skill in lep_skills:
            mcp_tool = {
                "name": skill["name"],
                "description": skill["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": skill["parameters"],
                    "required": [
                        k for k, v in skill["parameters"].items()
                        if v.get("required", False)
                    ]
                }
            }
            
            # Add approval warning for write operations
            if skill["operation_type"] == "write":
                mcp_tool["description"] += " (requires human approval)"
            
            mcp_tools.append(mcp_tool)
        
        return {"tools": mcp_tools}
    
    async def _handle_mcp_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        # Step 1: Request approval from LEP adapter
        approval_response = await self.lep_adapter._handle_request_approval({
            "skill_name": tool_name,
            "parameters": arguments,
            "reason": "MCP client requested operation",
            "estimated_impact": {
                "description": f"Executing {tool_name}",
                "risk_level": "medium"
            }
        })
        
        approval_token = approval_response.get("approval_token")
        
        if not approval_token:
            # Approval was rejected
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Operation rejected: {approval_response.get('state')}"
                    }
                ],
                "isError": True
            }
        
        # Step 2: Execute skill with approval token
        result = await self.lep_adapter._handle_call_skill({
            "skill_name": tool_name,
            "parameters": arguments,
            "approval_token": approval_token
        })
        
        # Step 3: Return MCP-formatted result
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }
    
    async def _handle_mcp_resources_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP resources/list request."""
        # LEP doesn't have a native resource list method
        # Return empty list for now
        return {"resources": []}
    
    async def _handle_mcp_resources_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP resources/read request."""
        uri = params.get("uri")
        
        # Parse LEP URI: lep://resource_name/param1/param2
        if not uri.startswith("lep://"):
            raise Exception(f"Invalid LEP URI: {uri}")
        
        parts = uri[6:].split("/")
        resource_name = parts[0]
        resource_params = {}
        
        # Parse parameters from URI
        if len(parts) > 1:
            resource_params["id"] = parts[1]
        
        # Call LEP getResource
        result = await self.lep_adapter._handle_get_resource({
            "resource_name": resource_name,
            "parameters": resource_params
        })
        
        # Return MCP-formatted result
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": "application/json",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }
    
    async def handle_mcp_request(self, request_data: str) -> str:
        """Handle an incoming MCP request."""
        return await self.mcp_handler.handle_request(request_data)
```

---

## Usage Example

### 1. Create LEP Adapter

```python
from lep_py.adapter.example_adapter import CustomerDatabaseAdapter

adapter = CustomerDatabaseAdapter()
```

### 2. Wrap with Bridge

```python
from lep_mcp_bridge import LEPMCPBridge

bridge = LEPMCPBridge(adapter)
```

### 3. Handle MCP Requests

```python
import asyncio
import json

async def main():
    # MCP client sends initialize request
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {
                "name": "Claude Desktop",
                "version": "1.0.0"
            }
        },
        "id": 1
    })
    
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Initialize response: {response}")
    
    # MCP client lists tools
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    })
    
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Tools list: {response}")
    
    # MCP client calls tool
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "updateCustomerBalance",
            "arguments": {
                "customer_id": "CUST001",
                "new_balance": 60000.00
            }
        },
        "id": 3
    })
    
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Tool call result: {response}")

asyncio.run(main())
```

---

## Claude Desktop Integration

### 1. Create MCP Server Configuration

Create `~/.config/claude/mcp_servers.json`:

```json
{
  "lep-customer-db": {
    "command": "python3",
    "args": ["/path/to/lep_mcp_server.py"],
    "env": {}
  }
}
```

### 2. Create MCP Server Script

Create `/path/to/lep_mcp_server.py`:

```python
#!/usr/bin/env python3
import asyncio
import sys
import json
from lep_py.adapter.example_adapter import CustomerDatabaseAdapter
from lep_mcp_bridge import LEPMCPBridge

async def main():
    # Create LEP adapter
    adapter = CustomerDatabaseAdapter()
    
    # Wrap with MCP bridge
    bridge = LEPMCPBridge(adapter)
    
    # Read MCP requests from stdin
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        
        # Handle request
        response = await bridge.handle_mcp_request(line)
        
        # Write response to stdout
        sys.stdout.write(response + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Restart Claude Desktop

Claude Desktop will now see your LEP adapter as an MCP server!

---

## Benefits

1. **Ecosystem Integration**: LEP adapters work with any MCP client
2. **Familiar Tooling**: Developers can use MCP tools they already know
3. **Broader Adoption**: Reduces friction for LEP adoption
4. **Interoperability**: Demonstrates commitment to open standards

---

## Future Enhancements

1. **Bidirectional Bridge**: Allow MCP servers to be used as LEP adapters
2. **Advanced Approval UI**: Integrate with MCP's notification system
3. **Resource Discovery**: Implement dynamic resource listing
4. **Streaming Support**: Enable streaming for long-running operations

---

**Built with ❤️ for the public good**  
*Evolve, Don't Replace*
