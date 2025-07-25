# app/graph/workflow.py

from langgraph.graph import StateGraph, START ,END
from app.agents.case_management_supervisor import case_management_supervisor_node
from app.agents.incident_agent import incident_node
from app.graph.state import State


case_management_builder = StateGraph(State)
case_management_builder.add_node("supervisor", case_management_supervisor_node)
case_management_builder.add_node("incident_agent", incident_node)

case_management_builder.add_edge(START, "supervisor")
case_management_graph = case_management_builder.compile()

