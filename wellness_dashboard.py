
import streamlit as st
import pandas as pd
import altair as alt
from adaptive_engine import progress_summary
from timezone_manager import user_today

PLUM = "#74345F"
PINK = "#B55B98"
LAVENDER = "#AD79BC"


def render_wellness_dashboard(rows):

    st.subheader("🌸 My Wellness Journey")
    st.caption(
        "Every small step towards your wellbeing matters."
    )

    if rows is None:
        st.warning("Wellness history is unavailable.")
        return

    if not rows:
        st.info(
            "Your wellness journey starts here. "
            "Complete your first wellness check-in "
            "whenever you feel ready."
        )

    summary = progress_summary(rows)
    df = pd.DataFrame(rows)

    st.caption("Your wellness history for the last 7 days")

    dates = pd.Series(dtype="datetime64[ns]")

    if "date" in df.columns:
        dates = pd.to_datetime(
            df["date"], errors="coerce"
        )

    active_days = dates.dropna().dt.date.nunique()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Check-ins", summary["checkins"])

    with c2:
        st.metric("Completed", summary["completed"])

    with c3:
        st.metric("Active days", active_days)

    st.divider()

    st.markdown("#### Daily wellness activity")

    if not rows or not dates.dropna().empty:

        daily = (
            dates.dropna()
            .dt.normalize()
            .value_counts()
            .sort_index()
        )

        end = pd.Timestamp(user_today())

        period = pd.date_range(
            end=end, periods=7, freq="D"
        )

        daily = daily.reindex(period, fill_value=0)

        chart_data = pd.DataFrame({
            "Date": daily.index,
            "Check-ins": daily.values
        })

        chart_data["Day"] = (
            chart_data["Date"].dt.strftime("%d %b")
        )

        chart = alt.Chart(chart_data).mark_bar(
            color=PINK,
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        ).encode(
            x=alt.X(
                "Day:O",
                sort=chart_data["Day"].tolist(),
                title=None,
                axis=alt.Axis(labelAngle=0)
            ),
            y=alt.Y(
                "Check-ins:Q",
                scale=alt.Scale(zero=True, domainMin=0, domainMax=max(1, int(daily.max()))),
                axis=alt.Axis(tickMinStep=1),
                title="Check-ins"
            ),
            tooltip=["Day", "Check-ins"]
        ).properties(height=180)

        st.altair_chart(
            chart,
            width="stretch"
        )

        st.caption(
            "Seven-day activity window ending today."
        )

    else:
        st.caption("No valid check-in dates available.")

    st.markdown("#### Activity completion")

    fraction = float(summary["completion_fraction"])
    fraction = max(0.0, min(1.0, fraction))

    st.progress(fraction)

    if rows:
        st.caption(
            f"{fraction:.0%} of check-ins marked completed. "
            "Activities are optional, not obligations."
        )
    else:
        st.caption(
            "No activities recorded yet. "
            "Take small steps at your own pace."
        )

    st.divider()

    st.markdown("#### My wellness patterns")

    if not rows:
        st.caption(
            "Your energy, sleep and stress patterns "
            "will appear here after your first check-in."
        )

    patterns = [
        ("energy", "Energy levels", LAVENDER),
        ("sleep", "Sleep quality", "#9275BB"),
        ("stress", "Stress levels", "#D28AAB")
    ]

    for field, label, colour in patterns:

        if field not in df.columns:
            continue

        counts = df[field].dropna().value_counts()

        if counts.empty:
            continue

        data = pd.DataFrame({
            "Response": counts.index.astype(str),
            "Check-ins": counts.values
        })

        st.markdown(f"**{label}**")

        chart = alt.Chart(data).mark_bar(
            color=colour,
            orient="horizontal",
            cornerRadiusEnd=5,
            size=18
        ).encode(
            x=alt.X(
                "Check-ins:Q",
                scale=alt.Scale(
                    domain=[0, max(1, len(rows))]
                ),
                axis=alt.Axis(tickMinStep=1),
                title="Check-ins"
            ),
            y=alt.Y(
                "Response:N",
                sort="-x",
                title=None
            ),
            tooltip=["Response", "Check-ins"]
        ).properties(
            height=alt.Step(36)
        )

        st.altair_chart(
            chart,
            width="stretch"
        )

    st.divider()

    with st.expander("📋 My wellness history"):

        fields = {
            "date": "Date",
            "context": "Wellness context",
            "goal": "Wellness goal",
            "energy": "Energy",
            "sleep": "Sleep",
            "stress": "Stress",
            "completed": "Activity completed"
        }

        available = [
            f for f in fields if f in df.columns
        ]

        if not rows:
            st.caption("No wellness records in this period.")

        if available:
            st.dataframe(
                df[available].rename(columns=fields),
                hide_index=True,
                width="stretch"
            )

    st.markdown("#### 💗 AdaptiveCare Encouragement")

    st.info(
        "Your wellness journey is personal. "
        "Rest when you need to, celebrate small steps, "
        "and continue at your own pace."
    )

    st.caption(
        "These summaries reflect self-reported wellness "
        "information, not a medical assessment."
    )
