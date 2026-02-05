"""
LegacyEvolve Protocol (LEP) v2.0 - MCP Bridge

This module provides a bridge between LEP adapters and MCP (Model Context Protocol) clients,
enabling LEP adapters to be used with MCP-enabled applications like Claude Desktop.
"""

import json
from typing import Any, Dict, List
from ..adapter.base_adapter import BaseLEPAdapter
from ..core.jsonrpc import JSONRPCHandler


class LEPMCPBridge:
    """
    Bridge between LEP adapters and MCP clients.
    
    This class translates MCP protocol calls into LEP protocol calls,
    enabling LEP adapters to be used with MCP-enabled applications.
    """
    
    def __init__(self, lep_adapter: BaseLEPAdapter):
        """
        Initialize the bridge with an LEP adapter.
        
        Args:
            lep_adapter: The LEP adapter to wrap
        """
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
        # In a production system, you could enumerate available resources
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
        """
        Handle an incoming MCP request.
        
        Args:
            request_data: JSON-RPC 2.0 request string
            
        Returns:
            JSON-RPC 2.0 response string
        """
        return await self.mcp_handler.handle_request(request_data)
