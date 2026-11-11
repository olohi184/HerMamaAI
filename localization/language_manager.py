"""Draft UI localization; clinical instructions stay in source English pending review."""
import json
from pathlib import Path
import streamlit as st

LANGUAGES = {"en": "English", "ha": "Hausa", "yo": "Yorùbá", "ig": "Igbo"}
ROOT = Path(__file__).resolve().parent.parent / "locales"

@st.cache_data
def _load(code):
    if code not in LANGUAGES:
        code = "en"
    with (ROOT / f"{code}.json").open(encoding="utf-8") as handle:
        return json.load(handle)

def label(key, language=None):
    code = language or st.session_state.get("hm_language", "en")
    return _load(code).get(key) or _load("en").get(key) or key

def choose_language():
    return st.selectbox(
        "🌍 Language / Harshe / Èdè / Asụsụ",
        options=list(LANGUAGES),
        format_func=lambda code: LANGUAGES[code],
        key="hm_language",
        help=label("language.help")
    )

# Phase 1: Keep health instructions and safety-critical guidance in English
# until qualified linguistic and healthcare review is completed.
CLINICAL_PREFIXES = ("preg.", "post.", "baby.", "mama.", "well.", "learn.", "safety.")
# Only explicitly approved non-medical interface labels are translated in Phase 1.
# Everything else defaults to the English source, including new text added later.
SAFE_UI_LABELS = frozenset({
    "Explore your care", "Your postpartum care journey",
    "Choose what you need today. These are educational tools, not clinical monitoring.",
    "How are you feeling today?", "Physical recovery", "Emotional well-being",
    "Support around you", "Doing okay", "Having a difficult day",
    "I have support", "I could use more help", "Comfortable today",
    "Some concerns", "I need support", "🌼 Recovery guidance",
    "💗 Gentle check-in", "📅 Follow-up planning",
    "🌼 Visit Calm Corner →", "🌼 Calm Corner",
    "🌷 MamaCare Continuity", "🏡 Home", "📖 Learning hub",
    "🌷 Emotional wellness", "💞 MamaCare journey",
    "My follow-up checklist", "Choose a recovery stage",
    # Additional non-clinical interface copy used in MamaCare and AdaptiveCare.
    "Optional self-reflection only. Answers remain in the current Streamlit session and are not sent to a healthcare professional.",
    "Consider asking someone you trust for one specific practical task today.",
    "You deserve care, rest and support.",
    "Checklists are session-only. This module does not book appointments or send reminders.",
    "🌱 AdaptiveCare",
    "Check-in saved. Suggestions have been refreshed using the latest session record.",
    "You already saved a check-in for this goal today. You can clear the session and retest if needed.",
    "📅 Open CareCalendar →",
    "You selected {goal} as your wellness goal.",
    "You selected {capacity} energy.",
    "Transparent if/then rules based on your choices; no AI diagnosis or machine-learning prediction.",
    "Share of check-ins marked completed; NOT a measure of medical outcomes or clinical adherence.",
    "Add an appointment",
    "Visit type",
    "Appointment date",
    "Appointment time",
    "Optional short label",
    "Add to my calendar",
    "My planned appointments",
    "No appointments entered yet. Add a visit above to begin.",
    "⬇️ Add to phone calendar (.ics)",
    "Remove",
    "How to add a reminder to your phone",
    "What to prepare before a visit",
    "A small step today",
    "I have written down a question to ask at my next antenatal visit.",
    "Explore MamaCare Continuity →",
    "Gentle ways to reach out",
    "Emotional wellness toolkit",
    "Check in with yourself",
    "Simple connection ideas",
    "🌼 Open the Calm Corner",
    "🌼 Motherhood Calm Corner",
    "Choose a gentle activity",
    "🌸 Game 1: Grow your garden",
    "A little space to grow, at your own pace. 🌿",
    "🌷 Plant a flower",
    "↺ Start a new garden",
    "☁️ Game 2: Choose a gentle moment",
    "🦋 Game 3: Memory Garden",
    "🌸 A little garden of surprises 🌿",
    "🌿 Turn cards back",
    "Your Memory Garden is blooming!",
    "All three pairs found. Beautifully done — enjoy this little moment.",
    "↺ Play Memory Garden again",
    "🔤 Game 4: Mama Word Garden",
    "Scrambled letters: ",
    "Your answer",
    "Type the word here",
    "Check word",
    "Reveal word",
    "Next word →",
    "Beautifully done!",
    "🫙 Game 5: Gratitude Jar",
    "Choose a thought to keep",
    "💗 Add to my jar",
    "↺ Empty my jar",
    "Your jar is ready for kind thoughts.",
    "Educational antenatal milestones",
    "Make your calendar work for you",
    "Questions for your maternity team",
    "Pregnancy learning topics",
    "Nutrition, rest and everyday well-being",
    "Understanding antenatal checks",
    "Preparing for delivery",
    "Questions about baby's movement",
    "More postpartum recovery topics",
    "Healing and comfort",
    "Feeding support without judgment",
    "Sleep, fatigue and asking for practical help",
    "Mood and relationships after birth",
    "When to seek professional support",
    "🎨 Game 6: Colour & Bloom",
    "Design a bouquet by choosing flowers in your favourite colours.",
    "Pick a flower",
    "🌷 Add to bouquet",
    "↺ New bouquet",
    "💗 A kind reminder",
    "You deserve support, rest and care. Taking a small break is enough for now.",
    "Return to Emotional Wellness →",
    "Why postnatal visits matter",
    "What to bring to an appointment",
    "Pregnancy: planning questions",
    "Postpartum: the weeks after birth",
    "Emotional well-being and seeking help",
    "Using HerMamaAI safely",
    "🌼 Try the Calm Corner",
    "Added to this session's calendar. This does not book a clinic visit.",
    "📅 Plan an antenatal visit in CareCalendar →",
    "Tap **Plant a flower** to create a little garden. There is no timer and no wrong move.",
    "Arrange the letters into a gentle word. Take your time, or reveal the answer whenever you wish.",
    "A gentle hint: the word begins with {letter}. You can try again or reveal the answer.",
    "Collect kind thoughts in your jar. No journal, account or personal details needed.",
    "All game choices are temporary for this app session and are not saved as personal records.",
    "Visit type",
    "Antenatal visit",
    "Postnatal follow-up",
    "Other maternity appointment",
    "👪 Demo family profiles",
    "Add a demo parent and baby",
    "Fictional parent alias",
    "Fictional baby alias",
    "Demo baby's birth date",
    "Add demo profile",
    "Add a fictional family to start the demonstration.",
    "Demo parent",
    "Demo baby",
    "Demo parent profiles",
    "Demo baby profiles",
    "Clear all demo profiles and entries",
    "Select state or FCT",
    "Select city",
    "Quickly explore a Phase 2 state",
    "🏥 View maternity-service evidence ↗",
    "☎️ View published contact source ↗",
    "🗺️ Search on Google Maps / Directions ↗",
    "📖 View government source ↗",
    "Questions to ask a facility before a routine visit",
    "Plant flowers and watch your little garden bloom.",
    "Find a calm scene and enjoy a quiet pause.",
    "Match cheerful pictures at your own pace.",
    "Unscramble gentle, encouraging words.",
    "Collect small moments worth remembering.",
    "Create a colourful bouquet of flowers.",
    "📅 My CareCalendar",
    "🤰 Pregnancy care",
    "💗 Postpartum recovery",
    "Your bouquet begins here.",
    "Choose a flower to create something lovely.",
    "Indicative visit milestones and vaccines to discuss",
    "Tap a vaccine name to learn what it helps protect against.",
    "✅ Record a vaccine already received",
    "👶 BabyCare — Immunization Tracker",
    "Provide both fictional aliases.",
    "Counts reflect only fictional profiles in this session, not real users.",
    "Selected demo baby's birth date:",
    "🔎 What might my baby need at this age?",
    "Choose a routine visit age",
    "Add reminder",
    "📚 Understand the vaccines",
    "📅 Plan a future vaccination visit",
    "Routine visit milestone",
    "Planned clinic visit date (future dates allowed)",
    "Demo clinic (optional)",
    "Save planned visit",
    "Future visit saved to this demo baby's session.",
    "Select vaccine from the clinic card",
    "If Other, type the vaccine name",
    "Dose number as shown on card (optional)",
    "Date administered",
    "Clinic (optional — avoid personal details)",
    "Save to this session",
    "Saved temporarily in this session.",
    "📊 My saved vaccination entries",
    "Vaccination records for selected baby",
    "⬇️ Download parent-reported record (CSV)",
    "Clear all temporary immunization entries",
    "No immunization entries recorded in this session.",
    "Check official guidance",
    "Nigeria Ministry of Health childhood schedule ↗",
    "UNICEF Nigeria immunization schedule ↗",
    "Nigeria National Primary Health Care Development Agency ↗",
    "Find Care Across Nigeria",
    "Phase 2 expansion — explore teaching hospitals in seven additional states",
    "Showing {count} government-listed institution(s). Not an exhaustive list of Nigerian hospitals.",
    "Hospital-specific maternity services and contact details awaiting review",
})


def t(key):
    """Phase 1: preserve English medical content pending qualified review."""
    if key.startswith(CLINICAL_PREFIXES):
        return label(key, "en")
    return label(key)


def localized_navigation(page):
    return label("nav." + page)


def ui(source):
    """Localize interface labels, retaining English for medical guidance."""
    if source not in SAFE_UI_LABELS:
        return source
    catalog = _load(st.session_state.get("hm_language", "en"))
    if "ui." + source in catalog:
        return label("ui." + source)
    if "nav." + source in catalog:
        return label("nav." + source)
    return source


def display_option(value):
    """Render localized select/radio options while retaining stable English IDs."""
    return ui(value)
