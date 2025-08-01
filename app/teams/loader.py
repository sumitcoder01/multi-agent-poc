# app/teams/loader.py

import importlib
from app.utils.schemas import NodeDescription
from app.data.dynamic_db import AGENTS_TABLE, TEAMS_TABLE, TEAM_MEMBERS_TABLE

def load_app_config_from_db():
    """
    Simulates querying a database to dynamically build the application's
    agent hierarchy and configuration at startup.
    """
    print("--- Loading application configuration from dummy database... ---")
    
    # --- 1. Load All Enabled Worker Nodes ---
    all_worker_nodes = {}
    agent_id_to_name_map = {}
    
    for agent_data in AGENTS_TABLE:
        if agent_data["is_enabled"]:
            agent_name = agent_data["name"]
            module_path = agent_data["python_module"]
            node_function_name = f"{agent_name}_node"
            
            try:
                # Dynamically import the python module
                module = importlib.import_module(module_path)
                # Get the node function from the imported module
                node_function = getattr(module, node_function_name)
                all_worker_nodes[agent_name] = node_function
                agent_id_to_name_map[agent_data["id"]] = agent_name
            except (ImportError, AttributeError) as e:
                print(f"!!! WARNING: Could not load node '{node_function_name}' from '{module_path}'. Error: {e} !!!")

    # --- 2. Build the Hierarchical Registry ---
    hierarchical_registry = {"__main__": []}
    agent_id_to_desc_map = {
        agent["id"]: NodeDescription(name=agent["name"], description=agent["description"])
        for agent in AGENTS_TABLE if agent["is_enabled"]
    }

    for team_data in TEAMS_TABLE:
        if team_data["is_enabled"]:
            team_name = team_data["name"]
            
            # Add team to the top-level supervisor's list
            if team_data["parent_team_id"] is None:
                hierarchical_registry["__main__"].append(
                    NodeDescription(name=team_name, description=team_data["description"])
                )
            
            # Find all members of this team
            member_agent_ids = [
                m["agent_id"] for m in TEAM_MEMBERS_TABLE if m["team_id"] == team_data["id"]
            ]
            
            # Get the full NodeDescription for each member
            team_members = [
                agent_id_to_desc_map[agent_id] for agent_id in member_agent_ids if agent_id in agent_id_to_desc_map
            ]
            
            # Add the team and its members to the registry
            hierarchical_registry[team_name] = team_members

    print("--- Configuration loaded successfully. ---")
    return hierarchical_registry, all_worker_nodes