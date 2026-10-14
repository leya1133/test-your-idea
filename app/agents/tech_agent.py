from crewai import Agent
from app.config import get_llm
from app.tools.github_tools import github_health_check_tool
from app.tools.search_tools import deep_web_search_tool

def get_tech_agent() -> Agent:
    """
    3. Technical Feasibility Lead
    Inspects GitHub repositories for stars, commit dates, open source licenses, and estimates MVP build duration.
    """
    return Agent(
        role="Principal Software Architect & Technical Feasibility Lead",
        goal="Assess technical complexity, recommend optimal tech stack, inspect GitHub open-source health (stars, commit activity, license), and estimate MVP build time.",
        backstory=(
            "You are a veteran CTO with expertise in full-stack architecture, AI system integration, and rapid prototyping. "
            "You rigorously check open source repos for activity (checking if they are abandoned), audit licenses, and estimate realistic dev timelines."
        ),
        tools=[github_health_check_tool, deep_web_search_tool],
        llm=get_llm(),
        max_iter=3,
        verbose=True,
        allow_delegation=False
    )
