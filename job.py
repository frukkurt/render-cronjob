from fastapi import FastAPI
import datetime
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

app = FastAPI()

client = MultiServerMCPClient(
    {
        "Multitool": {
            "url": "https://mcp-server-sn9o.onrender.com/mcp/",
            "transport": "streamable_http",
        }
    }
)

@app.get("/run")
async def run_job():
    now = datetime.datetime.now().isoformat()
    tools = await client.get_tools()
    return {"status": "ok", "time": now, "tools": str(tools)}
