"""AdaptiveCare: non-clinical, session-only maternal wellness prototype."""
from datetime import date, timedelta
import streamlit as st

GOALS = {
    "Rest and recovery": ["Take a short rest break", "Set aside a quiet wind-down period"],
    "Emotional wellbeing": ["Try a two-minute breathing exercise", "Write down one supportive thought"],
    "Social connection": ["Check in with a trusted person", "Ask someone for practical support"],
    "Care preparation": ["Write down questions for your next care visit", "Check your upcoming appointment details"],
}
CONCERNS = ("None", "I have a health concern", "I need urgent medical help")

def plan_for(goal, capacity, setback):
    actions = GOALS[goal]
    if capacity == "Low" or setback:
        return [actions[0]], "A smaller step is enough today. You can restart without catching up."
    return actions, "Choose manageable steps and adjust whenever you need."

def render_adaptivecare():
    st.title("🌱 AdaptiveCare")
    st.caption("Experimental maternal wellness habit support • Educational only • No diagnosis or treatment")
    st.warning("Not clinically reviewed. For urgent or severe symptoms, seek immediate in-person medical care or local emergency services. Do not rely on this app for triage.")
    st.info("This demo stores entries only in the current Streamlit session. Do not enter names, medical records or sensitive health information.")
    stage = st.selectbox("Wellness context", ["Pregnancy", "Postpartum", "General maternal wellbeing"])
    goal = st.selectbox("Choose one wellness goal", list(GOALS))
    capacity = st.select_slider("How much energy do you have for a small step today?", options=["Low", "Moderate", "High"], value="Moderate")
    setback = st.checkbox("I missed a previous goal or need an easier restart")
    concern = st.selectbox("Do you need professional support?", CONCERNS)
    if concern == CONCERNS[2]:
        st.error("Please seek immediate in-person medical assistance or contact your local emergency service. This prototype cannot assess urgency.")
        return
    if concern == CONCERNS[1]:
        st.warning("Contact a qualified midwife, doctor or healthcare facility for advice. This app cannot assess symptoms or recommend care.")
    actions, message = plan_for(goal, capacity, setback)
    st.subheader("Your suggested small steps")
    st.write(message)
    for action in actions:
        st.write("• " + action)
    if "adaptivecare_log" not in st.session_state:
        st.session_state.adaptivecare_log = []
    completed = st.checkbox("I completed at least one suggested step today", key="adaptivecare_done")
    if st.button("Save today's check-in", type="primary"):
        st.session_state.adaptivecare_log.append({
            "date": date.today().isoformat(), "context": stage,
            "goal": goal, "capacity": capacity, "setback": setback,
            "completed": completed
        })
        st.success("Check-in saved for this browser session.")
    log = st.session_state.adaptivecare_log
    st.subheader("Progress in this session")
    st.metric("Check-ins", len(log))
    if log:
        st.metric("Steps completed", sum(int(item["completed"]) for item in log))
        st.progress(sum(int(item["completed"]) for item in log) / len(log))
        st.dataframe(log, use_container_width=True, hide_index=True)
        if st.button("Clear session check-ins"):
            st.session_state.adaptivecare_log = []
            st.rerun()
    st.caption("Prototype metrics describe recorded interactions, not clinical outcomes or proven behaviour change.")
