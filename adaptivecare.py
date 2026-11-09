"""Streamlit AdaptiveCare v2 interface: rule-based, educational, session-only."""
from datetime import date
import streamlit as st
from localization.language_manager import t, display_option
from adaptive_engine import GOALS, STAGES, CAPACITIES, CONCERNS, build_plan, progress_summary

def render_adaptivecare():
    st.title("🌱 AdaptiveCare")
    st.caption(t("ac.intro"))
    st.warning("Not clinically reviewed or validated. Not a medical device, diagnosis, symptom checker, triage tool or emergency service. For urgent or severe symptoms, seek immediate in-person medical care.")
    st.info("Demo privacy: check-ins exist only in this Streamlit session; they are not synced across visits or sent to healthcare providers. Do not enter personal or medical information.")
    if "adaptivecare_v2_log" not in st.session_state:
        st.session_state.adaptivecare_v2_log = []
    log = st.session_state.adaptivecare_v2_log
    if st.session_state.pop("ac_saved_notice", False):
        st.success("Check-in saved. Suggestions have been refreshed using the latest session record.")
    stage = st.selectbox(t("ac.context"), STAGES, format_func=display_option, key="ac_stage")
    goal = st.selectbox(t("ac.goal"), list(GOALS), format_func=display_option, key="ac_goal")
    capacity = st.select_slider(t("ac.energy"), options=CAPACITIES, format_func=display_option, value="Moderate", key="ac_capacity")
    setback = st.checkbox(t("ac.restart"), key="ac_setback")
    concern = st.selectbox(t("ac.concern"), CONCERNS, format_func=display_option, key="ac_concern")
    previous = next((row["completed"] for row in reversed(log) if row.get("goal") == goal), None)
    plan = build_plan(stage, goal, capacity, setback, concern, previous)
    if plan.urgency != "none":
        if plan.urgency == "urgent":
            st.error(plan.support)
        else:
            st.warning(plan.support)
        st.caption("Personal wellness planning and check-in controls are hidden when you request health assistance.")
        return

    st.subheader(t("ac.steps"))
    st.write(plan.message)
    for action in plan.actions:
        st.write("• " + action)
    with st.expander(t("ac.why")):
        for reason in plan.explanation:
            st.write("• " + reason)
        st.caption("Transparent if/then rules based on your choices; no AI diagnosis or machine-learning prediction.")

    completed = st.checkbox(t("ac.completed"), key="ac_completed")
    if st.button(t("ac.save"), type="primary", key="ac_save"):
        if log and log[-1]["date"] == date.today().isoformat() and log[-1]["goal"] == goal:
            st.info("You already saved a check-in for this goal today. You can clear the session and retest if needed.")
        else:
            log.append({"date": date.today().isoformat(), "context": stage,
                        "goal": goal, "energy": capacity, "restart": setback,
                        "completed": bool(completed)})
            st.session_state.ac_saved_notice = True
            st.rerun()

    st.subheader(t("ac.dashboard"))
    summary = progress_summary(log)
    left, right = st.columns(2)
    left.metric(t("ac.count"), summary["checkins"])
    right.metric(t("ac.completed_count"), summary["completed"])
    if log:
        st.progress(summary["completion_fraction"])
        st.caption("Share of check-ins marked completed; NOT a measure of medical outcomes or clinical adherence.")
        st.dataframe(list(reversed(log)), use_container_width=True, hide_index=True)
        if st.button(t("ac.clear"), key="ac_clear"):
            st.session_state.adaptivecare_v2_log = []
            st.rerun()
    st.caption("This version intentionally stores no medical history, names, symptoms, or location. There are no automatic notifications or provider integrations. For early pilot use, clinical, privacy, security and accessibility reviews are still required.")
