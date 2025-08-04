# app/graph/main_workflow.py

from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from app.graph.state import State

from app.agents.supervisor_factory import create_supervisor_agent

# Import the compiled team sub-graphs
from app.teams.research_team import research_graph
from app.teams.case_management_team import case_management_graph
from app.teams.signal_team import signal_graph

main_supervisor = create_supervisor_agent("__main__")

# 2. Initialize the main StateGraph.
main_graph_builder = StateGraph(State)

# 3. Add the nodes to the graph.
main_graph_builder.add_node("supervisor", main_supervisor)
main_graph_builder.set_entry_point("supervisor")

main_graph_builder.add_node("research_team", research_graph)
main_graph_builder.add_node("case_management_team", case_management_graph)
main_graph_builder.add_node("signal_team", signal_graph)

super_graph = main_graph_builder.compile()