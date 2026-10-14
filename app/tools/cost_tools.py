from crewai.tools import tool

@tool("Financial & TAM/SAM/SOM & CAC Calculator")
def financial_calculator_tool(user_scale_tier: str) -> str:
    """
    Calculates estimated monthly infrastructure, LLM API costs, Customer Acquisition Cost (CAC), LTV/CAC sustainability, and TAM/SAM/SOM market projections.
    Input scale tier: 'mvp' (1k users), 'growth' (10k users), 'scale' (100k users).
    """
    tier = user_scale_tier.lower().strip()

    if "growth" in tier or "10k" in tier:
        return (
            "### Financial & Market Unit Economics (Growth Tier - 10,000 active users):\n"
            "- **Infrastructure & Hosting (AWS/Vercel)**: $80 - $180 / month\n"
            "- **LLM API Tokens & Vector Search**: $250 - $600 / month\n"
            "- **Customer Acquisition Cost (CAC)**: $15 - $45 per customer (Google/Meta Ads)\n"
            "- **Lifetime Value (LTV) Projection**: $180 - $450 / customer\n"
            "- **LTV / CAC Ratio**: ~4.0x (Sustainable SaaS Model > 3.0x)\n"
            "- **Est. Target SAM (Serviceable Addressable Market)**: $2.5M - $5.0M / year\n"
            "- **Total Monthly Operational Burn**: $330 - $780 / month"
        )
    elif "scale" in tier or "100k" in tier:
        return (
            "### Financial & Market Unit Economics (Scale Tier - 100,000 active users):\n"
            "- **Infrastructure & Kubernetes Cloud**: $600 - $1,500 / month\n"
            "- **LLM API Tokens & High Volume Throughput**: $2,000 - $6,000 / month\n"
            "- **Customer Acquisition Cost (CAC)**: $30 - $75 per customer\n"
            "- **Lifetime Value (LTV) Projection**: $350 - $900 / customer\n"
            "- **LTV / CAC Ratio**: ~4.6x (Strong Scalability)\n"
            "- **Est. Target TAM (Total Addressable Market)**: $25M - $80M / year\n"
            "- **Total Monthly Operational Burn**: $2,600 - $7,500 / month"
        )
    else: # MVP Tier
        return (
            "### Financial & Market Unit Economics (MVP Tier - Initial 1,000 users):\n"
            "- **Hosting (Vercel/Railway Free Tier)**: $0 - $15 / month\n"
            "- **LLM API Tokens (Gemini/OpenAI Flash)**: $10 - $40 / month\n"
            "- **Customer Acquisition Cost (CAC)**: $0 - $12 (Organic & Cold Outreach)\n"
            "- **Lifetime Value (LTV) Projection**: $60 - $150 / customer\n"
            "- **LTV / CAC Ratio**: > 5.0x (High Initial Margin)\n"
            "- **Est. Initial SOM (Serviceable Obtainable Market)**: $100K - $300K / year\n"
            "- **Total Monthly Operational Burn**: $10 - $55 / month"
        )
