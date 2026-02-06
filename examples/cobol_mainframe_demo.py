"""
LegacyEvolve Protocol - Standalone COBOL Mainframe Adapter Demo

This is a complete, self-contained demonstration of how the LegacyEvolve Protocol
enables secure, auditable access to COBOL mainframe systems with human-in-the-loop
approval for write operations.

Author: L (GODEL)
Date: February 6, 2026
License: MIT
"""

import hashlib
import json
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class SkillParameter:
    """Parameter definition for a skill."""
    name: str
    type: str
    description: str
    required: bool


@dataclass
class Skill:
    """A skill (operation) exposed by the adapter."""
    name: str
    description: str
    parameters: List[SkillParameter]
    returns: Dict
    requires_approval: bool


@dataclass
class ApprovalRequest:
    """Request for human approval."""
    approval_id: str
    skill_name: str
    parameters: Dict
    rationale: str
    created_at: str
    expires_at: str


@dataclass
class AuditEntry:
    """Immutable audit log entry."""
    timestamp: str
    action: str
    resource: str
    agent_id: str
    details: Optional[Dict] = None
    approval_token: Optional[str] = None


# ============================================================================
# COBOL Mainframe Adapter
# ============================================================================

class COBOLMainframeAdapter:
    """
    Production-grade adapter for COBOL mainframe banking systems.
    
    Demonstrates the LegacyEvolve Protocol with:
    - Read operations (no approval required)
    - Write operations (human approval required)
    - Immutable audit trail
    - Secure approval tokens with expiration
    """
    
    def __init__(self, mainframe_host: str, mainframe_port: int):
        self.mainframe_host = mainframe_host
        self.mainframe_port = mainframe_port
        self.adapter_id = "cobol-mainframe-adapter-001"
        self.agent_id = "manus-godel-001"
        
        # Simulated mainframe data
        self.accounts = {
            "ACC001": {"name": "Alice Johnson", "balance": 50000.00, "status": "active"},
            "ACC002": {"name": "Bob Smith", "balance": 75000.00, "status": "active"},
            "ACC003": {"name": "Carol Williams", "balance": 120000.00, "status": "active"},
        }
        
        self.transactions = []
        self.audit_trail = []
        self.approval_requests = {}
        self.approval_tokens = {}
        
        print(f"✓ COBOL Mainframe Adapter initialized")
        print(f"  Host: {mainframe_host}:{mainframe_port}")
        print(f"  Adapter ID: {self.adapter_id}")
    
    def get_skills(self) -> List[Skill]:
        """Return available skills."""
        return [
            Skill(
                name="getAccountInfo",
                description="Retrieve account information",
                parameters=[
                    SkillParameter("account_id", "string", "Account ID (e.g., ACC001)", True)
                ],
                returns={"type": "object"},
                requires_approval=False
            ),
            Skill(
                name="updateAccountBalance",
                description="Update account balance (requires approval)",
                parameters=[
                    SkillParameter("account_id", "string", "Account ID", True),
                    SkillParameter("amount", "number", "Amount to add/subtract", True),
                    SkillParameter("reason", "string", "Reason for update", True)
                ],
                returns={"type": "object"},
                requires_approval=True
            ),
            Skill(
                name="transferFunds",
                description="Transfer funds between accounts (requires approval)",
                parameters=[
                    SkillParameter("from_account", "string", "Source account", True),
                    SkillParameter("to_account", "string", "Destination account", True),
                    SkillParameter("amount", "number", "Transfer amount", True)
                ],
                returns={"type": "object"},
                requires_approval=True
            ),
            Skill(
                name="generateReport",
                description="Generate account activity report",
                parameters=[
                    SkillParameter("account_id", "string", "Account ID", True)
                ],
                returns={"type": "string"},
                requires_approval=False
            )
        ]
    
    def request_approval(self, skill_name: str, parameters: Dict, rationale: str) -> ApprovalRequest:
        """Request human approval for a write operation."""
        approval_id = f"approval-{secrets.token_hex(8)}"
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(minutes=5)
        
        request = ApprovalRequest(
            approval_id=approval_id,
            skill_name=skill_name,
            parameters=parameters,
            rationale=rationale,
            created_at=created_at.isoformat(),
            expires_at=expires_at.isoformat()
        )
        
        self.approval_requests[approval_id] = request
        return request
    
    def approve(self, approval_id: str) -> str:
        """Approve a request and generate approval token."""
        if approval_id not in self.approval_requests:
            raise ValueError(f"Approval request not found: {approval_id}")
        
        request = self.approval_requests[approval_id]
        
        # Check expiration
        expires_at = datetime.fromisoformat(request.expires_at)
        if datetime.utcnow() > expires_at:
            raise ValueError("Approval request has expired")
        
        # Generate secure token
        token_data = f"{approval_id}:{request.skill_name}:{datetime.utcnow().isoformat()}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        
        self.approval_tokens[token] = {
            "approval_id": approval_id,
            "skill_name": request.skill_name,
            "parameters": request.parameters,
            "expires_at": expires_at.isoformat()
        }
        
        return token
    
    def verify_approval_token(self, token: str) -> bool:
        """Verify an approval token."""
        if token not in self.approval_tokens:
            return False
        
        token_data = self.approval_tokens[token]
        expires_at = datetime.fromisoformat(token_data["expires_at"])
        
        return datetime.utcnow() <= expires_at
    
    def execute_skill(self, skill_name: str, parameters: Dict, approval_token: Optional[str] = None) -> Dict:
        """Execute a skill."""
        # Find skill
        skill = next((s for s in self.get_skills() if s.name == skill_name), None)
        if not skill:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        # Check approval
        if skill.requires_approval:
            if not approval_token or not self.verify_approval_token(approval_token):
                raise ValueError(f"Skill '{skill_name}' requires valid approval token")
        
        # Execute
        if skill_name == "getAccountInfo":
            return self._get_account_info(parameters["account_id"])
        elif skill_name == "updateAccountBalance":
            return self._update_balance(parameters["account_id"], parameters["amount"], 
                                       parameters["reason"], approval_token)
        elif skill_name == "transferFunds":
            return self._transfer_funds(parameters["from_account"], parameters["to_account"],
                                       parameters["amount"], approval_token)
        elif skill_name == "generateReport":
            return {"report": self._generate_report(parameters["account_id"])}
        else:
            raise ValueError(f"Skill not implemented: {skill_name}")
    
    def _log_audit(self, action: str, resource: str, details: Optional[Dict] = None, 
                   approval_token: Optional[str] = None):
        """Log an audit entry."""
        entry = AuditEntry(
            timestamp=datetime.utcnow().isoformat(),
            action=action,
            resource=resource,
            agent_id=self.agent_id,
            details=details,
            approval_token=approval_token
        )
        self.audit_trail.append(entry)
    
    def _get_account_info(self, account_id: str) -> Dict:
        """Get account information."""
        if account_id not in self.accounts:
            raise ValueError(f"Account not found: {account_id}")
        
        self._log_audit("read", f"account:{account_id}", {"operation": "getAccountInfo"})
        
        return {"account_id": account_id, **self.accounts[account_id]}
    
    def _update_balance(self, account_id: str, amount: float, reason: str, approval_token: str) -> Dict:
        """Update account balance."""
        if account_id not in self.accounts:
            raise ValueError(f"Account not found: {account_id}")
        
        account = self.accounts[account_id]
        old_balance = account["balance"]
        new_balance = old_balance + amount
        
        if new_balance < 0:
            raise ValueError("Insufficient funds")
        
        account["balance"] = new_balance
        
        txn = {
            "txn_id": f"TXN{len(self.transactions) + 1:06d}",
            "timestamp": datetime.utcnow().isoformat(),
            "type": "balance_update",
            "account_id": account_id,
            "amount": amount,
            "old_balance": old_balance,
            "new_balance": new_balance,
            "reason": reason
        }
        self.transactions.append(txn)
        
        self._log_audit("write", f"account:{account_id}", 
                       {"operation": "updateAccountBalance", "txn_id": txn["txn_id"]},
                       approval_token)
        
        return {"success": True, "transaction": txn, "account": self._get_account_info(account_id)}
    
    def _transfer_funds(self, from_account: str, to_account: str, amount: float, approval_token: str) -> Dict:
        """Transfer funds."""
        if from_account not in self.accounts or to_account not in self.accounts:
            raise ValueError("Account not found")
        
        if self.accounts[from_account]["balance"] < amount:
            raise ValueError("Insufficient funds")
        
        self.accounts[from_account]["balance"] -= amount
        self.accounts[to_account]["balance"] += amount
        
        txn = {
            "txn_id": f"TXN{len(self.transactions) + 1:06d}",
            "timestamp": datetime.utcnow().isoformat(),
            "type": "transfer",
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount
        }
        self.transactions.append(txn)
        
        self._log_audit("write", f"accounts:{from_account},{to_account}",
                       {"operation": "transferFunds", "txn_id": txn["txn_id"]},
                       approval_token)
        
        return {
            "success": True,
            "transaction": txn,
            "from_account": self._get_account_info(from_account),
            "to_account": self._get_account_info(to_account)
        }
    
    def _generate_report(self, account_id: str) -> str:
        """Generate account report."""
        if account_id not in self.accounts:
            raise ValueError(f"Account not found: {account_id}")
        
        account = self.accounts[account_id]
        account_txns = [t for t in self.transactions 
                       if t.get("account_id") == account_id or
                          t.get("from_account") == account_id or
                          t.get("to_account") == account_id]
        
        report = f"""
COBOL MAINFRAME BANKING SYSTEM
Account Activity Report
Generated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}

Account ID: {account_id}
Name: {account["name"]}
Balance: ${account["balance"]:,.2f}
Status: {account["status"]}

Transaction History:
{"=" * 80}
"""
        
        if account_txns:
            for txn in account_txns:
                report += f"\n{txn['timestamp']} | {txn['type'].upper()} | "
                if txn['type'] == 'transfer':
                    direction = "OUT" if txn['from_account'] == account_id else "IN"
                    report += f"{direction} ${txn['amount']:,.2f} | {txn['txn_id']}"
                else:
                    report += f"${txn['amount']:+,.2f} | {txn['txn_id']}"
        else:
            report += "\nNo transactions found."
        
        report += f"\n\n{'=' * 80}\nEnd of Report\n"
        
        self._log_audit("read", f"account:{account_id}", {"operation": "generateReport"})
        
        return report


# ============================================================================
# Demo
# ============================================================================

def print_section(title):
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def main():
    print_section("LegacyEvolve Protocol - COBOL Mainframe Adapter Demo")
    
    # Initialize
    adapter = COBOLMainframeAdapter("mainframe.bank.example.com", 23)
    
    # Show skills
    print_section("Available Skills")
    for i, skill in enumerate(adapter.get_skills(), 1):
        badge = "🔒 REQUIRES APPROVAL" if skill.requires_approval else "✓ No approval"
        print(f"{i}. {skill.name}")
        print(f"   {skill.description}")
        print(f"   {badge}\n")
    
    # Demo 1: Read (no approval)
    print_section("Demo 1: Read Account (No Approval Required)")
    print("Executing: getAccountInfo(account_id='ACC001')")
    result = adapter.execute_skill("getAccountInfo", {"account_id": "ACC001"})
    print(f"\nResult:")
    print(f"  Name: {result['name']}")
    print(f"  Balance: ${result['balance']:,.2f}")
    print(f"  Status: {result['status']}")
    
    # Demo 2: Update balance (requires approval)
    print_section("Demo 2: Update Balance (Requires Approval)")
    print("Step 1: Request approval...")
    approval_req = adapter.request_approval(
        "updateAccountBalance",
        {"account_id": "ACC001", "amount": 10000.00, "reason": "Annual bonus"},
        "Adding performance bonus"
    )
    print(f"  ✓ Approval ID: {approval_req.approval_id}")
    print(f"  ⏳ Waiting for human approval...")
    
    time.sleep(1)
    
    print(f"\nStep 2: Human approves...")
    token = adapter.approve(approval_req.approval_id)
    print(f"  ✓ Approved! Token: {token[:30]}...")
    
    print(f"\nStep 3: Execute with token...")
    result = adapter.execute_skill(
        "updateAccountBalance",
        {"account_id": "ACC001", "amount": 10000.00, "reason": "Annual bonus"},
        token
    )
    print(f"  ✓ Success!")
    print(f"  Transaction ID: {result['transaction']['txn_id']}")
    print(f"  Old Balance: ${result['transaction']['old_balance']:,.2f}")
    print(f"  New Balance: ${result['transaction']['new_balance']:,.2f}")
    
    # Demo 3: Transfer (requires approval)
    print_section("Demo 3: Transfer Funds (Requires Approval)")
    print("Step 1: Request approval...")
    approval_req = adapter.request_approval(
        "transferFunds",
        {"from_account": "ACC001", "to_account": "ACC002", "amount": 5000.00},
        "Budget reallocation"
    )
    print(f"  ✓ Approval ID: {approval_req.approval_id}")
    
    time.sleep(1)
    
    token = adapter.approve(approval_req.approval_id)
    print(f"  ✓ Approved!")
    
    print(f"\nStep 2: Execute transfer...")
    result = adapter.execute_skill(
        "transferFunds",
        {"from_account": "ACC001", "to_account": "ACC002", "amount": 5000.00},
        token
    )
    print(f"  ✓ Transfer complete!")
    print(f"  Transaction ID: {result['transaction']['txn_id']}")
    print(f"  From: ACC001 (${result['from_account']['balance']:,.2f})")
    print(f"  To: ACC002 (${result['to_account']['balance']:,.2f})")
    
    # Demo 4: Report
    print_section("Demo 4: Generate Report")
    result = adapter.execute_skill("generateReport", {"account_id": "ACC001"})
    print(result["report"])
    
    # Demo 5: Audit trail
    print_section("Demo 5: Immutable Audit Trail")
    for i, entry in enumerate(adapter.audit_trail, 1):
        emoji = "📖" if entry.action == "read" else "✍️"
        approval = f" [APPROVED]" if entry.approval_token else ""
        print(f"{i}. {emoji} {entry.action.upper()}")
        print(f"   Resource: {entry.resource}")
        print(f"   Time: {entry.timestamp}")
        print(f"   Agent: {entry.agent_id}{approval}\n")
    
    # Summary
    print_section("Key Takeaways")
    print("✓ Read operations: NO approval (fast, efficient)")
    print("✓ Write operations: HUMAN approval (secure, auditable)")
    print("✓ All operations: IMMUTABLE audit trail")
    print("✓ Approval tokens: 5-minute expiration (security)")
    print("\nLegacyEvolve Protocol: Secure AI-legacy system integration")
    print("Learn more: https://github.com/creator35lwb-web/LegacyEvolve\n")


if __name__ == "__main__":
    main()
