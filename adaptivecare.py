"""Streamlit AdaptiveCare v2 interface: rule-based, educational, session-only."""
from datetime import date
import streamlit as st
from adaptive_engine import GOALS, STAGES, CAPACITIES, CONCERNS, build_plan, progress_summary

def render_adaptivecare():
    st.title("🌱 AdaptiveCare")
    st.caption("Experimental, rule-based maternal wellness habit support • Educational demonstration")
    st.warning("Not clinically reviewed or validated. Not a medical device, diagnosis, symptom checker, triage tool or emergency service. For urgent or severe symptoms, seek immediate in-person medical care.")
    st.info("Demo privacy: check-ins exist only in this Streamlit session; they are not synced across visits or sent to healthcare providers. Do not enter personal or medical information.")
    if "adaptivecare_v2_log" not in st.session_state:
        st.session_state.adaptivecare_v2_log = []
    log = st.session_state.adaptivecare_v2_log
    if st.session_state.pop("ac_saved_notice", False):
        st.success("Check-in saved. Suggestions have been refreshed using the latest session record.")
    stage = st.selectbox("Wellness context", STAGES, key="ac_stage")
    goal = st.selectbox("Choose one wellness goal", list(GOALS), key="ac_goal")
    capacity = st.select_slider("How much energy do you have for a small step today?", options=CAPACITIES, value="Moderate", key="ac_capacity")
    setback = st.checkbox("I missed a previous goal or need an easier restart", key="ac_setback")
    concern = st.selectbox("Do you need professional support?", CONCERNS, key="ac_concern")
    previous = next((row["completed"] for row in reversed(log) if row.get("goal") == goal), None)
    plan = build_plan(stage, goal, capacity, setback, concern, previous)
    if plan.urgency != "none":
        if plan.urgency == "urgent":
            st.error(plan.support)
        else:
            st.warning(plan.support)
        st.caption("Personal wellness planning and check-in controls are hidden when you request health assistance.")
        return

    st.subheader("Your optional small steps")
    st.write(plan.message)
    for action in plan.actions:
        st.write("• " + action)
    with st.expander("Why were these suggestions shown?"):
        for reason in plan.explanation:
            st.write("• " + reason)
        st.caption("Transparent if/then rules based on your choices; no AI diagnosis or machine-learning prediction.")

    completed = st.checkbox("I completed at least one suggested step today", key="ac_completed")
    if st.button("Save today's check-in", type="primary", key="ac_save"):
        if log and log[-1]["date"] == date.today().isoformat() and log[-1]["goal"] == goal:
            st.info("You already saved a check-in for this goal today. You can clear the session and retest if needed.")
        else:
            log.append({"date": date.today().isoformat(), "context": stage,
                        "goal": goal, "energy": capacity, "restart": setback,
                        "completed": bool(completed)})
            st.session_state.ac_saved_notice = True
            st.rerun()

    st.subheader("Wellness check-in dashboard")
    summary = progress_summary(log)
    left, right = st.columns(2)
    left.metric("Check-ins this session", summary["checkins"])
    right.metric("Self-reported completed check-ins", summary["completed"])
    if log:
        st.progress(summary["completion_fraction"])
        st.caption("Share of check-ins marked completed; NOT a measure of medical outcomes or clinical adherence.")
        st.dataframe(list(reversed(log)), use_container_width=True, hide_index=True)
        if st.button("Clear session records", key="ac_clear"):
            st.session_state.adaptivecare_v2_log = []
            st.rerun()
    st.caption("This version intentionally stores no medical history, names, symptoms, or location. There are no automatic notifications or provider integrations. For early pilot use, clinical, privacy, security and accessibility reviews are still required.")
