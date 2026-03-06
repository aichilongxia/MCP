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


@mcp.tool()
async def server_info(ctx: Context) -> dict[str, str]:
    """Return some basic server/runtime info."""
    return {
        "name": ctx.fastmcp.name,
        "request_id": str(ctx.request_id),
    }


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """A simple dynamic resource."""
    return f"Hello, {name}!"


@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """A prompt template example."""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


def main() -> None:
    # Default transport for FastMCP direct execution is stdio.
    mcp.run()


if __name__ == "__main__":
    main()
