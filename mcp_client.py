"""MCP stdio client demo.

This client spawns the local FastMCP server as a subprocess using stdio.

Run:
  uv run python mcp_client.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from pydantic import AnyUrl

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


async def run() -> None:
    server_path = Path(__file__).with_name("mcp_server.py")

    server_params = StdioServerParameters(
        # Use the current interpreter (inside `.venv` when running via `uv run`)
        command=sys.executable,
        args=[str(server_path)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            prompts = await session.list_prompts()
            print(f"Prompts: {[p.name for p in prompts.prompts]}")

            resources = await session.list_resources()
            print(f"Resources: {[str(r.uri) for r in resources.resources]}")

            tools = await session.list_tools()
            print(f"Tools: {[t.name for t in tools.tools]}")

            # Read a dynamic resource
            greeting = await session.read_resource(AnyUrl("greeting://World"))
            if greeting.contents and isinstance(greeting.contents[0], types.TextResourceContents):
                print(f"Resource greeting://World -> {greeting.contents[0].text}")

            # Call a tool
            result = await session.call_tool("add", arguments={"a": 5, "b": 3})
            if result.content and isinstance(result.content[0], types.TextContent):
                print(f"Tool add(5,3) text -> {result.content[0].text}")
            print(f"Tool add(5,3) structured -> {result.structuredContent}")

            info = await session.call_tool("server_info", arguments={})
            print(f"Tool server_info structured -> {info.structuredContent}")


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
