import os
import uuid
import time
import asyncio
from typing import Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import nest_asyncio
nest_asyncio.apply()

from app.security.sanitizer import sanitize_user_input
from app.tasks.filter_task import get_filter_task
from app.tasks.market_task import get_market_task
from app.tasks.demand_task import get_demand_task
from app.tasks.tech_task import get_tech_task
from app.tasks.financial_task import get_financial_task
from app.tasks.judge_task import get_judge_task
from app.agents.judge_agent import get_judge_agent
from crewai import Crew, Process, Task

app = FastAPI(
    title="TSI - Test Your Idea Enterprise v4.0",
    version="4.0.0",
    docs_url="/api/docs",
    redoc_url=None
)

# Enable Hardened CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# In-memory job store with TTL metadata
JOBS: Dict[str, Dict[str, Any]] = {}
JOB_TTL_SECONDS = 3600  # 1 Hour TTL

class EvaluateRequest(BaseModel):
    title: str
    description: str
    target_audience: str

class AskJudgeRequest(BaseModel):
    job_id: str
    question: str

def purge_expired_jobs():
    """
    Background garbage collector that purges jobs older than TTL (1 hour)
    to prevent in-memory data leaks and memory exhaustion.
    """
    now = time.time()
    expired_ids = [
        job_id for job_id, job_data in JOBS.items()
        if now - job_data.get("created_at", now) > JOB_TTL_SECONDS
    ]
    for job_id in expired_ids:
        JOBS.pop(job_id, None)

async def run_single_task_async(task: Task) -> str:
    """Helper to run an individual task in its own Crew instance for parallel execution."""
    crew = Crew(agents=[task.agent], tasks=[task], verbose=False)
    res = await crew.kickoff_async()
    return str(res)

def run_crew_job(job_id: str, title: str, description: str, target_audience: str):
    """
    Executes the CrewAI workflow with Parallel Research Execution & Skeptic VC Judge Synthesis.
    """
    try:
        purge_expired_jobs()
        
        JOBS[job_id]["status"] = "running"
        JOBS[job_id]["current_step"] = "0. Saniye Güvenlik & Ön Kontrol Filtresinde..."

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Step 0: Pre-Validation Filter Task
        filter_task = get_filter_task(title, description, target_audience)
        filter_crew = Crew(agents=[filter_task.agent], tasks=[filter_task], verbose=False)
        filter_res = loop.run_until_complete(filter_crew.kickoff_async())
        filter_output = str(filter_res).upper()

        if "INVALID_SPAM" in filter_output:
            JOBS[job_id]["status"] = "failed"
            JOBS[job_id]["error"] = f"Ön Kontrol Filtresi: {filter_output}. Lütfen geçerli bir iş fikri giriniz."
            loop.close()
            return

        JOBS[job_id]["current_step"] = "1-4. Ajanlar Paralel Taramada (Pazar, Talep, Teknik, Finans)..."

        # Step 1-4: Parallel Research Agent Tasks
        task_market = get_market_task(title, description, target_audience)
        task_demand = get_demand_task(title, description, target_audience)
        task_tech = get_tech_task(title, description, target_audience)
        task_financial = get_financial_task(title, description, target_audience)

        # Execute 4 research tasks in parallel for 5x speed boost
        parallel_results = loop.run_until_complete(asyncio.gather(
            run_single_task_async(task_market),
            run_single_task_async(task_demand),
            run_single_task_async(task_tech),
            run_single_task_async(task_financial)
        ))

        agent_names = [
            "📊 Market & Competitor Agent (market_agent.py)",
            "💬 Demand & Sentiment Agent (demand_agent.py)",
            "🛠️ Technical Feasibility Agent (tech_agent.py)",
            "💰 Financial & Legal Agent (financial_agent.py)"
        ]

        task_outputs = []
        for idx, res_text in enumerate(parallel_results):
            task_outputs.append({
                "agent_name": agent_names[idx],
                "output": res_text
            })

        JOBS[job_id]["agent_outputs"] = task_outputs
        JOBS[job_id]["current_step"] = "5. Hakem (Judge) Ajanı Sentez Raporunu Hazırlıyor..."

        # Step 5: Judge Agent Synthesis Task
        task_judge = get_judge_task(title, description, target_audience)
        judge_crew = Crew(agents=[task_judge.agent], tasks=[task_judge], verbose=True)
        final_verdict_res = loop.run_until_complete(judge_crew.kickoff_async())
        loop.close()

        final_report_str = str(final_verdict_res)

        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["current_step"] = "Tamamlandı"
        JOBS[job_id]["final_report"] = final_report_str

    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)
        print(f"[ERROR] Job {job_id} failed: {e}")

@app.post("/api/evaluate")
def evaluate_idea(req: EvaluateRequest, background_tasks: BackgroundTasks):
    clean_title = sanitize_user_input(req.title, max_length=200)
    clean_description = sanitize_user_input(req.description, max_length=2000)
    clean_target = sanitize_user_input(req.target_audience, max_length=300)

    if not clean_title or not clean_description:
        raise HTTPException(status_code=400, detail="Fikir başlığı ve açıklaması zorunludur.")
    
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        "job_id": job_id,
        "title": clean_title,
        "description": clean_description,
        "target_audience": clean_target,
        "status": "pending",
        "current_step": "Ajanlar hazırlanıyor...",
        "agent_outputs": [],
        "final_report": "",
        "error": None,
        "created_at": time.time()
    }

    background_tasks.add_task(run_crew_job, job_id, clean_title, clean_description, clean_target)
    return {"job_id": job_id, "status": "pending"}

@app.get("/api/status/{job_id}")
def get_job_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="İşlem bulunamadı veya oturum süresi doldu.")
    return JOBS[job_id]

from app.rag.vector_rag import rag_engine

@app.post("/api/ask-judge")
def ask_judge_followup(req: AskJudgeRequest):
    """
    Interactive Q&A Endpoint: Uses RAG (Retrieval-Augmented Generation) to answer founder questions
    without hallucination by retrieving exact chunks from previous research reports.
    """
    job_id = req.job_id
    question = sanitize_user_input(req.question, max_length=500)

    if job_id not in JOBS or JOBS[job_id]["status"] != "completed":
        raise HTTPException(status_code=400, detail="Önce geçerli bir test analizi tamamlanmalıdır.")

    try:
        job = JOBS[job_id]
        
        # Retrieve RAG Context
        rag_context = rag_engine.retrieve(question, top_k=2)

        judge_agent = get_judge_agent()
        
        prompt = (
            f"You are the Skeptic VC Chief Investment Officer evaluating '{job['title']}'.\n"
            f"Grounding RAG Context:\n{rag_context}\n\n"
            f"Previous Executive Report:\n{job['final_report']}\n\n"
            f"The founder asks you this follow-up question: '{question}'.\n"
            f"Provide a concise, direct, and actionable advice based strictly on the ground data."
        )

        qa_task = Task(
            description=prompt,
            expected_output="A direct, concise, actionable answer backed by RAG context.",
            agent=judge_agent
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        qa_crew = Crew(agents=[judge_agent], tasks=[qa_task], verbose=False)
        answer_res = loop.run_until_complete(qa_crew.kickoff_async())
        loop.close()

        return {"job_id": job_id, "question": question, "answer": str(answer_res)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hakem yanıtı oluşturulamadı: {str(e)}")

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if not os.path.exists(frontend_dir):
    os.makedirs(frontend_dir, exist_ok=True)

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=True)
