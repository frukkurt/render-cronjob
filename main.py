from fastapi import FastAPI
import datetime
import asyncio
import requests
import uvicorn
import httpx
from langchain_mcp_adapters.client import MultiServerMCPClient

app = FastAPI()
mcp_url = "https://mcp-server-sn9o.onrender.com/mcp/"
client = MultiServerMCPClient(
    {
        "Multitool": {
            "url": mcp_url,
            "transport": "streamable_http",
        }
    }
)

# @app.get("/run")
# async def run_job():
#     now = datetime.datetime.now().isoformat()
#     tools = await client.get_tools()

#     # ตัวอย่าง: call อีก endpoint เพื่อตรวจสอบ health
#     url_path = "https://nuviade-agent-new.onrender.com/health"
#     response = requests.get(url_path)

#     url_path_1 = "https://dynamic-prompt-yebz.onrender.com
#     response_1 = requests.get(url_path_1)

#     return {
#         "status": "ok",
#         "time": now,
#         "tools": str(tools),
#         "ping": response.json() if response.ok else "failed"
#     }
@app.get("/run")
async def run_job():
    now = datetime.datetime.now().isoformat()
    tools = None
    tools = await client.get_tools()

    # ตัวอย่าง list ของ API ที่ต้องการเรียก
    urls = [
        "https://nuviade-agent-new.onrender.com/health",
        "https://dynamic-prompt-yebz.onrender.com/health",
        # "https://another-service.onrender.com/health"
    ]

    results = []

    # ใช้ async client เพื่อให้ไม่ block
    async with httpx.AsyncClient(timeout=10) as client:
        # สร้าง task หลายตัวพร้อมกัน
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # ประมวลผลผลลัพธ์แต่ละตัว
        for url, resp in zip(urls, responses):
            if isinstance(resp, Exception):
                results.append({"url": url, "status": "error", "message": str(resp)})
            elif resp.status_code == 200:
                results.append({"url": url, "status": "ok", "response": resp.json()})
            else:
                results.append({"url": url, "status": f"HTTP {resp.status_code}"})
    if tools is not None:
        results.append({"url": mcp_url, "status": f"{str([str(i.name) for  i in tools ])}"})
    else :
        results.append({"url": mcp_url, "status": f"FAILL"})
        

    return {
        "status": "ok",
        "time": now,
        "results": results
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
