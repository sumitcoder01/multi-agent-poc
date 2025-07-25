# app/graph/workflow.py

from langgraph.graph import StateGraph, START ,END
from app.graph.state import State
from app.agents.teams_supervisor import call_research_team, call_case_management_team, teams_supervisor_node

# Define the graph.
super_builder = StateGraph(State)
super_builder.add_node("supervisor", teams_supervisor_node)
super_builder.add_node("research_team", call_research_team)
super_builder.add_node("case_management_team", call_case_management_team)

super_builder.add_edge(START, "supervisor")
super_graph = super_builder.compile()


