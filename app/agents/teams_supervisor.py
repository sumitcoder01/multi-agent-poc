
from app.utils.make_supervisor import make_supervisor_node
from langgraph.types import Command
from typing import Literal
from app.graph.state import State
from app.llm.llm_client import llm
from langchain_core.messages import HumanMessage
from app.graph.research_workflow import research_graph
from app.graph.case_management_workflow import case_management_graph


members= ["research_team", "case_management_team"]

system_prompt = (
        "You are a top-level supervisor. Your only job is to route a user's request to the correct "
        f"specialized team: {members}. You must follow a strict set of rules to make your decision.\n\n"
        "## ROUTING RULES (Follow in this exact order):\n"
        "1.  **KEYWORD SCAN (HIGHEST PRIORITY):** First, scan the user's entire query for any of the "
        "following high-priority keywords: **'incident', 'transaction', 'focal party', 'INC-', 'TRN-', 'FP-'**. "
        "If you find ANY of these keywords, you MUST immediately route to the `case_management_team`.\n\n"
        "2.  **GENERAL RESEARCH (LOWER PRIORITY):** If and only if NONE of the high-priority keywords from "
        "Rule #1 are present, and the query is a general question (e.g., 'what is...', 'tell me about...'), "
        "then you should route to the `research_team`.\n\n"
        "3.  **COMPLETION CHECK:** If the last message in the conversation is from one of your teams "
        f"({', '.join(members)}), the task is complete. You MUST respond with `FINISH`.\n\n"
        "## YOUR RESPONSE:\n"
        "Your final response must be a single word: either a team name (e.g., `case_management_team`) or `FINISH`."
)
teams_supervisor_node = make_supervisor_node(llm , members , system_prompt)


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
    response = case_management_graph.invoke({"messages": state["messages"][-1]})
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