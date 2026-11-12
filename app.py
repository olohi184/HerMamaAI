import streamlit as st
from mamacare import render_mamacare
from adaptivecare import render_adaptivecare
from localization.language_manager import choose_language, localized_navigation, t, ui, display_option, label as localized_label
from datetime import date, datetime, time, timedelta
from html import escape

from mobile_branding import ensure_official_mobile_icons
ensure_official_mobile_icons()

# Use the actual PNG image, rather than passing its filename as an icon string.
from pathlib import Path
from PIL import Image
_BRAND_LOGO = Path(__file__).resolve().parent / "HerMamaAI Mother and Baby Emblem.png"
with Image.open(_BRAND_LOGO) as _logo:
    _page_icon = _logo.copy()
st.set_page_config(page_title="HerMamaAI | Maternal Wellness", page_icon=_page_icon, layout="wide", initial_sidebar_state="collapsed")
# Attach the HerMamaAI install manifest to the top-level document.
# Streamlit does not expose a native page-manifest configuration option.
# This trusted, zero-height component only inserts a manifest link and theme color;
# it does not register a service worker or cache sensitive maternal-health data.
import streamlit.components.v1 as components
components.html("""
<script>
try {
  const doc = window.parent.document;
  if (!doc.querySelector('link[rel="manifest"][data-hermamaai]')) {
    const link = doc.createElement('link');
    link.rel = 'manifest';
    link.href = '/app/static/manifest.json?brand=official-20261108';
    link.setAttribute('data-hermamaai', 'true');
    doc.head.appendChild(link);
  }
  // Keep one canonical favicon and re-apply it if Streamlit updates the head.
  // Safari can otherwise retain an older Streamlit icon after a rerender.
  const iconUrl = '/app/static/hermamaai-original-brand-192.png?favicon=20261109';
  const syncBrandIcons = () => {
    const head = doc.head;
    const branded = head.querySelector('link[rel="icon"][data-hermamaai="true"]');
    const conflicting = [...head.querySelectorAll('link[rel~="icon"]')]
      .filter(link => link !== branded && link.rel !== 'apple-touch-icon');
    conflicting.forEach(link => link.remove());
    if (!branded) {
      const link = doc.createElement('link');
      link.rel = 'icon';
      link.type = 'image/png';
      link.sizes = '192x192';
      link.href = iconUrl;
      link.setAttribute('data-hermamaai', 'true');
      head.appendChild(link);
    } else if (branded.getAttribute('href') !== iconUrl) {
      branded.href = iconUrl;
    }
    // Preserve the existing iOS home-screen icon independently.
    let apple = head.querySelector('link[rel="apple-touch-icon"][data-hermamaai="true"]');
    if (!apple) {
      apple = doc.createElement('link');
      apple.rel = 'apple-touch-icon';
      apple.sizes = '192x192';
      apple.href = iconUrl;
      apple.setAttribute('data-hermamaai', 'true');
      head.appendChild(apple);
    }
  };
  syncBrandIcons();
  // Keep the production performance fix: do not observe and repeatedly
  // modify Streamlit's document head on rerenders.
  if (!doc.querySelector('meta[name="theme-color"][data-hermamaai]')) {
    const meta = doc.createElement('meta');
    meta.name = 'theme-color';
    meta.content = '#8c287e';
    meta.setAttribute('data-hermamaai', 'true');
    doc.head.appendChild(meta);
  }
} catch (_) {
  // In browsers that restrict iframe parent access, the main app stays functional.
}
</script>
""", height=0)
# Reduce Streamlit developer controls; Cloud-managed Fork/GitHub links may remain.
st.set_option("client.toolbarMode", "minimal")
PAGES = ["🏡 Home", "👶 BabyCare", "📅 CareCalendar", "🤰 Pregnancy care", "💞 MamaCare journey", "💗 Postpartum recovery", "🌷 Emotional wellness", "🏥 Find care", "📖 Learning hub", "🌼 Calm Corner", "🌱 AdaptiveCare"]
if "page" not in st.session_state:
    st.session_state.page = PAGES[0]
def go(page):
    st.session_state.page = page
def card(title, icon, body):
    st.markdown(f'<div class="feature"><span class="feature-icon">{icon}</span><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');
html,body,[data-testid="stApp"]{font-family:'DM Sans',sans-serif}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 8% 12%,#f0d5f8,transparent 35%),radial-gradient(circle at 94% 15%,#ffd9ed,transparent 35%),linear-gradient(170deg,#fff7fc,#f9f0ff 65%,#fff8f8)}
.block-container{max-width:1440px!important;padding-top:.6rem!important;padding-bottom:3rem!important}
h1,h2,h3{color:#43145e}
.hm-hero{position:relative;overflow:hidden;border-radius:30px;padding:32px 5% 48px;min-height:360px;background:radial-gradient(ellipse at 55% 30%,#fff8fc 0%,#ffecf5 37%,transparent 72%),linear-gradient(115deg,#edc5f1,#fbe2f0 55%,#e6b3dd);box-shadow:0 20px 45px #65317a22;border:1px solid #f6d9ee}
.hm-hero:after{content:"";position:absolute;left:-5%;bottom:-72px;width:110%;height:120px;background:#fff8fd;border-radius:50% 50% 0 0}
.hm-hero-grid{display:grid;grid-template-columns:1.3fr 1fr;align-items:center;gap:2%;position:relative;z-index:1}
.hm-copy h1{font:700 clamp(3.8rem,8vw,7.5rem)/1.04 'Playfair Display',serif;letter-spacing:-.055em;color:#43105f;margin:0 0 9px;white-space:nowrap}
.hm-copy h1 span{color:#d72a94}
.hm-copy h2{font:italic 600 clamp(1.1rem,2.3vw,1.9rem)/1.3 'Playfair Display',serif;color:#56216d;margin:8px 0 16px}
.hm-copy p{font-size:1.05rem;line-height:1.6;color:#5c416a;max-width:560px}
.hm-art{display:flex;justify-content:center;align-items:center;min-height:265px}
.hm-art img{width:min(310px,85%);max-height:300px;object-fit:contain;filter:drop-shadow(0 14px 22px #75397c35)}
.hm-eyebrow{font-size:.75rem;letter-spacing:.17em;font-weight:800;color:#9b3a83;margin-bottom:18px}
.hm-kicker{font:italic 600 1.35rem 'Playfair Display',serif;color:#6a2a80}
.hm-card{border-radius:24px;padding:23px;min-height:190px;border:1px solid #f0d7eb;box-shadow:0 12px 25px #6e357515;margin:8px 0}
.hm-card h3{margin:12px 0;color:#521c6b;font-size:1.18rem}
.hm-card p{color:#624e69;line-height:1.6}
.hm-pink{background:linear-gradient(140deg,#fff5fa,#ffe1f0)}
.hm-lilac{background:linear-gradient(140deg,#f9f1ff,#e9ddff)}
.hm-peach{background:linear-gradient(140deg,#fffaf1,#ffebd4)}
.hm-mint{background:linear-gradient(140deg,#effff9,#d9f8ed)}
.hm-icon{font-size:2.3rem}
.section-head{font:700 clamp(1.65rem,3vw,2.25rem) 'Playfair Display',serif;color:#482456;margin:24px 0 12px}
.lead{color:#67576c;line-height:1.7;font-size:1.02rem}
.feature{background:#fff9fd;border:1px solid #edd9e9;border-radius:20px;padding:20px;margin:10px 0}
.feature-icon{font-size:2rem}.feature h3{font-size:1.1rem;margin:8px 0}.feature p{color:#685a6d}
.soft{background:#f8eefa;border:1px solid #edd9f0;border-radius:18px;padding:20px 23px;margin:18px 0;color:#533c5d}
.timeline{background:#fffafd;border:1px solid #ecdce9;border-left:5px solid #b565a1;border-radius:16px;padding:18px 22px;margin:10px 0}
.timeline b{color:#573464}
.footer{border-top:1px solid #eadce8;margin-top:30px;padding:20px 0;color:#76697b;font-size:.85rem}
[data-testid="stButton"] button{border-radius:22px!important;min-height:46px!important;font-weight:700!important;border:1px solid #e8c9e6!important;background:#fff9fd!important;color:#67287e!important}
[data-testid="stButton"] button:hover{border-color:#d52b92!important;color:#bc268b!important}
[data-testid="stButton"] button[kind="primary"]{background:#cc288d!important;color:white!important}
[data-testid="stAlert"]{border-radius:17px!important}
@media(max-width:720px){.block-container{padding-left:.8rem!important;padding-right:.8rem!important}.hm-hero{padding:25px 20px 45px}.hm-hero-grid{grid-template-columns:1fr;text-align:center}.hm-copy h1{font-size:clamp(2.8rem,11vw,4.8rem)}.hm-copy p{margin:auto}.hm-art{min-height:150px}.hm-art img{width:180px;max-height:180px}.hm-eyebrow{font-size:.62rem}.hm-card{min-height:0}}

/* Refined brand-first hero: the logo already contains the HerMamaAI wordmark. */
.hm-hero-refined{min-height:0!important;display:flex;flex-direction:column;align-items:center;text-align:center;padding:24px 24px 55px!important}
.hm-hero-refined .hm-eyebrow{margin:0 0 10px;font-size:.72rem}
.hm-logo-focus{position:relative;z-index:1;display:flex;justify-content:center;width:100%}
.hm-logo-focus img{width:min(440px,88%);height:auto;max-height:360px;object-fit:contain;filter:drop-shadow(0 12px 20px #5b226a20)}
.hm-single-message{position:relative;z-index:1;font-size:1.07rem;font-weight:600;line-height:1.55;color:#58276d;margin:8px auto 0;max-width:650px}
@media(max-width:720px){.hm-hero-refined{padding:22px 12px 48px!important}.hm-logo-focus img{width:min(340px,96%)}.hm-single-message{font-size:.95rem}}
.garden-bed{min-height:125px;border-radius:22px;background:linear-gradient(135deg,#fff0f9,#f0e4ff);border:1px solid #edd2ec;padding:25px;font-size:2rem;line-height:1.9;text-align:center;color:#683479}.calm-scene{border-radius:20px;padding:28px;background:linear-gradient(120deg,#e8fbf2,#f8f0ff);border:1px solid #d8ebdf;font-size:1.1rem;line-height:1.8;color:#4f4960;margin:15px 0}
/* Mobile usability: legible controls, compact navigation and scrollable records. */
@media (max-width: 720px) {
  .block-container {max-width:100%!important;padding: .65rem .85rem 2.5rem!important}
  [data-testid="stButton"] button {min-height:48px!important;font-size:.92rem!important;white-space:normal!important;line-height:1.3!important;padding:.55rem .6rem!important}
  [data-testid="stTextInput"] input,[data-testid="stDateInput"] input,[data-testid="stSelectbox"] [data-baseweb="select"] {font-size:16px!important;min-height:44px}
  [data-testid="stDataFrame"] {max-width:100%!important;overflow-x:auto!important}
  [data-testid="stAlert"] {font-size:.92rem!important}
  .section-head {font-size:1.65rem!important}
  .hm-card {padding:16px!important;min-height:0!important}
  .footer {font-size:.8rem!important;line-height:1.6!important}
}

/* Compact mobile-first home header and unobtrusive Streamlit chrome. */
@media (max-width:720px) {
 .hm-hero-refined {padding:8px 10px 20px!important;border-radius:18px!important;min-height:0!important}
 .hm-hero-refined:after {display:none!important}
 .hm-logo-focus img {width:min(215px,70vw)!important;max-height:185px!important;object-fit:contain!important}
 .hm-single-message {font-size:.82rem!important;line-height:1.35!important;margin:0 auto!important}
 .section-head {margin:12px 0 6px!important}
 .lead {font-size:.92rem!important;line-height:1.45!important}
 [data-testid="stVerticalBlock"] {gap:.55rem}
}

/* Homepage touch targets and mobile spacing; keep safety disclosures accessible. */
@media(max-width:720px){
  [data-testid="stButton"] button {min-height:42px!important;padding:.35rem .35rem!important;font-size:.88rem!important;border-radius:14px!important}
  .hm-hero-refined {padding:6px 10px 15px!important}
  .hm-logo-focus img {width:min(190px,62vw)!important;max-height:160px!important}
  .hm-single-message {font-size:.78rem!important}
  [data-testid="stExpander"] summary {padding:.65rem!important}
}
</style>
""",unsafe_allow_html=True)

# Compact brand header is shown only on the homepage, leaving feature pages room to breathe.
if st.session_state.page == "🏡 Home":
    st.markdown(f"""<section class="hm-hero hm-hero-refined">
    <div class="hm-logo-focus"><img src="https://raw.githubusercontent.com/olohi184/HerMamaAI/main/HerMamaAI%20Mother%20and%20Baby%20Emblem.png" alt="HerMamaAI mother and baby brand logo"></div>
    <p class="hm-single-message">{escape(t("home.tagline"))}</p>
    </section>""", unsafe_allow_html=True)
    st.caption(t("home.prototype"))

# Navigation stays near the top so key services are easy to reach on Android.
choose_language()
if st.session_state.hm_language != "en":
    st.info(t("language.notice"))
nav = ["🏡 Home","👶 BabyCare","🤰 Pregnancy care","💞 MamaCare journey","💗 Postpartum recovery","📅 CareCalendar","🌷 Emotional wellness","🏥 Find care","📖 Learning hub","🌼 Calm Corner","🌱 AdaptiveCare"]
if st.session_state.page == "🏡 Home":
    st.markdown("#### " + t("home.explore"))
    quick = [
        (t("home.pregnancy"), "🤰 Pregnancy care"),
        (t("home.mamacare"), "💞 MamaCare journey"),
        (t("home.babycare"), "👶 BabyCare"),
        (t("home.calendar"), "📅 CareCalendar"),
        (t("home.findcare"), "🏥 Find care"),
        (t("home.wellness"), "🌷 Emotional wellness"),
        (t("home.adaptive"), "🌱 AdaptiveCare"),
    ]
    for offset in range(0, len(quick), 2):
        cols = st.columns(2)
        for col, (label, target) in zip(cols, quick[offset:offset + 2]):
            with col:
                st.button(label, key="quick_" + target, use_container_width=True, on_click=go, args=(target,))
st.selectbox(t("nav.explore"), nav, index=nav.index(st.session_state.page) if st.session_state.page in nav else 0, format_func=localized_navigation, key="hm_mobile_nav", on_change=lambda: go(st.session_state.hm_mobile_nav))
with st.expander(t("safety.heading"), expanded=False):
    st.warning("HerMamaAI is an educational research prototype. It is not a clinician, diagnosis tool, medical device or emergency service. For serious symptoms, seek immediate in-person medical care.")
    st.caption(t("safety.review_status"))
st.caption(t("safety.caption"))
if st.session_state.hm_language != "en":
    # This is a translation-status notice, not a translated clinical instruction.
    # Display the local-language draft alongside the English safety fallback.
    st.warning(localized_label("safety.emergency_translation_notice") + "\n\n" + localized_label("safety.emergency_translation_notice", "en"))
page = st.session_state.page
if page == "🌱 AdaptiveCare":
    render_adaptivecare()

elif page == "🏡 Home":
    st.markdown(f'<div class="section-head" style="text-align:center">{escape(t("home.welcome"))}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="lead" style="text-align:center">{escape(t("home.lead"))}</p>', unsafe_allow_html=True)
    with st.expander(t("home.about")):
        st.write(t("home.about_body"))
    st.markdown(f'<div class="soft"><b>{escape(t("home.continues"))}</b> {escape(t("home.continues_body"))}</div>',unsafe_allow_html=True)
    st.button(t("home.calm"), key="home_calm", use_container_width=True, on_click=go, args=("🌼 Calm Corner",))

elif page == "📅 CareCalendar":
    st.markdown('<div class="section-head">' + escape(ui('📅 My CareCalendar')) + '</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">' + escape(ui('A simple place to organize antenatal and postnatal visits, and explore topics to discuss with your maternity team.')) + '</p>',unsafe_allow_html=True)
    st.info(ui("**Two different things:** Your appointments are dates you enter from your care plan. Suggested milestones below are educational topics only — not booked appointments or a personalized medical schedule."))
    st.caption(ui("Privacy: entries are held in this app session only. They are not saved to a database or sent to a clinic. Avoid entering personal medical information or identifying clinic details on a shared device."))
    if "care_appointments" not in st.session_state:
        st.session_state.care_appointments = []
    with st.form("carecalendar_add",clear_on_submit=True):
        st.markdown("#### " + ui("Add an appointment"))
        kind = st.selectbox(ui("Visit type"),["Antenatal visit","Postnatal follow-up","Other maternity appointment"], format_func=display_option)
        a,b = st.columns(2)
        with a:
            ap_date = st.date_input(ui("Appointment date"),value=date.today(),min_value=date.today())
        with b:
            ap_time = st.time_input(ui("Appointment time"),value=time(10,0),step=1800)
        note = st.text_input(ui("Optional short label"),placeholder="e.g. Routine check-up",max_chars=70)
        submitted = st.form_submit_button(ui("Add to my calendar"),type="primary",use_container_width=True)
        if submitted:
            st.session_state.care_appointments.append({"kind":kind,"date":ap_date,"time":ap_time,"note":note.strip()})
            st.success(ui("Added to this session's calendar. This does not book a clinic visit."))
    st.markdown("#### " + ui("My planned appointments"))
    items = sorted(enumerate(st.session_state.care_appointments),key=lambda x:(x[1]["date"],x[1]["time"]))
    if not items:
        st.caption(ui("No appointments entered yet. Add a visit above to begin."))
    for original_index, ap in items:
        st.markdown(f'<div class="timeline"><b>📍 {escape(ap["date"].strftime("%a %d %b %Y"))} · {escape(ap["time"].strftime("%I:%M %p"))}</b><br>{escape(display_option(ap["kind"]))}{(" · " + escape(ap["note"])) if ap["note"] else ""}</div>',unsafe_allow_html=True)
        c1,c2=st.columns([3,1])
        with c1:
            start=datetime.combine(ap["date"],ap["time"])
            end=start+timedelta(hours=1)
            def ics_safe(value):
                return str(value).replace("\\","\\\\").replace(";","\\;").replace(",","\\,").replace("\n","\\n")
            title=ics_safe("HerMamaAI: "+ap["kind"]+(" - "+ap["note"] if ap["note"] else ""))
            ics="\r\n".join(["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//WechimAI//HerMamaAI//EN","BEGIN:VEVENT","UID:hermamaai-"+str(original_index)+"-"+start.strftime("%Y%m%dT%H%M%S")+"@local","DTSTAMP:"+datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),"DTSTART:"+start.strftime("%Y%m%dT%H%M%S"),"DTEND:"+end.strftime("%Y%m%dT%H%M%S"),"SUMMARY:"+title,"DESCRIPTION:Personal planning reminder only. Confirm timing with your maternity team. Time is local to your calendar.","BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:HerMamaAI appointment reminder - confirm details with your maternity team.","TRIGGER:-P1D","END:VALARM","END:VEVENT","END:VCALENDAR",""])
            st.download_button(ui("⬇️ Add to phone calendar (.ics)"),data=ics,file_name="hermamaai-appointment.ics",mime="text/calendar",key=f"ics_{original_index}",use_container_width=True)
        with c2:
            if st.button(ui("Remove"),key=f"remove_{original_index}",use_container_width=True):
                st.session_state.care_appointments.pop(original_index)
                st.rerun()
    st.markdown("#### " + ui("Educational antenatal milestones"))
    st.caption(ui("These are discussion prompts, not dates or a substitute for local antenatal guidance. Your maternity team determines your individual care schedule."))
    with st.expander(ui("Early pregnancy · Establishing antenatal care"),expanded=True):
        st.write(ui("Discuss when to begin antenatal care, recommended screening, nutrition and supplements, medicines, and whom to call for urgent concerns."))
    with st.expander(ui("Middle pregnancy · Ongoing monitoring")):
        st.write(ui("Ask about the recommended timing of check-ups, scans and tests, your baby's development, and any symptoms that concern you."))
    with st.expander(ui("Later pregnancy · Preparing for birth")):
        st.write(ui("Discuss your birth preferences, delivery location, transport plan, emergency contacts and postpartum follow-up arrangements."))
    with st.expander(ui("After delivery · Continuing postnatal care")):
        st.write(ui("Ask your maternity team when to return after discharge, what recovery symptoms need assessment, and how to obtain feeding and emotional support."))
    st.error("**Urgent symptoms?** Heavy bleeding, seizures, chest pain, difficulty breathing, severe headache or visual changes, fainting, or thoughts of harming yourself or your baby need immediate professional help. Do not wait for a calendar reminder.")

    st.markdown("#### " + ui("Make your calendar work for you"))
    with st.expander(ui("How to add a reminder to your phone")):
        st.write(ui("Enter the appointment date and time given by your maternity team, select Add to my calendar, then use the .ics download button. Open the downloaded file in your phone's calendar and confirm that the event appears. The exported event requests a reminder 1 day before the appointment; whether an alert appears depends on your phone calendar app and notification settings. HerMamaAI itself does not send notifications. For appointments less than 1 day away, set a suitable reminder manually in your calendar."))
    with st.expander(ui("What to prepare before a visit")):
        st.write(ui("Bring any maternity notes you have, a list of medicines or supplements, questions you want answered, and any instructions your maternity team has given you. Ask a trusted person to help with transport if needed."))

elif page == "🤰 Pregnancy care":
    st.markdown('<div class="section-head">' + escape(ui("🤰 Pregnancy care")) + '</div>',unsafe_allow_html=True)
    st.markdown(f'<p class="lead">{escape(t("preg.intro"))}</p>',unsafe_allow_html=True)
    st.button(ui("📅 Plan an antenatal visit in CareCalendar →"),use_container_width=True,on_click=go,args=("📅 CareCalendar",))
    st.subheader(ui("Questions for your maternity team"))
    for i,q in enumerate(["When should I attend my next antenatal visit?","Which symptoms mean I should seek urgent help?","Which medicines or supplements are appropriate for me?","What is my birth and emergency transport plan?"]):
        st.checkbox(ui(q),key=f"preg_{i}")
    st.error(ui("Seek urgent medical assessment for vaginal bleeding, severe abdominal pain, severe headache or vision changes, seizures, chest pain or trouble breathing.") + ("\n\n" + ui("English reference:") + " Seek urgent medical assessment for vaginal bleeding, severe abdominal pain, severe headache or vision changes, seizures, chest pain or trouble breathing." if st.session_state.get("hm_language", "en") != "en" else ""))

    st.markdown("#### " + ui("Pregnancy learning topics"))
    with st.expander(ui("Nutrition, rest and everyday well-being")):
        st.write(ui("Ask your maternity team about a varied diet, food safety, hydration, recommended supplements, activity, rest and any individual restrictions. Avoid starting or stopping medicines or supplements based on app content."))
    with st.expander(ui("Understanding antenatal checks")):
        st.write(ui("Antenatal visits may include blood pressure measurement, laboratory tests, screening, fetal growth monitoring and discussion of symptoms. What is appropriate depends on your stage of pregnancy, medical history and local guidance."))
    with st.expander(ui("Preparing for delivery")):
        st.write(ui("Discuss where you plan to give birth, how you will travel there, whom to contact, what to pack and who can support you. Review emergency arrangements with your maternity team."))
    with st.expander(ui("Questions about baby's movement")):
        st.write("Ask your maternity team what movements to expect and what to do if movement decreases or changes. Seek prompt professional assessment for concerns about reduced movement; do not wait for an app or a scheduled visit.")
    st.markdown("#### " + ui("A small step today"))
    st.checkbox(ui("I have written down a question to ask at my next antenatal visit."),key="preg_extra")
    
elif page == "💞 MamaCare journey":
    render_mamacare(go)

elif page == "💗 Postpartum recovery":
    st.markdown('<div class="section-head">' + escape(ui("💗 Postpartum recovery")) + '</div>',unsafe_allow_html=True)
    st.markdown(f'<p class="lead">{escape(t("post.intro"))}</p>',unsafe_allow_html=True)
    with st.expander(ui("The first days after birth"),expanded=True):
        st.write("Ask your team about bleeding, pain, feeding, wound care, blood pressure checks where indicated, sleep, and when to return for follow-up.")
    with st.expander(ui("Weeks 2–6: stay connected")):
        st.write("Do not dismiss new or worsening symptoms. Contact your maternity facility if you miss an appointment or are concerned about recovery.")
    with st.expander(ui("Beyond six weeks")):
        st.write("Persistent pain, mood changes, bladder or pelvic-floor symptoms, feeding concerns or other ongoing difficulties deserve professional assessment.")
    st.button(ui("Explore MamaCare Continuity →"),type="primary",use_container_width=True,on_click=go,args=("💞 MamaCare journey",))
    st.error(ui("**Urgent warning signs:** Heavy bleeding, chest pain, trouble breathing, seizures, severe headache or vision changes, fainting, fever with severe illness, or thoughts of harming yourself or your baby. Seek emergency medical care immediately.") + ("\n\n" + ui("English reference:") + " **Urgent warning signs:** Heavy bleeding, chest pain, trouble breathing, seizures, severe headache or vision changes, fainting, fever with severe illness, or thoughts of harming yourself or your baby. Seek emergency medical care immediately." if st.session_state.get("hm_language", "en") != "en" else ""))

    st.markdown("#### " + ui("More postpartum recovery topics"))
    with st.expander(ui("Healing and comfort")):
        st.write(ui("Recovery varies after vaginal birth and caesarean birth. Ask your clinician about pain control, incision or perineal care, expected bleeding, safe activity and when to seek assessment for changes."))
    with st.expander(ui("Feeding support without judgment")):
        st.write("Whether breastfeeding, formula feeding or combining approaches, seek individualized guidance from qualified professionals if feeding is painful, difficult or worrying. Your well-being matters too.")
    with st.expander(ui("Sleep, fatigue and asking for practical help")):
        st.write(ui("Rest can be difficult with a newborn. Consider asking trusted people for help with household tasks and discuss severe or persistent exhaustion with your care team."))
    with st.expander(ui("Mood and relationships after birth")):
        st.write("Emotional changes can affect parents and relationships. Talk openly with someone you trust and contact a qualified professional if distress persists, intensifies or interferes with daily life.")
    
elif page == "🌷 Emotional wellness":
    st.markdown('<div class="section-head">' + escape(ui("🌷 Emotional wellness")) + '</div>',unsafe_allow_html=True)
    st.markdown(f'<p class="lead">{escape(t("well.intro"))}</p>',unsafe_allow_html=True)
    card("You can ask for help","💬","If sadness, anxiety, hopelessness or overwhelm persists, worsens, or affects daily life, speak with a qualified healthcare professional.")
    st.subheader(ui("Gentle ways to reach out"))
    st.write("• Tell someone you trust how you are feeling.\n\n• Ask for practical help with meals, chores or childcare.\n\n• Discuss mood and sleep concerns at a postnatal appointment.")
    st.error("If you may harm yourself or someone else, or experience severe confusion or unusual perceptions, seek emergency medical help immediately and ask a trusted person to stay with you.")

    st.markdown("#### " + ui("Emotional wellness toolkit"))
    with st.expander(ui("Check in with yourself")):
        st.write("You might gently ask: What do I need today? Have I eaten and rested as much as I can? Is there someone I can talk to? These prompts are not a mental-health assessment.")
    with st.expander(ui("Simple connection ideas")):
        st.write(ui("Consider sending a short message to a trusted friend, asking someone to sit with you, or sharing a specific task you need help with."))
    with st.expander(ui("When to seek professional support")):
        st.write("Persistent sadness, intense anxiety, hopelessness, inability to function, or distressing thoughts deserve prompt assessment by a qualified healthcare professional. Emergency symptoms need immediate help.")
    st.button(ui("🌼 Open the Calm Corner"),key="wellness_calm",use_container_width=True,on_click=go,args=("🌼 Calm Corner",))
    
elif page == "👶 BabyCare":
    from babycare import render_babycare
    render_babycare()

elif page == "🏥 Find care":
    from find_care import render_find_care
    render_find_care()

elif page == "🌼 Calm Corner":
    st.markdown('<div class="section-head">' + escape(ui("🌼 Motherhood Calm Corner")) + '</div>',unsafe_allow_html=True)
    st.markdown(f'<p class="lead">{escape(t("calm.intro"))}</p>',unsafe_allow_html=True)
    st.info("These are general relaxation activities, not treatment for anxiety, depression or physical symptoms. Stop any activity that feels uncomfortable. If you feel unwell or have urgent symptoms, seek professional medical care.")
    st.subheader(ui("Choose a gentle activity"))
    st.caption(ui("Pick a peaceful moment just for you. No pressure, no scores."))
    activities = [
        ("🌸", "Grow your garden", "Plant flowers and watch your little garden bloom.", "#fff0f7", "#a91470"),
        ("☁️", "Gentle moments", "Find a calm scene and enjoy a quiet pause.", "#eef5ff", "#385e9b"),
        ("🦋", "Memory Garden", "Match cheerful pictures at your own pace.", "#f2edff", "#7140a5"),
        ("🔤", "Mama Word Garden", "Unscramble gentle, encouraging words.", "#fff5e9", "#95601e"),
        ("🫙", "Gratitude Jar", "Collect small moments worth remembering.", "#edf9f3", "#237b62"),
        ("🎨", "Colour & Bloom", "Create a colourful bouquet of flowers.", "#fff0f2", "#a94465"),
    ]
    if "calm_activity" not in st.session_state:
        st.session_state.calm_activity = 0
    st.markdown("""<style>
    div[class*="st-key-calm_choice_"] button {
        min-height: 58px !important;
        border-radius: 0 0 18px 18px !important;
        border: 1px solid #e8cde8 !important;
        background: #ffffffcc !important;
        color: #682c73 !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 18px #6330730c !important;
    }
    div[class*="st-key-calm_choice_"] button:hover {
        border-color: #bc70c4 !important;
        background: #f9eafb !important;
    }
    .calm-activity-card {
        padding: 22px 16px 14px;
        border: 1px solid #e8cde8;
        border-radius: 18px 18px 0 0;
        min-height: 168px;
        text-align: center;
        box-shadow: 0 8px 18px #6330730c;
    }
    .calm-activity-card.selected { border: 2px solid #a94eb5; box-shadow: 0 8px 24px #a94eb52b; }
    .calm-activity-icon { font-size: 2.4rem; margin-bottom: 4px; }
    .calm-activity-title { font-size: 1.12rem; font-weight: 750; margin-bottom: 7px; }
    .calm-activity-desc { font-size: .92rem; line-height: 1.4; color: #61576b; }
    .calm-selected { font-size: .76rem; font-weight: 700; color: #842b8b; margin-top: 7px; }
    </style>""", unsafe_allow_html=True)
    for start in (0, 3):
        cols = st.columns(3, gap="medium")
        for offset, col in enumerate(cols):
            index = start + offset
            symbol, name, description, background, accent = activities[index]
            # Reuse existing translated game headings for the activity cards.
            game_heading = (
                "🌸 Game 1: Grow your garden",
                "☁️ Game 2: Choose a gentle moment",
                "🦋 Game 3: Memory Garden",
                "🔤 Game 4: Mama Word Garden",
                "🫙 Game 5: Gratitude Jar",
                "🎨 Game 6: Colour & Bloom",
            )[index]
            localized_name = ui(game_heading)
            active = st.session_state.calm_activity == index
            with col:
                st.markdown(
                    '<div class="calm-activity-card'+(' selected' if active else '')+'" style="background:'+background+'">'
                    '<div class="calm-activity-icon">'+symbol+'</div>'
                    '<div class="calm-activity-title" style="color:'+accent+'">'+escape(localized_name)+'</div>'
                    '<div class="calm-activity-desc">'+escape(ui(description))+'</div>'
                    + ('<div class="calm-selected">● '+escape(ui("Currently selected"))+'</div>' if active else '') + '</div>',
                    unsafe_allow_html=True
                )
                if st.button(ui("Playing now ✓" if active else "Explore activity →"), key=f"calm_choice_{index}", use_container_width=True):
                    st.session_state.calm_activity = index
                    st.rerun()
    # Offline-first, reviewed recordings for Nigerian languages. Never substitute
    # an English browser voice for a missing Hausa/Yoruba/Igbo recording.
    from localization.offline_calm_audio import approved_audio_path
    _spoken_code = st.session_state.get("hm_language", "en")
    if _spoken_code in ("ha", "yo", "ig"):
        _approved_recording = approved_audio_path(
            _spoken_code, st.session_state.calm_activity
        )
        if _approved_recording is not None:
            st.audio(str(_approved_recording), format=(
                "audio/mpeg" if _approved_recording.suffix == ".mp3" else "audio/wav"
            ))
        else:
            st.info(t("audio.voice_unavailable"))
            st.caption(t("calm.offline_audio_pending"))
    else:
        # Optional, user-triggered browser audio for non-medical Calm Corner text only.
        # The browser must have a matching installed voice; do not silently use a
        # different language or claim offline/multilingual audio availability.
        import json as _audio_json
        _spoken_code = st.session_state.get("hm_language", "en")
        _speech_tags = {"en": "en", "ha": "ha", "yo": "yo", "ig": "ig"}
        _spoken_description = ui(activities[st.session_state.calm_activity][2])
        _audio_keys = ("listen", "stop", "unsupported", "voice_unavailable",
                       "finished", "playback_error", "playing", "stopped")
        _speech_data = _audio_json.dumps({
            "text": _spoken_description,
            "language": _speech_tags.get(_spoken_code, "en"),
            "messages": {key: t("audio." + key) for key in _audio_keys},
        }, ensure_ascii=False).replace("<", "\\u003c")
        components.html("""
        <div style="font:14px system-ui,sans-serif;color:#6b4771">
          <button id="hm-speak" type="button" style="padding:9px 14px;border-radius:10px;border:1px solid #b57cbd;background:#fff;color:#682c73;cursor:pointer">🔊 <span id="hm-listen-label"></span></button>
          <button id="hm-stop" type="button" style="padding:9px 14px;border-radius:10px;border:1px solid #ddd;background:#fff;cursor:pointer"><span id="hm-stop-label"></span></button>
          <p id="hm-audio-status" role="status" aria-live="polite" style="margin:5px 0"></p>
        </div>
        <script>
        const item = """ + _speech_data + """;
        const status = document.getElementById('hm-audio-status');
        document.getElementById('hm-listen-label').textContent = item.messages.listen;
        document.getElementById('hm-stop-label').textContent = item.messages.stop;
        const synth = window.speechSynthesis;
        let voices = [];
        let activeUtterance = null;
        const refreshVoices = () => {
          voices = synth ? synth.getVoices() : [];
          return voices;
        };
        const voiceFor = () => refreshVoices().find(v =>
          (v.lang || '').toLowerCase().split(/[-_]/)[0] === item.language
        );
        // Safari and Chrome may populate voices after the component first renders.
        if (synth) {
          refreshVoices();
          if (synth.addEventListener) {
            synth.addEventListener('voiceschanged', refreshVoices);
          } else {
            synth.onvoiceschanged = refreshVoices;
          }
        }
        document.getElementById('hm-speak').addEventListener('click', () => {
          if (!synth || !window.SpeechSynthesisUtterance) {
            status.textContent = item.messages.unsupported; return;
          }
          const voice = voiceFor();
          if (!voice) {
            // Display the translated explanation and the requested language code.
            // Do not silently fall back to an English voice.
            status.textContent = item.messages.voice_unavailable + ' (' + item.language + ')';
            return;
          }
          synth.cancel();
          const utterance = new SpeechSynthesisUtterance(item.text);
          activeUtterance = utterance; // Keep a reference until playback ends.
          utterance.lang = voice.lang;
          utterance.voice = voice;
          utterance.onstart = () => { status.textContent = item.messages.playing; };
          utterance.onend = () => {
            if (activeUtterance === utterance) {
              status.textContent = item.messages.finished;
              activeUtterance = null;
            }
          };
          utterance.onerror = (event) => {
            if (activeUtterance === utterance) {
              status.textContent = item.messages.playback_error +
                (event.error ? ' (' + event.error + ')' : '');
              activeUtterance = null;
            }
          };
          status.textContent = item.messages.playing;
          synth.speak(utterance);
        });
        document.getElementById('hm-stop').addEventListener('click', () => {
          activeUtterance = null;
          if (synth) synth.cancel();
          status.textContent = item.messages.stopped;
        });
        </script>
        """, height=90)
        st.caption("Audio is optional and device-dependent. Only Calm Corner activity descriptions are eligible; medical guidance is not read aloud.")
    st.divider()
    st.markdown("""<style>
    @keyframes mamaBloom { from {opacity:0;transform:translateY(9px) scale(.9)} to {opacity:1;transform:translateY(0) scale(1)} }
    @keyframes mamaFloat { 0%,100% {transform:translateY(0)} 50% {transform:translateY(-5px)} }
    .mama-garden-stage { min-height:175px; padding:25px 18px 20px; border-radius:25px; border:1px solid #e9c8df; background:linear-gradient(180deg,#fff0f8 0%,#f8efff 70%,#e5f5e9 70%,#d3efd8 100%); text-align:center; display:flex; align-items:center; justify-content:center; flex-direction:column; gap:14px; overflow:hidden; }
    .mama-garden-stage .mama-flowers {font-size:2.7rem; line-height:1.8; letter-spacing:5px; animation:mamaBloom .45s ease-out both; overflow-wrap:anywhere}
    .mama-garden-stage .mama-empty {font-size:1.12rem;color:#6b4771;line-height:1.6}
    .mama-scene-stage {border:1px solid #d7d0ee;border-radius:25px;min-height:170px;padding:24px;background:linear-gradient(125deg,#edf7ff,#fff1f8,#f2edff);text-align:center}
    .mama-scene-stage .scene-icon {font-size:3.5rem;animation:mamaFloat 5s ease-in-out infinite}
    .mama-scene-stage .scene-text {max-width:700px;margin:12px auto 0;color:#544760;font-size:1.08rem;line-height:1.6}
    .mama-jar-stage {min-height:145px;padding:22px;border-radius:25px;background:linear-gradient(135deg,#e9f9f1,#f7e9ff);border:1px solid #d4e8dc;text-align:center}
    .mama-jar-stage .jar-icon {font-size:3rem;animation:mamaFloat 5s ease-in-out infinite}
    .mama-jar-stage .jar-notes {color:#5d3e69;font-size:1.05rem;line-height:1.9}
    .mama-memory-intro {text-align:center;color:#78437c;font-size:1.08rem;font-weight:650;padding:12px 8px;margin:8px 0 15px;border-radius:18px;background:linear-gradient(100deg,#fff2f9,#f0f9f2)}
    div[class*="st-key-memory_"] button {min-height:112px!important;width:100%!important;max-width:none!important;border-radius:22px!important;border:2px solid #e6b8e7!important;background:linear-gradient(140deg,#fff7fc,#f0e5ff)!important;box-shadow:0 6px 16px rgba(106,52,127,.11)!important;font-size:2.7rem!important;color:#873d96!important;transition:transform .18s ease,background .18s ease,box-shadow .18s ease!important}
    div[class*="st-key-memory_"] button:hover:not(:disabled) {transform:translateY(-3px);background:linear-gradient(140deg,#ffeaf6,#e6d7ff)!important;box-shadow:0 10px 22px rgba(106,52,127,.18)!important}
    div[class*="st-key-memory_"] button:disabled {opacity:1!important}
    div[class*="st-key-memory_"] button p {font-size:clamp(1.9rem,3vw,2.7rem)!important;line-height:1.25!important} 
    div.st-key-memory_reset button, div.st-key-memory_flip_back button {width:100%!important;max-width:none!important;min-height:52px!important;font-size:1rem!important} 
    div.st-key-memory_reset button p, div.st-key-memory_flip_back button p {font-size:1rem!important} 
    .mama-memory-finish {display:flex;flex-direction:column;align-items:center;gap:10px;padding:24px 15px;margin-top:18px;text-align:center;background:linear-gradient(120deg,#fff0f8,#e8f9ed,#f1e8ff);border:1px solid #e7c5e4;border-radius:24px;color:#673870}
    .mama-memory-flowers {font-size:2.4rem;animation:mamaBloom .6s ease-out both}
    @media(max-width:640px){div[class*="st-key-memory_"] button{min-height:80px!important;font-size:1.7rem!important;border-radius:16px!important}}
    @media(prefers-reduced-motion:reduce){div[class*="st-key-memory_"] button{transition:none!important}div[class*="st-key-memory_"] button:hover:not(:disabled){transform:none}.mama-memory-flowers{animation:none!important}}
    .mama-word-tiles {display:flex;flex-wrap:wrap;justify-content:center;gap:clamp(7px,2vw,18px);padding:22px 12px;border-radius:24px;background:linear-gradient(135deg,#fff9e9,#fff0f8);border:1px solid #f1d4a9}
    .mama-letter-tile {display:inline-flex;align-items:center;justify-content:center;min-width:clamp(48px,10vw,78px);height:clamp(58px,12vw,88px);padding:8px;border-radius:18px;background:#fff;color:#793674;font-size:clamp(1.7rem,4vw,2.6rem);font-weight:800;box-shadow:0 6px 18px rgba(112,54,110,.13);border:1px solid #f0d5e6}
    .mama-word-celebrate {margin:12px 0;padding:18px;border-radius:20px;background:linear-gradient(115deg,#f7e8ff,#fff1f5,#eaf9f0);border:1px solid #ebc9e4;display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center;color:#63346c}
    .mama-word-flowers {font-size:2rem;animation:mamaBloom .55s ease-out both}
    .mama-word-stage {border:1px solid #f1d4a9;border-radius:24px;background:linear-gradient(135deg,#fff9e9,#fff0f8);text-align:center;padding:28px 12px;font-size:2.5rem;font-weight:800;letter-spacing:10px;color:#803c79}
    @media(prefers-reduced-motion:reduce){.mama-garden-stage .mama-flowers,.mama-scene-stage .scene-icon,.mama-jar-stage .jar-icon{animation:none!important}}
    </style>""",unsafe_allow_html=True)
    if st.session_state.calm_activity == 0:
        st.markdown("### " + ui("🌸 Game 1: Grow your garden"))
        st.write(ui("Tap **Plant a flower** to create a little garden. There is no timer and no wrong move."))
        if "garden_count" not in st.session_state:
            st.session_state.garden_count = 0
        flowers = ["🌷","🌸","🌻","🌼","🪻","🌺"]
        st.markdown("""<style>
        .hm-garden {position:relative;overflow:hidden;min-height:285px;border-radius:28px;
          background:linear-gradient(180deg,#f9e8ff 0%,#fff0f6 42%,#e2f7ee 76%,#c4e7c3 100%);
          border:1px solid #eac5e5;box-shadow:0 12px 30px rgba(114,54,112,.09)}
        .hm-garden-sun{position:absolute;top:20px;right:11%;width:67px;height:67px;border-radius:50%;
          background:#fff5c5;box-shadow:0 0 45px 16px #fff6d9a8}
        .hm-garden-hill{position:absolute;bottom:-42px;left:-8%;width:116%;height:115px;
          background:linear-gradient(180deg,#a7d9a9,#77bd96);border-radius:50% 50% 0 0}
        .hm-garden-hill.two{bottom:-69px;left:30%;background:#8ccaa3;height:125px}
        .hm-garden-cloud{position:absolute;top:26px;left:9%;font-size:2.5rem;opacity:.8}
        .hm-garden-butterfly{position:absolute;top:70px;right:25%;font-size:2.1rem;animation:hmFloat 5s ease-in-out infinite}
        .hm-garden-flowerbed{position:relative;z-index:2;display:flex;justify-content:center;align-items:end;
          flex-wrap:wrap;gap:10px 16px;padding:115px 20px 28px;min-height:285px}
        .hm-garden-flower{font-size:clamp(2.3rem,5vw,3.5rem);line-height:1.25;display:inline-block;
          filter:drop-shadow(0 7px 5px #456a4d30);animation:hmBloom .65s cubic-bezier(.2,1.3,.4,1) both}
        .hm-garden-empty{position:relative;z-index:2;align-self:center;text-align:center;
          background:#ffffffc9;border-radius:20px;padding:16px 22px;color:#64376a;font-weight:600}
        .hm-garden-caption{text-align:center;color:#76416e;font-size:.94rem;margin:10px 0 18px}
        @keyframes hmBloom{from{transform:scale(.25) translateY(20px);opacity:.1}to{transform:scale(1) translateY(0);opacity:1}}
        @keyframes hmFloat{0%,100%{transform:translate(0,0) rotate(-8deg)}50%{transform:translate(-16px,-12px) rotate(8deg)}}
        @media(max-width:640px){.hm-garden{min-height:235px}.hm-garden-flowerbed{min-height:235px;padding:100px 14px 22px;gap:7px}}
        @media(prefers-reduced-motion:reduce){.hm-garden-flower,.hm-garden-butterfly{animation:none!important}}
        </style>""",unsafe_allow_html=True)
        planted = st.session_state.garden_count
        blooms = "".join('<span class="hm-garden-flower" aria-label="flower">'+flowers[i % len(flowers)]+'</span>' for i in range(planted))
        if not blooms:
            blooms = ('<div class="hm-garden-empty">'
                      + escape(t("calm.garden_empty_title"))
                      + '<br>'
                      + escape(t("calm.garden_empty_instruction"))
                      + '</div>')
        garden_html = ('<div class="hm-garden" role="img" aria-label="A peaceful illustrated garden with '
                       +str(planted)+' planted flowers"><div class="hm-garden-sun"></div>'
                       '<div class="hm-garden-cloud">☁️</div><div class="hm-garden-butterfly">🦋</div>'
                       '<div class="hm-garden-hill"></div><div class="hm-garden-hill two"></div>'
                       '<div class="hm-garden-flowerbed">'+blooms+'</div></div>')
        st.markdown(garden_html,unsafe_allow_html=True)
        st.markdown('<p class="hm-garden-caption">' + escape(ui("A little space to grow, at your own pace. 🌿")) + '</p>',unsafe_allow_html=True)
        g1,g2=st.columns(2)
        with g1:
            if st.button(ui("🌷 Plant a flower"),key="plant_flower",use_container_width=True):
                st.session_state.garden_count=min(24,st.session_state.garden_count+1)
                st.rerun()
        with g2:
            if st.button(ui("↺ Start a new garden"),key="reset_garden",use_container_width=True):
                st.session_state.garden_count=0
                st.rerun()
        if st.session_state.garden_count>=24:
            st.success(t("calm.garden_complete"))
    if st.session_state.calm_activity == 1:
        st.markdown("### " + ui("☁️ Game 2: Choose a gentle moment"))
        moments = {
            "🌤️ A peaceful morning":"Imagine a quiet morning, a comfortable chair and a warm cup of something you enjoy.",
            "🌿 A garden breeze":"Picture leaves moving softly in a garden. Notice the colors and shapes around you.",
            "🌊 A calm shoreline":"Imagine gentle waves rolling in and out. Rest your attention on the scene without forcing your breathing.",
            "🌙 A quiet evening":"Imagine soft evening light and a safe, restful space. Allow yourself a moment without a task to complete."
        }
        scene=st.radio("Pick a relaxing scene",list(moments),horizontal=True,key="calm_scene")
        scene_key = {
            "🌤️ A peaceful morning": "morning",
            "🌿 A garden breeze": "garden",
            "🌊 A calm shoreline": "shore",
            "🌙 A quiet evening": "evening"
        }[scene]
        scene_art = {
            "morning": '<div class="hm-sun"></div><div class="hm-cloud">☁️</div><div class="hm-hills"></div><div class="hm-art-detail">🌼 🌷 🌻</div>',
            "garden": '<div class="hm-sun"></div><div class="hm-cloud">☁️</div><div class="hm-hills"></div><div class="hm-art-detail">🌿 🌸 🦋 🌷 🌿</div>',
            "shore": '<div class="hm-sun"></div><div class="hm-cloud">☁️</div><div class="hm-water"></div><div class="hm-art-detail">🐚 🌊 🐚</div>',
            "evening": '<div class="hm-moon">🌙</div><div class="hm-stars">✦　✧　✦　✧</div><div class="hm-hills"></div><div class="hm-art-detail">🌿 ✨ 🌷</div>'
        }
        st.markdown("""<style>
        .hm-moment{position:relative;isolation:isolate;overflow:hidden;border-radius:28px;
          border:1px solid #e5c8e9;min-height:330px;margin:14px 0 10px;
          box-shadow:0 14px 32px #693d7420}
        .hm-moment.morning{background:linear-gradient(180deg,#fff1d6,#ffe7df 60%,#e6f5df)}
        .hm-moment.garden{background:linear-gradient(180deg,#f3e5ff,#e9f9ee 65%,#c7e6c9)}
        .hm-moment.shore{background:linear-gradient(180deg,#d9f1ff,#eaf8ff 60%,#b4e4eb)}
        .hm-moment.evening{background:linear-gradient(180deg,#403264,#8d6d9d 72%,#b9a4c8)}
        .hm-sun{position:absolute;top:34px;right:15%;height:75px;width:75px;border-radius:50%;
          background:#fff1b4;box-shadow:0 0 45px 15px #fff0b88a}
        .hm-cloud{position:absolute;top:42px;left:13%;font-size:3rem;opacity:.82;animation:hmDrift 9s ease-in-out infinite}
        .hm-hills{position:absolute;bottom:-80px;left:-10%;width:120%;height:170px;
          border-radius:50% 50% 0 0;background:linear-gradient(#add9b1,#7cbb9b)}
        .hm-water{position:absolute;bottom:0;left:0;width:100%;height:40%;
          background:repeating-linear-gradient(175deg,#9dd9e6,#b8e9ee 16px,#d0f4f6 24px)}
        .hm-moon{position:absolute;top:25px;right:17%;font-size:4.5rem}
        .hm-stars{position:absolute;top:36px;left:13%;font-size:2rem;color:#fff5d6;letter-spacing:20px}
        .hm-art-detail{position:absolute;bottom:54px;left:0;right:0;text-align:center;
          font-size:clamp(2.5rem,5vw,4.3rem);letter-spacing:12px;animation:hmSway 5s ease-in-out infinite}
        .hm-moment-message{position:relative;z-index:2;margin:14px auto 18px;padding:15px 22px;
          width:min(88%,720px);background:#fffffff0;color:#573766;border-radius:18px;
          text-align:center;line-height:1.6;font-size:1.04rem;box-shadow:0 6px 24px #48335119}
        .hm-moment.evening .hm-moment-message{background:#fff9f4ed}
        @keyframes hmDrift{0%,100%{transform:translateX(0)}50%{transform:translateX(22px)}}
        @keyframes hmSway{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
        @media(max-width:640px){.hm-moment{min-height:310px}.hm-moment-message{margin-top:14px}
          .hm-art-detail{letter-spacing:2px;font-size:2.3rem}}
        @media(prefers-reduced-motion:reduce){.hm-cloud,.hm-art-detail{animation:none!important}}
        </style>""",unsafe_allow_html=True)
        st.markdown('<div class="hm-moment '+scene_key+'" aria-label="Peaceful '+scene_key+
                    ' landscape">'+scene_art[scene_key]+'</div><div class="hm-moment-message" role="note">'+
                    escape(moments[scene])+'</div>',unsafe_allow_html=True)
        st.markdown("""<style>
        div.st-key-memory_0 button, div.st-key-memory_1 button, div.st-key-memory_2 button,
        div.st-key-memory_3 button, div.st-key-memory_4 button, div.st-key-memory_5 button {
          min-height: 94px !important;
          background: linear-gradient(145deg,#f2e5ff,#ffe8f4) !important;
          border: 2px solid #c58bd3 !important;
          border-radius: 20px !important;
          box-shadow: 0 5px 14px rgba(99,40,112,.12) !important;
        }
        div.st-key-memory_0 button p, div.st-key-memory_1 button p, div.st-key-memory_2 button p,
        div.st-key-memory_3 button p, div.st-key-memory_4 button p, div.st-key-memory_5 button p {
          color: #64236f !important; font-size: 2.2rem !important; font-weight: 800 !important;
        }
        div.st-key-memory_0 button:hover, div.st-key-memory_1 button:hover, div.st-key-memory_2 button:hover,
        div.st-key-memory_3 button:hover, div.st-key-memory_4 button:hover, div.st-key-memory_5 button:hover {
          border-color: #a833a0 !important; background: #f4d6f2 !important;
        }
        </style>""", unsafe_allow_html=True)
        st.divider()
    if st.session_state.calm_activity == 2:
        import random
        st.markdown("### " + ui("🦋 Game 3: Memory Garden"))
        st.write(ui("Discover three matching pairs of cheerful garden pictures. No clock, no score — just a peaceful moment."))
        if "memory_cards" not in st.session_state:
            st.session_state.memory_cards = ["🌷", "🦋", "💗", "🌷", "💗", "🦋"]
            random.shuffle(st.session_state.memory_cards)
            st.session_state.memory_open = []
            st.session_state.memory_found = []
        cards = st.session_state.memory_cards
        st.markdown('<div class="mama-memory-intro">' + escape(ui("🌸 A little garden of surprises 🌿")) + '</div>', unsafe_allow_html=True)
        for row_start in (0, 3):
            cols = st.columns(3)
            for offset, col in enumerate(cols):
                idx = row_start + offset
                matched = idx in st.session_state.memory_found
                flipped = idx in st.session_state.memory_open
                label = (cards[idx] + " ✓") if matched else (cards[idx] if flipped else "🌿")
                state_style = ("background:linear-gradient(145deg,#e4f8e8,#d4f0de)!important;border-color:#77c997!important;" if matched else ("background:linear-gradient(145deg,#ffe3f2,#f9d9f5)!important;border-color:#d788c9!important;" if flipped else ""))
                if state_style:
                    st.markdown(f'<style>div.st-key-memory_{idx} button {{{state_style}}}</style>', unsafe_allow_html=True)
                with col:
                    if st.button(label, key=f"memory_{idx}", use_container_width=True, disabled=matched or flipped or len(st.session_state.memory_open)>=2, help=ui("Matched garden pair" if matched else "Turn over garden card")):
                        st.session_state.memory_open.append(idx)
                        st.rerun()
        if len(st.session_state.memory_open) == 2:
            first, second = st.session_state.memory_open
            if cards[first] == cards[second]:
                st.session_state.memory_found.extend([first, second])
                st.session_state.memory_open = []
                st.rerun()
            else:
                st.info("These pictures are different. Enjoy another look, then turn them back when you're ready.")
                if st.button(ui("🌿 Turn cards back"), key="memory_flip_back", use_container_width=True):
                    st.session_state.memory_open = []
                    st.rerun()
        if len(st.session_state.memory_found) == 6:
            st.markdown('<div class="mama-memory-finish" role="status"><div class="mama-memory-flowers">🌸 🦋 🌷 💗 🌼</div><strong>' + escape(ui("Your Memory Garden is blooming!")) + '</strong><span>' + escape(ui("All three pairs found. Beautifully done — enjoy this little moment.")) + '</span></div>', unsafe_allow_html=True)
        if st.button(ui("↺ Play Memory Garden again"), key="memory_reset", use_container_width=True):
            st.session_state.memory_cards = ["🌷", "🦋", "💗", "🌷", "💗", "🦋"]
            random.shuffle(st.session_state.memory_cards)
            st.session_state.memory_open = []
            st.session_state.memory_found = []
            st.rerun()

        st.divider()
    if st.session_state.calm_activity == 3:
        st.markdown("### " + ui("🔤 Game 4: Mama Word Garden"))
        st.write(ui("Arrange the letters into a gentle word. Take your time, or reveal the answer whenever you wish."))
        puzzles = [("ERAC", "CARE", "Care for yourself, too."), ("TSER", "REST", "Rest is valuable."), ("EPOH", "HOPE", "Small hopeful moments matter."), ("MOLBO", "BLOOM", "Grow at your own pace.")]
        if "word_index" not in st.session_state:
            st.session_state.word_index = 0
        scrambled, answer, encouragement = puzzles[st.session_state.word_index % len(puzzles)]
        tiles = "".join('<span class="mama-letter-tile">'+escape(letter)+'</span>' for letter in scrambled)
        st.markdown('<div class="mama-word-tiles" aria-label="'+escape(ui("Scrambled letters: "))+escape(" ".join(scrambled))+'">'+tiles+'</div>', unsafe_allow_html=True)
        guess = st.text_input(ui("Your answer"), key=f"word_guess_{st.session_state.word_index}", max_chars=20, placeholder=ui("Type the word here"))
        w1, w2, w3 = st.columns(3)
        with w1:
            check_clicked = st.button(ui("Check word"), key="word_check", use_container_width=True)
        with w2:
            reveal_clicked = st.button(ui("Reveal word"), key="word_reveal", use_container_width=True)
        with w3:
            next_clicked = st.button(ui("Next word →"), key="word_next", use_container_width=True)
        if next_clicked:
            st.session_state.word_index += 1
            st.session_state.pop("word_feedback", None)
            st.rerun()
        if check_clicked:
            if guess.strip().upper().replace(" ", "") == answer:
                st.session_state.word_feedback = ("correct", encouragement)
            else:
                st.session_state.word_feedback = ("hint", answer[0])
        if reveal_clicked:
            st.session_state.word_feedback = ("reveal", (answer, encouragement))
        feedback = st.session_state.get("word_feedback")
        if feedback:
            kind, message = feedback
            if kind == "correct":
                st.markdown('<div class="mama-word-celebrate" role="status"><span class="mama-word-flowers">🌸 🌷 🌼 🦋</span><strong>'+escape(ui("Beautifully done!"))+'</strong><span>'+escape(ui(message))+'</span></div>', unsafe_allow_html=True)
            elif kind == "reveal":
                st.info(message[0] + " — " + ui(message[1]))
            else:
                st.info(ui("A gentle hint: the word begins with {letter}. You can try again or reveal the answer.").format(letter=message))

        st.divider()
    if st.session_state.calm_activity == 4:
        st.markdown("### " + ui("🫙 Game 5: Gratitude Jar"))
        st.write(ui("Collect kind thoughts in your jar. No journal, account or personal details needed."))
        affirmations = ["🌸 A small moment of peace", "💜 Kindness toward myself", "🌿 A chance to rest", "☀️ A fresh beginning", "🦋 Support when I need it"]
        if "jar_notes" not in st.session_state:
            st.session_state.jar_notes = []
        chosen_note = st.selectbox(ui("Choose a thought to keep"), affirmations, format_func=display_option, key="jar_choice")
        j1, j2 = st.columns(2)
        with j1:
            if st.button(ui("💗 Add to my jar"), key="jar_add", use_container_width=True):
                if chosen_note not in st.session_state.jar_notes:
                    st.session_state.jar_notes.append(chosen_note)
                st.rerun()
        with j2:
            if st.button(ui("↺ Empty my jar"), key="jar_clear", use_container_width=True):
                st.session_state.jar_notes = []
                st.rerun()
        jar_contents = "<div class='jar-notes'>"+"<br>".join(escape(ui(n)) for n in st.session_state.jar_notes)+"</div>" if st.session_state.jar_notes else "<div class='jar-notes'>" + escape(ui("Your jar is ready for kind thoughts.")) + "</div>"
        st.markdown('<div class="mama-jar-stage"><div class="jar-icon">🫙</div>'+jar_contents+'</div>', unsafe_allow_html=True)

        st.divider()
    if st.session_state.calm_activity == 5:
        st.markdown("### " + ui("🎨 Game 6: Colour & Bloom"))
        st.write(ui("Design a bouquet by choosing flowers in your favourite colours."))
        bloom_choices = {"Pink blossom 🌸":"🌸", "Purple flower 🪻":"🪻", "Yellow sunflower 🌻":"🌻", "Red hibiscus 🌺":"🌺", "White daisy 🌼":"🌼"}
        if "bouquet" not in st.session_state:
            st.session_state.bouquet = []
        bloom_name = st.selectbox(ui("Pick a flower"), list(bloom_choices), format_func=display_option, key="bouquet_choice")
        b1, b2 = st.columns(2)
        with b1:
            if st.button(ui("🌷 Add to bouquet"), key="bouquet_add", use_container_width=True):
                st.session_state.bouquet = (st.session_state.bouquet + [bloom_choices[bloom_name]])[-18:]
                st.rerun()
        with b2:
            if st.button(ui("↺ New bouquet"), key="bouquet_reset", use_container_width=True):
                st.session_state.bouquet = []
                st.rerun()
        bouquet_content = '<div class="mama-flowers">'+" ".join(st.session_state.bouquet)+'</div>' if st.session_state.bouquet else '<div class="mama-empty">💐 ' + escape(ui('Your bouquet begins here.')) + '<br>' + escape(ui('Choose a flower to create something lovely.')) + '</div>'
        st.markdown('<div class="mama-garden-stage">'+bouquet_content+'</div>', unsafe_allow_html=True)
        st.caption(ui("All game choices are temporary for this app session and are not saved as personal records."))
    st.markdown("### " + ui("💗 A kind reminder"))
    st.write(ui("You deserve support, rest and care. Taking a small break is enough for now."))
    st.button(ui("Return to Emotional Wellness →"),key="calm_return",use_container_width=True,on_click=go,args=("🌷 Emotional wellness",))

else:
    st.markdown('<div class="section-head">📖 Learning hub</div>',unsafe_allow_html=True)
    st.markdown(f'<p class="lead">{escape(t("learn.intro"))}</p>',unsafe_allow_html=True)
    with st.expander(ui("Why postnatal visits matter"),expanded=True):
        st.write(ui("Postnatal care helps qualified professionals identify complications, support recovery and address emotional or feeding concerns. Follow the schedule your healthcare team recommends."))
    with st.expander(ui("What to bring to an appointment")):
        st.write(ui("Bring your discharge notes if available, a medication list, and questions about symptoms, feeding, recovery and your next follow-up."))
    with st.expander(ui("When to seek emergency help")):
        st.write("Heavy bleeding, chest pain, difficulty breathing, seizures, severe headache or vision changes, fainting, severe illness with fever, or thoughts of harming yourself or your baby need urgent professional attention.")
    with st.expander(ui("Pregnancy: planning questions")):
        st.write(ui("Discuss antenatal visits, recommended screening, medicines, nutrition, baby's movement, delivery plans and emergency transport with your maternity team."))
    with st.expander(ui("Postpartum: the weeks after birth")):
        st.write(ui("Discuss healing, feeding, sleep, blood pressure checks where indicated, emotional health and continued follow-up. Recovery may continue beyond six weeks."))
    with st.expander(ui("Emotional well-being and seeking help")):
        st.write("A trusted person and a qualified healthcare professional can help with persistent or worsening emotional distress. Severe confusion or thoughts of harm need emergency care.")
    with st.expander(ui("Using HerMamaAI safely")):
        st.write(ui("HerMamaAI is a prototype for general education and personal planning. It does not diagnose illness, monitor symptoms, send appointments to clinics or replace medical advice."))
    st.button(ui("🌼 Try the Calm Corner"),key="learning_calm",use_container_width=True,on_click=go,args=("🌼 Calm Corner",))
    st.caption(ui("Educational content requires clinical review before a real-world health pilot."))

st.markdown('<div class="footer"><b>HerMamaAI AdaptiveCare | Maternal &amp; Child Health Digital Innovation | Version 5.2</b><br>Developed by <b>WechimAI Integrated Engineering &amp; ICT Ltd</b> · Abuja, Nigeria.<br>Multilingual maternal and child health education, pregnancy and postnatal wellness support, and family-care planning. Existing health guidance has been reviewed by a qualified healthcare practitioner.<br><b>Safety &amp; Privacy:</b> For education and support only; not a substitute for professional medical advice, diagnosis, treatment or emergency services. Not clinically validated or approved as a medical device. BabyCare profiles, vaccination entries and planned visits are temporary session-based demonstration data, not securely retained medical records. Do not enter real personal or child health information. Additional privacy, safeguarding, accessibility and security assessments are needed before real-world deployment.</div>',unsafe_allow_html=True)
