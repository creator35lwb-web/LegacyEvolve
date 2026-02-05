"""
LegacyEvolve Protocol (LEP) v2.0 - Example Adapter

This is a simple example adapter that simulates a legacy "Customer Database" system.
It demonstrates how to implement the LEP protocol for a real legacy system.
"""

from typing import Any, Dict, List
from ..models.protocol import Skill, OperationType, ApprovalState
from .base_adapter import BaseLEPAdapter


class CustomerDatabaseAdapter(BaseLEPAdapter):
    """
    Example adapter for a simulated legacy customer database.
    
    This adapter provides:
    - Read operations: Query customer records
    - Write operations: Update customer information
    """

    def __init__(self):
        super().__init__(
            adapter_name="CustomerDatabaseAdapter",
            adapter_version="1.0.0"
        )
        
        # Simulated database
        self.customers = {
            "CUST001": {
                "id": "CUST001",
                "name": "Acme Corporation",
                "balance": 50000.00,
                "status": "active"
            },
            "CUST002": {
                "id": "CUST002",
                "name": "Globex Industries",
                "balance": 125000.00,
                "status": "active"
            },
            "CUST003": {
                "id": "CUST003",
                "name": "Initech LLC",
                "balance": 75000.00,
                "status": "suspended"
            }
        }

    def get_skills(self) -> List[Skill]:
        """Return the list of skills this adapter provides."""
        return [
            Skill(
                name="getCustomerInfo",
                description="Retrieve customer information by ID",
                parameters={
                    "customer_id": {"type": "string", "required": True}
                },
                returns={"type": "object"},
                operation_type=OperationType.READ
            ),
            Skill(
                name="updateCustomerBalance",
                description="Update a customer's account balance",
                parameters={
                    "customer_id": {"type": "string", "required": True},
                    "new_balance": {"type": "number", "required": True}
                },
                returns={"type": "object"},
                operation_type=OperationType.WRITE
            ),
            Skill(
                name="updateCustomerStatus",
                description="Update a customer's account status",
                parameters={
                    "customer_id": {"type": "string", "required": True},
                    "new_status": {"type": "string", "required": True, "enum": ["active", "suspended", "closed"]}
                },
                returns={"type": "object"},
                operation_type=OperationType.WRITE
            )
        ]

    async def get_resource_impl(self, resource_name: str, parameters: Dict[str, Any]) -> Any:
        """Implement resource retrieval from the legacy system."""
        if resource_name == "customer":
            customer_id = parameters.get("customer_id")
            if customer_id in self.customers:
                return self.customers[customer_id]
            else:
                raise Exception(f"Customer {customer_id} not found")
        else:
            raise Exception(f"Unknown resource: {resource_name}")

    async def call_skill_impl(self, skill_name: str, parameters: Dict[str, Any]) -> Any:
        """Implement skill execution on the legacy system."""
        if skill_name == "getCustomerInfo":
            customer_id = parameters.get("customer_id")
            if customer_id in self.customers:
                return self.customers[customer_id]
            else:
                raise Exception(f"Customer {customer_id} not found")
        
        elif skill_name == "updateCustomerBalance":
            customer_id = parameters.get("customer_id")
            new_balance = parameters.get("new_balance")
            
            if customer_id not in self.customers:
                raise Exception(f"Customer {customer_id} not found")
            
            old_balance = self.customers[customer_id]["balance"]
            self.customers[customer_id]["balance"] = new_balance
            
            return {
                "success": True,
                "customer_id": customer_id,
                "old_balance": old_balance,
                "new_balance": new_balance
            }
        
        elif skill_name == "updateCustomerStatus":
            customer_id = parameters.get("customer_id")
            new_status = parameters.get("new_status")
            
            if customer_id not in self.customers:
                raise Exception(f"Customer {customer_id} not found")
            
            old_status = self.customers[customer_id]["status"]
            self.customers[customer_id]["status"] = new_status
            
            return {
                "success": True,
                "customer_id": customer_id,
                "old_status": old_status,
                "new_status": new_status
            }
        
        else:
            raise Exception(f"Unknown skill: {skill_name}")

    async def request_human_approval(
        self,
        skill_name: str,
        parameters: Dict[str, Any],
        reason: str,
        estimated_impact: Dict[str, Any]
    ) -> ApprovalState:
        """
        Request approval from a human operator.
        
        In a production system, this would:
        1. Send a notification to the operator's UI
        2. Wait for their response
        3. Return the approval state
        
        For this example, we auto-approve all requests.
        """
        print(f"\n=== APPROVAL REQUEST ===")
        print(f"Skill: {skill_name}")
        print(f"Parameters: {parameters}")
        print(f"Reason: {reason}")
        print(f"Estimated Impact: {estimated_impact}")
        print(f"======================\n")
        
        # In production, this would be interactive
        # For now, auto-approve
        return ApprovalState.APPROVED
