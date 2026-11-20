"""Streamlit AdaptiveCare v2: educational wellness support with optional private storage."""
from datetime import timedelta
from html import escape
import streamlit as st

from auth_ui import render_auth, render_password_recovery
from wellness_store import load_history, save_checkin, delete_history
from timezone_manager import user_today
from wellness_dashboard import render_wellness_dashboard

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

    today = user_today()

    if st.session_state.pop("ac_reset_private_consent", False):
        st.session_state["ac_private_storage_consent"] = False

    private_history = None
    use_private_history = False

    # Private wellness account integration
    if render_password_recovery():
        return

    st.caption(t("ac.intro"))

    with st.expander("🔐 My Wellness Account"):
        st.caption(
            "Private account testing. "
            "Use fictional wellness information only."
        )
        user = render_auth()

    if user is not None:
        reset_user = st.session_state.pop("ac_reset_history_controls", None)
        if reset_user == str(user.id):
            st.session_state.pop(
                "ac_confirm_private_delete_" + str(user.id), None
            )
            st.session_state.pop(
                "ac_use_private_history_" + str(user.id), None
            )

        if st.session_state.pop("ac_private_deleted_notice", False):
            st.success(ui("Saved wellness history deletion completed."))

        st.subheader("Private Wellness History")

        st.caption(
            "Your saved wellness check-ins "
            "from the last seven days."
        )

        try:
            private_history = load_history(days=7)
        except Exception:
            private_history = None
            st.warning(
                "Private wellness history is currently unavailable. "
                "Please try again later."
            )

        if private_history is not None:
            render_wellness_dashboard(private_history)

            use_private_history = st.checkbox(
                ui("Use my saved wellness history to personalize suggestions."),
                key="ac_use_private_history_" + str(user.id)
            )

            with st.expander(ui("Manage private wellness history")):
                st.warning(ui(
                    "Deleting private wellness history permanently removes "
                    "all saved wellness check-ins from your account, "
                    "not only those from the last seven days."
                ))

                confirm_delete = st.checkbox(
                    ui("I understand and confirm permanent deletion."),
                    key="ac_confirm_private_delete_" + str(user.id)
                )

                if st.button(
                    ui("Delete all private wellness history"),
                    key="ac_delete_private_history",
                    disabled=not confirm_delete
                ):
                    try:
                        delete_history()
                        remaining = load_history(days=365)
                        if remaining:
                            st.error(ui("History deletion could not be confirmed."))
                        else:
                            st.session_state["ac_private_deleted_notice"] = True
                            st.session_state["ac_reset_private_consent"] = True
                            st.session_state[
                                "ac_reset_history_controls"
                            ] = str(user.id)
                            st.rerun()
                    except Exception:
                        st.error(ui(
                            "History deletion could not be confirmed. "
                            "Please try again."
                        ))

    if user is not None:
        if st.session_state.pop(
            "ac_private_saved_notice", False
        ):
            st.success(ui(
                "Private wellness check-in saved successfully."
            ))
    else:
        st.session_state.pop(
            "ac_private_saved_notice", None
        )

    st.divider()

    st.warning("Existing maternal-health guidance has been reviewed by a qualified healthcare practitioner. The new adaptive wellness planner provides non-clinical support; it does not diagnose, triage or provide emergency care. For urgent or severe symptoms, seek immediate in-person medical care.")
    st.info(ui(
        "Wellness tracking is optional. Temporary check-ins remain "
        "in this session. Signed-in users may separately consent "
        "to saving check-ins in their private online account. "
        "Use fictional wellness information during testing."
    ))
    if "adaptivecare_v2_log" not in st.session_state:
        st.session_state.adaptivecare_v2_log = []
    log = st.session_state.adaptivecare_v2_log
    if st.session_state.pop("ac_saved_notice", False):
        st.success(ui("Check-in saved. Suggestions have been refreshed using the latest session record."))
    if st.button(ui("Clear temporary session history"), key="ari_delete"):
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
    combined_history = {}

    if user is not None and use_private_history and private_history is not None:
        for row in private_history:
            combined_history[(row["date"], row["goal"])] = row

    if consent:
        for row in log:
            combined_history[(row["date"], row["goal"])] = row

    plan = recovery_plan(
        stage=stage,
        goal=goal,
        capacity=capacity,
        setback=setback,
        concern=concern,
        sleep=sleep,
        stress=stress,
        history=list(combined_history.values()),
        today=today
    )
    if plan.urgency != "none":
        if plan.urgency == "urgent":
            st.error(plan.support)
        else:
            st.warning(plan.support)
        st.caption(ui("Personal wellness planning and check-in controls are hidden when you request health assistance."))
        return

    st.subheader(t("ac.steps"))
    st.markdown(f'<div class="ari-coach"><h3>{escape(ui("Your adaptive wellness plan"))}</h3>{escape(ui(plan.message))}</div>', unsafe_allow_html=True)
    activity_checks = [st.checkbox(ui(action), key=f"ari_activity_{today}_{goal}_{i}") for i, action in enumerate(plan.actions)]
    st.caption(ui("All activities are optional. Rest is a valid choice."))
    with st.expander(t("ac.why")):
        for reason in plan.explanation:
            st.write("• " + localize_reason(reason))
        st.caption(ui("Transparent if/then rules based on your choices; no AI diagnosis or machine-learning prediction."))

    completed = any(activity_checks)
    if st.button(t("ac.save"), type="primary", key="ac_save", disabled=not consent):
        if any(row["date"] == today.isoformat() and row["goal"] == goal for row in log):
            st.info(ui("You already saved a check-in for this goal today. You can clear the session and retest if needed."))
        else:
            log.append({"date": today.isoformat(), "context": stage,
                        "goal": goal, "energy": capacity, "restart": setback,
                        "completed": bool(completed), "sleep": sleep, "stress": stress})
            st.session_state.ac_saved_notice = True
            st.rerun()


    if user is not None:
        with st.container(border=True):
            st.subheader(ui("Private wellness storage"))

            st.caption(ui(
                "Save your wellness progress to your private "
                "account and access it across visits."
            ))

            private_consent = st.checkbox(
                ui(
                    "I consent to storing this wellness "
                    "check-in in my private account."
                ),
                key="ac_private_storage_consent"
            )

            st.caption(ui(
                "Online storage is optional and separate "
                "from temporary session tracking."
            ))

            if st.button(
                ui("Save Private Check-in"),
                key="ac_private_save",
                disabled=not private_consent
            ):
                record = {
                    "goal": goal,
                    "context": stage,
                    "energy": capacity,
                    "restart": setback,
                    "completed": bool(completed),
                    "sleep": sleep,
                    "stress": stress
                }

                try:
                    saved = save_checkin(
                        record,
                        consent=private_consent
                    )
                except Exception:
                    st.error(ui(
                        "Private saving could not be confirmed. "
                        "Please try again."
                    ))
                else:
                    if not saved:
                        st.warning(ui(
                            "The save could not be confirmed. "
                            "Please check your private history."
                        ))
                    else:
                        st.session_state[
                            "ac_private_saved_notice"
                        ] = True
                        st.session_state["ac_reset_private_consent"] = True
                        st.rerun()

    else:
        st.caption(ui(
            "Sign in to your wellness account to save "
            "your progress across visits."
        ))

    st.subheader(ui("Temporary wellness progress"))

    st.subheader(t("ac.dashboard"))
    weekly = weekly_progress(log, today=today)
    metrics = [("Check-in days (7 days)", "recorded_days"), ("Activity days (7 days)", "completed_days"), ("Consistency (7 days)", "weekly_streak")]
    st.markdown('<div class="ari-metrics">' + "".join(f'<div class="ari-metric">{escape(ui(label))}<strong>{weekly[key]}</strong></div>' for label, key in metrics) + "</div>", unsafe_allow_html=True)
    st.caption(ui("A missed day is not a failure. These counts are not clinical outcomes."))
    st.progress(weekly["completed_days"] / 7)
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
        st.dataframe(list(reversed(log)), width="stretch", hide_index=True)
        if st.button(t("ac.clear"), key="ac_clear"):
            st.session_state.adaptivecare_v2_log = []
            st.rerun()
    st.caption(ui(
        "Private check-ins contain selected wellness categories "
        "and are associated with your account. They are not "
        "medical records. There are no automatic notifications "
        "or provider integrations. Use fictional information "
        "during testing. Clinical, privacy, security and "
        "accessibility reviews are still required."
    ))
