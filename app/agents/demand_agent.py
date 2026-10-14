from crewai import Agent
from app.config import get_llm
from app.tools.search_tools import deep_web_search_tool

def get_demand_agent() -> Agent:
    """
    2. Demand & Sentiment Specialist
    Uncovers user pain points, community discussions, customer reviews, and demand urgency.
    """
    return Agent(
        role="Consumer Demand & Sentiment Specialist",
        goal="Uncover real user pain points, search intent, community sentiment, and existing demand patterns.",
        backstory=(
            "You are a digital customer researcher expert in analyzing online discussions, customer review sites, "
            "forum threads, and search trends to measure how urgently target customers need a problem solved."
        ),
        tools=[deep_web_search_tool],
        llm=get_llm(),
        max_iter=3,
        verbose=True,
        allow_delegation=False
    )
