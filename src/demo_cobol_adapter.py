"""
LegacyEvolve Protocol - COBOL Mainframe Adapter Demo

This demo showcases the production-grade COBOL mainframe adapter,
demonstrating secure, auditable access to legacy systems with
human-in-the-loop approval for write operations.

Author: L (GODEL)
Date: February 6, 2026
"""

import sys
import time
from lep_py.adapter.cobol_mainframe_adapter import COBOLMainframeAdapter


def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def main():
    print_section("LegacyEvolve Protocol - COBOL Mainframe Adapter Demo")
    
    # Initialize adapter
    print("Initializing COBOL Mainframe Adapter...")
    adapter = COBOLMainframeAdapter(
        mainframe_host="mainframe.bank.example.com",
        mainframe_port=23,
        connection_string="USER=ADMIN;PASSWORD=***"
    )
    print(f"✓ Connected to: {adapter.system_name} v{adapter.system_version}\n")
    
    # Show available skills
    print_section("Available Skills (Operations)")
    skills = adapter.get_skills()
    for i, skill in enumerate(skills, 1):
        approval_badge = "🔒 REQUIRES APPROVAL" if skill.requires_approval else "✓ No approval needed"
        print(f"{i}. {skill.name}")
        print(f"   {skill.description}")
        print(f"   {approval_badge}\n")
    
    # Show available resources
    print_section("Available Resources (Data)")
    resources = adapter.get_resources()
    for i, resource in enumerate(resources, 1):
        print(f"{i}. {resource.name}")
        print(f"   URI: {resource.uri}")
        print(f"   Description: {resource.description}\n")
    
    # Demo 1: Read account info (no approval)
    print_section("Demo 1: Read Account Information (No Approval Required)")
    print("Executing: getAccountInfo(account_id='ACC001')")
    account_info = adapter.execute_skill("getAccountInfo", {"account_id": "ACC001"})
    print(f"\nResult:")
    print(f"  Account ID: {account_info['account_id']}")
    print(f"  Name: {account_info['name']}")
    print(f"  Balance: ${account_info['balance']:,.2f}")
    print(f"  Status: {account_info['status']}")
    
    # Demo 2: Update balance (requires approval)
    print_section("Demo 2: Update Account Balance (Requires Human Approval)")
    print("Executing: updateAccountBalance(account_id='ACC001', amount=10000, reason='Bonus payment')")
    print("\nStep 1: Request approval...")
    approval_request = adapter.request_approval(
        skill_name="updateAccountBalance",
        parameters={
            "account_id": "ACC001",
            "amount": 10000.00,
            "reason": "Annual bonus payment"
        },
        rationale="Adding annual performance bonus to employee account"
    )
    print(f"  ✓ Approval request created: {approval_request.approval_id}")
    print(f"  ⏳ Waiting for human approval...")
    print(f"\n  Approval Request Details:")
    print(f"    Skill: {approval_request.skill_name}")
    print(f"    Rationale: {approval_request.rationale}")
    print(f"    Expires: {approval_request.expires_at}")
    
    print(f"\n  [Simulating human review and approval...]")
    time.sleep(2)
    
    print(f"\nStep 2: Human approves the request...")
    approval_token = adapter.approve(approval_request.approval_id)
    print(f"  ✓ Approval granted!")
    print(f"  Token: {approval_token[:30]}...")
    
    print(f"\nStep 3: Execute the operation with approval token...")
    result = adapter.execute_skill(
        "updateAccountBalance",
        {
            "account_id": "ACC001",
            "amount": 10000.00,
            "reason": "Annual bonus payment"
        },
        approval_token=approval_token
    )
    print(f"  ✓ Operation completed successfully!")
    print(f"\n  Transaction Details:")
    print(f"    Transaction ID: {result['transaction']['transaction_id']}")
    print(f"    Old Balance: ${result['transaction']['old_balance']:,.2f}")
    print(f"    New Balance: ${result['transaction']['new_balance']:,.2f}")
    print(f"    Amount: ${result['transaction']['amount']:+,.2f}")
    
    # Demo 3: Transfer funds (requires approval)
    print_section("Demo 3: Transfer Funds Between Accounts (Requires Human Approval)")
    print("Executing: transferFunds(from='ACC001', to='ACC002', amount=5000)")
    print("\nStep 1: Request approval...")
    approval_request = adapter.request_approval(
        skill_name="transferFunds",
        parameters={
            "from_account": "ACC001",
            "to_account": "ACC002",
            "amount": 5000.00
        },
        rationale="Transfer funds for inter-department budget reallocation"
    )
    print(f"  ✓ Approval request created: {approval_request.approval_id}")
    
    print(f"\n  [Simulating human review and approval...]")
    time.sleep(2)
    
    approval_token = adapter.approve(approval_request.approval_id)
    print(f"  ✓ Approval granted!")
    
    print(f"\nStep 2: Execute the transfer...")
    result = adapter.execute_skill(
        "transferFunds",
        {
            "from_account": "ACC001",
            "to_account": "ACC002",
            "amount": 5000.00
        },
        approval_token=approval_token
    )
    print(f"  ✓ Transfer completed successfully!")
    print(f"\n  Transaction Details:")
    print(f"    Transaction ID: {result['transaction']['transaction_id']}")
    print(f"    From: {result['transaction']['from_account']} (Balance: ${result['from_account']['balance']:,.2f})")
    print(f"    To: {result['transaction']['to_account']} (Balance: ${result['to_account']['balance']:,.2f})")
    print(f"    Amount: ${result['transaction']['amount']:,.2f}")
    
    # Demo 4: Generate report
    print_section("Demo 4: Generate Account Activity Report")
    print("Executing: generateAccountReport(account_id='ACC001')")
    report = adapter.execute_skill("generateAccountReport", {"account_id": "ACC001"})
    print(report)
    
    # Demo 5: Show audit trail
    print_section("Demo 5: Immutable Audit Trail")
    print("All operations are logged in an immutable audit trail:\n")
    audit_trail = adapter.get_audit_trail()
    for i, entry in enumerate(audit_trail, 1):
        action_emoji = "📖" if entry.action == "read" else "✍️"
        approval_badge = f" [APPROVED: {entry.approval_token[:10]}...]" if entry.approval_token else ""
        print(f"{i}. {action_emoji} {entry.action.upper()}")
        print(f"   Resource: {entry.resource}")
        print(f"   Timestamp: {entry.timestamp}")
        print(f"   Agent: {entry.agent_id}{approval_badge}")
        if entry.details:
            print(f"   Details: {entry.details}")
        print()
    
    # Summary
    print_section("Demo Complete - Key Takeaways")
    print("✓ Read operations require NO approval (fast, efficient)")
    print("✓ Write operations require HUMAN approval (secure, auditable)")
    print("✓ All operations are logged in an IMMUTABLE audit trail")
    print("✓ Approval tokens expire after 5 minutes (security)")
    print("✓ Legacy systems can be safely integrated with modern AI agents")
    print("\nThe LegacyEvolve Protocol enables secure, ethical AI-legacy system integration.")
    print("Learn more: https://github.com/creator35lwb-web/LegacyEvolve\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
