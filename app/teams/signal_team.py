# app/teams/signal_team.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from app.graph.state import State

# Import the corrected supervisor factory
from app.agents.supervisor_factory import create_supervisor_agent

# Import the specific worker node for THIS team
from app.agents.signal_agent import signal_node


# 1. Create the supervisor for THIS team by calling the factory.
#    We must capture both the agent and its dynamically created tools.
signal_supervisor, signal_tools = create_supervisor_agent("signal_team")

# 2. Initialize the StateGraph for this team.
signal_graph_builder = StateGraph(State)

# 3. Add the supervisor and a ToolNode for its handoff tools.
signal_graph_builder.add_node("supervisor", signal_supervisor)
signal_graph_builder.add_node("handoff_tool_executor", ToolNode(signal_tools))

# 4. Add the worker node for this team.
#    The name here MUST match the name in the registry.
signal_graph_builder.add_node("signal_agent", signal_node)

# 5. Set the entry point for this team's graph.
signal_graph_builder.set_entry_point("supervisor")


# 7. Define the robust routing logic after the supervisor acts.
def route_after_supervisor(state: State):
    """If the supervisor responds with a tool call, route to the tool executor. Otherwise, END."""
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "handoff_tool_executor"
    else:
        return END

signal_graph_builder.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "handoff_tool_executor": "handoff_tool_executor",
        END: END
    }
)

# 8. Compile the graph.
signal_graph = signal_graph_builder.compile()