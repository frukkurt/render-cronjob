from fastapi import FastAPI
import datetime
import asyncio
import requests
import uvicorn
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

    # ตัวอย่าง: call อีก endpoint เพื่อตรวจสอบ health
    url_path = "https://nuviade-agent-new.onrender.com/health"
    response = requests.get(url_path)

    return {
        "status": "ok",
        "time": now,
        "tools": str(tools),
        "ping": response.json() if response.ok else "failed"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# ----------------------------------------
# Run locally with: python main.py
# Render จะใช้ Procfile แทน
# ----------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
