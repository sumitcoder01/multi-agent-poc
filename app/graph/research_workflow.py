# app/graph/workflow.py

from langgraph.graph import StateGraph, START ,END
from app.agents.research_supervisor import research_supervisor_node
from app.agents.web_agent import search_node
from app.agents.wiki_agent import wiki_node
from app.graph.state import State

research_builder = StateGraph(State)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("web_search", search_node)
research_builder.add_node("wiki_search", wiki_node)

research_builder.add_edge(START, "supervisor")
research_graph = research_builder.compile()
