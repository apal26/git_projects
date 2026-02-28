# math_server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("MathServer")

# Expose a function as a tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    print ("************** adding two numbers")
    return a + b

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
