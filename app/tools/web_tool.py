from langchain_tavily import TavilySearch
from app.core.config import TAVILY_API_KEY

web_tool = TavilySearch(max_results=3 , api_key=TAVILY_API_KEY)
