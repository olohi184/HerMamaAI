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
    st.markdown("### Indicative visit milestones")
    st.caption("These are common age milestones, NOT a complete or individually verified list of vaccines due. National schedules and eligibility can change.")
    for label, amount, unit in MILESTONES:
        due = _milestone_date(dob, amount, unit)
        a, b = st.columns([3, 1])
        with a:
            st.write(f"**{label}** — {due.strftime('%d %b %Y')} · " + ("Past / today" if due <= date.today() else "Upcoming"))
        with b:
            st.download_button("Add reminder", _ics(due, label), file_name=f"babycare_{label.replace(' ', '_')}.ics", mime="text/calendar", key=f"babycare_ics_{amount}_{unit}")
    st.markdown("### Parent-entered immunization record")
    st.caption("For your own reference only. Entries are not verified by a clinician and do not replace a child's official immunization card.")
    if "babycare_records" not in st.session_state:
        st.session_state.babycare_records = []
    with st.form("babycare_record_form", clear_on_submit=True):
        vaccine = st.text_input("Vaccine or dose as written on the child's clinic card", max_chars=100)
        administered = st.date_input("Date administered", value=date.today(), max_value=date.today(), key="babycare_administered")
        clinic = st.text_input("Clinic (optional — avoid personal details)", max_chars=100)
        submitted = st.form_submit_button("Save to this session")
    if submitted:
        if not vaccine.strip():
            st.error("Enter the vaccine or dose from the clinic card.")
        else:
            st.session_state.babycare_records.append({"Vaccine / dose": vaccine.strip(), "Date administered": administered.isoformat(), "Clinic (optional)": clinic.strip(), "Status": "Parent-reported; not clinically verified"})
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
    st.link_button("Nigeria National Primary Health Care Development Agency ↗", "https://nphcda.gov.ng/", use_container_width=True)
    st.caption("Before real-world clinical use: confirm schedule and vaccine names with NPHCDA and a Nigerian immunization clinician; complete privacy, accessibility, and safeguarding review.")
