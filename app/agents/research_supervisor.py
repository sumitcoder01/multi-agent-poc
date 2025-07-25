
from app.utils.make_supervisor import make_supervisor_node
from app.llm.llm_client import llm

members= ["web_search", "wiki_search"]

system_prompt = (
        "You are a supervisor managing a research team. Your available workers are: "
        f"{members}. Your goal is to answer the user's original question by "
        "delegating tasks to your workers.\n\n"
        "## INSTRUCTIONS:\n"
        "1.  **Examine the *entire* conversation history, especially the original user query.**\n"
        "2.  **Critically evaluate the last message.** If the last message is from a worker "
        "(`wiki_search` or `web_search`) and it contains a satisfactory answer to the user's "
        "original request, the task is complete. You MUST respond with `FINISH`.\n"
        "3.  **Delegate if the task is not yet complete.** Based on the user's request, choose the best worker. `wiki_search` is for specific, encyclopedic topics. `web_search` is for all other research.\n"
        "4.  **Respond with only the worker's name or `FINISH`.** Do not answer the question yourself."
    )

research_supervisor_node = make_supervisor_node(llm  , members , system_prompt)