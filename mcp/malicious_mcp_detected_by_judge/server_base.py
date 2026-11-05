"""
Base commune pour les serveurs MCP dynamiques (HTTP/SSE).

Fournit une factory create_sse_app() qui prend une instance MCPServer
et retourne une app ASGI Starlette prete a etre servie par uvicorn.

Chaque serveur dynamique importe cette base et passe sa propre
instance MCPServer configuree avec ses outils/ressources.

Usage dans un serveur dynamique :
    from server_base import MCPServer, run

    mcp = MCPServer("mon-serveur")

    @mcp.resource("memo://test")
    def ma_ressource() -> str:
        return "contenu"

    if __name__ == "__main__":
        run(mcp, port=8001)

Commande de scan associee :
    mcp-scanner --analyzers yara,llm --format detailed resources \
        --server-url http://localhost:8001/sse
"""

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount

try:  # mcp 2.x
    from mcp.server import MCPServer
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as MCPServer


def create_sse_app(mcp: MCPServer) -> Starlette:
    """Retourne une app ASGI Starlette exposant le serveur MCP via SSE."""
    return Starlette(
        routes=[
            Mount("/", app=mcp.sse_app()),
        ]
    )


def run(mcp: MCPServer, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Lance le serveur uvicorn sur host:port."""
    app = create_sse_app(mcp)
    print(f"[*] Serveur MCP SSE demarre sur http://{host}:{port}/sse")
    print(f"[*] Commande de scan ressources :")
    print(f"    mcp-scanner --analyzers yara,llm --format detailed resources \\")
    print(f"        --server-url http://{host}:{port}/sse")
    uvicorn.run(app, host=host, port=port)
