"""
Test script for the LegacyEvolve Protocol (LEP) v2.0 implementation.

This script demonstrates:
1. Initializing a session
2. Listing available skills
3. Reading data (no approval needed)
4. Requesting approval for a write operation
5. Executing a write operation with approval
6. Retrieving the audit trail
"""

import asyncio
import json
from lep_py.adapter.example_adapter import CustomerDatabaseAdapter


async def main():
    print("=" * 60)
    print("LegacyEvolve Protocol (LEP) v2.0 - Test Demonstration")
    print("=" * 60)
    print()
    
    # Create adapter instance
    adapter = CustomerDatabaseAdapter()
    
    # Test 1: Initialize session
    print("Test 1: Initialize Session")
    print("-" * 60)
    init_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "session/initialize",
        "params": {
            "client_name": "Test Client",
            "client_version": "1.0.0",
            "supported_lep_versions": ["2.0"],
            "client_capabilities": {
                "notifications": True,
                "diff_support": False,
                "cancellation": True
            }
        },
        "id": 1
    })
    response = await adapter.handle_request(init_request)
    print(f"Request: {init_request}")
    print(f"Response: {response}")
    print()
    
    # Test 2: List available skills
    print("Test 2: List Available Skills")
    print("-" * 60)
    list_skills_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/listSkills",
        "params": {},
        "id": 2
    })
    response = await adapter.handle_request(list_skills_request)
    print(f"Response: {response}")
    print()
    
    # Test 3: Get customer info (read operation - no approval needed)
    print("Test 3: Get Customer Info (Read Operation)")
    print("-" * 60)
    get_resource_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/getResource",
        "params": {
            "resource_name": "customer",
            "parameters": {"customer_id": "CUST001"}
        },
        "id": 3
    })
    response = await adapter.handle_request(get_resource_request)
    print(f"Response: {response}")
    print()
    
    # Test 4: Request approval for balance update
    print("Test 4: Request Approval for Balance Update")
    print("-" * 60)
    approval_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "security/requestApproval",
        "params": {
            "skill_name": "updateCustomerBalance",
            "parameters": {
                "customer_id": "CUST001",
                "new_balance": 60000.00
            },
            "reason": "Customer requested credit increase",
            "estimated_impact": {
                "description": "Balance will increase from $50,000 to $60,000",
                "risk_level": "medium"
            }
        },
        "id": 4
    })
    response = await adapter.handle_request(approval_request)
    response_data = json.loads(response)
    approval_token = response_data["result"]["approval_token"]
    print(f"Response: {response}")
    print(f"Approval Token: {approval_token}")
    print()
    
    # Test 5: Execute the approved skill
    print("Test 5: Execute Approved Skill")
    print("-" * 60)
    call_skill_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/callSkill",
        "params": {
            "skill_name": "updateCustomerBalance",
            "parameters": {
                "customer_id": "CUST001",
                "new_balance": 60000.00
            },
            "approval_token": approval_token
        },
        "id": 5
    })
    response = await adapter.handle_request(call_skill_request)
    print(f"Response: {response}")
    print()
    
    # Test 6: Verify the change by reading again
    print("Test 6: Verify the Change")
    print("-" * 60)
    verify_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "legacy/getResource",
        "params": {
            "resource_name": "customer",
            "parameters": {"customer_id": "CUST001"}
        },
        "id": 6
    })
    response = await adapter.handle_request(verify_request)
    print(f"Response: {response}")
    print()
    
    # Test 7: Get audit trail
    print("Test 7: Get Audit Trail")
    print("-" * 60)
    audit_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "security/getAuditTrail",
        "params": {},
        "id": 7
    })
    response = await adapter.handle_request(audit_request)
    print(f"Response: {json.dumps(json.loads(response), indent=2)}")
    print()
    
    # Test 8: Shutdown session
    print("Test 8: Shutdown Session")
    print("-" * 60)
    shutdown_request = json.dumps({
        "jsonrpc": "2.0",
        "method": "session/shutdown",
        "params": {},
        "id": 8
    })
    response = await adapter.handle_request(shutdown_request)
    print(f"Response: {response}")
    print()
    
    print("=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
