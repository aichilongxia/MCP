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


def _print_tool_result(prefix: str, result: types.CallToolResult) -> None:
    if result.isError:
        print(f"{prefix} -> ERROR")

    if result.content:
        for block in result.content:
            if isinstance(block, types.TextContent):
                print(f"{prefix} text -> {block.text}")
            else:
                print(f"{prefix} content -> {type(block).__name__}")

    if result.structuredContent is not None:
        print(f"{prefix} structured -> {result.structuredContent}")


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

            if prompts.prompts:
                prompt = await session.get_prompt(
                    "greet_user",
                    arguments={"name": "Alice", "style": "friendly"},
                )
                if prompt.messages:
                    print(f"Prompt greet_user -> {prompt.messages[0].content}")

            resources = await session.list_resources()
            print(f"Resources: {[str(r.uri) for r in resources.resources]}")

            templates = await session.list_resource_templates()
            print(f"Resource templates: {[t.uriTemplate for t in templates.resourceTemplates]}")

            tools = await session.list_tools()
            print(f"Tools: {[t.name for t in tools.tools]}")

            # Read a dynamic resource
            greeting = await session.read_resource(AnyUrl("greeting://World"))
            if greeting.contents:
                first = greeting.contents[0]
                if isinstance(first, types.TextResourceContents):
                    print(f"Resource greeting://World -> {first.text}")
                else:
                    print(f"Resource greeting://World -> {type(first).__name__}")

            # Call a tool
            result = await session.call_tool("add", arguments={"a": 5, "b": 3})
            _print_tool_result("Tool add(5,3)", result)

            info = await session.call_tool("server_info", arguments={})
            _print_tool_result("Tool server_info", info)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
