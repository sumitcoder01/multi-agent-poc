# app/tools/signal_tool.py

import json
from typing import Optional
from langchain_core.tools import tool
from app.data.dummy_data import signals_db

@tool
def get_signal_details(incident_id: Optional[str] = None) -> str:
    """
    Fetch signal details. If an incident_id is provided
    If no ID is provided, it returns generic information about the types of signals tracked.
    """
    print(f"--- Tool: Searching for Signals (Incident ID: {incident_id}) ---")
    if incident_id:
        # Return specific signals if an ID is provided
        details = signals_db.get(incident_id, {"error": f"No signals found for Incident ID '{incident_id}'."})
    else:
        # Return generic info if no ID is provided
        details = signals_db.get("_generic_info", {"error": "Generic signal information not available."})

    return details