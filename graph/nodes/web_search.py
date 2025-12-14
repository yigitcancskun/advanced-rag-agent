from typing import Any, Dict
from graph.state import GraphState
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.documents import Document
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Initialize DuckDuckGo search tool (no API key needed!)
web_search_tool = DuckDuckGoSearchResults(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
    """
    Web search using DuckDuckGo (free, no API key required)
    
    Args:
        state: Current graph state with question and documents
        
    Returns:
        Updated state with web search results added to documents
    """
    print("------WEB SEARCH (DuckDuckGo)------------")

    question = state["question"]
    documents = state.get("documents", []) or []

    # Perform web search
    search_results = web_search_tool.invoke(question)
    
    # DuckDuckGo returns a string, create Document from it
    web_results = Document(page_content=str(search_results))

    # Add to existing documents
    documents.append(web_results)
        
    return {"question": question, "documents": documents}