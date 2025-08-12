# app/agents/supervisor_factory.py

from typing import List
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, BaseMessage
from app.llm.llm_client import llm
from app.teams.registry import HIERARCHICAL_REGISTRY
from app.tools.handoff import create_handoff_tool
from langchain_core.messages import HumanMessage

def create_supervisor_agent(supervisor_name: str):
    """
    A generic factory that creates a supervisor agent for any team and
    returns both the agent runnable and the list of tools it was created with.
    """
    # 1. Get the list of members this supervisor manages from the registry.
    members = HIERARCHICAL_REGISTRY[supervisor_name]

    # 2. Dynamically create a handoff tool for each member.
    tools = []
    member_names = [m.name for m in members]
    for member in members:
        handoff_tool = create_handoff_tool(
            agent_name=member.name,
            description=member.description
        )
        tools.append(handoff_tool)

    system_prompt = (
        "You are a supervisor. Your role is to manage a workflow by analyzing the conversation "
        "history and deciding the next step. You can either delegate to a subordinate by calling "
        "a tool, or you can provide the final answer to the user if the task is complete.\n\n"
        "## YOUR AVAILABLE SUBORDINATES (TOOLS):\n"
        "\n".join(f"- **{tool.name}**: {tool.description}" for tool in tools) +
        "\n\n"
        "## YOUR DECISION-MAKING PROCESS (Follow these steps in order):\n"
        "1.  **Examine the `name` of the last message in the conversation.**\n"
        "2.  **Check for Worker Completion:** If the `name` of the last message is one of your subordinates "
        f"({', '.join(member_names)}), it means that worker has just finished its task. The overall job is complete. "
        "You MUST provide a final, concluding answer to the user based on that worker's result. "
        "**Do NOT use any more tools.**\n"
        "3.  **Delegate if Necessary:** If the last message is from the user (i.e., its `name` is not a subordinate's name), "
        "you MUST choose the single best tool to call to delegate the task.\n"
        "4.  **Handle Greetings:** If the user's request is a simple greeting and does not require delegation, "
        "you may respond with a polite, conversational message without using a tool.\n\n"
        "Your final output must be either a single tool call OR a direct conversational response."
    )

    def supervisor_prompt_modifier(state: dict) -> List[BaseMessage]:
        """
        Injects the system prompt. It passes the full message history so the
        supervisor can see the 'name' of the last message.
        """
        # We pass the full history so the supervisor can see the 'name'.
        return [SystemMessage(content=system_prompt)] + state["messages"]
        
    # 4. Create the ReAct agent.
    agent = create_react_agent(
        llm,
        tools,
        prompt=supervisor_prompt_modifier
    )

    # 5. Return the agent
    return agent