import streamlit as st

st.set_page_config(page_title="HerMamaAI | Maternal Wellness", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html,body,[class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"] {background:linear-gradient(180deg,#fff8fc 0%,#fff 48%,#fbf7ff 100%);}
.block-container {max-width:1120px;padding-top:1.5rem;padding-bottom:3rem;}
h1,h2,h3 {color:#382244;}
.hero {background:linear-gradient(115deg,#6e3a8a,#a64c91 60%,#d36f9d);border-radius:24px;padding:34px 38px;color:white;margin-bottom:22px;box-shadow:0 12px 30px rgba(91,41,112,.15);}
.hero h1 {font-family:'Playfair Display',serif;color:white;font-size:clamp(2rem,4vw,3.3rem);margin:0 0 10px;}
.hero p {color:#fff5fc;font-size:1.08rem;line-height:1.6;max-width:650px;margin:0;}
.eyebrow {font-size:.78rem;letter-spacing:.13em;text-transform:uppercase;font-weight:700;color:#ffe5f4;margin-bottom:12px;}
.card {background:white;border:1px solid #f0e1ed;border-radius:18px;padding:23px;margin:7px 0 16px;box-shadow:0 5px 18px rgba(78,43,85,.05);min-height:168px;}
.card h3 {font-size:1.2rem;margin:8px 0;}
.card p {color:#685e70;font-size:.96rem;line-height:1.55;margin:0;}
.section {font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#40284a;margin:18px 0 8px;}
.note {background:#fff4e8;border-left:4px solid #d68a3e;border-radius:10px;padding:16px 18px;color:#664c31;margin:18px 0;}
.soft {background:#f5effa;border-radius:14px;padding:18px 20px;margin:12px 0;color:#47354e;}
.footer {border-top:1px solid #eadde9;padding-top:20px;margin-top:30px;color:#776c7b;font-size:.85rem;}
[data-testid="stRadio"] label {font-weight:600;}
@media(max-width:640px){.block-container{padding:1rem 1rem 2rem}.hero{padding:26px 22px;border-radius:18px}.card{min-height:0}.hero h1{font-size:2.15rem}}
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="hero"><div class="eyebrow">WechimAI • Maternal wellness innovation</div><h1>💜 HerMamaAI</h1><p>Care, knowledge and reassurance for every stage of motherhood — from pregnancy through recovery and beyond.</p></div>""", unsafe_allow_html=True)

st.info("**Educational prototype (Version 3).** This app is not a medical device, diagnosis service, clinician, or emergency response service. Its content has not yet undergone formal clinical review. For urgent symptoms, seek immediate in-person medical care.")

sections = ["🏠 Home", "🤰 Pregnancy", "💗 Postpartum", "💞 MamaCare Continuity", "🌷 Emotional well-being", "🏥 Find care"]
section = st.radio("Explore HerMamaAI", sections, horizontal=True, label_visibility="collapsed")

if section == "🏠 Home":
    st.markdown('<div class="section">Your motherhood companion</div>', unsafe_allow_html=True)
    st.write("Explore trusted-care topics at your own pace. Choose a section above to learn more.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div style="font-size:2rem">🤰</div><h3>Pregnancy guidance</h3><p>Learn about antenatal visits, questions to ask your maternity team, and symptoms that require urgent attention.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div style="font-size:2rem">🌷</div><h3>Emotional well-being</h3><p>Recognize emotional changes and learn when to reach out for compassionate professional support.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div style="font-size:2rem">💗</div><h3>Postpartum recovery</h3><p>Explore physical and emotional recovery after birth, including the important weeks after leaving hospital.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div style="font-size:2rem">🏥</div><h3>Find appropriate care</h3><p>Prepare for appointments and learn when to seek urgent help from a qualified healthcare provider.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="soft"><b>Our vision:</b> Every mother deserves support after delivery — not only during pregnancy. HerMamaAI aims to encourage continuity of maternal care, especially in the weeks following childbirth.</div>', unsafe_allow_html=True)

elif section == "🤰 Pregnancy":
    st.markdown('<div class="section">Pregnancy guidance</div>', unsafe_allow_html=True)
    st.write("Regular antenatal care helps healthcare professionals monitor your health and your baby’s development. Ask your maternity provider which visits, tests and vaccinations are appropriate for you.")
    st.markdown("**Questions for your antenatal appointment**")
    for q in ["When should I attend my next antenatal visit?", "Which symptoms mean I should seek urgent care?", "Which medicines or supplements are appropriate for me?", "What is my birth and emergency transport plan?"]:
        st.checkbox(q, key="preg_"+q)
    st.warning("Seek urgent assessment for vaginal bleeding, severe abdominal pain, severe headache, vision changes, seizures, chest pain or difficulty breathing.")

elif section == "💗 Postpartum":
    st.markdown('<div class="section">Postpartum recovery matters</div>', unsafe_allow_html=True)
    st.write("Recovery continues well beyond discharge. Serious complications can develop in the days and weeks after birth, even when delivery seemed uncomplicated. Keep your recommended postnatal appointments and contact your maternity team about new or worsening symptoms.")
    with st.expander("The first days after birth", expanded=True):
        st.write("Ask your care team about bleeding, pain, feeding, wound care, blood pressure checks where indicated, sleep, and the timing of your follow-up appointment.")
    with st.expander("Weeks 2–6: don't lose contact"):
        st.write("Continue monitoring your recovery with your healthcare provider. New severe symptoms need urgent assessment. If you missed a follow-up, contact your maternity facility to arrange one.")
    with st.expander("Beyond six weeks"):
        st.write("Physical and emotional recovery can take longer than six weeks. Discuss persistent pain, mood changes, bladder symptoms, feeding concerns, or other ongoing difficulties with a qualified provider.")
    st.error("**Urgent postpartum warning signs:** Heavy bleeding; chest pain; trouble breathing; seizures; severe headache or vision changes; fainting; fever with feeling very unwell; or thoughts of harming yourself or your baby. Seek emergency medical care immediately. Do not wait for an app response.")

elif section == "💞 MamaCare Continuity":
    st.markdown('<div class="section">💞 MamaCare Continuity</div>', unsafe_allow_html=True)
    st.write("**Care should not stop when a mother leaves the hospital.** Explore the stages of postpartum recovery, prepare questions for your maternity team, and learn which warning signs require urgent medical attention.")
    st.info("This is an educational journey, not a medical assessment or a personalized follow-up service. No responses are stored or sent to a clinician. Follow the postnatal schedule given by your healthcare team.")

    stage = st.selectbox("Explore a recovery stage", [
        "Days 1–7 · Early recovery",
        "Weeks 2–3 · Stay connected",
        "Weeks 4–6 · Recovery and well-being",
        "After 6 weeks · Continuing care",
    ])
    if stage.startswith("Days"):
        st.markdown("### 🌸 Days 1–7: Early recovery")
        st.write("After delivery, ask your maternity team about normal recovery, bleeding, pain control, wound or perineal care, feeding support, and when your next postnatal contact should happen. Follow your discharge instructions.")
        questions = ["Do I know how to contact my maternity facility?", "Have I reviewed my discharge instructions?", "Do I know when my next postnatal appointment is?"]
    elif stage.startswith("Weeks 2"):
        st.markdown("### 💗 Weeks 2–3: Stay connected")
        st.write("New complications can arise after a mother returns home. Do not dismiss new or worsening symptoms. Keep scheduled postnatal contacts, and contact your maternity team if you missed one or are concerned about your recovery.")
        questions = ["Do I have a way to contact a qualified healthcare professional?", "Have I arranged any recommended follow-up?", "Do I know how to reach urgent care if needed?"]
    elif stage.startswith("Weeks 4"):
        st.markdown("### 🌷 Weeks 4–6: Recovery and well-being")
        st.write("Discuss ongoing physical recovery, feeding concerns, sleep, emotional well-being, contraception if relevant, and any symptoms that affect daily life. Ask your healthcare provider which follow-up appointments you need.")
        questions = ["Have I prepared questions for my postnatal appointment?", "Have I considered discussing emotional well-being with my provider?", "Do I know whom to contact about persistent symptoms?"]
    else:
        st.markdown("### 🌿 Beyond six weeks: Continuing care")
        st.write("Recovery is different for every mother and may continue beyond six weeks. Persistent pain, mood concerns, pelvic-floor symptoms, or other problems deserve professional attention rather than being ignored.")
        questions = ["Do I know where to seek help for ongoing concerns?", "Have I discussed persistent symptoms with a qualified provider?", "Do I know how to arrange continuing care?"]

    st.markdown("#### Questions to prepare for your care team")
    st.caption("These checkboxes are for on-screen planning only. They are not a clinical checklist or confirmation that you are medically well.")
    for i, question in enumerate(questions):
        st.checkbox(question, key=f"continuity_{stage}_{i}")

    with st.expander("What should I ask at my next postnatal contact?"):
        st.write("Ask about your recovery, any new or persistent symptoms, recommended checks, emotional well-being, feeding support, and the timing of your next follow-up. Share any concerns directly with your care team.")

    st.error("**Get urgent medical help now** for heavy bleeding, chest pain, difficulty breathing, seizures, severe headache or vision changes, fainting, fever with severe illness, or thoughts of harming yourself or your baby. Go to the nearest emergency facility or contact local emergency services. Do not wait for an app response.")
    st.markdown('<div class="soft"><b>Coming later, after clinical and privacy review:</b> optional reminders, verified care navigation, and consent-based follow-up with healthcare partners. These services are not active in this prototype.</div>', unsafe_allow_html=True)

elif section == "🌷 Emotional well-being":
    st.markdown('<div class="section">Your emotional well-being</div>', unsafe_allow_html=True)
    st.write("Pregnancy and new motherhood can bring many emotions. You deserve compassionate support, rest where possible, and space to talk about how you feel.")
    st.markdown('<div class="card"><h3>💬 You are allowed to ask for help</h3><p>Consider speaking with a trusted person and a qualified healthcare professional if sadness, anxiety, hopelessness, or overwhelm persists, worsens, or affects daily life.</p></div>', unsafe_allow_html=True)
    st.markdown("**Gentle check-in ideas**")
    st.write("• Tell someone how you're feeling today.\n\n• Ask for practical help with meals, chores or childcare.\n\n• Bring mood or sleep concerns to your postnatal appointment.")
    st.error("If you feel at risk of harming yourself or someone else, or experience severe confusion or unusual perceptions, seek emergency medical help now and ask a trusted person to stay with you.")

elif section == "🏥 Find care":
    st.markdown('<div class="section">Finding the right care</div>', unsafe_allow_html=True)
    st.write("HerMamaAI does not yet provide a verified clinic directory, appointment booking, or emergency dispatch. For care, contact your maternity facility, a qualified local healthcare professional, or your local emergency service.")
    st.markdown("**Before contacting a healthcare provider, you may want to note:**")
    st.write("• Whether you are pregnant or how long it has been since delivery.\n\n• Your symptoms and when they began.\n\n• Any medications, known conditions, or relevant discharge instructions.\n\n• The best way to reach the facility and arrange safe transport.")
    st.warning("If you have severe symptoms, do not use a routine appointment pathway. Seek emergency assessment immediately.")

st.markdown('<div class="footer">HerMamaAI Version 3 • Developed by <b>WechimAI Integrated Engineering & ICT Ltd</b> • Abuja, Nigeria • Educational demonstration only.<br>No accounts, symptom histories, or sensitive health records are collected by this prototype. Interactive checkboxes remain within this browser session. Clinical review, safeguarding, accessibility testing, and privacy assessment are required before a public health pilot.</div>', unsafe_allow_html=True)

