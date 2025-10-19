from fastapi import FastAPI
import datetime
import asyncio
import requests
import uvicorn
import httpx
from langchain_mcp_adapters.client import MultiServerMCPClient

app = FastAPI()

mcp_url = "https://mcp-server-sn9o.onrender.com/mcp/"
mcp_client = MultiServerMCPClient(  # 👈 เปลี่ยนชื่อ
    {
        "Multitool": {
            "url": mcp_url,
            "transport": "streamable_http",
        }
    }
)

@app.get("/run")
async def run_job():
    now = datetime.datetime.now().isoformat()

    # เริ่ม MCP
    print(f"[{now}] 🔧 MCP client started...")
    tools = await mcp_client.get_tools()

    urls = [
        "https://nuviade-agent-new.onrender.com/health",
        "https://dynamic-prompt-yebz.onrender.com/health",
    ]

    results = []

    # ✅ ใช้ชื่อ httpx_client เพื่อไม่ชนกับ mcp_client
    async with httpx.AsyncClient(timeout=10) as httpx_client:
        tasks = [httpx_client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for url, resp in zip(urls, responses):
            if isinstance(resp, Exception):
                results.append({"url": url, "status": "error", "message": str(resp)})
            elif resp.status_code == 200:
                results.append({"url": url, "status": "ok", "response": resp.json()})
            else:
                results.append({"url": url, "status": f"HTTP {resp.status_code}"})

    # ✅ เพิ่ม log ของ MCP tool ที่ดึงได้
    if tools:
        tool_names = [t.name for t in tools]
        results.append({"url": mcp_url, "status": "MCP ok", "tools": tool_names})
    else:
        results.append({"url": mcp_url, "status": "MCP FAIL"})

    print(f"[{now}] ✅ MCP run complete")

    return {
        "status": "ok",
        "time": now,
        "results": results
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
