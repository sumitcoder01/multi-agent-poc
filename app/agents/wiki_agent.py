# app/agents/wiki_agent.py

from langgraph.prebuilt import create_react_agent
from typing import Literal
from langchain_core.messages import HumanMessage
from app.tools.wiki_tool import wiki_tool
from app.llm.llm_client import llm
from langgraph.types import Command
from app.graph.state import State
from langchain_core.messages import HumanMessage


tools = [wiki_tool]

wiki_agent = create_react_agent(llm , tools)

def wiki_node(state: State) -> Command[Literal["supervisor"]]:
    result = wiki_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="wiki_search")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )


