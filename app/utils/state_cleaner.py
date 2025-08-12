# app/utils/state_cleaner.py

from app.graph.state import State

def clean_and_prepare_state_for_team(state: State) -> dict:
    """
    This is a critical entry node for all sub-graphs. It takes the full
    state passed by a handoff command and "cleans" it, so the sub-graph
    only receives the original user query. This prevents state pollution
    and is the key to making hierarchical handoffs work.
    """
    print("--- Cleaning state for sub-graph ---")
    
    # The original user query is always the first message.
    original_user_query = state["messages"][0]
    
    # Return a new, clean state containing only that first message.
    return {"messages": [original_user_query]}