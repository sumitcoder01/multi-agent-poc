
from app.utils.make_supervisor import make_supervisor_node
from app.prompts.research_supervisor import research_supervisor_prompt
from app.llm.groq_client import llm

members= ["web_search", "wiki_search"]
system_prompt = research_supervisor_prompt(members)
research_supervisor_node = make_supervisor_node(llm , system_prompt , members)