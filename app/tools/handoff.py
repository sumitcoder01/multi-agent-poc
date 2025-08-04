# app/tools/handoff.py

from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.graph import MessagesState
from langgraph.types import Command


def create_handoff_tool(*, agent_name: str, description: str) -> tool:
    """
    Factory function to create a specialized handoff tool for a specific agent or team.

    This tool, when called, returns a `Command` object that gives a direct
    instruction to the LangGraph executor to "go to" the specified node.
    """
    # The tool's name must be consistent for the LLM to call it.
    name = f"assign_task_to_{agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        """The actual tool implementation that returns a routing Command."""
        tool_message = {
            "role": "tool",
            "content": f"The task has been successfully assigned to the {agent_name}. They will now perform the work.",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        print(f"Assigning task to {agent_name}...")
        
        return Command(
            # Tells the graph to jump to the node with this name.
            # It's crucial that the graph has a node with this exact 'agent_name'.
            goto=agent_name,
            # We must also update the state with the new tool message.
            update={"messages": state["messages"] + [tool_message]},
            # This specifies the handoff happens in the parent graph.
            graph=Command.PARENT,
        )

    return handoff_tool