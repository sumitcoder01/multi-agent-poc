from langgraph.prebuilt import create_react_agent
from app.llm.llm_client import llm
from typing import Literal
from langgraph.types import Command
from app.tools.case_management_tools import get_transaction_details
from app.graph.state import State
from langchain_core.messages import HumanMessage

tools=[get_transaction_details]

transaction_agent  = create_react_agent(
    llm , 
    tools,
    prompt=("""You are a specialized agent responsible for fetching financial transaction data.
    Your ONLY task is to use the `get_transaction_details` tool to find information based on the user's query.
    Do not add any commentary or explanation to the result.""")
)

def transaction_node(state: State) -> Command[Literal["supervisor"]]:
    result = transaction_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="transaction_agent")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )