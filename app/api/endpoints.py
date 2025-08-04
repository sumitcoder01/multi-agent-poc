# app/api/endpoints.py

import traceback
from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from app.graph.main_workflow import super_graph as graph_app
from langgraph.errors import GraphRecursionError

class QueryRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/invoke")
async def invoke_workflow(request: QueryRequest):
    """
    Invokes the multi-agent workflow with robust error handling.
    """
    recursion_limit = 25  # A higher, safer limit
    initial_state = {"messages": [HumanMessage(content=request.query)]}
    
    try:
        final_state = await graph_app.ainvoke(
            initial_state,
            {"recursion_limit": recursion_limit}
        )
        response_content = final_state['messages'][-1].content
        
    except GraphRecursionError:
        print("--- ERROR: GraphRecursionError ---")
        raise HTTPException(status_code=500, detail="The agent team entered an infinite loop. Please check supervisor prompts.")
        
    except Exception:
        # This will now catch ANY error and print its full traceback
        print("--- ERROR: An unexpected error occurred in the graph ---")
        traceback.print_exc() # This prints the full error to your console
        raise HTTPException(status_code=500, detail="An internal error occurred in the agent workflow.")

    return {"response": response_content}