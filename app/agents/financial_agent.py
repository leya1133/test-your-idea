from crewai import Agent
from app.config import get_llm
from app.tools.cost_tools import financial_calculator_tool

def get_financial_agent() -> Agent:
    """
    4. Financial & Legal Auditor
    Estimates cloud infrastructure, LLM token burn, Customer Acquisition Cost (CAC), TAM/SAM/SOM market size, and GDPR/KVKK compliance risks.
    """
    return Agent(
        role="Fintech Cost Modeler & Compliance Auditor",
        goal="Estimate infrastructure/API costs, model unit economics (CAC, LTV, burn rate), estimate TAM/SAM/SOM market size, and highlight regulatory risks (KVKK, GDPR).",
        backstory=(
            "You are a technology CFO and legal compliance strategist. You analyze business model sustainability, "
            "marketing acquisition costs (CAC), market size projections (TAM/SAM/SOM), and regulatory compliance considerations."
        ),
        tools=[financial_calculator_tool],
        llm=get_llm(),
        max_iter=3,
        verbose=True,
        allow_delegation=False
    )
