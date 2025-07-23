# app/api/endpoints.py

from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from app.graph.workflow import super_graph as graph_app

class QueryRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/invoke")
async def invoke_workflow(request: QueryRequest):
    """
    This endpoint invokes the multi-agent workflow and returns only the
    final response from the agent.
    """
    # Define the initial state for the graph
    initial_state = {"messages": [HumanMessage(content=request.query)]}

    # Run the graph until the end
    final_state = await graph_app.ainvoke(initial_state)

    # The final answer is always the last message in the state
    final_response = final_state['messages'][-1]

    # Return only the content of that final message
    return {"response": final_response.content}