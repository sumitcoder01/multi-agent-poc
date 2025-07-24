from langgraph.prebuilt import create_react_agent
from app.llm.llm_client import llm
from typing import Literal
from langgraph.types import Command
from app.graph.state import State
from langchain_core.messages import HumanMessage

def add(a: float, b: float):
    """Add two numbers."""
    return a + b

def substract(a: float, b: float):
    """Subtract two numbers."""
    return a - b


def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float):
    """Divide two numbers."""
    return a / b

tools=[add, multiply, divide, substract]


math_agent = create_react_agent(llm , tools)

def math_node(state: State) -> Command[Literal["supervisor"]]:
    result = math_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="math")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )