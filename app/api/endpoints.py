# app/api/endpoints.py

import json
import traceback
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import (
    HumanMessage, AIMessage, ToolMessage, BaseMessage, AIMessageChunk
)
from pydantic import BaseModel
from app.graph.main_workflow import super_graph as graph_app
from app.agents.sql_agent import sql_agent
from langgraph.types import Command
from langgraph.errors import GraphRecursionError

def _serialize_event_data(data):
    """
    Recursively checks for and converts non-serializable objects
    (like Command or ToolMessage) into a JSON-friendly format.
    """
    if isinstance(data, Command):
        return {"type": "Command", "goto": data.goto}
    if isinstance(data, ToolMessage):
        return {"type": "ToolMessage", "content": data.content, "tool_call_id": data.tool_call_id}
    if isinstance(data, dict):
        return {key: _serialize_event_data(value) for key, value in data.items()}
    if isinstance(data, list):
        return [_serialize_event_data(item) for item in data]
    return data


class QueryRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/sql_route")
async def invoke_sql_agent_stream(request: QueryRequest):
    """
    Directly invokes ONLY the SQL agent and streams back its internal steps
    (the "chain of thought") using Server-Sent Events (SSE).
    This is for testing and debugging the sql_agent in isolation.
    """
    initial_state = {"messages": [HumanMessage(content=request.query)]}

    async def stream_generator():
        """This is the generator function that will be streamed."""
        try:
            # We use astream, which is the async version of stream.
            # stream_mode="values" gives us the full state at each step.
            async for step in sql_agent.astream(
                initial_state,
                stream_mode="values",
            ):
                # The most recent action is the last message in the list.
                last_message = step["messages"][-1]
                
                # Determine the type of step and format the content
                event_type = "step" # Default
                content = ""
                if isinstance(last_message, AIMessage) and last_message.tool_calls:
                    event_type = "tool_call"
                    content = {
                        "tool": last_message.tool_calls[0]['name'],
                        "tool_input": last_message.tool_calls[0]['args']
                    }
                elif isinstance(last_message, ToolMessage):
                    event_type = "tool_result"
                    content = {
                        "tool": last_message.name,
                        "tool_output": last_message.content
                    }
                elif isinstance(last_message, AIMessage):
                    event_type = "final_answer"
                    content = last_message.content

                # Format the event as a Server-Sent Event (SSE)
                event_data = {
                    "event": event_type,
                    "data": content
                }
                yield f"data: {json.dumps(event_data)}\n\n"

            # Signal the end of the stream
            yield f"data: {json.dumps({'event': 'stream_end'})}\n\n"

        except Exception:
            print("--- ERROR: An unexpected error occurred in the SQL agent stream ---")
            traceback.print_exc()
            error_data = {"event": "error", "data": "An internal error occurred."}
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

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

@router.post("/stream")
async def stream_workflow(request: QueryRequest):
    """
    Invokes the multi-agent workflow and streams back a complete, verbose log
    of all intermediate steps, including the handoff tool's tool_call_id.
    """
    recursion_limit = 25
    initial_state = {"messages": [HumanMessage(content=request.query)]}

    async def stream_generator():
        """This is the generator function that will be streamed."""
        try:
            async for event in graph_app.astream_events(
                initial_state,
                {"recursion_limit": recursion_limit},
                version="v2"
            ):
                kind = event["event"]
                data = event["data"]
                
                if kind == "on_llm_end":
                    run_output = data.get("output")
                    if isinstance(run_output, AIMessage) and run_output.tool_calls:
                        event_data = {
                            "event": "llm_tool_decision",
                            "data": { "node": event["name"], "tool_calls": run_output.tool_calls }
                        }
                        yield f"data: {json.dumps(event_data)}\n\n"
                
                # --- THIS IS THE DEFINITIVE, CORRECT TOOL_END HANDLER ---
                if kind == "on_tool_end":
                    tool_output = data.get("output")
                    serializable_output = tool_output # Default

                    # Check if the output is a Command object from our handoff tool
                    if isinstance(tool_output, Command):
                        # The tool_call_id is inside the 'update' payload
                        # that the Command carries.
                        tool_call_id = None
                        if "messages" in tool_output.update and tool_output.update["messages"]:
                            # The ToolMessage we created is the last one in the list
                            last_message = tool_output.update["messages"][-1]
                            # It's a dict, so we can safely .get() the id
                            if isinstance(last_message, dict):
                                tool_call_id = last_message.get("tool_call_id")

                        serializable_output = {
                            "type": "HandoffCommand",
                            "goto": tool_output.goto,
                            "tool_call_id": tool_call_id # <-- We have the ID!
                        }
                    # Handle standard worker tool results
                    elif isinstance(tool_output, ToolMessage):
                        serializable_output = {"type": "ToolMessage", "content": tool_output.content, "tool_call_id": tool_output.tool_call_id}
                        
                    event_data = {
                        "event": "tool_result",
                        "data": { "node": event["name"], "tool_output": serializable_output }
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"

                if kind == "on_chat_model_stream":
                    chunk = data.get("chunk")
                    if isinstance(chunk, AIMessageChunk):
                        token = chunk.content
                        if token:
                            event_data = {"event": "token", "data": token}
                            yield f"data: {json.dumps(event_data)}\n\n"

            yield f"data: {json.dumps({'event': 'stream_end'})}\n\n"

        except Exception:
            print("--- ERROR: An unexpected error occurred during the stream ---")
            traceback.print_exc()
            error_data = {"event": "error", "data": "An internal error occurred."}
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")