"""Educational postpartum continuity module for HerMamaAI. No database storage."""
import streamlit as st

STAGES = {
    "Days 1–7": ("Early recovery", "Review your discharge instructions, arrange your recommended postnatal contact, and ask for support with rest, food, feeding and recovery."),
    "Week 2": ("Recovery takes time", "Discuss fever, worsening pain, wound concerns, feeding difficulties or other symptoms with a qualified healthcare professional."),
    "Weeks 3–4": ("Stay connected", "Serious complications can develop after leaving hospital. Seek assessment for new or worsening symptoms. Emotional well-being deserves attention too."),
    "Weeks 5–6": ("Prepare for your review", "Ask about healing, mood, sleep, contraception if relevant, feeding and any ongoing symptoms. Follow your own maternity team's schedule."),
    "Beyond 6 weeks": ("Care continues", "Postpartum concerns can continue or begin after six weeks. Seek care whenever needed; do not wait for an appointment."),
}
DANGER = [
    "Heavy bleeding (such as soaking a pad in an hour), or large clots",
    "Chest pain, difficulty breathing or fainting",
    "Seizures, severe headache or changes in vision",
    "High fever or severe or worsening abdominal pain",
    "One-sided leg pain, redness or swelling",
    "Thoughts of harming yourself or your baby, or feeling unable to stay safe",
]

def render_mamacare(go=None):
    st.markdown("## 🌷 MamaCare Continuity")
    st.write("Care does not end at childbirth. Explore supportive postpartum information and prepare for follow-up with your maternity team.")
    st.warning("Educational prototype only — not a diagnosis, clinical assessment or emergency service. This content has not yet undergone clinical review.")
    st.markdown("### Your postpartum care journey")
    st.caption("Choose what you need today. These are educational tools, not clinical monitoring.")
    options = ["🌼 Recovery guidance", "💗 Gentle check-in", "🚨 Warning signs", "📅 Follow-up planning"]
    section = st.radio("Explore your care", options, horizontal=True, key="mc_section", label_visibility="collapsed")
    st.divider()
    if section == options[0]:
        phase = st.selectbox("Choose a recovery stage", list(STAGES), key="mamacare_phase")
        title, guidance = STAGES[phase]
        st.subheader(title)
        st.write(guidance)
        st.caption("These stages are educational, not a prescribed follow-up schedule. Every recovery is different.")
        if go is not None:
            st.button("🌼 Visit Calm Corner →", key="mc_calm", on_click=go, args=("🌼 Calm Corner",), use_container_width=True)
    elif section == options[1]:
        st.subheader("How are you feeling today?")
        st.caption("Optional self-reflection only. Answers remain in the current Streamlit session and are not sent to a healthcare professional.")
        physical = st.radio("Physical recovery", ["Comfortable today", "Some concerns", "I need medical help"], index=None, key="mc_physical")
        mood = st.radio("Emotional well-being", ["Doing okay", "Having a difficult day", "I need support"], index=None, key="mc_mood")
        support = st.radio("Support around you", ["I have support", "I could use more help"], index=None, key="mc_support")
        if physical == "I need medical help":
            st.warning("Contact your maternity care team promptly. For severe or sudden symptoms, seek emergency care now.")
        if mood == "I need support":
            st.warning("Contact a qualified healthcare professional and someone you trust. If you may harm yourself or your baby, seek emergency help now and do not stay alone.")
        if support == "I could use more help":
            st.info("Consider asking someone you trust for one specific practical task today.")
        if physical or mood or support:
            st.write("You deserve care, rest and support.")
    elif section == options[2]:
        st.subheader("Postpartum warning signs")
        for item in DANGER:
            st.markdown("- " + item)
        st.error("If any of these occur, go to the nearest emergency department or contact local emergency services immediately. Do not wait for an app response.")
        st.caption("This list is not exhaustive. Seek care for any concerning symptoms.")
    elif section == options[3]:
        st.subheader("My follow-up checklist")
        st.write("Use your maternity team's own follow-up instructions and appointment schedule.")
        tasks = [
            "Confirm my next postpartum appointment",
            "Write down questions about pain, bleeding or healing",
            "Ask about emotional well-being and sleep",
            "Discuss feeding and contraception if relevant",
            "Arrange transport or someone to accompany me if needed",
        ]
        for i, task in enumerate(tasks):
            st.checkbox(task, key=f"mc_task_{i}")
        if go is not None:
            st.button("📅 Open CareCalendar →", key="mc_calendar", on_click=go, args=("📅 CareCalendar",), use_container_width=True)
        st.caption("Checklists are session-only. This module does not book appointments or send reminders.")
