"""Adaptive Recovery Intelligence: deterministic, non-clinical wellness planning."""
from datetime import date, timedelta
from dataclasses import replace
from adaptive_engine import build_plan

def recovery_plan(*, stage, goal, capacity, setback, concern, sleep, stress,
                  history=(), today=None):
    today = today or date.today()
    if sleep not in ("Restful", "Interrupted", "Poor") or stress not in ("Low", "Moderate", "High"):
        raise ValueError("Unknown wellness selection")
    base = build_plan(stage, goal, capacity, setback, concern)
    if base.urgency != "none":
        return base
    past = sorted((r for r in history if r.get("goal") == goal
                   and r.get("date", "") < today.isoformat()), key=lambda r: r["date"])
    last = past[-1] if past else None
    reasons = []
    if sleep in ("Poor", "Interrupted"):
        reasons.append("You reported disrupted rest.")
    if stress == "High":
        reasons.append("You reported high stress.")
    if last and last.get("completed") is False:
        reasons.append("Your last recorded activity was not completed.")
    if last and (today - date.fromisoformat(last["date"])).days > 1:
        reasons.append("There is a gap in your recorded check-ins; this does not mean you missed care.")
    if capacity == "Low" or setback or reasons:
        return replace(base, actions=base.actions[:1],
                       explanation=base.explanation + tuple(reasons),
                       message="Comeback Coach: choose one optional small step or rest today. You can restart whenever ready.")
    return base

def weekly_progress(history, today=None):
    """Count unique recorded days, not clinical adherence or health outcomes."""
    today = today or date.today()
    start = today - timedelta(days=6)
    days = {r["date"] for r in history if start.isoformat() <= r.get("date", "") <= today.isoformat()}
    completed = {r["date"] for r in history if r.get("completed") is True and r.get("date") in days}
    streak = 0
    cursor = today if today.isoformat() in completed else today - timedelta(days=1)
    while cursor.isoformat() in completed:
        streak += 1
        cursor -= timedelta(days=1)
    return {"recorded_days": len(days), "completed_days": len(completed), "weekly_streak": streak}
