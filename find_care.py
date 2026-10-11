"""Educational Find Care directory: source-based Nigerian teaching hospitals."""
from urllib.parse import quote
import streamlit as st

SOURCE_URL = "https://health.gov.ng/teaching-hospitals/"
# State, city and institution name transcribed from the Federal Ministry of Health
# teaching-hospitals directory. City names are broad location labels, not
# independently verified street addresses or evidence of maternity availability.
HOSPITALS = [("FCT","Abuja","National Hospital Abuja"),
    ("FCT","Gwagwalada","University of Abuja Teaching Hospital"),
    ("Kaduna","Zaria","Ahmadu Bello University Teaching Hospital"),
    ("Kano","Kano","Aminu Kano Teaching Hospital"),
    ("Bauchi","Bauchi","Abubakar Tafawa Balewa University Teaching Hospital"),
    ("Ebonyi","Abakaliki","Alex Ekweme University Teaching Hospital"),
    ("Kebbi","Birnin Kebbi","Federal Teaching Hospital Birnin Kebbi"),
    ("Gombe","Gombe","Federal Teaching Hospital Gombe"),
    ("Ekiti","Ido-Ekiti","Federal Teaching Hospital Ido-Ekiti"),
    ("Katsina","Katsina","Federal Teaching Hospital Katsina"),
    ("Kogi","Lokoja","Federal Teaching Hospital Lokoja"),
    ("Osun","Ila-Orangun","Federal University of Health Sciences Teaching Hospital"),
    ("Benue","Otukpo","Federal University of Health Sciences Teaching Hospital"),
    ("Imo","Owerri","Federal University Teaching Hospital Owerri"),
    ("Taraba","Wukari","Federal University Teaching Hospital Wukari"),
    ("Nasarawa","Lafia","Federal University Teaching Hospital Lafia"),
    ("Edo","Irrua","Irrua Specialist Teaching Hospital"),
    ("Plateau","Jos","Jos University Teaching Hospital"),
    ("Ebonyi","Uburu","David Umahi University of Health Sciences Teaching Hospital"),
    ("Lagos","Lagos","Lagos University Teaching Hospital"),
    ("Adamawa","Yola","Modibo Adama University Teaching Hospital"),
    ("Anambra","Nnewi","Nnamdi Azikiwe University Teaching Hospital"),
    ("Osun","Ile-Ife","Obafemi Awolowo University Teaching Hospital"),
    ("Jigawa","Dutse","Rasheed Shekoni Teaching Hospital"),
    ("Edo","Benin City","University of Benin Teaching Hospital"),
    ("Oyo","Ibadan","University College Hospital"),
    ("Cross River","Calabar","University of Calabar Teaching Hospital"),
    ("Sokoto","Sokoto","Usman Danfodio University Teaching Hospital"),
    ("Kwara","Ilorin","University of Ilorin Teaching Hospital"),
    ("Borno","Maiduguri","University of Maiduguri Teaching Hospital"),
    ("Enugu","Enugu","University of Nigeria Teaching Hospital"),
    ("Rivers","Port Harcourt","University of Port Harcourt Teaching Hospital"),
    ("Akwa Ibom","Uyo","University of Uyo Teaching Hospital")]

# Official website findings are published information, not live phone verification.
# Only display institution contact details sourced from the institution itself.
OFFICIAL_DETAILS = {
    "University of Abuja Teaching Hospital": {
        "service": "Obstetrics & Gynaecology department documented on hospital website",
        "service_url": "https://www.uath.gov.ng/department_profile",
        "contact": "+234 704 004 5614",
        "contact_url": "https://www.uath.gov.ng/contact",
    },
    "Lagos University Teaching Hospital": {
        "service": "Obstetrics & Gynaecology department documented on hospital website",
        "service_url": "https://luth.gov.ng/departments/obstetrics/",
    },
}

def render_find_care():
    st.markdown('<div class="section-head">🏥 Find Care Across Nigeria</div>', unsafe_allow_html=True)
    st.markdown('<p class="lead">Explore a starter directory of government-listed teaching hospitals in Abuja and other Nigerian cities. This is a planning aid, not a clinical referral or booking service.</p>', unsafe_allow_html=True)
    st.error("**Emergency warning:** Heavy bleeding, chest pain, trouble breathing, seizures, severe headache or visual changes, fainting, or thoughts of harming yourself or your baby need immediate in-person emergency assessment. Go to the nearest appropriate emergency department or contact local emergency services. Do not wait for this app.")
    st.warning("**Important:** Being listed by the Federal Ministry of Health does not mean HerMamaAI has verified maternity services, opening hours, emergency capacity, precise map location or current operations. **None of these hospitals is claimed as a HerMamaAI partner.** Confirm details with the facility before a non-urgent visit.")
    st.caption("Only phone numbers published on official hospital websites are shown; they have not been independently tested. HerMamaAI does not request your live location or store your medical information here.")
    regions = ["All listed states and FCT"] + sorted({item[0] for item in HOSPITALS})
    selected_region = st.selectbox("Select state or FCT", regions, index=regions.index("FCT"), key="findcare_region")
    region_results = [item for item in HOSPITALS if selected_region == regions[0] or item[0] == selected_region]
    cities = ["All listed cities"] + sorted({item[1] for item in region_results})
    selected_city = st.selectbox("Select city", cities, key="findcare_city")
    results = [item for item in region_results if selected_city == cities[0] or item[1] == selected_city]
    st.caption(f"Showing {len(results)} government-listed institution(s). Not an exhaustive list of Nigerian hospitals.")
    for region, city, name in results:
        with st.container(border=True):
            st.markdown(f"#### 🏥 {name}")
            st.write(f"📍 {city}, {region}, Nigeria")
            st.caption("Institution listed in government directory · Service availability unverified · No partnership claimed")
            details = OFFICIAL_DETAILS.get(name)
            if details:
                st.success("Official hospital website reviewed · Current clinic hours and capacity NOT confirmed")
                st.write(details["service"])
                st.link_button("🏥 Official department information ↗", details["service_url"], use_container_width=True)
                if details.get("contact"):
                    st.write("Published hospital contact (not independently tested): " + details["contact"])
                    st.link_button("☎️ Official hospital contact page ↗", details["contact_url"], use_container_width=True)
            else:
                st.caption("Hospital-specific maternity services and contact details awaiting review")

            query = quote(f"{name}, {city}, {region}, Nigeria", safe="")
            st.link_button("🗺️ Search on Google Maps / Directions ↗", f"https://www.google.com/maps/search/?api=1&query={query}", use_container_width=True)
            st.link_button("📖 View government source ↗", SOURCE_URL, use_container_width=True)
    st.info("**City not listed?** This starter directory covers the cities represented by the ministry's teaching-hospital list, not every Nigerian city or maternity facility. Contact your local primary healthcare centre or state health authority for other options. In an emergency, use the nearest appropriate emergency service instead of travelling to a distant listed hospital.")
    with st.expander("Questions to ask a facility before a routine visit"):
        st.markdown("- Do you currently provide antenatal and postnatal care?\n- Are the relevant services available on the day I plan to visit?\n- Do I need a referral or appointment?\n- What are the emergency and after-hours arrangements?\n- Can you confirm the correct entrance and address?")
    st.caption("Source: Federal Ministry of Health and Social Welfare, Teaching Hospitals directory. Directory needs periodic rechecking, independent service verification and clinical review before real-world pilot use.")
