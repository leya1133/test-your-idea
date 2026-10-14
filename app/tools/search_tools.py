import os
from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Deep Web Search Tool")
def deep_web_search_tool(query: str) -> str:
    """
    Performs deep web research for competitor analysis, market trends, user complaints, or product news.
    Supports Tavily AI if TAVILY_API_KEY is present, with fallback to DuckDuckGo search.
    """
    tavily_key = os.getenv("TAVILY_API_KEY", "").strip()
    
    # Optional Tavily API Integration
    if tavily_key and not tavily_key.startswith("your_"):
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=tavily_key)
            response = client.search(query=query, search_depth="advanced", max_results=5)
            results = []
            for item in response.get("results", []):
                results.append(f"Title: {item.get('title')}\nURL: {item.get('url')}\nContent: {item.get('content')}\n")
            if results:
                return "\n---\n".join(results)
        except Exception as e:
            print(f"[Tavily Search Fallback] {e}")

    # Fallback: DuckDuckGo Search
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n")
        
        if not results:
            return f"No web search results found for query: '{query}'"
        return "\n---\n".join(results)
    except Exception as e:
        return f"Error executing web search for '{query}': {str(e)}"
