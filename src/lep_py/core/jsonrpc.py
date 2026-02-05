"""
LegacyEvolve Protocol (LEP) v2.0 - JSON-RPC 2.0 Transport Layer

This module provides the core JSON-RPC 2.0 communication primitives.
"""

import json
from typing import Any, Dict, Optional, Callable
from ..models.protocol import (
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCError,
    LEPErrorCode
)


class JSONRPCHandler:
    """Handles JSON-RPC 2.0 request/response processing."""

    def __init__(self):
        self.methods: Dict[str, Callable] = {}
        self.request_id_counter = 0

    def register_method(self, name: str, handler: Callable):
        """Register a method handler."""
        self.methods[name] = handler

    def create_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> JSONRPCRequest:
        """Create a JSON-RPC 2.0 request."""
        self.request_id_counter += 1
        return JSONRPCRequest(
            jsonrpc="2.0",
            method=method,
            params=params,
            id=self.request_id_counter
        )

    def create_response(self, request_id: int, result: Any) -> JSONRPCResponse:
        """Create a successful JSON-RPC 2.0 response."""
        return JSONRPCResponse(
            jsonrpc="2.0",
            result=result,
            id=request_id
        )

    def create_error_response(self, request_id: Optional[int], code: int, message: str, data: Any = None) -> JSONRPCResponse:
        """Create an error JSON-RPC 2.0 response."""
        error = JSONRPCError(code=code, message=message, data=data)
        return JSONRPCResponse(
            jsonrpc="2.0",
            error={"code": error.code, "message": error.message, "data": error.data},
            id=request_id
        )

    async def handle_request(self, request_data: str) -> str:
        """Handle an incoming JSON-RPC 2.0 request."""
        try:
            request_dict = json.loads(request_data)
        except json.JSONDecodeError:
            response = self.create_error_response(
                None,
                LEPErrorCode.PARSE_ERROR,
                "Invalid JSON"
            )
            return json.dumps(response.__dict__)

        # Validate request structure
        if not isinstance(request_dict, dict) or request_dict.get("jsonrpc") != "2.0":
            response = self.create_error_response(
                request_dict.get("id"),
                LEPErrorCode.INVALID_REQUEST,
                "Invalid Request"
            )
            return json.dumps(response.__dict__)

        method = request_dict.get("method")
        params = request_dict.get("params", {})
        request_id = request_dict.get("id")

        # Check if method exists
        if method not in self.methods:
            response = self.create_error_response(
                request_id,
                LEPErrorCode.METHOD_NOT_FOUND,
                f"Method '{method}' not found"
            )
            return json.dumps(response.__dict__)

        # Execute method
        try:
            handler = self.methods[method]
            result = await handler(params)
            response = self.create_response(request_id, result)
            return json.dumps(response.__dict__)
        except Exception as e:
            response = self.create_error_response(
                request_id,
                LEPErrorCode.INTERNAL_ERROR,
                f"Internal error: {str(e)}"
            )
            return json.dumps(response.__dict__)

    def serialize_request(self, request: JSONRPCRequest) -> str:
        """Serialize a request to JSON."""
        return json.dumps({
            "jsonrpc": request.jsonrpc,
            "method": request.method,
            "params": request.params,
            "id": request.id
        })

    def deserialize_response(self, response_data: str) -> JSONRPCResponse:
        """Deserialize a response from JSON."""
        response_dict = json.loads(response_data)
        return JSONRPCResponse(
            jsonrpc=response_dict.get("jsonrpc", "2.0"),
            result=response_dict.get("result"),
            error=response_dict.get("error"),
            id=response_dict.get("id")
        )
