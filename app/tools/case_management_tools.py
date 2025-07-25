# app/tools/case_management_tools.py

import json
from langchain_core.tools import tool
from app.data.dummy_data import incidents_db, transactions_db, focal_parties_db

@tool
def get_incident_details(incident_id: str) -> str:
    """
    Fetch Incident Details based on incident_id
    """
    print(f"--- Tool: Searching for Incident ID: {incident_id} ---")
    details = incidents_db.get(incident_id, {"error": f"Incident ID '{incident_id}' not found."})
    print(details)
    return details

@tool
def get_transaction_details(transaction_id: str) -> str:
    """
    Fetch Transaction Details based on incident_id
    """
    print(f"--- Tool: Searching for Transaction ID: {transaction_id} ---")
    details = transactions_db.get(transaction_id, {"error": f"Transaction ID '{transaction_id}' not found."})
    return details

@tool
def get_focal_party_details(focal_party_id: str) -> str:
    """
    Fetch Focal party Details based on incident_id
    """
    print(f"--- Tool: Searching for Focal Party ID: {focal_party_id} ---")
    details = focal_parties_db.get(focal_party_id, {"error": f"Focal Party ID '{focal_party_id}' not found."})
    return details