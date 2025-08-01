# app/utils/supervisor_factory.py

from typing import List, Literal, TypedDict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END

from app.utils.schemas import NodeDescription
from app.graph.state import State


def create_supervisor_node(llm: BaseChatModel, supervisor_name: str, members: List[NodeDescription]):
    """
    A generic factory that creates a supervisor node for any team using a
    robust and compatible method.
    """
    # Create the list of options for the router, including the FINISH option.
    options = ["FINISH"] + [member.name for member in members]

    # Dynamically create the Pydantic model for the router.
    class Router(TypedDict):
        """Routes the conversation to the next worker or concludes it."""
        next: Literal[*options]

    # --- THIS IS THE CORRECTED, MORE COMPATIBLE PROMPT & CHAIN ---
    
    # 1. Generate the detailed system prompt.
    system_prompt = (
        f"You are the supervisor for the '{supervisor_name}' team. Your role is to manage the "
        "workflow by routing tasks to the appropriate worker or ending the process. "
        "You must analyze the conversation history and the user's request to make a decision.\n\n"
        "Here are your available workers and their responsibilities:\n"
        # Dynamically list the available workers and their responsibilities.
        "\n".join(f"- **{member.name}**: {member.description}" for member in members) +
        "\n\n"
        "## DECISION-MAKING PROCESS:\n"
        "1.  **Examine the conversation history.** Pay close attention to the original user query and the results from previous workers.\n"
        "2.  **Check for Completion:** If a worker has already provided a satisfactory answer to the user's query, you MUST respond with `FINISH`.\n"
        "3.  **Delegate:** If the task is not yet complete, choose the single best worker to continue the task by responding with their name.\n"
        "4.  **Your response MUST be one of these exact options:** " + ", ".join(options)
    )
    
    # 2. Create a ChatPromptTemplate.
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{messages}"),
        ]
    )

    # 3. Chain the prompt with the LLM and the structured output parser.
    # This is the most compatible way to do it.
    prompt_and_llm_chain = prompt | llm.with_structured_output(Router)

    def supervisor_node(state: State) -> dict:
        """The actual node function that will be executed in the graph."""
        print(f"--- SUPERVISOR: {supervisor_name} ---")

        # Invoke the chain. The input to the prompt is the 'messages' from the state.
        routing_decision = prompt_and_llm_chain.invoke(
            {"messages": state["messages"]}
        )
        next_node = routing_decision['next']
        print(f"--- Supervisor '{supervisor_name}' decision: Route to '{next_node}' ---")

        # If the supervisor chooses to finish, map it to the graph's END node.
        if next_node == "FINISH":
            return {"next_node": END}
        else:
            return {"next_node": next_node}

    return supervisor_node