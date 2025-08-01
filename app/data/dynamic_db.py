# app/data/dynamic_db.py

# Simulates the 'agents' table in a database.
AGENTS_TABLE = [
    {
        "id": 1,
        "name": "wiki_search_agent",
        "description": "A specialist that queries Wikipedia. Use for well-defined, encyclopedic topics (e.g., history, science, biographies).",
        "python_module": "app.agents.wiki_agent",
        "is_enabled": True
    },
    {
        "id": 2,
        "name": "web_search_agent",
        "description": "A generalist that performs broad internet searches. Use for timely events, opinions, or ambiguous queries.",
        "python_module": "app.agents.web_agent",
        "is_enabled": True
    },
    {
        "id": 3,
        "name": "incident_agent",
        "description": "Fetches details about a specific security or operational incident using its ID (e.g., 'INC-001').",
        "python_module": "app.agents.incident_agent",
        "is_enabled": True
    },
    {
        "id": 4,
        "name": "transaction_agent",
        "description": "Fetches details about a specific financial transaction using its ID (e.g., 'TRN-102').",
        "python_module": "app.agents.transaction_agent",
        "is_enabled": True
    },
    {
        "id": 5,
        "name": "focal_party_agent",
        "description": "Fetches details about a person or entity (a focal party) using their ID (e.g., 'FP-ALICE').",
        "python_module": "app.agents.focal_party_agent",
        "is_enabled": True
    },
    {
        "id": 6,
        "name": "signal_agent",
        "description": "Looks up security and operational signals, with or without an incident ID.",
        "python_module": "app.agents.signal_agent",
        "is_enabled": True
    },
    {
        "id": 7, # Example of a disabled agent
        "name": "experimental_agent",
        "description": "An experimental agent that is currently not in use.",
        "python_module": "app.agents.experimental_agent",
        "is_enabled": False
    },
]

# Simulates the 'teams' table in a database.
TEAMS_TABLE = [
    {
        "id": 101,
        "name": "research_team",
        "description": "This team handles all requests for general information, facts, current events, and explanations.",
        "parent_team_id": None, # This indicates it's a top-level team
        "is_enabled": True
    },
    {
        "id": 102,
        "name": "case_management_team",
        "description": "This team handles requests related to specific internal company data like incidents, transactions, and focal parties.",
        "parent_team_id": None,
        "is_enabled": True
    },
    {
        "id": 103,
        "name": "signal_team",
        "description": "This team handles requests related to security signals and rule violations.",
        "parent_team_id": None,
        "is_enabled": True
    },
]

# Simulates the 'team_members' junction table.
TEAM_MEMBERS_TABLE = [
    # Research Team Members
    {"team_id": 101, "agent_id": 1}, # research_team -> wiki_search_agent
    {"team_id": 101, "agent_id": 2}, # research_team -> web_search_agent
    
    # Case Management Team Members
    {"team_id": 102, "agent_id": 3}, # case_management_team -> incident_agent
    {"team_id": 102, "agent_id": 4}, # case_management_team -> transaction_agent
    {"team_id": 102, "agent_id": 5}, # case_management_team -> focal_party_agent

    # Signal Team Members
    {"team_id": 103, "agent_id": 6}, # signal_team -> signal_agent
]