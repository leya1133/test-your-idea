from crewai import Agent
from app.config import get_llm

def get_filter_agent() -> Agent:
    """
    0. Saniye Pre-Validation & Spam Filter Agent.
    Evaluates whether the user input is a valid, coherent business idea before running heavy multi-agent research.
    Saves 95% token cost on invalid inputs.
    """
    return Agent(
        role="Pre-Validation & Spam Filter Gatekeeper",
        goal="Instantly determine if the input is a valid, coherent business/product idea or spam/gibberish.",
        backstory=(
            "You are a strict technical gatekeeper for the idea validation pipeline. Your job is to filter out "
            "nonsense, spam, gibberish, or empty input within milliseconds to protect system resources and API budget."
        ),
        tools=[],
        llm=get_llm(),
        max_iter=1,
        verbose=True,
        allow_delegation=False
    )
