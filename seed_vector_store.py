# seed_vector_store.py

import os
import psycopg2
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

FEW_SHOT_QUERIES = [
    # Simple Lookups
    "Who reported the incident with the title 'Unauthorized Server Access'?",
    "What is the summary for incident INC-002?",
    "Show me the details for transaction TRN-101.",

    # Counts and Aggregations
    "How many incidents are currently in 'Open' status?",
    "What is the total transaction amount in 'USD' for all 'Completed' transactions?",
    "What is the average transaction amount for incidents with 'High' priority?",

    # Filtering and Sorting
    "List the full names of all focal parties with the role 'Compliance Officer'.",
    "Show me all 'Pending' transactions.",
    "List all incidents, ordered by their priority.",

    # Complex JOINs
    "Find the email address of the person who is the source for transaction TRN-101.",
    "What is the name of the person who reported the incident related to transaction TRN-103?",
    "List the titles of all incidents reported by 'Alice Anderson'.",
]

def get_database_schema(db_url: str) -> str:
    """Connects to the database and extracts the full schema for all tables."""
    print("Connecting to database to extract schema...")
    # This function is correct and does not need to change.
    # ... (rest of the function is the same)
    compatible_url = db_url.replace("postgresql+psycopg2://", "postgresql://")
    conn = psycopg2.connect(compatible_url)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
    tables = [row[0] for row in cur.fetchall()]
    full_schema = ""
    for table in tables:
        cur.execute(f"SELECT 'CREATE TABLE ' || '{table}' || ' (' || string_agg(column_name || ' ' || data_type, ', ') || ');' FROM information_schema.columns WHERE table_name = '{table}' GROUP BY table_name;")
        schema_string = cur.fetchone()[0]
        full_schema += schema_string + "\n\n"
    cur.close()
    conn.close()
    print("Schema extraction complete.")
    return full_schema.strip()


def seed_vector_store():
    """
    Initializes a ChromaDB vector store, populates it with database schema
    and few-shot queries using Google Gemini embeddings, and persists it to disk.
    """
    print("--- Starting vector store seeding script ---")
    load_dotenv()
    
    # Load the necessary variables from the environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        print("!!! ERROR: GOOGLE_API_KEY not found in .env file. Aborting. !!!")
        return

    # --- THIS IS THE CRITICAL CHANGE ---
    # 1. Initialize the Google Generative AI Embedding function.
    #    The model "embedding-001" is Google's latest text embedding model.
    try:
        print("Initializing Google Gemini embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", 
            google_api_key=GOOGLE_API_KEY
        )
    except Exception as e:
        print(f"!!! ERROR: Could not initialize Google embeddings. Ensure your GOOGLE_API_KEY is set correctly. Error: {e} !!!")
        return

    # 2. Initialize the Chroma vector store
    db_directory = "./chroma_db_sql" # Using a new directory for the new embeddings
    print(f"Initializing ChromaDB, which will be persisted to '{db_directory}'...")
    vector_store = Chroma(
        collection_name="sql_rag_collection",
        embedding_function=embeddings,
        persist_directory=db_directory,
    )

    # 3. Prepare the documents to be added
    print("Preparing documents for vectorization...")
    database_schema_doc = get_database_schema(DATABASE_URL)
    documents = [database_schema_doc] + FEW_SHOT_QUERIES
    
    # 4. Add the documents to the vector store
    print(f"Adding {len(documents)} documents to the vector store... (This may take a moment)")
    vector_store.add_texts(documents)

if __name__ == "__main__":
    seed_vector_store()