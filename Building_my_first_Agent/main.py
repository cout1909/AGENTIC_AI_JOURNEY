import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool

# Load environment variables from .env file
load_dotenv()

# 1. Initialize the model
model = init_chat_model("mistral-large-latest", model_provider="mistralai")

# 2. Define your tools
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together. Use for multiplication operations."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second. Returns error if dividing by zero."""
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

# 3. Create the LangChain Agent - that's it!
agent = create_agent(model, [multiply, divide])

# 4. Run it
result = agent.invoke({"messages": [
    ("user", "What is 15 multiplied by 8, then divided by 3?")
]})

# 5. Print the final answer
print(result["messages"][-1].content)