"""
LegacyEvolve Protocol (LEP) v2.0 - Base Adapter

This module provides the base class for all LEP adapters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import secrets
import hashlib

from ..models.protocol import (
    Skill,
    ApprovalRequest,
    ApprovalResponse,
    ApprovalState,
    AuditEvent,
    InitializeRequest,
    InitializeResponse,
    SessionCapabilities,
    ProgressUpdate,
    LEPErrorCode
)
from ..core.jsonrpc import JSONRPCHandler


class BaseLEPAdapter(ABC):
    """
    Base class for all LEP adapters.
    
    Subclasses must implement:
    - get_skills(): Return the list of available skills
    - get_resource_impl(): Implement resource retrieval
    - call_skill_impl(): Implement skill execution
    """

    def __init__(self, adapter_name: str, adapter_version: str):
        self.adapter_name = adapter_name
        self.adapter_version = adapter_version
        self.lep_version = "2.0"
        self.capabilities = SessionCapabilities(
            notifications=True,
            diff_support=False,
            cancellation=True
        )
        
        # Session state
        self.session_initialized = False
        self.audit_trail: List[AuditEvent] = []
        self.active_approvals: Dict[str, Dict[str, Any]] = {}  # token -> approval data
        self.decision_counter = 0
        
        # JSON-RPC handler
        self.rpc_handler = JSONRPCHandler()
        self._register_methods()

    def _register_methods(self):
        """Register all LEP protocol methods."""
        self.rpc_handler.register_method("session/initialize", self._handle_initialize)
        self.rpc_handler.register_method("session/shutdown", self._handle_shutdown)
        self.rpc_handler.register_method("legacy/listSkills", self._handle_list_skills)
        self.rpc_handler.register_method("legacy/getResource", self._handle_get_resource)
        self.rpc_handler.register_method("legacy/callSkill", self._handle_call_skill)
        self.rpc_handler.register_method("security/requestApproval", self._handle_request_approval)
        self.rpc_handler.register_method("security/getAuditTrail", self._handle_get_audit_trail)

    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle session/initialize request."""
        self.session_initialized = True
        self._log_audit_event("session_initialized", None, None, None, None)
        
        return {
            "server_name": self.adapter_name,
            "server_version": self.adapter_version,
            "lep_version": self.lep_version,
            "server_capabilities": {
                "notifications": self.capabilities.notifications,
                "diff_support": self.capabilities.diff_support,
                "cancellation": self.capabilities.cancellation
            }
        }

    async def _handle_shutdown(self, params: Dict[str, Any]) -> None:
        """Handle session/shutdown request."""
        self._log_audit_event("session_shutdown", None, None, None, None)
        self.session_initialized = False
        return None

    async def _handle_list_skills(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle legacy/listSkills request."""
        skills = self.get_skills()
        return [
            {
                "name": skill.name,
                "description": skill.description,
                "parameters": skill.parameters,
                "returns": skill.returns,
                "operation_type": skill.operation_type.value
            }
            for skill in skills
        ]

    async def _handle_get_resource(self, params: Dict[str, Any]) -> Any:
        """Handle legacy/getResource request."""
        resource_name = params.get("resource_name")
        resource_params = params.get("parameters", {})
        
        result = await self.get_resource_impl(resource_name, resource_params)
        self._log_audit_event("get_resource", None, resource_name, resource_params, result)
        
        return result

    async def _handle_call_skill(self, params: Dict[str, Any]) -> Any:
        """Handle legacy/callSkill request."""
        skill_name = params.get("skill_name")
        skill_params = params.get("parameters", {})
        approval_token = params.get("approval_token")
        
        # Verify approval token
        if not self._verify_approval_token(approval_token, skill_name, skill_params):
            raise Exception("Invalid or expired approval token")
        
        # Execute skill
        result = await self.call_skill_impl(skill_name, skill_params)
        
        # Log to audit trail
        approval_data = self.active_approvals.get(approval_token, {})
        decision_id = approval_data.get("decision_id")
        self._log_audit_event("skill_executed", decision_id, skill_name, skill_params, result)
        
        # Invalidate single-use token
        if approval_token in self.active_approvals:
            del self.active_approvals[approval_token]
        
        return result

    async def _handle_request_approval(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle security/requestApproval request."""
        skill_name = params.get("skill_name")
        skill_params = params.get("parameters", {})
        reason = params.get("reason")
        estimated_impact = params.get("estimated_impact", {})
        
        # Generate decision ID
        self.decision_counter += 1
        decision_id = f"decision_{self.decision_counter}"
        
        # Request approval from human (this is where the UI would be invoked)
        approval_state = await self.request_human_approval(
            skill_name, skill_params, reason, estimated_impact
        )
        
        # Generate approval token if approved
        approval_token = None
        if approval_state == ApprovalState.APPROVED:
            approval_token = self._generate_approval_token(decision_id, skill_name, skill_params)
        
        # Log to audit trail
        self._log_audit_event("approval_requested", decision_id, skill_name, skill_params, approval_state.value)
        
        return {
            "state": approval_state.value,
            "decision_id": decision_id,
            "approval_token": approval_token
        }

    async def _handle_get_audit_trail(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle security/getAuditTrail request."""
        since_decision_id = params.get("since_decision_id")
        
        # Filter audit trail if needed
        if since_decision_id:
            # Find index of decision_id
            start_index = 0
            for i, event in enumerate(self.audit_trail):
                if event.decision_id == since_decision_id:
                    start_index = i + 1
                    break
            filtered_trail = self.audit_trail[start_index:]
        else:
            filtered_trail = self.audit_trail
        
        return [
            {
                "timestamp": event.timestamp,
                "event_type": event.event_type,
                "decision_id": event.decision_id,
                "skill_name": event.skill_name,
                "parameters": event.parameters,
                "result": event.result,
                "user_id": event.user_id
            }
            for event in filtered_trail
        ]

    def _generate_approval_token(self, decision_id: str, skill_name: str, params: Dict[str, Any]) -> str:
        """Generate a cryptographically secure approval token."""
        token = secrets.token_urlsafe(32)
        
        # Store token with metadata
        self.active_approvals[token] = {
            "decision_id": decision_id,
            "skill_name": skill_name,
            "parameters": params,
            "expires_at": datetime.now() + timedelta(minutes=5)  # 5-minute expiry
        }
        
        return token

    def _verify_approval_token(self, token: str, skill_name: str, params: Dict[str, Any]) -> bool:
        """Verify an approval token."""
        if token not in self.active_approvals:
            return False
        
        approval_data = self.active_approvals[token]
        
        # Check expiry
        if datetime.now() > approval_data["expires_at"]:
            del self.active_approvals[token]
            return False
        
        # Verify skill name and parameters match
        if approval_data["skill_name"] != skill_name:
            return False
        
        # For now, we do exact parameter matching
        # In production, you might want more sophisticated matching
        if approval_data["parameters"] != params:
            return False
        
        return True

    def _log_audit_event(
        self,
        event_type: str,
        decision_id: Optional[str],
        skill_name: Optional[str],
        parameters: Optional[Dict[str, Any]],
        result: Any
    ):
        """Log an event to the audit trail."""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            decision_id=decision_id,
            skill_name=skill_name,
            parameters=parameters,
            result=result,
            user_id="system"  # In production, this would be the actual user ID
        )
        self.audit_trail.append(event)

    # Abstract methods that subclasses must implement

    @abstractmethod
    def get_skills(self) -> List[Skill]:
        """Return the list of skills this adapter provides."""
        pass

    @abstractmethod
    async def get_resource_impl(self, resource_name: str, parameters: Dict[str, Any]) -> Any:
        """Implement resource retrieval from the legacy system."""
        pass

    @abstractmethod
    async def call_skill_impl(self, skill_name: str, parameters: Dict[str, Any]) -> Any:
        """Implement skill execution on the legacy system."""
        pass

    @abstractmethod
    async def request_human_approval(
        self,
        skill_name: str,
        parameters: Dict[str, Any],
        reason: str,
        estimated_impact: Dict[str, Any]
    ) -> ApprovalState:
        """Request approval from a human operator. This is where the UI integration happens."""
        pass

    # Public API

    async def handle_request(self, request_data: str) -> str:
        """Handle an incoming JSON-RPC 2.0 request."""
        return await self.rpc_handler.handle_request(request_data)
