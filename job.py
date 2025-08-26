import datetime
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# กำหนด client MCP
client = MultiServerMCPClient(
    {
        "Multitool": {
            "url": "https://mcp-server-sn9o.onrender.com/mcp/",
            "transport": "streamable_http",
        }
    }
)

async def main():
    now = datetime.datetime.now().isoformat()
    print(f"[CronJob] Running at {now}")

    # ตัวอย่าง: ดึง tools จาก MCP
    tools = await client.get_tools()
    print(f"Tools available: {tools}")

    # ---- ตรงนี้คุณจะใส่โค้ดทำงานจริงได้เลย ----
    # เช่น invoke agent, fetch API, save DB
    # agent = create_react_agent(llm, tools=tools) 
    # result = await agent.ainvoke("วันนี้อากาศเป็นยังไง?")
    # print(result)

if __name__ == "__main__":
    asyncio.run(main())
