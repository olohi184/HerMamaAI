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
    st.caption("No accounts or database. Use fictional profiles and sample records only. Information is temporary and may disappear when this session ends.")
    st.markdown("### 👪 Demo family profiles")
    st.caption("Fictional aliases only. These profiles are temporary, not authenticated accounts. Do not enter real children's health information.")
    if "babycare_families" not in st.session_state:
        st.session_state.babycare_families = {}
    families = st.session_state.babycare_families
    with st.expander("Add a demo parent and baby", expanded=not bool(families)):
        with st.form("babycare_new_family", clear_on_submit=True):
            parent_alias = st.text_input("Fictional parent alias", placeholder="Demo Parent A")
            baby_alias = st.text_input("Fictional baby alias", placeholder="Baby A")
            birth = st.date_input("Demo baby's birth date", value=date.today(), min_value=date(2015,1,1), max_value=date.today())
            add_family = st.form_submit_button("Add demo profile")
        if add_family:
            if parent_alias.strip() and baby_alias.strip():
                import uuid
                parent_id_new = next((k for k,v in families.items() if v["alias"].casefold() == parent_alias.strip().casefold()), None)
                if parent_id_new is None:
                    parent_id_new = uuid.uuid4().hex
                    families[parent_id_new] = {"alias": parent_alias.strip(), "babies": {}}
                baby_id_new = uuid.uuid4().hex
                families[parent_id_new]["babies"][baby_id_new] = {"alias": baby_alias.strip(), "dob": birth.isoformat(), "records": []}
                st.session_state.babycare_active_parent = parent_id_new
                st.session_state.babycare_active_baby = baby_id_new
                st.rerun()
            else:
                st.error("Provide both fictional aliases.")
    if not families:
        st.info("Add a fictional family to start the demonstration.")
        return
    parent_ids = list(families)
    parent_default = st.session_state.get("babycare_active_parent")
    if parent_default not in families:
        parent_default = parent_ids[0]
    parent_id = st.selectbox("Demo parent", parent_ids, index=parent_ids.index(parent_default), format_func=lambda k: families[k]["alias"])
    st.session_state.babycare_active_parent = parent_id
    babies = families[parent_id]["babies"]
    baby_ids = list(babies)
    baby_default = st.session_state.get("babycare_active_baby")
    if baby_default not in babies:
        baby_default = baby_ids[0]
    baby_id = st.selectbox("Demo baby", baby_ids, index=baby_ids.index(baby_default), format_func=lambda k: babies[k]["alias"])
    st.session_state.babycare_active_baby = baby_id
    baby = babies[baby_id]
    a, b = st.columns(2)
    a.metric("Demo parent profiles", len(families))
    b.metric("Demo baby profiles", sum(len(p["babies"]) for p in families.values()))
    st.caption("Counts reflect only fictional profiles in this session, not real users.")
    if st.button("Clear all demo profiles and entries"):
        st.session_state.babycare_families = {}
        st.rerun()
    dob = date.fromisoformat(baby["dob"])
    st.write("**Selected demo baby's birth date:** " + dob.strftime("%d %b %Y"))
    st.markdown("### 🔎 What might my baby need at this age?")
    st.caption("Demonstration only: this shows published routine visit examples, not personalized vaccine eligibility or a catch-up schedule.")
    age_choice = st.selectbox("Choose a routine visit age", list(VISITS.keys()), key="babycare_age_guide")
    st.info("**" + age_choice + ":** Ask your immunization clinic about " + VISITS[age_choice] + ".")
    st.caption("Some vaccines, including malaria vaccines, are introduced by location. Your clinic card and local health team determine what is actually due.")
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
    st.markdown("### 📚 Understand the vaccines")
    st.caption("Tap a vaccine name to learn what it helps protect against.")
    for name, meaning in VACCINES.items():
        with st.expander(name):
            st.write(meaning)
    st.markdown("### 📅 Plan a future vaccination visit")
    st.caption("A planned visit is NOT a vaccine already administered. Confirm appointment date and vaccines with the clinic.")
    if "planned_visits" not in baby:
        baby["planned_visits"] = []
    with st.form("babycare_plan_visit", clear_on_submit=True):
        planned_age = st.selectbox("Routine visit milestone", list(VISITS.keys()))
        suggested = next(_milestone_date(dob, amount, unit) for label, amount, unit in MILESTONES if label == planned_age)
        planned_date = st.date_input("Planned clinic visit date (future dates allowed)", value=max(date.today(), suggested), min_value=dob, max_value=date.today() + timedelta(days=3650))
        planned_clinic = st.text_input("Demo clinic (optional)", max_chars=100)
        plan_submit = st.form_submit_button("Save planned visit")
    if plan_submit:
        baby["planned_visits"].append({"Visit": planned_age, "Planned date": planned_date.isoformat(), "Clinic": planned_clinic.strip(), "Status": "Planned only — not administered"})
        st.success("Future visit saved to this demo baby's session.")
    if baby["planned_visits"]:
        st.dataframe(baby["planned_visits"], use_container_width=True, hide_index=True)
        for i, visit in enumerate(baby["planned_visits"]):
            st.download_button("📅 Download reminder: " + visit["Visit"] + " (" + visit["Planned date"] + ")", _ics(date.fromisoformat(visit["Planned date"]), visit["Visit"]), file_name="babycare_planned_visit_" + str(i+1) + ".ics", mime="text/calendar", key="babycare_planned_ics_" + str(i))
    st.markdown("### Parent-entered immunization record")
    st.caption("For your own reference only. Entries are not verified by a clinician and do not replace a child's official immunization card.")
    records = baby["records"]
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
            records.append({"Vaccine / dose": selected + (" — " + dose.strip() if dose.strip() else ""), "Date administered": administered.isoformat(), "Clinic (optional)": clinic.strip(), "Status": "Parent-reported; not clinically verified"})
            st.success("Saved temporarily in this session.")
    st.markdown("### 📊 My saved vaccination entries")
    st.metric("Vaccination records for selected baby", len(baby["records"]))
    st.caption("Counts vaccination entries saved in this session, not distinct parents, babies, or verified vaccinations. One parent may enter several doses.")
    if records:
        st.dataframe(records, use_container_width=True, hide_index=True)
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Vaccine / dose", "Date administered", "Clinic (optional)", "Status"])
        writer.writeheader()
        writer.writerows(records)
        st.download_button("⬇️ Download parent-reported record (CSV)", output.getvalue(), file_name="hermamaai_parent_reported_immunizations.csv", mime="text/csv")
        if st.button("Clear all temporary immunization entries"):
            baby["records"] = []
            st.rerun()
    else:
        st.caption("No immunization entries recorded in this session.")
    st.markdown("### Check official guidance")
    st.link_button("Nigeria Ministry of Health childhood schedule ↗", "https://health.gov.ng/wp-content/uploads/2025/06/SCD-Guideline-Final-2nd-Edition.pdf", use_container_width=True)
    st.link_button("UNICEF Nigeria immunization schedule ↗", "https://www.unicef.org/nigeria/documents/nigeria-immunization-schedule", use_container_width=True)
    st.link_button("Nigeria National Primary Health Care Development Agency ↗", "https://nphcda.gov.ng/", use_container_width=True)
    st.caption("Before real-world clinical use: confirm schedule and vaccine names with NPHCDA and a Nigerian immunization clinician; complete privacy, accessibility, and safeguarding review.")
