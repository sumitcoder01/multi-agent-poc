# app/main.py

from fastapi import FastAPI
from app.api.endpoints import router as api_router

# Initialize the FastAPI application with metadata
app = FastAPI(
    title="Multi-Agent System PoC",
    description="A Proof of Concept for a multi-agent system using LangGraph and FastAPI.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root GET endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Multi-Agent System API. Visit /docs for API documentation."}