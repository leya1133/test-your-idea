# 🚀 TSI – Test Your Idea

**A multi-agent AI system that stress-tests a startup or product idea and returns a Go / No-Go verdict.**

Five specialized [CrewAI](https://www.crewai.com/) agents research an idea from every angle — market, demand, technical feasibility, cost and legal risk — and a judge agent turns their findings into a weighted score and a final decision. The specialist agents run **in parallel** with `asyncio`, which brings a full analysis down to **~25 seconds**.

![TSI screenshot](1.png)

---

## 🤖 The agent team

| Agent | What it does |
|---|---|
| 🧹 **Filter** | Sanitizes the input and checks that the idea is specific enough to analyze |
| 📊 **Market & Competitor Specialist** | Scans the market and competitors with live web search and finds gaps |
| 💬 **Demand & Sentiment Specialist** | Estimates how urgently people feel the problem and analyzes sentiment |
| 🛠️ **Technical Feasibility Lead** | Searches GitHub projects and libraries to size the MVP and pick a tech stack |
| 💰 **Financial & Legal Auditor** | Simulates cloud / API costs and flags compliance risks (KVKK, GDPR) |
| ⚖️ **Chief Investment Officer (Judge)** | Synthesizes every report, applies a deterministic weighted scoring engine and decides **GO / CONDITIONAL GO / NO-GO** |

After the verdict you can keep asking the judge questions about the report; answers are grounded in the analysis through a small **RAG** layer.

## 🧱 Tech stack

Python · CrewAI · FastAPI · asyncio · OpenAI (`gpt-4o-mini`) · DuckDuckGo search · GitHub API · HTML/CSS/JS dashboard

```
app/
├── agents/        # one module per agent
├── tasks/         # task definitions for each agent
├── tools/         # web search, GitHub search, cost simulation
├── evaluators/    # deterministic scoring engine
├── rag/           # retrieval layer for follow-up questions
├── security/      # input sanitization
├── crew.py        # sequential crew (CLI)
└── server.py      # FastAPI server with parallel execution
frontend/          # web dashboard
main.py            # CLI entry point
```

## ⚙️ Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your own OpenAI API key:

```env
OPENAI_API_KEY="your-openai-api-key"
MODEL=openai/gpt-4o-mini
```

## ▶️ Run

**Web dashboard** (http://127.0.0.1:8000)

```bash
python -m app.server
```

**Command line**

```bash
python main.py "AI Return Assistant" "An autonomous bot that handles customer returns for e-commerce stores" "Shopify sellers"
```

The full judge report is printed to the console and saved to `output_report.md`.

---

Built by [Layan Bassout](https://leya1133.github.io) during an AI internship at Prodrom ICT Solutions, Fırat Technopark.
