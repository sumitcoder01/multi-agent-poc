# app/llm/groq_client.py

from langchain_groq import ChatGroq
from langchain_deepseek import ChatDeepSeek
from app.core.config import GROQ_API_KEY

# Initialize the Groq Chat Model
# We instantiate it here so it can be easily imported and used by our agents.
# We are choosing "llama3-8b-8192" for its speed and capability.
# llm = ChatDeepSeek(
#     groq_api_key=GROQ_API_KEY,
#     model_name="gemma2-9b-it"
# )

llm = ChatDeepSeek(
        model_name="deepseek-chat",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )