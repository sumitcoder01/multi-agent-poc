
from app.utils.make_supervisor import make_supervisor_node
from app.llm.llm_client import llm

members= ["math"]
math_supervisor_node = make_supervisor_node(llm , members)