import os
from crewai.mcp import MCPServerSSE


def get_make_mcp_server() -> MCPServerSSE:
    """Return a configured Make.com MCP server for the manager agent."""
    make_mcp_url=os.getenv("MAKE_MCP_URL")
    make_mcp_token = os.getenv("MAKE_MCP_TOKEN")

    if not make_mcp_url:
        raise ValueError("MAKE_MCP_URL is not set in .env")
    if not make_mcp_token:
        raise ValueError("MAKE_MCP_TOKEN is not set in .env")

    # Make.com MCP server exposes scenarios as callable tools via SSE.
    # The token goes in the Authorization header so the URL stays clean.
    return MCPServerSSE(
        url=f"{make_mcp_url}",
        headers={"Authorization": f"Bearer {make_mcp_token}"},
        cache_tools_list=True,
    )
