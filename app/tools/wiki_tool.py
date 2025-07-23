from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


if __name__=="__main__":
    docs = wiki_tool.invoke("INDIA")
    print(docs)


