"""Streamlit AdaptiveCare v2 interface: rule-based, educational, session-only."""
from datetime import date, timedelta
from html import escape
import streamlit as st
from localization.language_manager import t, ui, display_option
from adaptive_engine import GOALS, STAGES, CAPACITIES, CONCERNS, progress_summary
from adaptive_recovery import recovery_plan, weekly_progress

def localize_reason(reason):
    """Localize rule explanations without changing the rule engine's stored values."""
    if reason.startswith("You selected ") and reason.endswith(" as your wellness goal."):
        goal = reason[len("You selected "):-len(" as your wellness goal.")]
        return ui("You selected {goal} as your wellness goal.").format(goal=ui(goal))
    if reason.startswith("You selected ") and reason.endswith(" energy."):
        capacity = reason[len("You selected "):-len(" energy.")]
        return ui("You selected {capacity} energy.").format(capacity=ui(capacity.capitalize()))
    if reason.startswith("The context is ") and reason.endswith("; this does not change clinical advice or imply stage-specific medical recommendations."):
        stage = reason[len("The context is "):-len("; this does not change clinical advice or imply stage-specific medical recommendations.")]
        return ui("The context is {stage}; this does not change clinical advice or imply stage-specific medical recommendations.").format(stage=ui(stage.capitalize()))
    return ui(reason)

def render_adaptivecare():
    st.markdown("""<style>
    .ari-hero {background:linear-gradient(125deg,#592b68,#884478);color:white;padding:1.4rem;border-radius:1.2rem;margin-bottom:1rem}
    .ari-hero h2 {color:white!important;margin:0;font-size:1.65rem!important}
    .ari-hero p {color:white!important;margin:.5rem 0 0}
    .ari-coach {background:#f0e3f3;border:1px solid #dcc6e2;border-left:5px solid #884478;border-radius:1rem;padding:1.2rem;color:#41264b;margin:.6rem 0 1rem}
    .ari-coach h3 {color:#592b68!important;margin:0 0 .5rem;font-size:1.1rem!important}
    .ari-metrics {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.6rem;margin:.8rem 0}
    .ari-metric {background:#fff;border:1px solid #e4d4e8;border-radius:1rem;padding:1rem;color:#41264b;overflow-wrap:anywhere}
    .ari-metric strong {display:block;color:#70366f;font-size:1.8rem}
    @media(max-width:480px){.ari-metric{padding:.6rem;font-size:.75rem}.ari-metric strong{font-size:1.4rem}}
    .ari-week {display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:.3rem;margin:1rem 0}
    .ari-day {text-align:center;border:1px solid #e4d4e8;border-radius:.65rem;padding:.55rem .1rem;background:white;color:#41264b;font-size:.78rem}
    .ari-day strong {display:block;font-size:1.1rem}
    .ari-day.done {background:#e4f3eb;color:#24583d;border-color:#b8d8c5}
    @media(max-width:480px){.ari-hero{padding:1rem}.ari-day{font-size:.68rem}}
    </style>""", unsafe_allow_html=True)
    st.markdown(
        '<div class="ari-hero"><small>HERMAMAAI · ADAPTIVECARE 2.0</small>'
        f'<h2>{escape(ui("Your wellness companion"))}</h2>'
        f'<p>{escape(ui("Every small step matters."))}</p></div>',
        unsafe_allow_html=True)
    st.caption(t("ac.intro"))
    st.warning("Existing maternal-health guidance has been reviewed by a qualified healthcare practitioner. The new adaptive wellness planner provides non-clinical support; it does not diagnose, triage or provide emergency care. For urgent or severe symptoms, seek immediate in-person medical care.")
    st.info(ui("Demo privacy: check-ins exist only in this Streamlit session; they are not synced across visits or sent to healthcare providers. Do not enter personal or medical information."))
    if "adaptivecare_v2_log" not in st.session_state:
        st.session_state.adaptivecare_v2_log = []
    log = st.session_state.adaptivecare_v2_log
    if st.session_state.pop("ac_saved_notice", False):
        st.success(ui("Check-in saved. Suggestions have been refreshed using the latest session record."))
    if st.button(ui("Clear wellness history"), key="ari_delete"):
        log.clear()
        st.rerun()
    consent = st.checkbox(ui("I agree to use temporary session storage for optional wellness tracking."), key="ari_consent")
    if not consent:
        log.clear()
    st.subheader(ui("Daily wellness check-in"))
    stage = st.selectbox(t("ac.context"), STAGES, format_func=display_option, key="ac_stage")
    goal = st.selectbox(t("ac.goal"), list(GOALS), format_func=display_option, key="ac_goal")
    capacity = st.select_slider(t("ac.energy"), options=CAPACITIES, format_func=display_option, value="Moderate", key="ac_capacity")
    setback = st.checkbox(t("ac.restart"), key="ac_setback")
    concern = st.selectbox(t("ac.concern"), CONCERNS, format_func=display_option, key="ac_concern")
    sleep = st.radio(ui("How did you sleep?"), ("Restful", "Interrupted", "Poor"), format_func=display_option, horizontal=True, key="ari_sleep")
    stress = st.radio(ui("Stress today"), ("Low", "Moderate", "High"), format_func=display_option, horizontal=True, key="ari_stress")
    plan = recovery_plan(stage=stage, goal=goal, capacity=capacity, setback=setback, concern=concern, sleep=sleep, stress=stress, history=log if consent else ())
    if plan.urgency != "none":
        if plan.urgency == "urgent":
            st.error(plan.support)
        else:
            st.warning(plan.support)
        st.caption(ui("Personal wellness planning and check-in controls are hidden when you request health assistance."))
        return

    st.subheader(t("ac.steps"))
    st.markdown(f'<div class="ari-coach"><h3>{escape(ui("Your adaptive wellness plan"))}</h3>{escape(ui(plan.message))}</div>', unsafe_allow_html=True)
    activity_checks = [st.checkbox(ui(action), key=f"ari_activity_{date.today()}_{goal}_{i}") for i, action in enumerate(plan.actions)]
    st.caption(ui("All activities are optional. Rest is a valid choice."))
    with st.expander(t("ac.why")):
        for reason in plan.explanation:
            st.write("• " + localize_reason(reason))
        st.caption(ui("Transparent if/then rules based on your choices; no AI diagnosis or machine-learning prediction."))

    completed = any(activity_checks)
    if st.button(t("ac.save"), type="primary", key="ac_save", disabled=not consent):
        if any(row["date"] == date.today().isoformat() and row["goal"] == goal for row in log):
            st.info(ui("You already saved a check-in for this goal today. You can clear the session and retest if needed."))
        else:
            log.append({"date": date.today().isoformat(), "context": stage,
                        "goal": goal, "energy": capacity, "restart": setback,
                        "completed": bool(completed), "sleep": sleep, "stress": stress})
            st.session_state.ac_saved_notice = True
            st.rerun()

    st.subheader(t("ac.dashboard"))
    weekly = weekly_progress(log)
    metrics = [("Check-in days (7 days)", "recorded_days"), ("Activity days (7 days)", "completed_days"), ("Consistency (7 days)", "weekly_streak")]
    st.markdown('<div class="ari-metrics">' + "".join(f'<div class="ari-metric">{escape(ui(label))}<strong>{weekly[key]}</strong></div>' for label, key in metrics) + "</div>", unsafe_allow_html=True)
    st.caption(ui("A missed day is not a failure. These counts are not clinical outcomes."))
    st.progress(weekly["completed_days"] / 7)
    today = date.today()
    done_dates = {row["date"] for row in log if row.get("completed") is True}
    tiles = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        done = day.isoformat() in done_dates
        status = ui("Activity recorded") if done else ui("No completed activity recorded")
        css = "ari-day done" if done else "ari-day"
        marker = "✓" if done else "○"
        tiles.append(f'<div class="{css}" title="{escape(status, quote=True)}"><span>{day.day:02d}</span><strong>{marker}</strong></div>')
    st.markdown('<div class="ari-week">' + "".join(tiles) + "</div>", unsafe_allow_html=True)
    st.caption(ui("Past seven days: a check mark means at least one optional activity was recorded."))
    summary = progress_summary(log)
    left, right = st.columns(2)
    left.metric(t("ac.count"), summary["checkins"])
    right.metric(t("ac.completed_count"), summary["completed"])
    if log:
        st.progress(summary["completion_fraction"])
        st.caption(ui("Share of check-ins marked completed; NOT a measure of medical outcomes or clinical adherence."))
        st.dataframe(list(reversed(log)), use_container_width=True, hide_index=True)
        if st.button(t("ac.clear"), key="ac_clear"):
            st.session_state.adaptivecare_v2_log = []
            st.rerun()
    st.caption(ui("This version intentionally stores no medical history, names, symptoms, or location. There are no automatic notifications or provider integrations. For early pilot use, clinical, privacy, security and accessibility reviews are still required."))
