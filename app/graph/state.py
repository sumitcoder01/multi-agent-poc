# app/graph/state.py
from langgraph.graph import MessagesState

class State(MessagesState):
    next: str