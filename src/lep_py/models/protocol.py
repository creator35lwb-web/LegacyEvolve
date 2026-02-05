"""
LegacyEvolve Protocol (LEP) v2.0 - Core Data Models

This module defines the core data structures for the LEP protocol.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional
from enum import Enum


class OperationType(str, Enum):
    """Type of operation a skill performs."""
    READ = "read"
    WRITE = "write"


class ApprovalState(str, Enum):
    """State of an approval request."""
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Skill:
    """Represents a skill (function) exposed by an LEP adapter."""
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]
    operation_type: OperationType


@dataclass
class ApprovalRequest:
    """Request for human approval of a write operation."""
    skill_name: str
    parameters: Dict[str, Any]
    reason: str
    estimated_impact: Dict[str, Any]


@dataclass
class ApprovalResponse:
    """Response to an approval request."""
    state: ApprovalState
    decision_id: str
    approval_token: Optional[str] = None


@dataclass
class AuditEvent:
    """A single event in the audit trail."""
    timestamp: str
    event_type: str
    decision_id: Optional[str]
    skill_name: Optional[str]
    parameters: Optional[Dict[str, Any]]
    result: Optional[Any]
    user_id: Optional[str]


@dataclass
class SessionCapabilities:
    """Capabilities supported by a client or server."""
    notifications: bool = False
    diff_support: bool = False
    cancellation: bool = False


@dataclass
class InitializeRequest:
    """Request to initialize a LEP session."""
    client_name: str
    client_version: str
    supported_lep_versions: List[str]
    client_capabilities: SessionCapabilities


@dataclass
class InitializeResponse:
    """Response to an initialize request."""
    server_name: str
    server_version: str
    lep_version: str
    server_capabilities: SessionCapabilities


@dataclass
class ProgressUpdate:
    """Progress update for a long-running skill."""
    skill_name: str
    progress_percentage: float
    status_message: str


@dataclass
class JSONRPCRequest:
    """A JSON-RPC 2.0 request."""
    jsonrpc: str = "2.0"
    method: str = ""
    params: Optional[Dict[str, Any]] = None
    id: Optional[int] = None


@dataclass
class JSONRPCResponse:
    """A JSON-RPC 2.0 response."""
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[int] = None


@dataclass
class JSONRPCError:
    """A JSON-RPC 2.0 error object."""
    code: int
    message: str
    data: Optional[Any] = None


# Standard LEP Error Codes
class LEPErrorCode(int, Enum):
    """Standard error codes for LEP."""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    PERMISSION_DENIED = -32000
    APPROVAL_EXPIRED = -32001
    SKILL_EXECUTION_ERROR = -32002
    RESOURCE_NOT_FOUND = -32003
