from crewai import Task

def create_tasks(agents, idea_title, idea_description, target_audience):
    market_agent = agents["market_agent"]
    demand_agent = agents["demand_agent"]
    tech_agent = agents["tech_agent"]
    financial_agent = agents["financial_agent"]
    judge_agent = agents["judge_agent"]

    # Task 1: Market & Competitor Analysis
    task_market = Task(
        description=(
            f"Conduct a thorough market research for the following product idea:\n"
            f"- Idea Title: {idea_title}\n"
            f"- Description: {idea_description}\n"
            f"- Target Audience: {target_audience}\n\n"
            "Use the web search tool to find:\n"
            "1. At least 3 direct or indirect competitors currently active.\n"
            "2. Market gaps or missing features in current market solutions.\n"
            "3. Suggested Unique Value Proposition (USP) for this idea."
        ),
        expected_output=(
            "A structured report containing:\n"
            "- Competitor Table (Name, URL/Source, Key Strengths/Weaknesses)\n"
            "- Market Gap Analysis\n"
            "- Defensible Positioning & USP Recommendation"
        ),
        agent=market_agent
    )

    # Task 2: Demand & Sentiment Analysis
    task_demand = Task(
        description=(
            f"Analyze user demand and sentiment for the idea:\n"
            f"Idea: '{idea_title}' ({idea_description})\n"
            f"Target Audience: '{target_audience}'\n\n"
            "Search online discussions, review forums, and search trends to determine:\n"
            "1. Primary pain points experienced by target users.\n"
            "2. Current customer sentiment regarding existing workarounds.\n"
            "3. Demand Urgency Rating (Low / Medium / High) with justification."
        ),
        expected_output=(
            "A customer demand report containing:\n"
            "- Top 3 User Pain Points\n"
            "- Community Sentiment Summary\n"
            "- Demand Urgency Rating (1-10 scale with rationale)"
        ),
        agent=demand_agent
    )

    # Task 3: Technical Feasibility Analysis
    task_tech = Task(
        description=(
            f"Evaluate the technical feasibility for building an MVP of:\n"
            f"Idea: '{idea_title}' ({idea_description})\n\n"
            "Search GitHub and developer resources to determine:\n"
            "1. Existing open-source repos, tools, or frameworks that can be leveraged.\n"
            "2. Recommended core technology stack (Frontend, Backend, AI/Database).\n"
            "3. Estimated time to complete a functioning MVP (in days/weeks).\n"
            "4. Technical Risk Level (Low / Moderate / High)."
        ),
        expected_output=(
            "A technical feasibility report containing:\n"
            "- Recommended Tech Stack\n"
            "- Open-Source Projects / Reusable GitHub Repos\n"
            "- Estimated MVP Development Timeline\n"
            "- Major Technical Risk Factors"
        ),
        agent=tech_agent
    )

    # Task 4: Financial & Legal Risk Analysis
    task_financial = Task(
        description=(
            f"Estimate operational financial costs and regulatory compliance for:\n"
            f"Idea: '{idea_title}' ({idea_description})\n\n"
            "Use the cost calculator tool to estimate monthly infrastructure/API expenses across MVP, Growth, and Scale tiers.\n"
            "Also evaluate regulatory/legal compliance considerations (GDPR, KVKK, Data privacy, Copyright)."
        ),
        expected_output=(
            "A financial and legal audit report containing:\n"
            "- Monthly Operational Cost Estimates (MVP vs Growth vs Scale)\n"
            "- Monetization & Pricing Model Recommendations\n"
            "- Legal & Regulatory Compliance Risks (KVKK/GDPR/Privacy)"
        ),
        agent=financial_agent
    )

    # Task 5: Final Judge Evaluation (Synthesis & Verdict)
    task_judge = Task(
        description=(
            f"You are the Chief Investment Officer. Synthesize the reports provided by the 4 research agents for:\n"
            f"Idea Title: {idea_title}\n"
            f"Description: {idea_description}\n"
            f"Target Audience: {target_audience}\n\n"
            "Perform a rigorous final evaluation:\n"
            "1. Calculate an Overall Idea Score out of 100 based on:\n"
            "   - Market Opportunity (30%)\n"
            "   - User Demand Urgency (25%)\n"
            "   - Technical Feasibility (25%)\n"
            "   - Financial & Legal Sustainability (20%)\n"
            "2. Render a definitive verdict: **GO** (Score >= 75), **CONDITIONAL GO** (Score 55-74), or **NO-GO** (Score < 55).\n"
            "3. Provide top 3 action items if GO/CONDITIONAL GO, or key pivot suggestions if NO-GO."
        ),
        expected_output=(
            "A comprehensive Executive Verdict Report in Markdown format featuring:\n"
            "- Executive Summary & Overall Score (0-100)\n"
            "- Final Decision (GO / CONDITIONAL GO / NO-GO) in large header\n"
            "- Score Breakdown (Market, Demand, Technical, Financial)\n"
            "- Key Risks Matrix & Actionable Next Steps / Pivot Recommendations"
        ),
        agent=judge_agent
    )

    return [task_market, task_demand, task_tech, task_financial, task_judge]
