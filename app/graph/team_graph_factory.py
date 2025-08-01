# app/graph/team_graph_factory.py

from typing import List, Callable, Dict
from langgraph.graph import StateGraph
from app.graph.state import State
from app.utils.schemas import NodeDescription


def create_team_graph(
    supervisor_node: Callable,
    team_members: List[NodeDescription],
    all_worker_nodes: Dict[str, Callable]
) -> StateGraph:
    """
    A factory function to create a new sub-graph for a specialized team.
    This version ensures node names are consistent with the registry.
    """
    graph = StateGraph(State)
    graph.add_node("supervisor", supervisor_node)

    # --- THIS IS THE CORRECTED LOGIC ---
    # Use the 'name' from the NodeDescription for all node operations.
    for member in team_members:
        # Add the worker node to the graph using its official registry name
        graph.add_node(member.name, all_worker_nodes[member.name])
        # After any worker runs, it must report back to the supervisor
        graph.add_edge(member.name, "supervisor")

    graph.set_entry_point("supervisor")

    # The conditional edge now maps to the correct node names
    graph.add_conditional_edges(
        "supervisor",
        lambda state: state.get("next_node"),
        {member.name: member.name for member in team_members}
    )

    team_graph = graph.compile()
    return team_graph