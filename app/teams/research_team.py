# app/teams/research_team.py

from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from app.graph.state import State

from app.agents.supervisor_factory import create_supervisor_agent

from app.agents.wiki_agent import wiki_node
from app.agents.web_agent import search_node

# =====================================================================
# 1. Create the supervisor for THIS team and capture its tools.
research_supervisor = create_supervisor_agent("research_team")

# 2. Initialize the StateGraph.
research_graph_builder = StateGraph(State)

# 3. Add the supervisor and a ToolNode.
research_graph_builder.add_node("supervisor", research_supervisor)

research_graph_builder.add_node("wiki_search_agent", wiki_node)
research_graph_builder.add_node("web_search_agent", search_node)

# 5. Set the entry point.
research_graph_builder.set_entry_point("supervisor")

# 8. Compile the graph.
research_graph = research_graph_builder.compile()