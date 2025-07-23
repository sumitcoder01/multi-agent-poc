# app/graph/workflow.py

from langgraph.graph import StateGraph, START ,END
from app.agents.math_supervisor import math_supervisor_node
from app.agents.math_agent import math_node
from app.graph.state import State


math_builder = StateGraph(State)
math_builder.add_node("supervisor", math_supervisor_node)
math_builder.add_node("math", math_node)

math_builder.add_edge(START, "supervisor")
math_graph = math_builder.compile()

