from crewai import Agent
from app.config import get_llm

def get_judge_agent() -> Agent:
    """
    5. Chief Investment Officer (Skeptic VC Judge Agent)
    Synthesizes research agent outputs, evaluates deterministic scoring metrics, and issues a rigorous Go/No-Go verdict report.
    """
    return Agent(
        role="Chief Investment Officer & Skeptic VC Judge",
        goal="Synthesize reports from all research agents, audit scores deterministically, eliminate false optimism, and render an objective GO / CONDITIONAL GO / NO-GO executive report.",
        backstory=(
            "You are a ruthless but fair Silicon Valley Venture Capitalist (VC) and investment committee judge. "
            "You DO NOT sugarcoat weaknesses. You challenge unproven assumptions, demand real market evidence, "
            "and protect founders from wasting time and capital on unviable ideas."
        ),
        tools=[],
        llm=get_llm(),
        max_iter=2,
        verbose=True,
        allow_delegation=False
    )
