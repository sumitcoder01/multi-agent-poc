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

    prompt_header = (
        "You are a supervisor. Your sole responsibility is to analyze the user's request "
        "and delegate the task to the single most appropriate subordinate by calling "
        "the correct tool. Do not answer the user's question yourself.\n\n"
    )

    final_instruction = (
        "\n\n## INSTRUCTIONS:\n"
        "1.  Read the user's request.\n"
        "2.  Choose the single/one best tool to call to delegate the task.\n"
        "3.  If the request is a simple greeting (e.g., 'hello'), you may respond directly."
    )
    
    final_prompt_text = prompt_header + final_instruction

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

    # 5. Return the agent
    return agent