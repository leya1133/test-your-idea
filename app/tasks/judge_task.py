from crewai import Task
from app.agents.judge_agent import get_judge_agent

def get_judge_task(idea_title: str, idea_description: str, target_audience: str) -> Task:
    agent = get_judge_agent()
    return Task(
        description=(
            f"You are the Skeptic VC Chief Investment Officer. Synthesize research from all 4 agents for:\n"
            f"- Title: {idea_title}\n"
            f"- Description: {idea_description}\n"
            f"- Target Audience: {target_audience}\n\n"
            "Perform a rigorous final evaluation:\n"
            "1. Extract sub-scores (0-100) from previous reports: Market (30%), Demand (25%), Tech (25%), Financial (20%).\n"
            "2. Apply the deterministic weighted score formula:\n"
            "   Final Score = (Market * 0.30) + (Demand * 0.25) + (Tech * 0.25) + (Financial * 0.20)\n"
            "3. Issue verdict: **GO** (Score >= 75), **CONDITIONAL GO** (Score 55-74), or **NO-GO** (Score < 55).\n"
            "4. Challenge weak assumptions, highlight contradiction risks, and list 3 concrete action items or pivot advice."
        ),
        expected_output="Executive Verdict Report featuring Final Score (0-100), GO/NO-GO Verdict, Weighted Breakdown, Contradiction Risks, and Action Plan.",
        agent=agent
    )
