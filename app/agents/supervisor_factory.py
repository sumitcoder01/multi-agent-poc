# app/agents/supervisor_factory.py

from typing import List
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, BaseMessage
from app.llm.llm_client import llm
from app.teams.registry import HIERARCHICAL_REGISTRY
from app.tools.handoff import create_handoff_tool

def create_supervisor_agent(supervisor_name: str):
    """
    A generic factory that creates a supervisor agent for any team and
    returns both the agent runnable and the list of tools it was created with.
    """
    # 1. Get the list of members this supervisor manages from the registry.
    members = HIERARCHICAL_REGISTRY[supervisor_name]

    # 2. Dynamically create a handoff tool for each member.
    tools = []
    for member in members:
        handoff_tool = create_handoff_tool(
            agent_name=member.name,
            description=member.description
        )
        tools.append(handoff_tool)

    # 3. --- THIS IS THE NEW PROMPT WITH AN EXPLICIT "EXIT" RULE ---
    prompt_header = (
        "You are a supervisor agent. Your primary role is to analyze the user's request and "
        "decide the next step. You can either delegate the task to a subordinate worker/team "
        "by calling a tool, or you can conclude the conversation if no further action is needed.\n\n"
        "## AVAILABLE WORKERS/TEAMS (TOOLS):\n"
    )

    tool_descriptions = "\n".join(
        f"- **{tool.name}**: {tool.description}" for tool in tools
    )

    final_instruction = (
        "\n\n## DECISION PROCESS:\n"
        "1.  **Examine the user's request.**\n"
        "2.  **You MUST delegate the task by choosing the single best tool to call.** "
        "Your only job is to delegate to the correct worker or team. Do not respond directly."
    )

    final_prompt_text = prompt_header + tool_descriptions + final_instruction

    def supervisor_prompt_modifier(state: dict) -> List[BaseMessage]:
        """Injects the dynamically generated system prompt."""
        messages = state["messages"]
        modified_messages = [SystemMessage(content=final_prompt_text)] + messages
        return modified_messages
        
    # 4. Create the ReAct agent.
    agent = create_react_agent(
        llm,
        tools,
        prompt=supervisor_prompt_modifier
    )

    # 5. Return both the agent and the list of tools it uses.
    return agent, tools