
from app.utils.make_supervisor import make_supervisor_node
from app.llm.llm_client import llm

members= ["incident_agent" , "transaction_agent" , "focal_party_agent"]

system_prompt = (
        "You are a supervisor for a case management team. Your workers are: "
        f"{members}. Your primary responsibility is to check if a worker has "
        "already completed the task. If not, you must delegate to the single correct worker.\n\n"
        "## YOUR DECISION-MAKING PROCESS (Follow these steps in order):\n"
        "1.  **Examine the last message in the conversation.**\n"
        "2.  **Check for Worker Completion:** If the last message is from any of your workers "
        f"({members}), it means the requested task has just been completed. You MUST respond "
        "with `FINISH`.\n"
        "3.  **Delegate if Necessary:** If the last message is from the user, identify the ID "
        "type in the user's request ('INC-', 'TRN-', 'FP-') and respond with the single, "
        "corresponding worker's name (`incident_agent`, `transaction_agent`, or `focal_party_agent`).\n"
        "4.  **Your response must be either a single worker name or the word `FINISH`.**"
)

case_management_supervisor_node = make_supervisor_node(llm , members , system_prompt)