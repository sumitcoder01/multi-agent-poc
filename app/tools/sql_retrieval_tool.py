# app/tools/sql_retrieval_tool.py

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool

from app.core.config import (
    CHROMA_PATH,
    CHROMA_COLLECTION
)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db_directory = CHROMA_PATH

vector_store = Chroma(
    persist_directory=db_directory,
    embedding_function=embeddings,
    collection_name=CHROMA_COLLECTION
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

sql_retriever_tool = create_retriever_tool(
    retriever,
    name="retrieve_schema_and_examples",
    description=(
        "This is the most important tool. You MUST use it first to retrieve relevant "
        "database schema information and example queries based on the user's question. "
        "The input is the user's natural language question."
    ),
)