import streamlit as st
from datetime import date, datetime, time, timedelta
from html import escape

st.set_page_config(page_title="HerMamaAI | Maternal Wellness", page_icon="💗", layout="wide", initial_sidebar_state="collapsed")
PAGES = ["🏡 Home", "📅 CareCalendar", "🤰 Pregnancy care", "💞 MamaCare journey", "💗 Postpartum recovery", "🌷 Emotional wellness", "🏥 Find care", "📖 Learning hub"]
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
</style>
""",unsafe_allow_html=True)

st.markdown("""<section class="hm-hero"><div class="hm-hero-grid">
<div class="hm-copy"><div class="hm-eyebrow">WECHIMAI · MATERNAL WELLNESS INNOVATION</div>
<h1>HerMama<span>AI</span></h1><h2>Every Mother Deserves Continued Care.</h2>
<p>A caring companion for pregnancy, recovery and the journey beyond birth.</p>
<div class="hm-kicker">Healthy Mothers. Brighter Generations.</div></div>
<div class="hm-art"><img src="https://raw.githubusercontent.com/olohi184/HerMamaAI/main/HerMamaAI%20Mother%20and%20Baby%20Emblem.png" alt="Illustration of a mother embracing her baby"></div>
</div></section>""",unsafe_allow_html=True)

st.caption("EDUCATIONAL PROTOTYPE · DEVELOPED BY WECHIMAI · ABUJA, NIGERIA")
st.warning("**Important safety notice:** HerMamaAI is an educational prototype, not a clinician, diagnosis tool, medical device or emergency service. Content has not been clinically reviewed. For serious symptoms, seek immediate in-person medical care.")

# Real, accessible navigation controls, rather than non-interactive text inside a banner image.
nav = ["🏡 Home","🤰 Pregnancy care","💞 MamaCare journey","💗 Postpartum recovery","📅 CareCalendar","🌷 Emotional wellness","🏥 Find care","📖 Learning hub"]
nav_cols = st.columns(4)
for i, destination in enumerate(nav):
    with nav_cols[i % 4]:
        st.button(destination,key=f"nav_new_{i}",use_container_width=True,on_click=go,args=(destination,))
page = st.session_state.page

if page == "🏡 Home":
    st.markdown('<div class="section-head" style="text-align:center">Welcome to HerMamaAI</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead" style="text-align:center">Practical information and compassionate support for every stage of motherhood.</p>',unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    features=[
        (c1,"hm-pink","🤰","Pregnancy Support","Explore antenatal care, preparation and important warning signs.","Explore Pregnancy","🤰 Pregnancy care"),
        (c2,"hm-lilac","💞","MamaCare Continuity","Explore postpartum recovery and ongoing support after birth.","Explore Postpartum","💞 MamaCare journey"),
        (c3,"hm-peach","📅","Care Calendar","Plan antenatal and postnatal visits with your personal calendar.","Open Calendar","📅 CareCalendar"),
        (c4,"hm-mint","🌷","Emotional Wellness","Learn about self-care, emotional changes and seeking help.","Explore Wellness","🌷 Emotional wellness")
    ]
    for col,tone,icon,title,body,action,target in features:
        with col:
            st.markdown(f'<div class="hm-card {tone}"><div class="hm-icon">{icon}</div><h3>{title}</h3><p>{body}</p></div>',unsafe_allow_html=True)
            st.button(action+" →",key="home_"+target,use_container_width=True,on_click=go,args=(target,))
    st.markdown('<div class="soft"><b>Care continues after childbirth.</b> Learn when to contact your maternity team and how to prepare for follow-up care.</div>',unsafe_allow_html=True)

elif page == "📅 CareCalendar":
    st.markdown('<div class="section-head">📅 My CareCalendar</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">A simple place to organize antenatal and postnatal visits, and explore topics to discuss with your maternity team.</p>',unsafe_allow_html=True)
    st.info("**Two different things:** Your appointments are dates you enter from your care plan. Suggested milestones below are educational topics only — not booked appointments or a personalized medical schedule.")
    st.caption("Privacy: entries are held in this app session only. They are not saved to a database or sent to a clinic. Avoid entering personal medical information or identifying clinic details on a shared device.")
    if "care_appointments" not in st.session_state:
        st.session_state.care_appointments = []
    with st.form("carecalendar_add",clear_on_submit=True):
        st.markdown("#### Add an appointment")
        kind = st.selectbox("Visit type",["Antenatal visit","Postnatal follow-up","Other maternity appointment"])
        a,b = st.columns(2)
        with a:
            ap_date = st.date_input("Appointment date",value=date.today(),min_value=date.today())
        with b:
            ap_time = st.time_input("Appointment time",value=time(10,0),step=1800)
        note = st.text_input("Optional short label",placeholder="e.g. Routine check-up",max_chars=70)
        submitted = st.form_submit_button("Add to my calendar",type="primary",use_container_width=True)
        if submitted:
            st.session_state.care_appointments.append({"kind":kind,"date":ap_date,"time":ap_time,"note":note.strip()})
            st.success("Added to this session's calendar. This does not book a clinic visit.")
    st.markdown("#### My planned appointments")
    items = sorted(enumerate(st.session_state.care_appointments),key=lambda x:(x[1]["date"],x[1]["time"]))
    if not items:
        st.caption("No appointments entered yet. Add a visit above to begin.")
    for original_index, ap in items:
        st.markdown(f'<div class="timeline"><b>📍 {escape(ap["date"].strftime("%a %d %b %Y"))} · {escape(ap["time"].strftime("%I:%M %p"))}</b><br>{escape(ap["kind"])}{(" · " + escape(ap["note"])) if ap["note"] else ""}</div>',unsafe_allow_html=True)
        c1,c2=st.columns([3,1])
        with c1:
            start=datetime.combine(ap["date"],ap["time"])
            end=start+timedelta(hours=1)
            def ics_safe(value):
                return str(value).replace("\\","\\\\").replace(";","\\;").replace(",","\\,").replace("\n","\\n")
            title=ics_safe("HerMamaAI: "+ap["kind"]+(" - "+ap["note"] if ap["note"] else ""))
            ics="\r\n".join(["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//WechimAI//HerMamaAI//EN","BEGIN:VEVENT","UID:hermamaai-"+str(original_index)+"-"+start.strftime("%Y%m%dT%H%M%S")+"@local","DTSTAMP:"+datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),"DTSTART:"+start.strftime("%Y%m%dT%H%M%S"),"DTEND:"+end.strftime("%Y%m%dT%H%M%S"),"SUMMARY:"+title,"DESCRIPTION:Personal planning reminder only. Confirm timing with your maternity team. Time is local to your calendar.","END:VEVENT","END:VCALENDAR",""])
            st.download_button("⬇️ Add to phone calendar (.ics)",data=ics,file_name="hermamaai-appointment.ics",mime="text/calendar",key=f"ics_{original_index}",use_container_width=True)
        with c2:
            if st.button("Remove",key=f"remove_{original_index}",use_container_width=True):
                st.session_state.care_appointments.pop(original_index)
                st.rerun()
    st.markdown("#### Educational antenatal milestones")
    st.caption("These are discussion prompts, not dates or a substitute for local antenatal guidance. Your maternity team determines your individual care schedule.")
    with st.expander("Early pregnancy · Establishing antenatal care",expanded=True):
        st.write("Discuss when to begin antenatal care, recommended screening, nutrition and supplements, medicines, and whom to call for urgent concerns.")
    with st.expander("Middle pregnancy · Ongoing monitoring"):
        st.write("Ask about the recommended timing of check-ups, scans and tests, your baby's development, and any symptoms that concern you.")
    with st.expander("Later pregnancy · Preparing for birth"):
        st.write("Discuss your birth preferences, delivery location, transport plan, emergency contacts and postpartum follow-up arrangements.")
    with st.expander("After delivery · Continuing postnatal care"):
        st.write("Ask your maternity team when to return after discharge, what recovery symptoms need assessment, and how to obtain feeding and emotional support.")
    st.error("**Urgent symptoms?** Heavy bleeding, seizures, chest pain, difficulty breathing, severe headache or visual changes, fainting, or thoughts of harming yourself or your baby need immediate professional help. Do not wait for a calendar reminder.")

elif page == "🤰 Pregnancy care":
    st.markdown('<div class="section-head">🤰 Pregnancy care</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">Regular antenatal visits help your maternity team monitor your health and your baby’s development. Ask which appointments, tests and vaccinations are appropriate for you.</p>',unsafe_allow_html=True)
    st.button("📅 Plan an antenatal visit in CareCalendar →",use_container_width=True,on_click=go,args=("📅 CareCalendar",))
    st.subheader("Questions for your maternity team")
    for i,q in enumerate(["When should I attend my next antenatal visit?","Which symptoms mean I should seek urgent help?","Which medicines or supplements are appropriate for me?","What is my birth and emergency transport plan?"]):
        st.checkbox(q,key=f"preg_{i}")
    st.error("Seek urgent medical assessment for vaginal bleeding, severe abdominal pain, severe headache or vision changes, seizures, chest pain or trouble breathing.")

elif page == "💞 MamaCare journey":
    st.markdown('<div class="section-head">💞 MamaCare Continuity</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead"><b>Care should not stop when a mother leaves the hospital.</b> Explore each recovery stage and prepare for conversations with your healthcare team.</p>',unsafe_allow_html=True)
    st.info("This is educational planning, not a medical assessment or a personalized follow-up service. Your answers are not sent to a clinician. Follow the schedule given by your maternity team.")
    stages = [
        ("🌸 Days 1–7", "Early recovery", "Review discharge instructions, feeding support, bleeding, pain, wound or perineal care, and the date of your next postnatal contact.", ["Do I know how to contact my maternity facility?","Have I reviewed my discharge instructions?","Do I know when my next postnatal appointment is?"]),
        ("💗 Weeks 2–3", "Stay connected", "New or worsening problems can occur after returning home. Keep recommended contacts and ask for assessment if you are worried about your recovery.", ["Do I know how to contact a qualified professional?","Have I arranged my recommended follow-up?","Do I know how to access urgent care?"]),
        ("🌷 Weeks 4–6", "Recovery and well-being", "Discuss continuing physical recovery, feeding, sleep, emotional health, contraception where relevant, and any symptoms affecting everyday life.", ["Have I prepared questions for my appointment?","Could I discuss emotional well-being with my provider?","Do I know whom to contact about persistent symptoms?"]),
        ("🌿 After 6 weeks", "Continuing care", "Recovery may take longer than six weeks. Persistent pain, mood concerns, pelvic-floor symptoms or other problems deserve professional attention.", ["Do I know where to seek ongoing care?","Have I discussed persistent symptoms with a provider?","Do I know how to arrange continuing care?"])
    ]
    st.button("📅 Plan a postnatal follow-up →",use_container_width=True,on_click=go,args=("📅 CareCalendar",))
    st.markdown("#### Your recovery journey")
    for label,title,_,_ in stages:
        st.markdown(f'<div class="timeline"><b>{label}</b> · {title}</div>',unsafe_allow_html=True)
    selected = st.selectbox("Choose a stage to explore",[s[0] for s in stages])
    stage = next(s for s in stages if s[0]==selected)
    st.subheader(f"{stage[0]} · {stage[1]}")
    st.write(stage[2])
    st.markdown("#### Prepare for your next care contact")
    st.caption("Optional on-screen reminders only. Checking a box does not mean you are medically well.")
    for i,q in enumerate(stage[3]):
        st.checkbox(q,key=f"v4_stage_{selected}_{i}")
    with st.expander("Questions I can ask at my next appointment"):
        st.write("Ask about your recovery, new or ongoing symptoms, recommended checks, feeding support, emotional well-being, and when to return for follow-up. Discuss concerns directly with your care team.")
    st.error("**Get urgent medical help:** Heavy bleeding, chest pain, difficulty breathing, seizures, severe headache or vision changes, fainting, fever with severe illness, or thoughts of harming yourself or your baby require immediate professional assessment. Do not wait for an app response.")

elif page == "💗 Postpartum recovery":
    st.markdown('<div class="section-head">💗 Postpartum recovery</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">Recovery continues beyond discharge, and serious complications can arise even after an uncomplicated birth. Keep your recommended postnatal appointments.</p>',unsafe_allow_html=True)
    with st.expander("The first days after birth",expanded=True):
        st.write("Ask your team about bleeding, pain, feeding, wound care, blood pressure checks where indicated, sleep, and when to return for follow-up.")
    with st.expander("Weeks 2–6: stay connected"):
        st.write("Do not dismiss new or worsening symptoms. Contact your maternity facility if you miss an appointment or are concerned about recovery.")
    with st.expander("Beyond six weeks"):
        st.write("Persistent pain, mood changes, bladder or pelvic-floor symptoms, feeding concerns or other ongoing difficulties deserve professional assessment.")
    st.button("Explore MamaCare Continuity →",type="primary",use_container_width=True,on_click=go,args=("💞 MamaCare journey",))
    st.error("**Urgent warning signs:** Heavy bleeding, chest pain, trouble breathing, seizures, severe headache or vision changes, fainting, fever with severe illness, or thoughts of harming yourself or your baby. Seek emergency medical care immediately.")

elif page == "🌷 Emotional wellness":
    st.markdown('<div class="section-head">🌷 Emotional wellness</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">Pregnancy and new motherhood can bring many emotions. You deserve support and space to talk about how you feel.</p>',unsafe_allow_html=True)
    card("You can ask for help","💬","If sadness, anxiety, hopelessness or overwhelm persists, worsens, or affects daily life, speak with a qualified healthcare professional.")
    st.subheader("Gentle ways to reach out")
    st.write("• Tell someone you trust how you are feeling.\n\n• Ask for practical help with meals, chores or childcare.\n\n• Discuss mood and sleep concerns at a postnatal appointment.")
    st.error("If you may harm yourself or someone else, or experience severe confusion or unusual perceptions, seek emergency medical help immediately and ask a trusted person to stay with you.")

elif page == "🏥 Find care":
    st.markdown('<div class="section-head">🏥 Find appropriate care</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">Contact your maternity facility, a qualified healthcare professional or local emergency services. HerMamaAI does not yet offer a verified clinic directory, appointment booking or emergency dispatch.</p>',unsafe_allow_html=True)
    st.subheader("Before contacting a healthcare provider")
    for i,q in enumerate(["How long has it been since delivery, or how far along is the pregnancy?","What concerns or symptoms should I describe, and when did they start?","Do I have relevant discharge instructions or medication information?","How can I reach the facility safely?"]):
        st.checkbox(q,key=f"care_{i}")
    st.warning("For severe symptoms, do not wait for a routine appointment. Seek emergency assessment immediately.")

else:
    st.markdown('<div class="section-head">📖 Learning hub</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">A simple collection of topics to discuss with qualified maternity professionals.</p>',unsafe_allow_html=True)
    with st.expander("Why postnatal visits matter",expanded=True):
        st.write("Postnatal care helps qualified professionals identify complications, support recovery and address emotional or feeding concerns. Follow the schedule your healthcare team recommends.")
    with st.expander("What to bring to an appointment"):
        st.write("Bring your discharge notes if available, a medication list, and questions about symptoms, feeding, recovery and your next follow-up.")
    with st.expander("When to seek emergency help"):
        st.write("Heavy bleeding, chest pain, difficulty breathing, seizures, severe headache or vision changes, fainting, severe illness with fever, or thoughts of harming yourself or your baby need urgent professional attention.")
    st.caption("Educational content requires clinical review before a real-world health pilot.")

st.markdown('<div class="footer"><b>HerMamaAI · Version 5.1</b> — Developed by WechimAI Integrated Engineering & ICT Ltd · Abuja, Nigeria.<br>Educational demonstration only. No accounts or health records are collected by this prototype. Appointment entries and checkboxes are temporary session-only planning aids, not booking or clinical screening. Independent clinical review, safeguarding, accessibility testing and privacy assessment are required before real-world pilot use.</div>',unsafe_allow_html=True)
