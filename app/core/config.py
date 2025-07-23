# app/core/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- LLM Provider Selector ---
# This variable will determine which LLM is loaded.
# Accepted values: "groq", "openai", "deepseek", "huggingface"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()


# --- API Key Loading ---
# Load all potential API keys from the environment.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# --- Conditional Validation ---
# Raise an error at startup if the required key for the selected provider is missing.
if LLM_PROVIDER == 'groq' and not GROQ_API_KEY:
    raise ValueError("LLM_PROVIDER is 'groq', but GROQ_API_KEY is missing in .env")

if LLM_PROVIDER == 'openai' and not OPENAI_API_KEY:
    raise ValueError("LLM_PROVIDER is 'openai', but OPENAI_API_KEY is missing in .env")

if LLM_PROVIDER == 'deepseek' and not DEEPSEEK_API_KEY:
    raise ValueError("LLM_PROVIDER is 'deepseek', but DEEPSEEK_API_KEY is missing in .env")

if LLM_PROVIDER == 'huggingface' and not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("LLM_PROVIDER is 'huggingface', but HUGGINGFACEHUB_API_TOKEN is missing in .env")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file. Please add it.")