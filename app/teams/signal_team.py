# app/teams/signal_team.py

from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from app.graph.state import State

# Import the corrected supervisor factory
from app.agents.supervisor_factory import create_supervisor_agent

# Import the specific worker node for THIS team
from app.agents.signal_agent import signal_node


# 1. Create the supervisor for THIS team by calling the factory.
signal_supervisor = create_supervisor_agent("signal_team")

# 2. Initialize the StateGraph for this team.
signal_graph_builder = StateGraph(State)

# 3. Add the supervisor and a ToolNode for its handoff tools.
signal_graph_builder.add_node("supervisor", signal_supervisor)

signal_graph_builder.add_node("signal_agent", signal_node)

# 5. Set the entry point for this team's graph.
signal_graph_builder.set_entry_point("supervisor")

# 8. Compile the graph.
signal_graph = signal_graph_builder.compile()