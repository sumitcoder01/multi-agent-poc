
from app.utils.make_supervisor import make_supervisor_node
from app.prompts.math_supervisor import math_supervisor_prompt
from app.llm.groq_client import llm

members= ["math"]
system_prompt = math_supervisor_prompt(members)
math_supervisor_node = make_supervisor_node(llm, system_prompt , members)