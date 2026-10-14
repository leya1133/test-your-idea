from crewai import Task
from app.agents.tech_agent import get_tech_agent

def get_tech_task(idea_title: str, idea_description: str, target_audience: str) -> Task:
    agent = get_tech_agent()
    return Task(
        description=(
            f"Evaluate technical feasibility for:\n"
            f"- Title: {idea_title}\n"
            f"- Description: {idea_description}\n\n"
            "Use the GitHub Health Check Tool to inspect repos (checking stars, last commit date for abandoned status, and license):\n"
            "1. List existing open-source repos & frameworks.\n"
            "2. Flag any abandoned or GPL-restricted repos.\n"
            "3. Recommend optimal core tech stack.\n"
            "4. Estimate MVP dev duration in days/weeks.\n"
            "5. Provide a Technical Feasibility Sub-Score out of 100 with justification."
        ),
        expected_output="Recommended Tech Stack, GitHub Open-Source Health Audit, MVP Timeline, and Tech Feasibility Score (0-100).",
        agent=agent
    )
