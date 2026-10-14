import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🚀 Çok Ajanlı Fikir Test Etme Sistemi (Jupyter Notebook Edition)\n",
                "Bu notebook, bir ürün veya girişim fikrini **5 otonom yapay zekâ ajanı** ile canlı araştırmalar yaparak **GO / CONDITIONAL GO / NO-GO** raporuna dönüştürür."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📦 1. Adım: Paket Yükleme"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Bağımlılıkları yükleyin (İlk çalıştırmada gereklidir)\n",
                "!pip install crewai crewai-tools langchain-google-genai duckduckgo-search python-dotenv"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🔑 2. Adım: Gemini API Anahtarı ve LLM Ayarları"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "from crewai import LLM\n",
                "\n",
                "# ⚠️ Buraya kendi Google Gemini API Key'inizi yazın (https://aistudio.google.com/)\n",
                "os.environ[\"GEMINI_API_KEY\"] = \"YOUR_GEMINI_API_KEY_HERE\"\n",
                "\n",
                "# LLM Tanımlama (Gemini 1.5 Flash)\n",
                "llm = LLM(\n",
                "    model=\"gemini/gemini-1.5-flash\",\n",
                "    api_key=os.environ.get(\"GEMINI_API_KEY\"),\n",
                "    temperature=0.7\n",
                ")\n",
                "print(\"✅ LLM başarıyla yapılandırıldı!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🛠️ 3. Adım: Özel Ajan Araçlarının (Custom Tools) Tanımlanması"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from crewai.tools import tool\n",
                "from duckduckgo_search import DDGS\n",
                "\n",
                "@tool(\"Web Search Tool\")\n",
                "def web_search_tool(query: str) -> str:\n",
                "    \"\"\"Searches the live web using DuckDuckGo for competitor info, market trends, user reviews, or news.\"\"\"\n",
                "    try:\n",
                "        results = []\n",
                "        with DDGS() as ddgs:\n",
                "            for r in ddgs.text(query, max_results=5):\n",
                "                results.append(f\"Title: {r.get('title')}\\nURL: {r.get('href')}\\nSnippet: {r.get('body')}\\n\")\n",
                "        return \"\\n---\\n\".join(results) if results else f\"No search results found for: '{query}'\"\n",
                "    except Exception as e:\n",
                "        return f\"Error executing search: {str(e)}\"\n",
                "\n",
                "@tool(\"GitHub Search Tool\")\n",
                "def github_search_tool(query: str) -> str:\n",
                "    \"\"\"Searches GitHub repositories for open source libraries, tools, and technical precedents.\"\"\"\n",
                "    try:\n",
                "        search_query = f\"{query} site:github.com\"\n",
                "        results = []\n",
                "        with DDGS() as ddgs:\n",
                "            for r in ddgs.text(search_query, max_results=4):\n",
                "                results.append(f\"Repo/Project: {r.get('title')}\\nURL: {r.get('href')}\\nSummary: {r.get('body')}\\n\")\n",
                "        return \"\\n---\\n\".join(results) if results else f\"No GitHub repos found for: '{query}'\"\n",
                "    except Exception as e:\n",
                "        return f\"Error searching GitHub: {str(e)}\"\n",
                "\n",
                "@tool(\"Infrastructure & API Cost Calculator\")\n",
                "def cost_calculator_tool(user_scale_tier: str) -> str:\n",
                "    \"\"\"Calculates estimated monthly API and cloud infrastructure operational costs.\"\"\"\n",
                "    tier = user_scale_tier.lower().strip()\n",
                "    if \"growth\" in tier or \"10k\" in tier:\n",
                "        return \"### Monthly Cost (Growth Tier - 10k users):\\n- Hosting: $50-$120/mo\\n- API Tokens: $150-$400/mo\\n- Total: $245-$610/mo\"\n",
                "    elif \"scale\" in tier or \"100k\" in tier:\n",
                "        return \"### Monthly Cost (Scale Tier - 100k users):\\n- Hosting: $450-$1,200/mo\\n- API Tokens: $1,500-$4,500/mo\\n- Total: $2,250-$6,500/mo\"\n",
                "    else:\n",
                "        return \"### Monthly Cost (MVP Tier - 1k users):\\n- Hosting: $0-$15/mo\\n- API Tokens: $5-$35/mo\\n- Total: $5-$50/mo\"\n",
                "\n",
                "print(\"✅ Özel araçlar (Web Search, GitHub Search, Cost Calculator) tanımlandı!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🤖 4. Adım: 5 Otonom Ajanın Oluşturulması"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from crewai import Agent\n",
                "\n",
                "# 1. Market & Competitor Agent\n",
                "market_agent = Agent(\n",
                "    role=\"Senior Market Analyst & Competitive Intelligence Lead\",\n",
                "    goal=\"Identify top competitors, market gaps, market size, and Unique Value Proposition (USP).\",\n",
                "    backstory=\"Experienced VC market analyst specializing in competitive intelligence and market dynamics.\",\n",
                "    tools=[web_search_tool],\n",
                "    llm=llm,\n",
                "    verbose=True\n",
                ")\n",
                "\n",
                "# 2. Demand & Sentiment Agent\n",
                "demand_agent = Agent(\n",
                "    role=\"Consumer Demand & Sentiment Specialist\",\n",
                "    goal=\"Uncover real user pain points, community sentiment, and existing demand patterns.\",\n",
                "    backstory=\"Digital customer researcher expert in online discussions, customer reviews, and search intent.\",\n",
                "    tools=[web_search_tool],\n",
                "    llm=llm,\n",
                "    verbose=True\n",
                ")\n",
                "\n",
                "# 3. Technical Feasibility Agent\n",
                "tech_agent = Agent(\n",
                "    role=\"Principal Software Architect & Technical Feasibility Lead\",\n",
                "    goal=\"Assess technical complexity, recommend tech stack, leverage open-source code, and estimate MVP build time.\",\n",
                "    backstory=\"Veteran CTO with expertise in full-stack architecture, AI system integration, and rapid prototyping.\",\n",
                "    tools=[github_search_tool, web_search_tool],\n",
                "    llm=llm,\n",
                "    verbose=True\n",
                ")\n",
                "\n",
                "# 4. Financial & Legal Agent\n",
                "financial_agent = Agent(\n",
                "    role=\"Fintech Cost Modeler & Compliance Auditor\",\n",
                "    goal=\"Estimate infrastructure/API costs, model unit economics, and highlight regulatory risks (KVKK, GDPR).\",\n",
                "    backstory=\"Technology CFO and legal compliance strategist analyzing business model sustainability.\",\n",
                "    tools=[cost_calculator_tool],\n",
                "    llm=llm,\n",
                "    verbose=True\n",
                ")\n",
                "\n",
                "# 5. Judge Agent (Decision Engine)\n",
                "judge_agent = Agent(\n",
                "    role=\"Chief Investment Officer & System Judge\",\n",
                "    goal=\"Synthesize reports from all research agents, apply weighted scoring, and render GO / CONDITIONAL GO / NO-GO verdict.\",\n",
                "    backstory=\"Top-tier investment committee judge known for data-driven and pragmatic evaluations.\",\n",
                "    tools=[],\n",
                "    llm=llm,\n",
                "    verbose=True\n",
                ")\n",
                "\n",
                "print(\"✅ 5 Otonom Ajan başarıyla oluşturuldu!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📝 5. Adım: Test Edilecek Fikrin Belirlenmesi"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Buradaki bilgileri kendi fikirlerinize göre değiştirebilirsiniz:\n",
                "IDEA_TITLE = \"AI E-Ticaret İade Asistanı\"\n",
                "IDEA_DESCRIPTION = \"E-ticaret siteleri için müşteri iadelerini otomatik yöneten, kargo entegrasyonu sağlayan ve dolandırıcılık tespiti yapan otonom yapay zeka asistanı.\"\n",
                "TARGET_AUDIENCE = \"Shopify ve WooCommerce kullanan orta ölçekli e-ticaret mağaza sahipleri\"\n",
                "\n",
                "print(f\"📌 Test Fikri: {IDEA_TITLE}\")\n",
                "print(f\"🎯 Hedef Kitle: {TARGET_AUDIENCE}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📋 6. Adım: Görevlerin (Tasks) Tanımlanması"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from crewai import Task\n",
                "\n",
                "task_market = Task(\n",
                "    description=f\"Conduct market research for '{IDEA_TITLE}' ({IDEA_DESCRIPTION}). Find at least 3 competitors, market gaps, and USP.\",\n",
                "    expected_output=\"Competitor Table, Market Gap Analysis, and USP Recommendation.\",\n",
                "    agent=market_agent\n",
                ")\n",
                "\n",
                "task_demand = Task(\n",
                "    description=f\"Analyze user demand and pain points for '{IDEA_TITLE}' targeting '{TARGET_AUDIENCE}'. Rate demand urgency (1-10).\",\n",
                "    expected_output=\"Top 3 Pain Points, Community Sentiment, and Urgency Score.\",\n",
                "    agent=demand_agent\n",
                ")\n",
                "\n",
                "task_tech = Task(\n",
                "    description=f\"Evaluate technical feasibility for '{IDEA_TITLE}'. Recommend tech stack, GitHub repos, and estimate MVP build duration.\",\n",
                "    expected_output=\"Recommended Tech Stack, Open-Source Repos, and MVP Timeline.\",\n",
                "    agent=tech_agent\n",
                ")\n",
                "\n",
                "task_financial = Task(\n",
                "    description=f\"Estimate monthly API/cloud costs (MVP vs Growth vs Scale) and compliance risks (GDPR/KVKK) for '{IDEA_TITLE}'.\",\n",
                "    expected_output=\"Monthly Cost Estimates, Monetization Model, and Legal Risks.\",\n",
                "    agent=financial_agent\n",
                ")\n",
                "\n",
                "task_judge = Task(\n",
                "    description=(\n",
                "        f\"Synthesize reports from all research agents for '{IDEA_TITLE}'.\\n\"\n",
                "        \"1. Calculate an Overall Idea Score (0-100).\\n\"\n",
                "        \"2. Render a verdict: **GO** (Score >= 75), **CONDITIONAL GO** (Score 55-74), or **NO-GO** (Score < 55).\\n\"\n",
                "        \"3. Provide top 3 action items or pivot advice.\"\n",
                "    ),\n",
                "    expected_output=\"Comprehensive Executive Verdict Report with Final Score, GO/NO-GO Verdict, and Action Plan.\",\n",
                "    agent=judge_agent\n",
                ")\n",
                "\n",
                "print(\"✅ Tüm görevler başarıyla bağlandı!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🚀 7. Adım: Crew'i Çalıştırma & Hakem Raporu Alma"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from crewai import Crew, Process\n",
                "from IPython.display import Markdown\n",
                "\n",
                "crew = Crew(\n",
                "    agents=[market_agent, demand_agent, tech_agent, financial_agent, judge_agent],\n",
                "    tasks=[task_market, task_demand, task_tech, task_financial, task_judge],\n",
                "    process=Process.sequential,\n",
                "    verbose=True\n",
                ")\n",
                "\n",
                "print(\"🚀 Ajanlar çalışmaya başlıyor... (Bu işlem 2-4 dakika sürebilir)\")\n",
                "result = crew.kickoff()\n",
                "\n",
                "# Sonucu ekranda formatlı Markdown olarak göster\n",
                "Markdown(str(result))"
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

output_path = r"c:\Users\SPECIAL TEK\OneDrive\Masaüstü\projects_2026\test-your-idea\idea_validation_notebook.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("SUCCESS: Notebook written cleanly!")
