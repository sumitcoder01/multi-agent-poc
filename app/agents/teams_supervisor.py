
from app.utils.make_supervisor import make_supervisor_node
from langgraph.types import Command
from typing import Literal
from app.graph.state import State
from app.llm.llm_client import llm
from langchain_core.messages import HumanMessage
from app.graph.research_workflow import research_graph
from app.graph.case_management_workflow import case_management_graph


members= ["research_team", "case_management_team"]

teams_supervisor_node = make_supervisor_node(llm , members)


def call_research_team(state: State) -> Command[Literal["supervisor"]]:
    response = research_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, name="research_team"
                )
            ]
        },
        goto="supervisor",
    )


def call_case_management_team(state: State) -> Command[Literal["supervisor"]]:
    response = math_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, name="case_management_team"
                )
            ]
        },
        goto="supervisor",
    )