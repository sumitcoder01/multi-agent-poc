# app/teams/registry.py

from app.utils.schemas import NodeDescription

# --- Research Team Workers ---
wiki_worker = NodeDescription(
    name="wiki_search_agent",
    description="A specialist that queries Wikipedia. Use for well-defined, encyclopedic topics (e.g., history, science, biographies)."
)

web_worker = NodeDescription(
    name="web_search_agent",
    description="A generalist that performs broad internet searches. Use for timely events, opinions, or ambiguous queries."
)

# --- Case Management Team Workers ---
incident_worker = NodeDescription(
    name="incident_agent",
    description="Fetches details about a specific security or operational incident using its ID (e.g., 'INC-001')."
)

transaction_worker = NodeDescription(
    name="transaction_agent",
    description="Fetches details about a specific financial transaction using its ID (e.g., 'TRN-102')."
)

focal_party_worker = NodeDescription(
    name="focal_party_agent",
    description="Fetches details about a person or entity (a focal party) using their ID (e.g., 'FP-ALICE')."
)

signal_worker = NodeDescription(
    name="signal_agent",
    description="Looks up security and operational signals. Can be queried with an incident ID for specific signals or without for generic info."
)

sql_worker = NodeDescription(
    name="sql_agent",
    description="A specialized agent that can answer questions by querying a PostgreSQL database containing application data."
)

research_team_members = [wiki_worker, web_worker]
case_management_team_members = [incident_worker, transaction_worker, focal_party_worker]
signal_team_members = [signal_worker]
sql_team_members = [sql_worker]



research_team_supervisor = NodeDescription(
    name="research_team",
    description="This team handles all requests for general information, facts, current events, and explanations. Use for any non-specific query."
)

case_management_team_supervisor = NodeDescription(
    name="case_management_team",
    description="This team handles requests related to specific internal company data.do not use for query containing 'Signals'(High Priority statement). Use for any query containing an ID like 'INC-', 'TRN-', or 'FP-' or keywords like 'incident' or 'transaction'."
)

signal_team_supervisor = NodeDescription(
    name="signal_team",
    description="This team handles requests related to security signals and rule violations. Use for any query containing keywords like 'signal', 'rules', or 'violation'."
)

sql_team_supervisor = NodeDescription(
    name="sql_team",
    description="This team is the highest priority and MUST be used to querying a SQL database."
)


HIERARCHICAL_REGISTRY = {
    "__main__": [
        sql_team_supervisor,
        signal_team_supervisor,
        research_team_supervisor,
        case_management_team_supervisor
    ],
    "research_team": research_team_members,
    "case_management_team": case_management_team_members,
    "signal_team": signal_team_members,
    "sql_team": sql_team_members
}