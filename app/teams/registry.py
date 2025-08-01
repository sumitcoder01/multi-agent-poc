# app/teams/registry.py

from app.utils.schemas import NodeDescription

# =====================================================================
# ==               STEP 1: DEFINE ALL WORKER AGENTS                  ==
# =====================================================================
# These are the individual agents that perform the final tasks.
# Each description should be clear and concise for the supervisor LLM.

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

# --- Signal Team Workers ---
signal_worker = NodeDescription(
    name="signal_agent",
    description="Looks up security and operational signals. Can be queried with an incident ID for specific signals or without for generic info."
)


# =====================================================================
# ==                STEP 2: GROUP WORKERS INTO TEAMS                 ==
# =====================================================================
# This defines the membership of each sub-team.

research_team_members = [wiki_worker, web_worker]
case_management_team_members = [incident_worker, transaction_worker, focal_party_worker]
signal_team_members = [signal_worker]


# =====================================================================
# ==                STEP 3: DEFINE THE TOP-LEVEL TEAMS               ==
# =====================================================================
# These are the descriptions for the sub-graphs themselves.
# This is what the MAIN supervisor will see.

research_team_supervisor = NodeDescription(
    name="research_team",
    description="This team handles all requests for general information, facts, current events, and explanations. Use for any non-specific query."
)

case_management_team_supervisor = NodeDescription(
    name="case_management_team",
    description="This team handles requests related to specific internal company data. Use for any query containing an ID like 'INC-', 'TRN-', or 'FP-' or keywords like 'incident' or 'transaction'."
)

signal_team_supervisor = NodeDescription(
    name="signal_team",
    description="This team handles requests related to security signals and rule violations. Use for any query containing keywords like 'signal', 'rules', or 'violation'."
)


# =====================================================================
# ==           STEP 4: CREATE THE FINAL HIERARCHICAL REGISTRY        ==
# =====================================================================
# This dictionary maps a supervisor's name to the list of nodes it manages.
# The "__main__" key represents the top-level supervisor.

HIERARCHICAL_REGISTRY = {
    "__main__": [
        research_team_supervisor,
        case_management_team_supervisor,
        signal_team_supervisor
    ],
    "research_team": research_team_members,
    "case_management_team": case_management_team_members,
    "signal_team": signal_team_members
}