from crewai import Agent
from app.config import get_llm
from app.tools import web_search_tool, github_search_tool, cost_calculator_tool

def create_agents():
    llm = get_llm()

    # 1. Market & Competitor Agent
    market_agent = Agent(
        role="Senior Market Analyst & Competitive Intelligence Lead",
        goal="Identify top competitors, market gaps, market size (TAM/SAM/SOM), and Unique Value Proposition (USP) for the given idea.",
        backstory=(
            "You are a seasoned Venture Capital market analyst. You specialize in conducting rapid competitive intelligence, "
            "evaluating market dynamics, identifying existing alternatives, and finding defensible market positioning."
        ),
        tools=[web_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # 2. Demand & Sentiment Agent
    demand_agent = Agent(
        role="Consumer Demand & Sentiment Specialist",
        goal="Uncover real user pain points, search intent, community sentiment, and existing demand patterns for the proposed solution.",
        backstory=(
            "You are a digital customer researcher expert in analyzing online discussions, customer review sites, "
            "Reddit threads, and search trends to measure how urgently target customers need a problem solved."
        ),
        tools=[web_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # 3. Technical Feasibility Agent
    tech_agent = Agent(
        role="Principal Software Architect & Technical Feasibility Lead",
        goal="Assess technical complexity, recommend optimal tech stack, leverage existing open-source code, and estimate MVP build time.",
        backstory=(
            "You are a veteran CTO with expertise in full-stack architecture, AI system integration, and rapid prototyping. "
            "You evaluate technical feasibility, API availability, implementation hurdles, and realistic developer timelines."
        ),
        tools=[github_search_tool, web_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # 4. Financial & Legal Agent
    financial_agent = Agent(
        role="Fintech Cost Modeler & Compliance Auditor",
        goal="Estimate infrastructure/API costs, model unit economics, and highlight regulatory risks (KVKK, GDPR, Copyright).",
        backstory=(
            "You are a technology CFO and legal compliance strategist. You analyze business model sustainability, "
            "cloud server/API operational expenses across scaling tiers, and regulatory compliance considerations."
        ),
        tools=[cost_calculator_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    # 5. Judge Agent (Decision & Synthesis Engine)
    judge_agent = Agent(
        role="Chief Investment Officer & System Judge",
        goal="Synthesize reports from all 4 research agents, apply weighted scoring, compute confidence metrics, and render the final GO / CONDITIONAL GO / NO-GO verdict.",
        backstory=(
            "You are a top-tier venture investment committee judge known for data-driven, objective, and pragmatic evaluations. "
            "You weigh market opportunity against technical risk, consumer demand, and financial sustainability to give founders clear action plans."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    return {
        "market_agent": market_agent,
        "demand_agent": demand_agent,
        "tech_agent": tech_agent,
        "financial_agent": financial_agent,
        "judge_agent": judge_agent
    }
