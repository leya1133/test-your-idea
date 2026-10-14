from crewai import Task
from app.agents.filter_agent import get_filter_agent

def get_filter_task(idea_title: str, idea_description: str, target_audience: str) -> Task:
    agent = get_filter_agent()
    return Task(
        description=(
            f"Audit the following input for validity:\n"
            f"- Title: {idea_title}\n"
            f"- Description: {idea_description}\n"
            f"- Target Audience: {target_audience}\n\n"
            "Determine if this is a real, coherent business/product concept.\n"
            "If valid, return 'VALID_IDEA'.\n"
            "If invalid, spam, or gibberish, return 'INVALID_SPAM: [Reason]'."
        ),
        expected_output="'VALID_IDEA' if coherent business concept, or 'INVALID_SPAM: [Reason]' if gibberish.",
        agent=agent
    )
