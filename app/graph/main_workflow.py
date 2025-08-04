# app/graph/main_workflow.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from app.graph.state import State

from app.agents.supervisor_factory import create_supervisor_agent

# Import the compiled team sub-graphs
from app.teams.research_team import research_graph
from app.teams.case_management_team import case_management_graph
from app.teams.signal_team import signal_graph

# =====================================================================
# ==              BUILD THE MAIN APPLICATION GRAPH                   ==
# =====================================================================

# 1. Create the top-level supervisor and get its dynamically created tools.
main_supervisor, supervisor_tools = create_supervisor_agent("__main__")

# 2. Initialize the main StateGraph.
main_graph_builder = StateGraph(State)

# 3. Add the nodes to the graph.
main_graph_builder.add_node("supervisor", main_supervisor)
main_graph_builder.set_entry_point("supervisor")

# The ToolNode now correctly receives the dynamically created tools.
main_graph_builder.add_node("handoff_tool_executor", ToolNode(supervisor_tools))

main_graph_builder.add_node("research_team", research_graph)
main_graph_builder.add_node("case_management_team", case_management_graph)
main_graph_builder.add_node("signal_team", signal_graph)

# 4. Define the edges for the workflow.
# main_graph_builder.add_edge("research_team", "supervisor")
# main_graph_builder.add_edge("case_management_team", "supervisor")
# main_graph_builder.add_edge("signal_team", "supervisor")

def route_after_supervisor(state: State):
    """
    Decides the next step after the supervisor has acted.
    """
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "handoff_tool_executor"
    else:
        return END

main_graph_builder.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "handoff_tool_executor": "handoff_tool_executor",
        END: END
    }
)

# =====================================================================
# ==                   COMPILE THE FINAL APP                         ==
# =====================================================================

super_graph = main_graph_builder.compile()