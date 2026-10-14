from crewai import Crew, Process
from app.tasks.market_task import get_market_task
from app.tasks.demand_task import get_demand_task
from app.tasks.tech_task import get_tech_task
from app.tasks.financial_task import get_financial_task
from app.tasks.judge_task import get_judge_task

def run_idea_validation(idea_title: str, idea_description: str, target_audience: str) -> str:
    """
    Orchestrates the multi-agent idea validation workflow using isolated agent modules.
    """
    task_market = get_market_task(idea_title, idea_description, target_audience)
    task_demand = get_demand_task(idea_title, idea_description, target_audience)
    task_tech = get_tech_task(idea_title, idea_description, target_audience)
    task_financial = get_financial_task(idea_title, idea_description, target_audience)
    task_judge = get_judge_task(idea_title, idea_description, target_audience)

    tasks_list = [task_market, task_demand, task_tech, task_financial, task_judge]
    agents_list = [t.agent for t in tasks_list]

    crew = Crew(
        agents=agents_list,
        tasks=tasks_list,
        process=Process.sequential,
        verbose=True
    )

    print("\n" + "="*70)
    print(f"🚀 TSI Launching Modular Crew for: '{idea_title}'")
    print("="*70 + "\n")

    result = crew.kickoff()
    return str(result)
