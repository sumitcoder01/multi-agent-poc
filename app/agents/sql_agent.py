# app/agents/sql_agent.py

from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from app.llm.llm_client import llm
from app.graph.state import State
from typing import Literal
from langgraph.types import Command

from app.tools.sql_retrieval_tool import sql_retriever_tool
from app.tools.sql_tool import sql_tools


tools = [sql_retriever_tool] + sql_tools


sql_rag_agent_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a highly efficient PostgreSQL agent. Your only goal is to answer the user's question by generating and executing a SQL query.

To do this, you MUST follow this exact, efficient procedure:

1.  **Retrieve Relevant Context:** Your first and most important step is to call the `retrieve_schema_and_examples` tool. Use the user's natural language question as the input to this tool to get the most relevant table schemas and similar, working example queries.

2.  **Generate a Better Query:** You MUST use the context retrieved in the previous step to help you write a better, more accurate PostgreSQL query. Analyze the example queries and the provided schemas to construct your final query.

3.  **Execute Query:** Use the `QuerySQLDatabaseTool` with your newly constructed, syntactically correct PostgreSQL query to get the final answer.

**Safety Rule:**
- You MUST NOT use any DML statements (INSERT, UPDATE, DELETE, DROP).

Your final answer must be a clear, natural language response based on the data returned by your query.
"""
        ),
        ("placeholder", "{messages}"), 
    ]
)

sql_agent = create_react_agent(
    llm,
    tools,
    prompt=sql_rag_agent_prompt_template
)

def sql_node(state: State) -> Command[Literal["supervisor"]]:
    """
    Invokes the RAG SQL agent and returns a Command to update state and report back.
    """
    result = sql_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="sql_agent")
            ]
        },
        goto="supervisor",
    )