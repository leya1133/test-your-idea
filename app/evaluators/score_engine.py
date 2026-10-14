from pydantic import BaseModel, Field
from typing import Dict, Any

class IdeaEvaluationMetrics(BaseModel):
    market_score: int = Field(description="Market opportunity score (0-100)", ge=0, le=100)
    demand_score: int = Field(description="User demand & pain point urgency score (0-100)", ge=0, le=100)
    tech_feasibility_score: int = Field(description="Technical feasibility & implementation ease score (0-100)", ge=0, le=100)
    financial_viability_score: int = Field(description="Financial burn rate & legal compliance score (0-100)", ge=0, le=100)

def calculate_deterministic_score(market: int, demand: int, tech: int, financial: int) -> Dict[str, Any]:
    """
    Computes a hardcoded deterministic final score using weighted formula:
    Score = (Market * 0.30) + (Demand * 0.25) + (Tech * 0.25) + (Financial * 0.20)
    
    Returns strict decision: GO (>=75), CONDITIONAL GO (55-74), NO-GO (<55)
    """
    final_score = round(
        (market * 0.30) +
        (demand * 0.25) +
        (tech * 0.25) +
        (financial * 0.20),
        1
    )

    if final_score >= 75.0:
        verdict = "GO"
        verdict_turkish = "🟢 GO (Devam Et - Yüksek Potansiyel)"
    elif final_score >= 55.0:
        verdict = "CONDITIONAL GO"
        verdict_turkish = "🟡 CONDITIONAL GO (Şartlı Devam - Riskleri İyileştir)"
    else:
        verdict = "NO-GO"
        verdict_turkish = "🔴 NO-GO (Devam Etmeyin - Yüksek Risk / Yetersiz Pazar)"

    return {
        "final_score": final_score,
        "verdict": verdict,
        "verdict_turkish": verdict_turkish,
        "breakdown": {
            "market_weighted": round(market * 0.30, 1),
            "demand_weighted": round(demand * 0.25, 1),
            "tech_weighted": round(tech * 0.25, 1),
            "financial_weighted": round(financial * 0.20, 1)
        }
    }
