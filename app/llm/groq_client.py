# app/llm/groq_client.py

# Import all the possible chat models you want to support
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import ChatHuggingFace

# Import the configuration variables from your config file
from app.core.config import (
    LLM_PROVIDER,
    GROQ_API_KEY,
    HUGGINGFACEHUB_API_TOKEN
)

# Initialize the 'llm' variable that the rest of the app will use
llm = None

print(f"--- Initializing LLM with provider: {LLM_PROVIDER} ---")

# Use an if/elif/else block to instantiate the correct LLM based on the provider
if LLM_PROVIDER == 'groq':
    llm = ChatGroq(
        # The groq library requires the key to be passed as an argument
        groq_api_key=GROQ_API_KEY,
        model_name="gemma2-9b-it",
        temperature=0,
    )

elif LLM_PROVIDER == 'openai':
    # The OpenAI library automatically looks for the OPENAI_API_KEY env variable
    llm = ChatOpenAI(
        model_name="gpt-4o-mini", # A powerful and cost-effective model
        temperature=0,
        max_tokens=None,
    )

elif LLM_PROVIDER == 'deepseek':
    # The DeepSeek library automatically looks for the DEEPSEEK_API_KEY env variable
    llm = ChatDeepSeek(
        model_name="deepseek-chat",
        temperature=0,
        max_tokens=None,
        max_retries=2,
    )

elif LLM_PROVIDER == 'huggingface':
    llm = ChatHuggingFace(
        # The repo_id of the model you want to use from the Hugging Face Hub
        repo_id="google/gemma-2-9b-it",
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
        task="text-generation",
        model_kwargs={
            "temperature": 0.1,  # Set a slight temperature as some HF models fail at 0
            "max_new_tokens": 1024,
        },
    )

else:
    # If the provider is not recognized, raise an error
    raise ValueError(
        f"Invalid LLM_PROVIDER: '{LLM_PROVIDER}'. "
        "Must be 'groq', 'openai', 'deepseek', or 'huggingface'."
    )