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
    return label("ui." + source) if "ui." + source in _load(st.session_state.get("hm_language", "en")) else source


def display_option(value):
    """Render localized select/radio options while retaining stable English IDs."""
    return ui(value)
