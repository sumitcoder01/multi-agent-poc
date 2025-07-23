# app/api/endpoints.py

from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from app.graph.workflow import super_graph as graph_app
from langgraph.errors import GraphRecursionError

class QueryRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/invoke")
async def invoke_workflow(request: QueryRequest):
    """
    This endpoint invokes the multi-agent workflow and returns only the
    final response from the agent. It includes robust error handling.
    """
    # Define a sane recursion limit
    recursion_limit = 15
    
    # Define the initial state for the graph
    initial_state = {"messages": [HumanMessage(content=request.query)]}
    
    final_state = None  # Initialize final_state to None

    try:
        # Invoke the graph
        final_state = await graph_app.ainvoke(
            initial_state,
            {"recursion_limit": recursion_limit}
        )
        # Extract the final message if successful
        response_content = final_state['messages'][-1].content
        
    except GraphRecursionError:
        # If the graph loops, return a specific error message
        response_content = "The agent team could not reach a conclusion within the allowed number of steps. Please try rephrasing your query."
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        response_content = "An unexpected error occurred. Please check the server logs."

    # Return the final content, whether it's a success or an error message
    return {"response": response_content}