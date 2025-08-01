# app/graph/main_workflow.py

from langgraph.graph import StateGraph, END
from app.graph.state import as State
# Import the LLM client, which is shared by all supervisors
from app.llm.llm_client import llm
# Import the hierarchical registry that defines our teams and agents
from app.teams.registry import HIERARCHICAL_REGISTRY
# Import the factories for creating supervisors and team graphs
from app.utils.supervisor_factory import create_supervisor_node
from app.graph.team_graph_factory import create_team_graph
# Import all the individual worker agent nodes

from app.agents.web_agent import search_node as web_search_agent_node
from app.agents.wiki_agent import wiki_node as wiki_search_agent_node
from app.agents.incident_agent import incident_node as incident_agent_node
from app.agents.transaction_agent import transaction_node as transaction_agent_node
from app.agents.focal_party_agent import focal_party_node as focal_party_agent_node
from app.agents.signal_agent import signal_node as signal_agent_node



# =====================================================================

# ==        STEP 1: CREATE THE TEAM SUB-GRAPHS DYNAMICALLY           ==

# =====================================================================



# Create a dictionary to hold our compiled team graphs

team_graphs = {}



# A mapping from node names (strings) to the actual callable node functions

# This allows us to look up the function from the name defined in the registry

all_worker_nodes = {

    "web_search_agent": web_search_agent_node,

    "wiki_search_agent": wiki_search_agent_node,

    "incident_agent": incident_agent_node,

    "transaction_agent": transaction_agent_node,

    "focal_party_agent": focal_party_agent_node,

    "signal_agent": signal_agent_node,

}

# Iterate through the registry to build each team's graph

for team_name, team_members in HIERARCHICAL_REGISTRY.items():
    # We only create sub-graphs for actual teams, not the main supervisor's entry
    if team_name == "__main__":
        continue
    # Create the supervisor for this specific team
    supervisor_node = create_supervisor_node(llm, team_name, team_members)

    # Get the callable functions for this team's workers
    worker_nodes_for_team = [all_worker_nodes[member.name] for member in team_members]

    # Create the team's sub-graph using our factory

    team_graph = create_team_graph(supervisor_node, worker_nodes_for_team)

    # Store the compiled graph in our dictionary

    team_graphs[team_name] = team_graph

# =====================================================================

# ==      STEP 2: CREATE THE TOP-LEVEL SUPERVISOR AND MAIN GRAPH     ==

# =====================================================================

# The top-level supervisor manages the teams themselves

top_supervisor_members = HIERARCHICAL_REGISTRY["__main__"]

top_supervisor_node = create_supervisor_node(llm, "TeamSupervisor", top_supervisor_members)


# Initialize the main application graph

main_graph = StateGraph(State)

# Add the top-level supervisor as the entry point

main_graph.add_node("TeamSupervisor", top_supervisor_node)

main_graph.set_entry_point("TeamSupervisor")

# Add nodes for each team's sub-graph

for team_name, team_graph in team_graphs.items():

    main_graph.add_node(team_name, team_graph)


# Define the final routing logic from the top-level supervisor

def route_from_main_supervisor(state: State):

    """Reads the 'next_node' value from the state to route to a team or end."""

    return state.get("next_node")


main_graph.add_conditional_edges(

    "TeamSupervisor",

    route_from_main_supervisor,

    # The mapping tells the main graph which team sub-graph to call

    {team_name: team_name for team_name in team_graphs.keys()}

)

# After any team has finished its work, the entire process is over.

# The flow returns to the main supervisor, whose prompt will now tell it to FINISH.

for team_name in team_graphs.keys():

    main_graph.add_edge(team_name, "TeamSupervisor")

# =====================================================================

# ==                   STEP 3: COMPILE THE FINAL APP                 ==

# =====================================================================

# The final, compiled application graph

super_graph = main_graph.compile()