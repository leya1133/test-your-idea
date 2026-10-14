from crewai import Task
from app.agents.demand_agent import get_demand_agent

def get_demand_task(idea_title: str, idea_description: str, target_audience: str) -> Task:
    agent = get_demand_agent()
    return Task(
        description=(
            f"Analyze user demand and pain points for:\n"
            f"- Title: {idea_title}\n"
            f"- Description: {idea_description}\n"
            f"- Target Audience: {target_audience}\n\n"
            "Search online forums, user review sites, and discussion boards to determine:\n"
            "1. Top 3 urgent user pain points.\n"
            "2. Community sentiment regarding existing solutions/workarounds.\n"
            "3. Demand Urgency Sub-Score out of 100 with rationale."
        ),
        expected_output="Top 3 User Pain Points, Community Sentiment Summary, and Demand Score (0-100).",
        agent=agent
    )
