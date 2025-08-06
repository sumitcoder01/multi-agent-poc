from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage
from app.graph.state import State

from app.agents.supervisor_factory import create_supervisor_agent

from app.agents.sql_agent import sql_node

sql_supervisor = create_supervisor_agent("sql_team")

sql_graph_builder = StateGraph(State)

sql_graph_builder.add_node("supervisor", sql_supervisor)
sql_graph_builder.add_node("sql_agent", sql_node)

sql_graph_builder.set_entry_point("supervisor")
sql_graph_builder.add_edge("supervisor", "sql_agent")

sql_graph = sql_graph_builder.compile()