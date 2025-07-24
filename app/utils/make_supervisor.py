from typing import List, Optional, Literal, TypedDict
from langchain_core.language_models.chat_models import BaseChatModel
from app.graph.state import State
from langgraph.graph import END
from langgraph.types import Command


def make_supervisor_node(llm: BaseChatModel ,members: list[str]  , system_prompt:Optional[str] = None) -> str:
    options = ["FINISH"] + members

    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
    )
    
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        print(goto)
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    return supervisor_node