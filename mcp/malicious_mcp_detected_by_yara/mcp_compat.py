"""
Lance un serveur MCP (stdio) avec une liste d'outils et une fonction d'appel.

Compatible avec mcp 1.x (handlers par décorateurs) et mcp 2.x (handlers passés
au constructeur de Server).
"""

import asyncio

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server


def run_stdio_server(name: str, tools: list, call_tool) -> None:
    """tools: liste de types.Tool. call_tool(nom, arguments) -> str (texte renvoyé)."""
    if hasattr(Server, "list_tools"):  # mcp 1.x
        server = Server(name)

        @server.list_tools()
        async def _list_tools() -> list[types.Tool]:
            return tools

        @server.call_tool()
        async def _call_tool(tool_name: str, arguments: dict) -> list[types.TextContent]:
            return [types.TextContent(type="text", text=call_tool(tool_name, arguments))]

    else:  # mcp 2.x
        async def _list_tools(ctx, params) -> types.ListToolsResult:
            return types.ListToolsResult(tools=tools)

        async def _call_tool(ctx, params) -> types.CallToolResult:
            text = call_tool(params.name, params.arguments or {})
            return types.CallToolResult(content=[types.TextContent(type="text", text=text)])

        server = Server(name, on_list_tools=_list_tools, on_call_tool=_call_tool)

    async def main() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
