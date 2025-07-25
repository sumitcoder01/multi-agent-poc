from langgraph.prebuilt import create_react_agent
from app.llm.llm_client import llm
from typing import Literal
from langgraph.types import Command
from app.tools.signal_tool import get_signal_details
from app.graph.state import State
from langchain_core.messages import HumanMessage

tools=[get_signal_details]

signal_agent  = create_react_agent(
    llm , 
    tools,
    prompt=("""You are a specialized agent for retrieving security and operational signals.
    Your only job is to use the `get_signal_details` tool to find the information requested.
    You must pass the user's `incident_id` to the tool if they provide one.""")
)

def signal_node(state: State) -> Command[Literal["supervisor"]]:
    result = signal_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="signal_agent")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )