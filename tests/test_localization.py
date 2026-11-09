"""Phase 1 non-clinical localization smoke tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "ha", "yo", "ig")
NAV_KEYS = (
    "nav.🏡 Home", "nav.👶 BabyCare", "nav.🤰 Pregnancy care",
    "nav.💞 MamaCare journey", "nav.💗 Postpartum recovery",
    "nav.📅 CareCalendar", "nav.🌷 Emotional wellness",
    "nav.🏥 Find care", "nav.📖 Learning hub", "nav.🌼 Calm Corner",
    "nav.🌱 AdaptiveCare",
)

class LocalizationTests(unittest.TestCase):
    def test_catalogues_parse(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                with (ROOT / "locales" / f"{language}.json").open(encoding="utf-8") as handle:
                    self.assertIsInstance(json.load(handle), dict)

    def test_navigation_coverage(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                catalogue = json.loads((ROOT / "locales" / f"{language}.json").read_text(encoding="utf-8"))
                for key in NAV_KEYS:
                    self.assertTrue(catalogue.get(key), f"{language}: missing {key}")

    def test_internal_navigation_identifiers_preserved(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("format_func=localized_navigation", app)
        self.assertIn("on_change=lambda: go(st.session_state.hm_mobile_nav)", app)
        self.assertIn("choose_language()", app)

    def test_content_localization_and_safety_notices(self):
        required = ("safety.emergency_translation_notice", "safety.review_status",
                    "ui.Demo parent profiles", "ui.Demo baby profiles")
        english = json.loads((ROOT / "locales" / "en.json").read_text(encoding="utf-8"))
        for language in LANGUAGES:
            with self.subTest(language=language):
                catalogue = json.loads((ROOT / "locales" / f"{language}.json").read_text(encoding="utf-8"))
                self.assertEqual(set(catalogue), set(english))
                for key in required:
                    self.assertTrue(catalogue.get(key), f"{language}: missing {key}")

if __name__ == "__main__":
    unittest.main()
