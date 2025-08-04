# app/teams/research_team.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from app.graph.state import State

from app.agents.supervisor_factory import create_supervisor_agent

from app.agents.wiki_agent import wiki_node
from app.agents.web_agent import search_node

# =====================================================================
# ==              BUILD THE RESEARCH TEAM SUB-GRAPH                  ==
# =====================================================================

# 1. Create the supervisor for THIS team and capture its tools.
research_supervisor, research_tools = create_supervisor_agent("research_team")

# 2. Initialize the StateGraph.
research_graph_builder = StateGraph(State)

# 3. Add the supervisor and a ToolNode.
research_graph_builder.add_node("supervisor", research_supervisor)
research_graph_builder.add_node("handoff_tool_executor", ToolNode(research_tools))

# --- THIS IS THE CORRECTED LOGIC ---
# 4. Add the worker nodes using their OFFICIAL names from the registry.
research_graph_builder.add_node("wiki_search_agent", wiki_node)
research_graph_builder.add_node("web_search_agent", search_node)

# 5. Set the entry point.
research_graph_builder.set_entry_point("supervisor")


# 7. Define the routing logic after the supervisor acts.
def route_after_supervisor(state: State):
    """If the supervisor calls a tool, route to the executor. Otherwise, END."""
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "handoff_tool_executor"
    else:
        return END

research_graph_builder.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "handoff_tool_executor": "handoff_tool_executor",
        END: END
    }
)

# 8. Compile the graph.
research_graph = research_graph_builder.compile()