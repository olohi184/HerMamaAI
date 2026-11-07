"""Pure, explainable, non-clinical wellness habit suggestion engine."""
from dataclasses import dataclass
from typing import Optional

GOALS = {
    "Rest and recovery": ("Take a short rest break", "Set aside a quiet wind-down period"),
    "Emotional wellbeing": ("Try a two-minute quiet breathing pause if comfortable", "Write down one kind or supportive thought"),
    "Social connection": ("Send a brief check-in to a trusted person", "Ask a trusted person for practical support if helpful"),
    "Care preparation": ("Write down one question for your next care visit", "Review the date and location of your next booked visit"),
}
CONCERNS = ("None", "I have a health concern", "I need urgent medical help")
STAGES = ("Pregnancy", "Postpartum", "General maternal wellbeing")
CAPACITIES = ("Low", "Moderate", "High")

@dataclass(frozen=True)
class Plan:
    actions: tuple[str, ...]
    explanation: tuple[str, ...]
    message: str
    support: str
    urgency: str

def build_plan(stage: str, goal: str, capacity: str, setback: bool,
               concern: str, previous_completed: Optional[bool] = None) -> Plan:
    """Safety always overrides habit suggestions. No diagnosis or clinical triage."""
    if concern not in CONCERNS or stage not in STAGES or goal not in GOALS or capacity not in CAPACITIES:
        raise ValueError("Unknown selection")
    if concern == "I need urgent medical help":
        return Plan((), ("You indicated you need urgent medical help.",),
                    "Wellness suggestions are paused.",
                    "Seek immediate in-person medical assistance or contact your local emergency service. This app cannot assess urgency or provide emergency care.", "urgent")
    if concern == "I have a health concern":
        return Plan((), ("You indicated you have a health concern.",),
                    "Wellness suggestions are paused until you get appropriate advice.",
                    "Contact a qualified midwife, doctor or healthcare facility. This application does not assess symptoms, diagnose, or recommend treatment.", "concern")
    reasons = [f"You selected {goal.lower()} as your wellness goal."]
    simpler = capacity == "Low" or setback or previous_completed is False
    if capacity == "Low":
        reasons.append("You selected low energy, so the plan offers one optional small step.")
    else:
        reasons.append(f"You selected {capacity.lower()} energy.")
    if setback:
        reasons.append("You asked for an easier restart after a missed goal.")
    if previous_completed is False:
        reasons.append("Your last recorded check-in was incomplete, so the plan stays simple.")
    elif previous_completed is True:
        reasons.append("Your previous check-in recorded a completed small step.")
    reasons.append(f"The context is {stage.lower()}; this does not change clinical advice or imply stage-specific medical recommendations.")
    actions = GOALS[goal][:1] if simpler else GOALS[goal]
    message = ("One optional small step is enough; restarting is okay." if simpler
               else "Choose from these optional small steps; you can adjust at any time.")
    return Plan(tuple(actions), tuple(reasons), message, "", "none")

def progress_summary(rows: list[dict]) -> dict:
    total = len(rows)
    completed = sum(1 for row in rows if row.get("completed") is True)
    return {"checkins": total, "completed": completed,
            "completion_fraction": completed / total if total else 0.0}
