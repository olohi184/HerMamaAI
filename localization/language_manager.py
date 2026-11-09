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
