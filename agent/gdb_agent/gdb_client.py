import asyncio
import os
import sys
import json
#from contextlib import AsyncExitStack
from typing import Optional, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.callbacks.tracers import ConsoleCallbackHandler

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env (e.g., GOOGLE_API_KEY)

# Overriding the 'default' method of json.JSONEncoder to
# customize the json output for 'content'
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)

#Gemini LLM with deterministic output (temperature=0) and retry logic
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
    max_retries=2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# MCP server params to be passed to stdio_client that will invoke it in
# background
server_params = StdioServerParameters(
    command="python",
    args=['-m', 'gdb_mcp'],
)

# Main async function: connect, load tools, create agent, run chat loop
async def run_agent():
    async with stdio_client(server_params) as (istream, ostream):
        async with ClientSession(istream, ostream) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print("Loaded tools:", [tool.name for tool in tools])
            agent = create_react_agent(llm, tools)
            print("MCP session started! Type 'quit' to exit.")
            while True:
                query = input("\\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                # Send user query to agent and print formatted response
                response = await agent.ainvoke({"messages": query}, callbacks=[ConsoleCallbackHandler()])
                print(type(response))
                try:
                    #customize the json dump of the response
                    formatted = json.dumps(response, indent=2, cls=CustomEncoder)
                except Exception:
                    formatted = str(response)
                print("\\nResponse:")
                print(formatted)
    return

# Entry point: run the async agent loop
if __name__ == "__main__":
    asyncio.run(run_agent())

