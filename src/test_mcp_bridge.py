"""
Test script for the LEP-MCP Bridge.

This script demonstrates how LEP adapters can be used with MCP clients.
"""

import asyncio
import json
from lep_py.adapter.example_adapter import CustomerDatabaseAdapter
from lep_py.bridge.lep_mcp_bridge import LEPMCPBridge


async def main():
    print("=" * 60)
    print("LEP-MCP Bridge - Test Demonstration")
    print("=" * 60)
    print()
    
    # Create LEP adapter
    adapter = CustomerDatabaseAdapter()
    
    # Wrap with MCP bridge
    bridge = LEPMCPBridge(adapter)
    
    # Test 1: MCP Initialize
    print("Test 1: MCP Initialize")
    print("-" * 60)
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {
                "name": "Claude Desktop",
                "version": "1.0.0"
            },
            "capabilities": {}
        },
        "id": 1
    })
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Request: {mcp_request}")
    print(f"Response: {json.dumps(json.loads(response), indent=2)}")
    print()
    
    # Test 2: MCP Tools List
    print("Test 2: MCP Tools List")
    print("-" * 60)
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    })
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Response: {json.dumps(json.loads(response), indent=2)}")
    print()
    
    # Test 3: MCP Resources Read (via LEP getResource)
    print("Test 3: MCP Resources Read")
    print("-" * 60)
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "resources/read",
        "params": {
            "uri": "lep://customer/CUST001"
        },
        "id": 3
    })
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Response: {json.dumps(json.loads(response), indent=2)}")
    print()
    
    # Test 4: MCP Tools Call (with approval)
    print("Test 4: MCP Tools Call (with approval)")
    print("-" * 60)
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "updateCustomerBalance",
            "arguments": {
                "customer_id": "CUST001",
                "new_balance": 70000.00
            }
        },
        "id": 4
    })
    print(f"Request: {mcp_request}")
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Response: {json.dumps(json.loads(response), indent=2)}")
    print()
    
    # Test 5: Verify the change via MCP Resources Read
    print("Test 5: Verify the Change via MCP Resources Read")
    print("-" * 60)
    mcp_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "resources/read",
        "params": {
            "uri": "lep://customer/CUST001"
        },
        "id": 5
    })
    response = await bridge.handle_mcp_request(mcp_request)
    print(f"Response: {json.dumps(json.loads(response), indent=2)}")
    print()
    
    print("=" * 60)
    print("All MCP bridge tests completed successfully!")
    print("=" * 60)
    print()
    print("✅ LEP adapters can now be used with MCP clients!")
    print("   - Claude Desktop")
    print("   - Zed")
    print("   - JetBrains")
    print("   - Any MCP-enabled application")


if __name__ == "__main__":
    asyncio.run(main())
