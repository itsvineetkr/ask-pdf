from langchain.tools import Tool
from langchain.tools.tavily_search import TavilySearchResults
from .constants import TAVILY_API_KEY


def retrieval_tool_func(query, retriever):
    docs = retriever.get_relevant_documents(query)
    if docs:
        return "\n".join([doc.page_content for doc in docs])
    return "No relevant documents found."


def get_search_tool():
    tavily_search = TavilySearchResults(api_key=TAVILY_API_KEY)
    search_tool = Tool(
        name="WebSearch",
        func=lambda query: tavily_search.run(query),
        description="Performs a web search to fetch the latest information from the internet.",
    )
    return search_tool


def get_retrieval_tool(retriever):
    retrieval_tool = Tool(
        name="Document Retrieval",
        func=lambda query: retrieval_tool_func(query, retriever),
        description="Use this tool to retrieve relevant information from documents.",
    )
    return retrieval_tool
