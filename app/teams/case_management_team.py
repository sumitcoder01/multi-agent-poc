# app/teams/case_management_team.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from app.graph.state import State

# Import the corrected supervisor factory
from app.agents.supervisor_factory import create_supervisor_agent

# --- CORRECTED IMPORTS ---
# Import the specific worker nodes for THIS team
from app.agents.incident_agent import incident_node
from app.agents.transaction_agent import transaction_node
from app.agents.focal_party_agent import focal_party_node


# 1. Create the supervisor for THIS team by calling the factory.
#    We capture both the agent and its dynamically created tools.
case_management_supervisor, case_management_tools = create_supervisor_agent("case_management_team")

# 2. Initialize the StateGraph for this team.
case_management_graph_builder = StateGraph(State)

# 3. Add the supervisor and a ToolNode for its handoff tools.
case_management_graph_builder.add_node("supervisor", case_management_supervisor)
case_management_graph_builder.add_node("handoff_tool_executor", ToolNode(case_management_tools))

# 4. Add the worker nodes for this team.
#    The names here MUST match the names in the registry.
case_management_graph_builder.add_node("incident_agent", incident_node)
case_management_graph_builder.add_node("transaction_agent", transaction_node)
case_management_graph_builder.add_node("focal_party_agent", focal_party_node)

# 5. Set the entry point for this team's graph.
case_management_graph_builder.set_entry_point("supervisor")


# 7. Define the routing logic after the supervisor acts.
def route_after_supervisor(state: State):
    """If the supervisor responds with a tool call, route to the tool executor. Otherwise, END."""
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "handoff_tool_executor"
    else:
        return END

case_management_graph_builder.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "handoff_tool_executor": "handoff_tool_executor",
        END: END
    }
)

# 8. Compile the graph.
case_management_graph = case_management_graph_builder.compile()