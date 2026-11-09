"""Test language-manager behavior with a small Streamlit stub (no server needed)."""
import importlib
import sys
import types
import unittest


class FakeState(dict):
    def __getattr__(self, key):
        return self[key]


class LanguageManagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.previous = sys.modules.get("streamlit")
        fake = types.ModuleType("streamlit")
        fake.cache_data = lambda fn: fn
        fake.session_state = FakeState(hm_language="en")
        fake.selectbox = lambda label, options, **kwargs: options[0]
        sys.modules["streamlit"] = fake
        sys.modules.pop("localization.language_manager", None)
        cls.lm = importlib.import_module("localization.language_manager")
        cls.fake = fake

    @classmethod
    def tearDownClass(cls):
        sys.modules.pop("localization.language_manager", None)
        if cls.previous is None:
            sys.modules.pop("streamlit", None)
        else:
            sys.modules["streamlit"] = cls.previous

    def test_four_language_catalogs(self):
        for language in ("en", "ha", "yo", "ig"):
            self.assertTrue(self.lm._load(language))

    def test_switch_changes_notice(self):
        key = "safety.emergency_translation_notice"
        self.assertEqual(len({self.lm.label(key, lang) for lang in ("en", "ha", "yo", "ig")}), 4)

    def test_unknown_language_falls_back_to_english(self):
        key = "safety.review_status"
        self.assertEqual(self.lm.label(key, "xx"), self.lm.label(key, "en"))

    def test_missing_key_fallback(self):
        self.assertEqual(self.lm.label("missing.test.key", "ha"), "missing.test.key")

    def test_option_display_does_not_mutate_value(self):
        source = "Demo parent profiles"
        self.fake.session_state["hm_language"] = "ha"
        self.assertEqual(self.lm.display_option(source), source)  # not on Phase 1 allowlist
        self.assertEqual(source, "Demo parent profiles")

    def test_phase_one_clinical_guidance_stays_english(self):
        self.fake.session_state["hm_language"] = "ha"
        for key in ("safety.mamacare_physical", "safety.mamacare_emotional", "mama.intro", "preg.intro"):
            with self.subTest(key=key):
                self.assertEqual(self.lm.t(key), self.lm.label(key, "en"))
        self.assertEqual(self.lm.ui("Heavy bleeding requires emergency care"), "Heavy bleeding requires emergency care")
        self.assertEqual(self.lm.ui("Demo baby profiles"), "Demo baby profiles")

    def test_dynamic_placeholder(self):
        key = "ui.A gentle hint: the word begins with {letter}. You can try again or reveal the answer."
        for language in ("en", "ha", "yo", "ig"):
            self.assertIn("X", self.lm.label(key, language).format(letter="X"))

    def test_safety_notices_present(self):
        for language in ("en", "ha", "yo", "ig"):
            self.assertTrue(self.lm.label("safety.emergency_translation_notice", language).strip())
            self.assertTrue(self.lm.label("safety.review_status", language).strip())


if __name__ == "__main__":
    unittest.main()
