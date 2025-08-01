# app/utils/schemas.py

from pydantic import BaseModel

class NodeDescription(BaseModel):
    """
    A universal schema to describe any node in our agent hierarchy.
    This includes both team supervisors and individual worker agents.
    """
    # The unique name for the node, used for routing within the graph.
    # e.g., "research_team", "wiki_search_agent"
    name: str

    # A detailed description of what this node's purpose is.
    # This will be read by the parent supervisor's LLM to make routing decisions.
    description: str