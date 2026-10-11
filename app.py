import streamlit as st

st.set_page_config(page_title="HerMamaAI | Your motherhood companion", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

PAGES = ["🏡 Home", "🤰 Pregnancy care", "💞 MamaCare journey", "💗 Postpartum recovery", "🌷 Emotional wellness", "🏥 Find care", "📖 Learning hub"]
if "page" not in st.session_state:
    st.session_state.page = PAGES[0]

def go(page):
    st.session_state.page = page

def card(title, icon, body):
    st.markdown(f'<div class="feature"><span class="feature-icon">{icon}</span><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"] {background:linear-gradient(180deg,#fff9fc 0%,#fffdfd 52%,#faf7ff 100%);}
.block-container {max-width:1100px;padding-top:1.2rem;padding-bottom:2rem;}
h1,h2,h3 {color:#382441;}
.hero {background:linear-gradient(120deg,#59337d 0%,#a34f95 55%,#e28ba9 100%);border-radius:26px;padding:38px 42px;color:#fff;box-shadow:0 14px 38px rgba(91,44,106,.16);margin:0 0 18px;}
.hero .eyebrow {font-size:.74rem;letter-spacing:.15em;font-weight:800;text-transform:uppercase;color:#ffedf7;}
.hero h1 {font-family:'Playfair Display',serif;color:#fff;font-size:clamp(2.4rem,5vw,4rem);line-height:1.18;margin:12px 0;}
.hero p {font-size:1.05rem;line-height:1.65;color:#fff5fc;max-width:680px;margin:0;}
.feature {background:#fff;border:1px solid #eedeea;border-radius:22px;padding:22px;min-height:190px;box-shadow:0 7px 22px rgba(90,43,92,.055);margin:8px 0 12px;}
.feature-icon {font-size:2rem;}
.feature h3 {font-size:1.15rem;margin:12px 0 8px;}
.feature p {font-size:.94rem;line-height:1.65;color:#685d6c;margin:0;}
.section-head {font-family:'Playfair Display',serif;font-size:clamp(1.7rem,3vw,2.15rem);font-weight:700;color:#3f2a4b;margin:20px 0 10px;}
.lead {font-size:1.05rem;color:#615467;line-height:1.7;margin-bottom:14px;}
.soft {background:#f5edf8;border:1px solid #eadcf2;border-radius:17px;padding:20px 23px;margin:15px 0;color:#493654;line-height:1.65;}
.timeline {background:white;border:1px solid #eedeea;border-left:5px solid #b565a1;border-radius:16px;padding:18px 22px;margin:10px 0;}
.timeline b {color:#573464;}
.footer {border-top:1px solid #e8dbe8;margin-top:32px;padding:20px 0;color:#736b78;font-size:.83rem;line-height:1.7;}
[data-testid="stButton"] button {border-radius:13px;min-height:43px;font-weight:700;border-color:#ead9e8;}
[data-testid="stButton"] button[kind="primary"] {background:#763e88;border-color:#763e88;}
[data-testid="stSelectbox"] {max-width:580px;}
@media(max-width:650px){.block-container{padding:1rem .85rem 2rem}.hero{padding:28px 23px;border-radius:20px}.feature{min-height:0;padding:19px}.hero h1{font-size:2.5rem}}
</style>
""", unsafe_allow_html=True)

st.markdown('''<div class="hero"><div class="eyebrow">WECHIMAI · MATERNAL WELLNESS INNOVATION</div><h1>💜 HerMamaAI</h1><p>A caring companion for pregnancy, recovery and the journey beyond birth. Explore helpful education at your own pace.</p></div>''', unsafe_allow_html=True)
st.caption("VERSION 4 · EDUCATIONAL PROTOTYPE · DESIGNED IN ABUJA, NIGERIA")

st.warning("**Important safety notice:** HerMamaAI is an educational prototype, not a clinician, diagnosis tool, medical device or emergency service. Content has not been clinically reviewed. For serious symptoms, seek immediate in-person medical care.")

# A single dropdown is easier to use on narrow phones than a seven-item horizontal radio group.
st.selectbox("Explore HerMamaAI", PAGES, key="page")
page = st.session_state.page

if page == "🏡 Home":
    st.markdown('<div class="section-head">Welcome to your motherhood space</div>', unsafe_allow_html=True)
    st.markdown('<p class="lead">Support should not end at delivery. Find a topic that matters to you today, with a special focus on the weeks after leaving hospital.</p>', unsafe_allow_html=True)
    st.markdown('<div class="soft"><b>💞 Featured: MamaCare Continuity</b><br>Explore four stages of recovery after childbirth, prepare questions for your maternity team, and learn which warning signs need urgent attention.</div>', unsafe_allow_html=True)
    st.button("Explore the MamaCare journey →", type="primary", use_container_width=True, on_click=go, args=("💞 MamaCare journey",))
    c1,c2 = st.columns(2)
    with c1:
        card("Pregnancy care","🤰","Antenatal appointments, practical questions and signs that need prompt medical assessment.")
        st.button("Open pregnancy care →",use_container_width=True,on_click=go,args=("🤰 Pregnancy care",))
        card("Emotional wellness","🌷","Gentle support, conversations and knowing when to seek professional help.")
        st.button("Open emotional wellness →",use_container_width=True,on_click=go,args=("🌷 Emotional wellness",))
    with c2:
        card("Postpartum recovery","💗","Understand recovery after delivery and why follow-up matters beyond discharge.")
        st.button("Open postpartum recovery →",use_container_width=True,on_click=go,args=("💗 Postpartum recovery",))
        card("Find care","🏥","Prepare to contact your maternity team and know when routine care is not enough.")
        st.button("Open care guidance →",use_container_width=True,on_click=go,args=("🏥 Find care",))

elif page == "🤰 Pregnancy care":
    st.markdown('<div class="section-head">🤰 Pregnancy care</div>',unsafe_allow_html=True)
    st.markdown('<p class="lead">Regular antenatal visits help your maternity team monitor your health and your baby’s development. Ask which appointments, tests and vaccinations are appropriate for you.</p>',unsafe_allow_html=True)
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

st.markdown('<div class="footer"><b>HerMamaAI · Version 4</b> — Developed by WechimAI Integrated Engineering & ICT Ltd · Abuja, Nigeria.<br>Educational demonstration only. No accounts or identifiable health records are collected by this prototype. Checkboxes are temporary on-screen planning aids, not clinical screening. Independent clinical review, safeguarding, accessibility testing and privacy assessment are required before real-world pilot use.</div>',unsafe_allow_html=True)
