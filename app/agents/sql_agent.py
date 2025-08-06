# app/agents/sql_agent.py

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from app.llm.llm_client import llm
from app.graph.state import State
from typing import Literal
from langgraph.types import Command
from app.tools.sql_tool import sql_tools

sql_agent_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect="Postgres",
    top_k=5,
)
sql_agent = create_react_agent(
    llm,
    sql_tools,
    prompt=sql_agent_prompt
)

def sql_node(state: State) -> Command[Literal["supervisor"]]:
    """
    This node function follows the standard worker pattern for this application.
    It invokes the agent and returns a Command to update state and report back.
    """
    result = sql_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="sql_agent")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )