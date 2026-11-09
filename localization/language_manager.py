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

def t(key):
    """Translate a content key, falling back to reviewed English source."""
    return label(key)

def localized_navigation(page):
    return label("nav." + page)


def ui(source):
    """Translate non-clinical UI text without changing stored internal values.

    The English source is always used if a translation is missing.
    """
    return label("ui." + source) if "ui." + source in _load(st.session_state.get("hm_language", "en")) else source


def display_option(value):
    """Render localized select/radio options while retaining stable English IDs."""
    return ui(value)
