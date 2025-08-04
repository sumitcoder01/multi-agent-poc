# app/teams/case_management_team.py

from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from app.graph.state import State

# Import the corrected supervisor factory
from app.agents.supervisor_factory import create_supervisor_agent

from app.agents.incident_agent import incident_node
from app.agents.transaction_agent import transaction_node
from app.agents.focal_party_agent import focal_party_node


# 1. Create the supervisor for THIS team by calling the factory.
#    We capture both the agent and its dynamically created tools.
case_management_supervisor = create_supervisor_agent("case_management_team")

# 2. Initialize the StateGraph for this team.
case_management_graph_builder = StateGraph(State)

# 3. Add the supervisor and a ToolNode for its handoff tools.
case_management_graph_builder.add_node("supervisor", case_management_supervisor)

# 4. Add the worker nodes for this team.
case_management_graph_builder.add_node("incident_agent", incident_node)
case_management_graph_builder.add_node("transaction_agent", transaction_node)
case_management_graph_builder.add_node("focal_party_agent", focal_party_node)

# 5. Set the entry point for this team's graph.
case_management_graph_builder.set_entry_point("supervisor")


# 8. Compile the graph.
case_management_graph = case_management_graph_builder.compile()