from crewai import Task
from app.agents.financial_agent import get_financial_agent

def get_financial_task(idea_title: str, idea_description: str, target_audience: str) -> Task:
    agent = get_financial_agent()
    return Task(
        description=(
            f"Audit financial viability and legal compliance for:\n"
            f"- Title: {idea_title}\n"
            f"- Description: {idea_description}\n\n"
            "Use the financial calculator tool to estimate:\n"
            "1. Infrastructure/API monthly burn rate (MVP vs Growth vs Scale).\n"
            "2. Est. Customer Acquisition Cost (CAC) & TAM/SAM/SOM market size projections.\n"
            "3. Audit legal & regulatory compliance risks (KVKK, GDPR, AI Act).\n"
            "4. Provide a Financial Viability Sub-Score out of 100 with justification."
        ),
        expected_output="Monthly Burn Estimates, CAC/LTV Model, TAM/SAM/SOM Projections, Legal Risks, and Financial Viability Score (0-100).",
        agent=agent
    )
