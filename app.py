import streamlit as st
from datetime import date, datetime, time, timedelta
from html import escape

st.set_page_config(page_title="HerMamaAI | Your motherhood companion", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

PAGES = ["🏡 Home", "📅 CareCalendar", "🤰 Pregnancy care", "💞 MamaCare journey", "💗 Postpartum recovery", "🌷 Emotional wellness", "🏥 Find care", "📖 Learning hub"]
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
.hero-brand {display:flex;align-items:center;gap:22px;margin:18px 0 16px;}
.hero-logo {width:120px;height:120px;object-fit:contain;flex-shrink:0;filter:drop-shadow(0 5px 12px rgba(40,10,50,.16));}
.hero-brand h1 {margin:0 0 5px;overflow-wrap:anywhere;}
.hero-tagline {font-weight:700;font-size:clamp(.9rem,1.7vw,1.1rem);color:#fff1f9;letter-spacing:.01em;}
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
@media(max-width:650px){.block-container{padding:1rem .85rem 2rem}.hero{padding:28px 23px;border-radius:20px}.feature{min-height:0;padding:19px}.hero h1{font-size:2.3rem}.hero-brand{gap:12px}.hero-logo{width:82px;height:82px}}

/* HerMamaAI V5: centered identity and welcoming layered palette */
[data-testid="stAppViewContainer"] {background:radial-gradient(ellipse at 8% 8%,#f5e4f5 0%,transparent 43%),radial-gradient(ellipse at 92% 55%,#ffe5ee 0%,transparent 40%),linear-gradient(155deg,#fff5fa 0%,#f5efff 55%,#fff3f5 100%)!important;}
.block-container {max-width:1120px!important;}
.hero {text-align:center!important;background:linear-gradient(135deg,#50276e 0%,#88438b 48%,#d879a6 100%)!important;border:1px solid rgba(255,255,255,.28);padding:42px 30px 46px!important;box-shadow:0 22px 52px rgba(95,43,106,.22)!important;}
.hero .eyebrow {font-size:.76rem!important;letter-spacing:.19em!important;}
.hero-brand {display:flex!important;flex-direction:column!important;justify-content:center!important;align-items:center!important;gap:5px!important;margin:18px auto 18px!important;}
.hero-logo {width:min(260px,56vw)!important;height:auto!important;max-height:230px!important;object-fit:contain!important;filter:drop-shadow(0 10px 15px rgba(48,12,52,.22))!important;}
.hero-brand h1 {font-size:clamp(3rem,7vw,5.4rem)!important;line-height:1.08!important;margin:0!important;text-align:center!important;overflow-wrap:normal!important;}
.hero-tagline {font-size:clamp(1rem,2.1vw,1.3rem)!important;font-weight:800!important;letter-spacing:.025em!important;margin-top:8px!important;}
.hero p {margin:15px auto 0!important;max-width:710px!important;text-align:center!important;font-size:1.07rem!important;}
.feature {background:linear-gradient(145deg,rgba(255,255,255,.97),rgba(252,240,250,.96))!important;border:1px solid #e9cfe8!important;box-shadow:0 12px 28px rgba(94,45,104,.10)!important;transition:transform .2s ease,box-shadow .2s ease;}
.feature:hover {transform:translateY(-3px);box-shadow:0 18px 34px rgba(94,45,104,.14)!important;}
.soft {background:linear-gradient(115deg,#f8eafa,#fbe9f1)!important;border-color:#ebd4ed!important;box-shadow:0 8px 20px rgba(103,52,103,.06);}
.timeline {background:#fff9fe!important;box-shadow:0 6px 17px rgba(103,52,103,.06);}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {background:#fff8fd!important;border:1px solid #e6cbe5!important;border-radius:14px!important;}
[data-testid="stButton"] button {background:#fff8fd;border-color:#e9d0e8!important;}
[data-testid="stButton"] button[kind="primary"] {background:linear-gradient(90deg,#713d89,#b35b9d)!important;color:white!important;}
@media(max-width:650px){.hero{padding:28px 16px 34px!important}.hero-logo{width:min(205px,62vw)!important;max-height:190px!important}.hero-brand h1{font-size:clamp(2.5rem,11vw,3.6rem)!important}.hero p{font-size:.96rem!important}.hero .eyebrow{font-size:.64rem!important;letter-spacing:.1em!important}}


/* V5.1 refined approved-inspired layout */
.hero{padding:30px 26px 34px!important;border-radius:28px!important;background:linear-gradient(120deg,#572a76 0%,#82418b 46%,#d87da7 100%)!important;}
.hero-brand{margin:8px auto 12px!important;gap:3px!important;}
.hero-emblem{width:205px;height:144px;overflow:hidden;margin:0 auto 5px;display:flex;align-items:flex-start;justify-content:center;}
.hero-emblem .hero-logo{display:block;width:205px!important;height:auto!important;max-height:none!important;object-fit:initial!important;filter:drop-shadow(0 7px 13px rgba(45,12,57,.19))!important;}
.hero-brand h1{font-family:'Playfair Display',serif!important;font-size:clamp(3.2rem,7vw,5.1rem)!important;font-weight:700!important;line-height:1.06!important;margin:2px 0 5px!important;color:#fff!important;}
.hero-tagline{font-size:clamp(1.05rem,2.2vw,1.4rem)!important;font-weight:800!important;color:#fff!important;margin-top:7px!important;}
.hero p{font-size:1rem!important;max-width:630px!important;margin:14px auto!important;line-height:1.6!important;}
.hero-pills{display:flex;flex-wrap:wrap;justify-content:center;gap:9px;margin-top:18px;}
.hero-pills span{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.32);border-radius:30px;padding:7px 14px;color:white;font-weight:700;font-size:.78rem;}
[data-testid="stAppViewContainer"]{background:linear-gradient(145deg,#fff5fa 0%,#f7eafa 48%,#fff1f4 100%)!important;}
.feature{background:linear-gradient(145deg,#fffaff,#f9edf7)!important;border:1px solid #e9d1e8!important;}
@media(max-width:650px){.hero{padding:25px 14px 28px!important}.hero-emblem{width:165px;height:118px}.hero-emblem .hero-logo{width:165px!important}.hero-brand h1{font-size:clamp(2.6rem,12vw,3.5rem)!important}.hero-pills{gap:6px}.hero-pills span{font-size:.68rem;padding:6px 9px}}


/* V6 visual redesign inspired by approved reference, with working Streamlit controls */
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 8% 8%,#eac7f0 0%,transparent 37%),radial-gradient(circle at 93% 17%,#f6c4e2 0%,transparent 36%),linear-gradient(165deg,#fff6fc 0%,#f8efff 56%,#fff0f8 100%)!important;}
.block-container{max-width:1380px!important;padding-top:1rem!important;}
.hero-v6{position:relative;overflow:hidden;border-radius:28px 28px 50px 50px;background:radial-gradient(ellipse at 44% 36%,#fff5fd 0%,#f5d7f0 36%,transparent 70%),linear-gradient(120deg,#d69ad9 0%,#f8d3e7 46%,#cb83bc 100%);padding:22px 38px 48px;box-shadow:0 20px 48px rgba(106,44,115,.15);color:#431452;}
.hero-v6:before{content:"";position:absolute;bottom:-70px;left:-8%;width:120%;height:135px;background:rgba(137,48,148,.17);border-radius:50% 50% 0 0;transform:rotate(-2deg);}
.hero-v6:after{content:"";position:absolute;bottom:-100px;left:-5%;width:115%;height:140px;background:#fff6fc;border-radius:50% 50% 0 0;transform:rotate(2deg);}
.hero-top{display:flex;justify-content:space-between;align-items:center;gap:16px;background:rgba(255,255,255,.78);border:1px solid #fff;border-radius:40px;padding:12px 24px;box-shadow:0 6px 18px rgba(86,31,101,.08);}
.brand-small{font-family:'Playfair Display',serif;font-size:1.4rem;color:#44145d}.brand-small span,.hero-identity h1 span{color:#d22a91}.top-label{font-size:.69rem;font-weight:800;letter-spacing:.13em;color:#703e80;}
.hero-main{display:grid;grid-template-columns:1fr 1.7fr 2.5fr;align-items:center;gap:18px;position:relative;z-index:1;min-height:285px;}
.hero-left{font-family:'Playfair Display',serif;font-size:clamp(1.15rem,2.2vw,1.9rem);line-height:1.48;color:#542269;}
.hero-art{display:flex;justify-content:center;align-items:center;height:255px;overflow:hidden;}
.hero-art img{width:min(310px,100%);height:auto;object-fit:contain;filter:drop-shadow(0 12px 18px rgba(83,28,90,.13));}
.hero-identity{text-align:center}.hero-identity h1{font-family:'Playfair Display',serif;font-size:clamp(3.2rem,6.3vw,6.1rem);font-weight:700;letter-spacing:-.045em;color:#441057;line-height:1.1;margin:0;white-space:nowrap;}
.hero-rule{height:3px;width:80%;margin:10px auto;background:linear-gradient(90deg,transparent,#c72b90,transparent);}
.hero-identity h2{font-family:'Playfair Display',serif;font-style:italic;font-size:clamp(1rem,2vw,1.7rem);font-weight:600;color:#4b1a64;margin:10px 0;}
.hero-identity p{font-size:.92rem;color:#613e6b;margin:12px auto;max-width:470px;}
.hero-capabilities{display:flex;position:relative;z-index:2;justify-content:center;gap:12px;flex-wrap:wrap;margin:0 auto;}
.hero-capabilities span{background:rgba(255,255,255,.56);border:1px solid rgba(255,255,255,.75);padding:11px 16px;border-radius:30px;color:#5a2370;font-size:.74rem;font-weight:800;letter-spacing:.03em;}
.feature{min-height:185px!important;background:linear-gradient(140deg,#fff7fc,#f8e9f7)!important;border:1px solid #f0d4ea!important;box-shadow:0 10px 26px rgba(94,42,108,.09)!important;}
[data-testid="stButton"] button{border-radius:25px!important;}
[data-testid="stAlert"]{border-radius:18px!important;}
@media(max-width:850px){.hero-main{grid-template-columns:1fr 1.3fr;min-height:0;padding:18px 0}.hero-left{display:none}.hero-art{height:210px}.hero-art img{width:220px}.hero-identity h1{font-size:clamp(2.7rem,6vw,4.3rem)}.hero-v6{padding:16px 18px 42px}.top-label{display:none}}
@media(max-width:560px){.hero-main{display:flex;flex-direction:column;gap:0}.hero-art{height:175px}.hero-art img{width:190px}.hero-identity h1{font-size:clamp(2.6rem,11vw,3.5rem)}.hero-identity p{font-size:.86rem}.hero-capabilities{gap:6px}.hero-capabilities span{font-size:.61rem;padding:8px 10px}.brand-small{font-size:1.15rem}.hero-v6{border-radius:22px 22px 38px 38px}.hero-top{padding:9px 16px}}


/* V6.1 less repetition and a calmer visual hierarchy */
.clean-hero{padding:24px 46px 38px!important;border-radius:26px!important;background:linear-gradient(120deg,#f4d8ee,#f9e6f4 46%,#e8b6d9)!important;}
.clean-hero:before{height:75px!important;bottom:-48px!important;opacity:.45!important;}
.clean-hero:after{height:75px!important;bottom:-55px!important;}
.clean-hero .hero-top{justify-content:center!important;background:transparent!important;box-shadow:none!important;border:0!important;padding:0!important;}
.clean-hero .top-label{display:block!important;font-size:.73rem!important;letter-spacing:.16em!important;}
.clean-hero .hero-main{display:grid!important;grid-template-columns:minmax(190px, .9fr) minmax(0, 2fr)!important;gap:34px!important;min-height:245px!important;max-width:1050px;margin:0 auto!important;}
.clean-hero .hero-art{height:220px!important;overflow:hidden!important;align-items:flex-start!important;}
.clean-hero .hero-art img{width:260px!important;max-width:100%!important;transform:translateY(-1px);filter:drop-shadow(0 8px 16px rgba(86,40,92,.13))!important;}
.clean-hero .hero-identity h1{font-size:clamp(3.4rem,6.5vw,6rem)!important;letter-spacing:-.035em!important;color:#4b185d!important;}
.clean-hero .hero-identity h1 span{color:#ca2689!important;}
.clean-hero .hero-identity h2{font-size:clamp(1.05rem,1.9vw,1.6rem)!important;margin:10px 0!important;}
.clean-hero .hero-identity p{font-size:.99rem!important;margin:12px auto 0!important;}
@media(max-width:700px){.clean-hero{padding:20px 17px 32px!important}.clean-hero .hero-main{display:flex!important;flex-direction:column!important;gap:4px!important}.clean-hero .hero-art{height:155px!important}.clean-hero .hero-art img{width:185px!important}.clean-hero .hero-identity h1{font-size:clamp(2.8rem,10vw,4.2rem)!important}.clean-hero .top-label{font-size:.6rem!important;letter-spacing:.1em!important}}


/* V7: polished maternal wellness landing page */
[data-testid="stAppViewContainer"]{background:linear-gradient(160deg,#fff4fb 0%,#f8f0ff 48%,#fff8f9 100%)!important}
.block-container{max-width:1420px!important;padding-top:.65rem!important}
.hm-nav{display:flex;align-items:center;justify-content:space-between;gap:15px;flex-wrap:wrap;background:rgba(255,255,255,.92);border:1px solid #f3d8ef;border-radius:24px;padding:15px 24px;box-shadow:0 12px 28px #71357512;margin-bottom:12px}
.hm-wordmark{font-family:'Playfair Display',serif;color:#4c176c;font-size:1.65rem;font-weight:700}.hm-wordmark span{color:#d52a94}
.hm-nav-note{color:#6b3a80;font-size:.79rem;font-weight:700;letter-spacing:.04em}
.hm-hero{position:relative;overflow:hidden;min-height:345px;border-radius:32px;background:radial-gradient(circle at 68% 18%,#fff9fc 0%,transparent 48%),linear-gradient(125deg,#ecc5f2 0%,#f9d9ed 52%,#dca4db 100%);display:grid;grid-template-columns:1fr 1.5fr 1fr;gap:12px;align-items:center;padding:36px 35px 56px;box-shadow:0 20px 42px #71357521}
.hm-hero:after{content:"";position:absolute;bottom:-68px;left:-5%;width:110%;height:105px;background:#fff8fe;border-radius:50% 50% 0 0}
.hm-quote{font:italic 1.75rem/1.4 'Playfair Display',serif;color:#602879;z-index:1}
.hm-center{text-align:center;z-index:1}.hm-center h1{font:700 clamp(3.2rem,6vw,6rem)/1.08 'Playfair Display',serif;color:#57146c;margin:0}.hm-center h1 span{color:#d52b92}
.hm-center h2{font:italic 1.45rem/1.35 'Playfair Display',serif;color:#53216b;margin:12px 0}
.hm-center p{font-size:.96rem;color:#64446d}
.hm-emblem{display:block;width:150px;max-height:130px;object-fit:cover;object-position:top;margin:10px auto 0;filter:drop-shadow(0 8px 12px #692c7020)}
.hm-mother{font-size:clamp(5rem,12vw,10rem);text-align:center;filter:drop-shadow(0 15px 25px #783a7430);z-index:1;line-height:1.2}
.hm-ribbon{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;padding:17px;margin-top:-22px;position:relative;z-index:2;background:#ffffffbd;border-radius:25px;box-shadow:0 8px 24px #753b7520}
.hm-ribbon span{font-weight:800;font-size:.83rem;color:#682c7b}
.hm-card{border-radius:25px;padding:23px;min-height:175px;border:1px solid #f3d3eb;box-shadow:0 12px 25px #6e357512;margin:8px 0}
.hm-card h3{margin:10px 0;color:#521c6b;font-size:1.2rem}.hm-card p{color:#624e69;line-height:1.6}
.hm-pink{background:linear-gradient(140deg,#fff4fa,#ffe2f0)}.hm-lilac{background:linear-gradient(140deg,#f8f1ff,#e9ddff)}.hm-peach{background:linear-gradient(140deg,#fff9f0,#ffead0)}.hm-mint{background:linear-gradient(140deg,#effff9,#d9f8ed)}
.hm-icon{font-size:2.5rem}
@media(max-width:850px){.hm-hero{grid-template-columns:1fr 2fr;padding:26px 20px 45px}.hm-quote{display:none}.hm-mother{font-size:6rem}.hm-center h1{font-size:3.5rem}}
@media(max-width:570px){.hm-nav{justify-content:center}.hm-nav-note{display:none}.hm-hero{display:flex;flex-direction:column-reverse;gap:0;padding:20px 13px 40px;min-height:0}.hm-mother{font-size:5rem}.hm-center h1{font-size:3.1rem}.hm-center h2{font-size:1.15rem}.hm-emblem{width:105px;max-height:90px}.hm-ribbon{gap:10px}.hm-ribbon span{font-size:.7rem}}


/* V8 clean, editorial hero — replacesst.markdown('''<div class="hm-subbrand"><b>HerMama<span>AI</span></b><small>WECHIMAI · MATERNAL WELLNESS INNOVATION</small></div>
<div class="hm-hero">
<div class="hm-copy"><div class="hm-eyebrow">YOUR MATERNAL WELLNESS COMPANION</div><h1>HerMama<span>AI</span></h1><h2>Every Mother Deserves Continued Care.</h2><p>Thoughtful pregnancy guidance, postpartum recovery resources and ongoing support — all in one welcoming space.</p></div>
<div class="hm-art"><img src="https://raw.githubusercontent.com/olohi184/HerMamaAI/main/HerMamaAI%20Mother%20and%20Baby%20Emblem.png" alt="HerMamaAI mother and baby illustration"></div>
</div>''',unsafe_allow_html=True)
st.caption("EDUCATIONAL PROTOTYPE · CREATED BY WECHIMAI · ABUJA, NIGERIA")

# Prominent, functioning navigation — retains all original pages and their features.
nav_labels = ["🏡 Home","🤰 Pregnancy care","💞 MamaCare journey","💗 Postpartum recovery","📅 CareCalendar","🌷 Emotional wellness","🏥 Find care","📖 Learning hub"]
nav_cols = st.columns(4)
for i, destination in enumerate(nav_labels):
    with nav_cols[i % 4]:
        st.button(destination, key=f"nav_v8_{i}", use_container_width=True, on_click=go, args=(destination,))
page = st.session_state.page

st.warning("**Important safety notice:** HerMamaAI is an educational prototype, not a clinician, diagnosis tool, medical device or emergency service. Content has not been clinically reviewed. For serious symptoms, seek immediate in-person medical care.")

p-shadow(0 18px 22px #6a28782e)}
.hm-subbrand{display:flex;align-items:center;justify-content:space-between;gap:15px;margin-bottom:14px;padding:10px 16px}
.hm-subbrand b{font:700 1.3rem 'Playfair Display',serif;color:#51196d}.hm-subbrand b span{color:#d52b92}.hm-subbrand small{color:#885487;font-size:.75rem;letter-spacing:.1em;font-weight:800}
[data-testid="stButton"] button[kind="secondary"]{background:#fffafd!important;border:1px solid #ebcde6!important;color:#6b287c!important;min-height:45px}
[data-testid="stButton"] button:hover{border-color:#ca69ac!important;color:#a02d86!important}
@media(max-width:750px){.hm-hero{grid-template-columns:1fr!important;padding:28px 22px 40px!important;gap:0!important;text-align:center}.hm-copy h1{font-size:3.5rem!important}.hm-copy p{margin:auto}.hm-art{min-height:160px}.hm-art img{width:210px}.hm-subbrand small{display:none}}

</style>
""", unsafe_allow_html=True)

st.markdown('''<div class="hm-nav"><div class="hm-wordmark">HerMama<span>AI</span></div><div class="hm-nav-note">WECHIMAI · MATERNAL WELLNESS INNOVATION</div></div>
<div class="hm-hero">
<div class="hm-quote">Empowering<br>Mothers,<br>Healthier<br>Generations.</div>
<div class="hm-center"><h1>HerMama<span>AI</span></h1><h2>Every Mother Deserves Continued Care.</h2><p>Care and knowledge through pregnancy, recovery and beyond.</p><img class="hm-emblem" src="https://raw.githubusercontent.com/olohi184/HerMamaAI/main/HerMamaAI%20Mother%20and%20Baby%20Emblem.png" alt="HerMamaAI mother and baby emblem"></div>
<div class="hm-mother" aria-label="Expectant mother illustration">🤰🏽</div>
</div><div class="hm-ribbon"><span>🤰 Pregnancy support</span><span>💞 MamaCare continuity</span><span>📅 Care calendar</span><span>🌷 Emotional wellness</span></div>''',unsafe_allow_html=True)
st.caption("VERSION 7 · EDUCATIONAL PROTOTYPE · DESIGNED IN ABUJA, NIGERIA")

st.warning("**Important safety notice:** HerMamaAI is an educational prototype, not a clinician, diagnosis tool, medical device or emergency service. Content has not been clinically reviewed. For serious symptoms, seek immediate in-person medical care.")

# A single dropdown is easier to use on narrow phones than a seven-item horizontal radio group.
st.selectbox("Explore HerMamaAI", PAGES, key="page")
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
