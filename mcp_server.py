"""FastMCP server demo (stdio).

Run:
  uv run python mcp_server.py

Then you can connect with the demo client:
  uv run python mcp_client.py

Or use the inspector:
  uv run mcp dev mcp_server.py
"""

from __future__ import annotations

from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("mcp-demo", json_response=True)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
