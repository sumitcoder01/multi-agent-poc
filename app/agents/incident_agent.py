from langgraph.prebuilt import create_react_agent
from app.llm.llm_client import llm
from typing import Literal
from langgraph.types import Command
from app.graph.state import State
from langchain_core.messages import HumanMessage

tools=[]

incident_agent = create_react_agent(llm , tools)

def incident_node(state: State) -> Command[Literal["supervisor"]]:
    result = incident_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="incident_agent")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )