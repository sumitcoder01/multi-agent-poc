# app/tools/sql_tool.py

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from app.llm.llm_client import llm
from app.core.config import DATABASE_URL

db = SQLDatabase.from_uri(DATABASE_URL)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)


sql_tools = toolkit.get_tools()
