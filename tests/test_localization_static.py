"""Dependency-free static checks for the multilingual mobile selector."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MobileNavigationStaticTests(unittest.TestCase):
    def test_four_languages_available(self):
        source = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        for code in ("en", "ha", "yo", "ig"):
            self.assertIn(f'"{code}"', source)

    def test_navigation_selection_keeps_internal_ids(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("format_func=localized_navigation", source)
        self.assertIn("on_change=lambda: go(st.session_state.hm_mobile_nav)", source)

    def test_localized_labels_have_nonempty_values(self):
        for language in ("en", "ha", "yo", "ig"):
            with self.subTest(language=language):
                data = json.loads((ROOT / "locales" / f"{language}.json").read_text(encoding="utf-8"))
                self.assertTrue(all(isinstance(v, str) and v.strip() for v in data.values()))

if __name__ == "__main__":
    unittest.main()
