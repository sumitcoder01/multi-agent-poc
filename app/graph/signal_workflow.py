# app/graph/workflow.py

from langgraph.graph import StateGraph, START ,END
from app.agents.signal_supervisor import signal_supervisor_node
from app.agents.signal_agent import signal_node
from app.graph.state import State


signal_builder = StateGraph(State)
signal_builder.add_node("supervisor", signal_supervisor_node)
signal_builder.add_node("signal_agent", signal_node)

signal_builder.add_edge(START, "supervisor")
signal_graph = signal_builder.compile()
