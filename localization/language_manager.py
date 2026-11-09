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
CLINICAL_UI_TERMS = (
    "bleeding", "seizure", "fainting", "chest pain", "breathing",
    "headache", "vision changes", "fever", "infection", "emergency",
    "urgent", "warning signs", "medical", "clinical", "diagnos",
    "maternity", "healthcare", "health care", "hospital", "doctor",
    "midwife", "nurse", "symptom", "postpartum", "pregnancy",
    "prenatal", "postnatal", "breastfeed", "feeding", "contraception",
    "vaccin", "immuniz", "medication", "pain", "wound", "harm",
    "seek care", "seek help", "contact your", "care team",
    "discharge", "recovery", "follow-up", "newborn", "baby's health",
)


def t(key):
    """Phase 1: preserve English medical content pending qualified review."""
    if key.startswith(CLINICAL_PREFIXES):
        return label(key, "en")
    return label(key)


def localized_navigation(page):
    return label("nav." + page)


def ui(source):
    """Localize interface labels, retaining English for medical guidance."""
    if any(term in source.lower() for term in CLINICAL_UI_TERMS):
        return source
    return label("ui." + source) if "ui." + source in _load(st.session_state.get("hm_language", "en")) else source


def display_option(value):
    """Render localized select/radio options while retaining stable English IDs."""
    return ui(value)
