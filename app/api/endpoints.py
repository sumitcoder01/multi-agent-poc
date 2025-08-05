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
from langgraph.types import Command

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

@router.post("/stream")
async def stream_workflow(request: QueryRequest):
    """
    Invokes the multi-agent workflow and streams back a complete, verbose log
    of all intermediate steps, ensuring all data is correctly handled.
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
                    # Correctly check for AIMessage and its tool_calls attribute
                    if isinstance(run_output, AIMessage) and run_output.tool_calls:
                        event_data = {
                            "event": "llm_tool_decision",
                            "data": { "node": event["name"], "tool_calls": run_output.tool_calls }
                        }
                        yield f"data: {json.dumps(event_data)}\n\n"
                
                if kind == "on_tool_end":
                    tool_output = data.get("output")
                    serializable_output = tool_output
                    # Manually serialize the known non-serializable objects
                    if isinstance(tool_output, Command):
                        serializable_output = {"type": "Command", "goto": tool_output.goto}
                    elif isinstance(tool_output, ToolMessage):
                        serializable_output = {"type": "ToolMessage", "content": tool_output.content, "tool_call_id": tool_output.tool_call_id}
                        
                    event_data = {
                        "event": "tool_result",
                        "data": { "node": event["name"], "tool_output": serializable_output }
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"

                if kind == "on_chat_model_stream":
                    chunk = data.get("chunk")
                    # Correctly access the .content attribute of the AIMessageChunk
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