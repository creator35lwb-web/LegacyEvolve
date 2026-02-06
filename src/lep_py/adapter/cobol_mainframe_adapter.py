"""
COBOL Mainframe Adapter for LegacyEvolve Protocol (LEP)
Production-grade reference implementation

This adapter demonstrates how to integrate a COBOL mainframe system
with modern AI agents using the LegacyEvolve Protocol.

Author: L (GODEL)
Date: February 6, 2026
License: MIT
"""

import hashlib
import json
import logging
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from dataclasses import dataclass
from typing import Any

from ..core.jsonrpc import JSONRPCRequest, JSONRPCResponse
from .base_adapter import BaseLEPAdapter as BaseAdapter

# Define data structures
@dataclass
class SkillParameter:
    name: str
    type: str
    description: str
    required: bool

@dataclass
class Skill:
    name: str
    description: str
    parameters: List[SkillParameter]
    returns: Dict[str, Any]
    requires_approval: bool

@dataclass
class Resource:
    uri: str
    name: str
    description: str
    mime_type: str

@dataclass
class ApprovalRequest:
    approval_id: str
    skill_name: str
    parameters: Dict[str, Any]
    rationale: str
    expires_at: str

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class COBOLMainframeAdapter(BaseAdapter):
    """
    Production-grade adapter for COBOL mainframe systems.
    
    This adapter provides secure, auditable access to a COBOL mainframe
    through the LegacyEvolve Protocol, with human-in-the-loop approval
    for all write operations.
    
    Features:
    - Customer account management (read/update)
    - Transaction processing (deposits, withdrawals, transfers)
    - Batch job submission
    - Report generation
    - Comprehensive audit logging
    """
    
    def __init__(self, mainframe_host: str, mainframe_port: int, 
                 connection_string: str):
        """
        Initialize the COBOL mainframe adapter.
        
        Args:
            mainframe_host: Hostname of the mainframe
            mainframe_port: Port number for mainframe connection
            connection_string: Connection string for mainframe access
        """
        super().__init__(
            adapter_id="cobol-mainframe-adapter-001",
            adapter_name="COBOL Mainframe Adapter",
            adapter_version="1.0.0",
            system_name="IBM z/OS COBOL Banking System",
            system_version="5.2"
        )
        
        self.mainframe_host = mainframe_host
        self.mainframe_port = mainframe_port
        self.connection_string = connection_string
        
        # Simulated mainframe data (in production, this would connect to real mainframe)
        self.accounts = {
            "ACC001": {"name": "Alice Johnson", "balance": 50000.00, "status": "active"},
            "ACC002": {"name": "Bob Smith", "balance": 75000.00, "status": "active"},
            "ACC003": {"name": "Carol Williams", "balance": 120000.00, "status": "active"},
        }
        
        self.transactions = []
        
        logger.info(f"COBOL Mainframe Adapter initialized: {mainframe_host}:{mainframe_port}")
    
    def get_skills(self) -> List[Skill]:
        """
        Return the list of skills (operations) supported by this adapter.
        """
        return [
            Skill(
                name="getAccountInfo",
                description="Retrieve account information for a customer",
                parameters=[
                    SkillParameter(
                        name="account_id",
                        type="string",
                        description="Customer account ID (e.g., ACC001)",
                        required=True
                    )
                ],
                returns={
                    "type": "object",
                    "description": "Account information including name, balance, and status"
                },
                requires_approval=False
            ),
            Skill(
                name="updateAccountBalance",
                description="Update customer account balance (requires approval)",
                parameters=[
                    SkillParameter(
                        name="account_id",
                        type="string",
                        description="Customer account ID",
                        required=True
                    ),
                    SkillParameter(
                        name="amount",
                        type="number",
                        description="Amount to add (positive) or subtract (negative)",
                        required=True
                    ),
                    SkillParameter(
                        name="reason",
                        type="string",
                        description="Reason for balance update",
                        required=True
                    )
                ],
                returns={
                    "type": "object",
                    "description": "Updated account information"
                },
                requires_approval=True
            ),
            Skill(
                name="transferFunds",
                description="Transfer funds between accounts (requires approval)",
                parameters=[
                    SkillParameter(
                        name="from_account",
                        type="string",
                        description="Source account ID",
                        required=True
                    ),
                    SkillParameter(
                        name="to_account",
                        type="string",
                        description="Destination account ID",
                        required=True
                    ),
                    SkillParameter(
                        name="amount",
                        type="number",
                        description="Amount to transfer",
                        required=True
                    )
                ],
                returns={
                    "type": "object",
                    "description": "Transfer confirmation with transaction ID"
                },
                requires_approval=True
            ),
            Skill(
                name="generateAccountReport",
                description="Generate account activity report",
                parameters=[
                    SkillParameter(
                        name="account_id",
                        type="string",
                        description="Customer account ID",
                        required=True
                    ),
                    SkillParameter(
                        name="start_date",
                        type="string",
                        description="Report start date (YYYY-MM-DD)",
                        required=False
                    ),
                    SkillParameter(
                        name="end_date",
                        type="string",
                        description="Report end date (YYYY-MM-DD)",
                        required=False
                    )
                ],
                returns={
                    "type": "string",
                    "description": "Report content in text format"
                },
                requires_approval=False
            )
        ]
    
    def get_resources(self) -> List[Resource]:
        """
        Return the list of resources (data) accessible through this adapter.
        """
        return [
            Resource(
                uri="cobol://accounts",
                name="Customer Accounts",
                description="List of all customer accounts",
                mime_type="application/json"
            ),
            Resource(
                uri="cobol://transactions",
                name="Transaction History",
                description="Historical transaction records",
                mime_type="application/json"
            )
        ]
    
    def execute_skill(self, skill_name: str, parameters: Dict, 
                     approval_token: Optional[str] = None) -> Dict:
        """
        Execute a skill (operation) on the mainframe.
        
        Args:
            skill_name: Name of the skill to execute
            parameters: Skill parameters
            approval_token: Approval token (required for write operations)
        
        Returns:
            Skill execution result
        """
        # Find the skill
        skill = next((s for s in self.get_skills() if s.name == skill_name), None)
        if not skill:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        # Check if approval is required
        if skill.requires_approval:
            if not approval_token:
                raise ValueError(f"Skill '{skill_name}' requires approval token")
            
            # Verify approval token
            if not self.verify_approval_token(approval_token):
                raise ValueError("Invalid or expired approval token")
        
        # Execute the skill
        if skill_name == "getAccountInfo":
            return self._get_account_info(parameters["account_id"])
        
        elif skill_name == "updateAccountBalance":
            return self._update_account_balance(
                parameters["account_id"],
                parameters["amount"],
                parameters["reason"],
                approval_token
            )
        
        elif skill_name == "transferFunds":
            return self._transfer_funds(
                parameters["from_account"],
                parameters["to_account"],
                parameters["amount"],
                approval_token
            )
        
        elif skill_name == "generateAccountReport":
            return self._generate_account_report(
                parameters["account_id"],
                parameters.get("start_date"),
                parameters.get("end_date")
            )
        
        else:
            raise ValueError(f"Skill execution not implemented: {skill_name}")
    
    def read_resource(self, uri: str) -> str:
        """
        Read a resource (data) from the mainframe.
        
        Args:
            uri: Resource URI (e.g., "cobol://accounts")
        
        Returns:
            Resource content as string
        """
        if uri == "cobol://accounts":
            return json.dumps(self.accounts, indent=2)
        
        elif uri == "cobol://transactions":
            return json.dumps(self.transactions, indent=2)
        
        else:
            raise ValueError(f"Unknown resource: {uri}")
    
    # Private methods for skill implementation
    
    def _get_account_info(self, account_id: str) -> Dict:
        """Get account information."""
        if account_id not in self.accounts:
            raise ValueError(f"Account not found: {account_id}")
        
        account = self.accounts[account_id]
        
        # Log audit entry
        self.add_audit_entry(
            action="read",
            resource=f"account:{account_id}",
            details={"operation": "getAccountInfo"}
        )
        
        return {
            "account_id": account_id,
            **account
        }
    
    def _update_account_balance(self, account_id: str, amount: float, 
                               reason: str, approval_token: str) -> Dict:
        """Update account balance."""
        if account_id not in self.accounts:
            raise ValueError(f"Account not found: {account_id}")
        
        account = self.accounts[account_id]
        old_balance = account["balance"]
        new_balance = old_balance + amount
        
        if new_balance < 0:
            raise ValueError("Insufficient funds")
        
        # Update balance
        account["balance"] = new_balance
        
        # Record transaction
        transaction = {
            "transaction_id": f"TXN{len(self.transactions) + 1:06d}",
            "timestamp": datetime.utcnow().isoformat(),
            "account_id": account_id,
            "type": "balance_update",
            "amount": amount,
            "old_balance": old_balance,
            "new_balance": new_balance,
            "reason": reason,
            "approval_token": approval_token
        }
        self.transactions.append(transaction)
        
        # Log audit entry
        self.add_audit_entry(
            action="write",
            resource=f"account:{account_id}",
            details={
                "operation": "updateAccountBalance",
                "amount": amount,
                "reason": reason,
                "transaction_id": transaction["transaction_id"]
            },
            approval_token=approval_token
        )
        
        logger.info(f"Updated account {account_id}: {old_balance} -> {new_balance}")
        
        return {
            "success": True,
            "transaction": transaction,
            "account": self._get_account_info(account_id)
        }
    
    def _transfer_funds(self, from_account: str, to_account: str, 
                       amount: float, approval_token: str) -> Dict:
        """Transfer funds between accounts."""
        if from_account not in self.accounts:
            raise ValueError(f"Source account not found: {from_account}")
        if to_account not in self.accounts:
            raise ValueError(f"Destination account not found: {to_account}")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        
        # Check sufficient funds
        if self.accounts[from_account]["balance"] < amount:
            raise ValueError("Insufficient funds in source account")
        
        # Perform transfer
        self.accounts[from_account]["balance"] -= amount
        self.accounts[to_account]["balance"] += amount
        
        # Record transaction
        transaction = {
            "transaction_id": f"TXN{len(self.transactions) + 1:06d}",
            "timestamp": datetime.utcnow().isoformat(),
            "type": "transfer",
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "approval_token": approval_token
        }
        self.transactions.append(transaction)
        
        # Log audit entry
        self.add_audit_entry(
            action="write",
            resource=f"accounts:{from_account},{to_account}",
            details={
                "operation": "transferFunds",
                "from": from_account,
                "to": to_account,
                "amount": amount,
                "transaction_id": transaction["transaction_id"]
            },
            approval_token=approval_token
        )
        
        logger.info(f"Transferred ${amount} from {from_account} to {to_account}")
        
        return {
            "success": True,
            "transaction": transaction,
            "from_account": self._get_account_info(from_account),
            "to_account": self._get_account_info(to_account)
        }
    
    def _generate_account_report(self, account_id: str, 
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None) -> str:
        """Generate account activity report."""
        if account_id not in self.accounts:
            raise ValueError(f"Account not found: {account_id}")
        
        account = self.accounts[account_id]
        
        # Filter transactions
        account_transactions = [
            t for t in self.transactions
            if t.get("account_id") == account_id or
               t.get("from_account") == account_id or
               t.get("to_account") == account_id
        ]
        
        # Generate report
        report = f"""
COBOL MAINFRAME BANKING SYSTEM
Account Activity Report
Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}

Account ID: {account_id}
Account Holder: {account["name"]}
Current Balance: ${account["balance"]:,.2f}
Status: {account["status"]}

Transaction History:
{"=" * 80}
"""
        
        if account_transactions:
            for txn in account_transactions:
                report += f"\n{txn['timestamp']} | {txn['type'].upper()} | "
                if txn['type'] == 'transfer':
                    direction = "OUT" if txn['from_account'] == account_id else "IN"
                    report += f"{direction} ${txn['amount']:,.2f}"
                else:
                    report += f"${txn['amount']:+,.2f}"
                report += f" | TXN: {txn['transaction_id']}"
        else:
            report += "\nNo transactions found for this account."
        
        report += f"\n\n{'=' * 80}\nEnd of Report\n"
        
        # Log audit entry
        self.add_audit_entry(
            action="read",
            resource=f"account:{account_id}",
            details={"operation": "generateAccountReport"}
        )
        
        return report


# Example usage
if __name__ == "__main__":
    # Initialize adapter
    adapter = COBOLMainframeAdapter(
        mainframe_host="mainframe.example.com",
        mainframe_port=23,
        connection_string="USER=ADMIN;PASSWORD=***"
    )
    
    print("=== COBOL Mainframe Adapter Demo ===\n")
    
    # 1. Read account info (no approval needed)
    print("1. Reading account info...")
    account_info = adapter.execute_skill("getAccountInfo", {"account_id": "ACC001"})
    print(f"   Account: {account_info['name']}, Balance: ${account_info['balance']:,.2f}\n")
    
    # 2. Request approval for balance update
    print("2. Requesting approval for balance update...")
    approval_request = adapter.request_approval(
        skill_name="updateAccountBalance",
        parameters={
            "account_id": "ACC001",
            "amount": 10000.00,
            "reason": "Bonus payment"
        },
        rationale="Adding annual bonus to employee account"
    )
    print(f"   Approval requested: {approval_request.approval_id}")
    print(f"   Waiting for human approval...\n")
    
    # 3. Simulate human approval
    print("3. Simulating human approval...")
    approval_token = adapter.approve(approval_request.approval_id)
    print(f"   Approval granted: {approval_token[:20]}...\n")
    
    # 4. Execute balance update with approval token
    print("4. Executing balance update...")
    result = adapter.execute_skill(
        "updateAccountBalance",
        {
            "account_id": "ACC001",
            "amount": 10000.00,
            "reason": "Bonus payment"
        },
        approval_token=approval_token
    )
    print(f"   Transaction ID: {result['transaction']['transaction_id']}")
    print(f"   New balance: ${result['account']['balance']:,.2f}\n")
    
    # 5. Generate report
    print("5. Generating account report...")
    report = adapter.execute_skill("generateAccountReport", {"account_id": "ACC001"})
    print(report)
    
    # 6. Show audit trail
    print("\n6. Audit Trail:")
    audit_trail = adapter.get_audit_trail()
    for entry in audit_trail:
        print(f"   [{entry.timestamp}] {entry.action.upper()} - {entry.resource}")
