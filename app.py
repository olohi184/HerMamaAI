import streamlit as st
st.set_page_config(page_title='HerMamaAI | WechimAI',page_icon='💜',layout='centered')
st.markdown('''<style>.stApp{background:#fffafd;color:#33243c}.block-container{max-width:760px;padding-top:2rem}h1,h2,h3{color:#743c75}div.stButton>button{border-radius:14px}</style>''',unsafe_allow_html=True)
st.title('💜 HerMamaAI')
st.caption('By WechimAI Integrated Engineering & ICT Ltd · Educational prototype')
st.write('**Supporting mothers through pregnancy, postpartum recovery and beyond.**')
st.warning('Prototype only. Not a medical device, diagnosis service, or emergency response service. If you have serious symptoms, seek urgent medical care immediately.')
section=st.radio('Explore maternal support', ['Pregnancy','Postpartum recovery','Emotional well-being','Find care'],horizontal=False)
if section=='Pregnancy':
 st.header('Pregnancy education')
 st.write('Antenatal visits help healthcare professionals monitor your health and your baby’s development. Ask your maternity provider which visits and tests are recommended for you.')
 st.info('Seek urgent assessment for vaginal bleeding, severe abdominal pain, severe headache, visual changes, seizures, chest pain or difficulty breathing.')
elif section=='Postpartum recovery':
 st.header('Postpartum recovery')
 st.write('Recovery continues after birth. Attend recommended postnatal checkups, and tell your care team about physical or emotional changes.')
 st.error('Urgent warning signs include heavy bleeding, fever with feeling very unwell, severe headache or visual changes, chest pain, breathing difficulty, seizures, or one-sided leg swelling. Seek urgent medical care; do not wait for an app response.')
 st.write('Postpartum complications can occur after discharge, including weeks after delivery.')
elif section=='Emotional well-being':
 st.header('Your emotional well-being matters')
 st.write('Emotional changes after childbirth are common, but persistent sadness, hopelessness, anxiety, or difficulty coping deserve professional support. You deserve compassionate care.')
 st.warning('If you have thoughts of harming yourself or your baby, or experience confusion or unusual beliefs, seek immediate emergency help and tell a trusted person who can stay with you.')
 st.write('Consider speaking with a midwife, doctor, or qualified mental health professional.')
else:
 st.header('Find care')
 st.write('Contact your maternity hospital, antenatal clinic, community health centre, or a licensed health professional. We will add a verified Abuja care directory after partner review.')
 st.info('For emergencies, go to the nearest emergency department or call locally available emergency services. This prototype does not locate or contact providers.')
st.divider()
st.caption('No accounts, symptom records, or sensitive health data are collected by this prototype. Educational content requires clinical review before public release.')
