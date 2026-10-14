from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("Web Search Tool")
def web_search_tool(query: str) -> str:
    """
    Searches the live web using DuckDuckGo for competitor info, market trends, user reviews, or news.
    Input should be a clear search query string.
    """
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

@tool("GitHub Open Source Search Tool")
def github_search_tool(query: str) -> str:
    """
    Searches GitHub repositories for open source libraries, tools, and technical precedents matching a given tech stack or feature idea.
    """
    try:
        search_query = f"{query} site:github.com"
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(search_query, max_results=4):
                results.append(f"Repo/Project: {r.get('title')}\nURL: {r.get('href')}\nSummary: {r.get('body')}\n")
        
        if not results:
            return f"No GitHub repositories found for query: '{query}'"
        return "\n---\n".join(results)
    except Exception as e:
        return f"Error executing GitHub search for '{query}': {str(e)}"

@tool("Infrastructure & API Cost Calculator")
def cost_calculator_tool(user_scale_tier: str) -> str:
    """
    Calculates estimated monthly API and cloud infrastructure operational costs.
    Input tier must be one of: 'mvp' (1,000 users), 'growth' (10,000 users), 'scale' (100,000 users).
    """
    tier = user_scale_tier.lower().strip()
    
    if "growth" in tier or "10k" in tier or "10000" in tier:
        return (
            "### Estimated Monthly Operating Cost (Growth Tier - 10,000 active users):\n"
            "- Server / Cloud Hosting (Vercel / AWS EC2): $50 - $120/mo\n"
            "- LLM API Tokens (Gemini / OpenAI): $150 - $400/mo\n"
            "- Database & Vector Store (Supabase / Pinecone): $45 - $90/mo\n"
            "- Total Estimated Monthly Burn: $245 - $610 / month"
        )
    elif "scale" in tier or "100k" in tier or "100000" in tier:
        return (
            "### Estimated Monthly Operating Cost (Scale Tier - 100,000 active users):\n"
            "- Server / Cloud Infrastructure (AWS / GCP K8s): $450 - $1,200/mo\n"
            "- LLM API Tokens (High volume throughput): $1,500 - $4,500/mo\n"
            "- Database & Vector Store (Enterprise managed): $300 - $800/mo\n"
            "- Total Estimated Monthly Burn: $2,250 - $6,500 / month"
        )
    else: # MVP / Default
        return (
            "### Estimated Monthly Operating Cost (MVP Tier - Initial 1,000 users):\n"
            "- Server / Cloud Hosting (Free Tier / Railway / Render): $0 - $15/mo\n"
            "- LLM API Tokens (Gemini Flash / Free limits): $5 - $35/mo\n"
            "- Database (SQLite / Supabase Free): $0/mo\n"
            "- Total Estimated Monthly Burn: $5 - $50 / month"
        )
