import asyncio
import sys

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()


async def main():

    # 1. Connect to our MCP server
    client = MultiServerMCPClient({
        "github": {
            "transport": "stdio",
            "command": sys.executable,
            "args": ["github_server.py"],
        }
    })

    # 2. Discover tools from the MCP server
    tools = await client.get_tools()

    # 3. Create Mistral LLM
    model = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0
    )

    # 4. Create LangChain agent
    agent = create_agent(
        model=model,
        tools=tools
    )

    # 5. Give the agent a task
    response = await agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": "Tell me about the langchain-ai/langchain GitHub repository."
            }
        ]
    })

    # 6. Print final answer
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())