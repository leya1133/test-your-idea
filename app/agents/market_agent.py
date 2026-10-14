from crewai import Agent
from app.config import get_llm
from app.tools.search_tools import deep_web_search_tool

def get_market_agent() -> Agent:
    """
    1. Market & Competitor Specialist
    Conducts live web search for direct/indirect competitors, market positioning, and USP.
    """
    return Agent(
        role="Senior Market Analyst & Competitive Intelligence Lead",
        goal="Identify top competitors, market gaps, market size, and Unique Value Proposition (USP).",
        backstory=(
            "You are a seasoned Venture Capital market analyst. You conduct deep competitive intelligence, "
            "evaluate market dynamics, uncover hidden alternatives, and identify defensible market positioning."
        ),
        tools=[deep_web_search_tool],
        llm=get_llm(),
        max_iter=3,
        verbose=True,
        allow_delegation=False
    )
