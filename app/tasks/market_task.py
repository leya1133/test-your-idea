from crewai import Task
from app.agents.market_agent import get_market_agent

def get_market_task(idea_title: str, idea_description: str, target_audience: str) -> Task:
    agent = get_market_agent()
    return Task(
        description=(
            f"Conduct market research for:\n"
            f"- Title: {idea_title}\n"
            f"- Description: {idea_description}\n"
            f"- Target Audience: {target_audience}\n\n"
            "Use the deep web search tool to find:\n"
            "1. Top 3 direct and indirect competitors currently active.\n"
            "2. Critical market gaps or features competitors fail to deliver.\n"
            "3. Defensible positioning & Unique Value Proposition (USP).\n"
            "4. Provide a Market Opportunity Sub-Score out of 100 with justification."
        ),
        expected_output="Competitor Table, Market Gap Analysis, USP Recommendation, and Market Score (0-100).",
        agent=agent
    )
