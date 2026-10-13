"""BabyCare: session-only childhood immunization planning prototype."""
import csv
import io
from datetime import date, datetime, timedelta
import streamlit as st

# Visit milestones only. NOT a complete vaccine or catch-up schedule.
MILESTONES = [
    ("Birth", 0, "days"),
    ("6 weeks", 6, "weeks"),
    ("10 weeks", 10, "weeks"),
    ("14 weeks", 14, "weeks"),
    ("9 months", 9, "months"),
    ("15 months", 15, "months"),
]

VACCINES = {
 "BCG": "Protects against severe tuberculosis.",
 "OPV (oral polio)": "Oral drops protecting against polio.",
 "IPV (injected polio)": "Injection protecting against polio.",
 "Hepatitis B": "Protects against hepatitis B and related liver disease.",
 "Pentavalent": "Protects against diphtheria, tetanus, whooping cough, hepatitis B and Hib.",
 "PCV": "Protects against serious pneumococcal infections including some pneumonia and meningitis.",
 "Rotavirus": "Protects against severe rotavirus diarrhoea.",
 "Measles / measles-rubella": "Protects against measles; MR also protects against rubella.",
 "Yellow fever": "Protects against yellow fever.",
 "Meningococcal": "Protects against some meningococcal infections.",
 "Malaria vaccine": "Helps reduce malaria illness; local rollout varies.",
 "Vitamin A (not a vaccine)": "Supplement supporting vision and immunity.",
}
VISITS = {"Birth": "BCG, OPV birth dose, hepatitis B birth dose", "6 weeks": "Pentavalent 1, PCV 1, OPV 1, rotavirus 1, IPV 1", "10 weeks": "Pentavalent 2, PCV 2, OPV 2, rotavirus 2", "14 weeks": "Pentavalent 3, PCV 3, OPV 3, rotavirus 3, IPV 2", "9 months": "Measles or measles-rubella, yellow fever, meningococcal vaccine", "15 months": "Second measles-containing dose"}

def _add_months(d, months):
    import calendar
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))

def _milestone_date(dob, amount, unit):
    if unit == "months":
        return _add_months(dob, amount)
    if unit == "weeks":
        return dob + timedelta(weeks=amount)
    return dob + timedelta(days=amount)

def _ics(d, label):
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    next_day = d + timedelta(days=1)
    return ("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//HerMamaAI//BabyCare//EN\r\n"
            "BEGIN:VEVENT\r\nUID:babycare-" + d.strftime("%Y%m%d") + "-" + label.replace(" ", "-") + "@hermamaai\r\n"
            "DTSTAMP:" + stamp + "\r\nDTSTART;VALUE=DATE:" + d.strftime("%Y%m%d") +
            "\r\nDTEND;VALUE=DATE:" + next_day.strftime("%Y%m%d") +
            "\r\nSUMMARY:Discuss baby immunization visit with clinic (" + label + ")\r\n"
            "DESCRIPTION:Planning reminder only. Confirm vaccines and visit date with the child's healthcare provider.\r\n"
            "END:VEVENT\r\nEND:VCALENDAR\r\n")

def render_babycare():
    st.markdown("## 👶 BabyCare — Immunization Tracker")
    st.info("**Educational planning prototype.** This is not an official Nigerian immunization card, vaccine recommendation, medical record or clinic booking. Confirm the current NPHCDA schedule, individual vaccines, catch-up doses and timing with a qualified immunization provider.")
    st.warning("Do not delay medical care because of this app. For a missed dose, ask a healthcare professional for an individual catch-up plan; do not restart or change a vaccine series based on this calendar.")
    st.caption("No accounts or database: dates and entries are held only in this browser session. Download what you need before closing the app. Avoid entering full names or other identifying information.")
    dob = st.date_input("Baby's date of birth (for planning)", value=date.today(), min_value=date(2015,1,1), max_value=date.today(), key="babycare_dob")
    st.markdown("### Vaccines explained for first-time mothers")
    for name, meaning in VACCINES.items():
        with st.expander(name):
            st.write(meaning)
    st.markdown("### Indicative visit milestones and vaccines to discuss")
    st.caption("These are common age milestones, NOT a complete or individually verified list of vaccines due. National schedules and eligibility can change.")
    for label, amount, unit in MILESTONES:
        due = _milestone_date(dob, amount, unit)
        a, b = st.columns([3, 1])
        with a:
            st.write(f"**{label}** — {due.strftime('%d %b %Y')} · " + ("Past / today" if due <= date.today() else "Upcoming"))
        st.caption("Ask the clinic about: " + VISITS.get(label, "") + ". Confirm exact eligibility, doses and local availability.")
        with b:
            st.download_button("Add reminder", _ics(due, label), file_name=f"babycare_{label.replace(' ', '_')}.ics", mime="text/calendar", key=f"babycare_ics_{amount}_{unit}")
    st.markdown("### 🔎 What might my baby need at this age?")
    st.caption("Demonstration only: this shows published routine visit examples, not personalized vaccine eligibility or a catch-up schedule.")
    age_choice = st.selectbox("Choose a routine visit age", list(VISITS.keys()), key="babycare_age_guide")
    st.info("**" + age_choice + ":** Ask your immunization clinic about " + VISITS[age_choice] + ".")
    st.caption("Some vaccines, including malaria vaccines, are introduced by location. Your clinic card and local health team determine what is actually due.")
    st.markdown("### My vaccination progress (demonstration)")
    st.caption("This counts parent-entered records, not verified or completed immunization coverage.")
    entered_count = len(st.session_state.get("babycare_records", []))
    st.metric("Parent-reported entries this session", entered_count)
    st.markdown("### Parent-entered immunization record")
    st.caption("For your own reference only. Entries are not verified by a clinician and do not replace a child's official immunization card.")
    if "babycare_records" not in st.session_state:
        st.session_state.babycare_records = []
    with st.form("babycare_record_form", clear_on_submit=True):
        vaccine = st.selectbox("Select vaccine from the clinic card", ["Choose a vaccine"] + list(VACCINES.keys()) + ["Other"])
        other_vaccine = st.text_input("If Other, type the vaccine name", max_chars=100) if vaccine == "Other" else ""
        dose = st.text_input("Dose number as shown on card (optional)", max_chars=40)
        administered = st.date_input("Date administered", value=date.today(), max_value=date.today(), key="babycare_administered")
        clinic = st.text_input("Clinic (optional — avoid personal details)", max_chars=100)
        submitted = st.form_submit_button("Save to this session")
    if submitted:
        selected = other_vaccine.strip() if vaccine == "Other" else vaccine
        if selected == "Choose a vaccine" or not selected.strip():
            st.error("Enter the vaccine or dose from the clinic card.")
        else:
            st.session_state.babycare_records.append({"Vaccine / dose": selected + (" — " + dose.strip() if dose.strip() else ""), "Date administered": administered.isoformat(), "Clinic (optional)": clinic.strip(), "Status": "Parent-reported; not clinically verified"})
            st.success("Saved temporarily in this session.")
    records = st.session_state.babycare_records
    if records:
        st.dataframe(records, use_container_width=True, hide_index=True)
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Vaccine / dose", "Date administered", "Clinic (optional)", "Status"])
        writer.writeheader()
        writer.writerows(records)
        st.download_button("⬇️ Download parent-reported record (CSV)", output.getvalue(), file_name="hermamaai_parent_reported_immunizations.csv", mime="text/csv")
        if st.button("Clear all temporary immunization entries"):
            st.session_state.babycare_records = []
            st.rerun()
    else:
        st.caption("No immunization entries recorded in this session.")
    st.markdown("### Check official guidance")
    st.link_button("Nigeria Ministry of Health childhood schedule ↗", "https://health.gov.ng/wp-content/uploads/2025/06/SCD-Guideline-Final-2nd-Edition.pdf", use_container_width=True)
    st.link_button("UNICEF Nigeria immunization schedule ↗", "https://www.unicef.org/nigeria/documents/nigeria-immunization-schedule", use_container_width=True)
    st.link_button("Nigeria National Primary Health Care Development Agency ↗", "https://nphcda.gov.ng/", use_container_width=True)
    st.caption("Before real-world clinical use: confirm schedule and vaccine names with NPHCDA and a Nigerian immunization clinician; complete privacy, accessibility, and safeguarding review.")
