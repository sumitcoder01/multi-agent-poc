# app/core/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the API keys from the environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Basic validation to ensure the keys are set
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file. Please add it.")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file. Please add it.")