"""Static checks for multilingual release readiness.

Run: python -m unittest discover -s tests -p 'test_localization_integrity.py'
These checks do not validate translation quality or clinical safety.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "ha", "yo", "ig")
PLACEHOLDER = re.compile(r"\\{([A-Za-z_][A-Za-z_0-9]*)\\}")


def catalog(code):
    with (ROOT / "locales" / f"{code}.json").open(encoding="utf-8") as file:
        return json.load(file)


class LocalizationIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogs = {lang: catalog(lang) for lang in LANGUAGES}

    def test_language_catalogs_have_matching_keys(self):
        baseline = set(self.catalogs["en"])
        for lang in LANGUAGES[1:]:
            with self.subTest(language=lang):
                self.assertEqual(baseline, set(self.catalogs[lang]))

    def test_every_translation_is_nonempty(self):
        for lang, items in self.catalogs.items():
            for key, value in items.items():
                with self.subTest(language=lang, key=key):
                    self.assertIsInstance(value, str)
                    self.assertTrue(value.strip())

    def test_format_placeholders_are_preserved(self):
        english = self.catalogs["en"]
        for lang in LANGUAGES[1:]:
            for key, source in english.items():
                with self.subTest(language=lang, key=key):
                    self.assertEqual(
                        sorted(PLACEHOLDER.findall(source)),
                        sorted(PLACEHOLDER.findall(self.catalogs[lang][key])),
                    )

    def test_interface_translation_keys_exist(self):
        manager = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        # Every explicitly allowed UI translation must have an entry in each catalog.
        import ast
        tree = ast.parse(manager)
        whitelist = None
        for node in tree.body:
            if isinstance(node, ast.Assign):
                if any(isinstance(target, ast.Name) and target.id == "SAFE_UI_LABELS" for target in node.targets):
                    whitelist = ast.literal_eval(node.value.args[0])
                    break
        self.assertIsNotNone(whitelist)
        for source in whitelist:
            # Some navigation names use the dedicated nav.* catalog namespace.
            key = "ui." + source
            nav_key = "nav." + source
            for lang, items in self.catalogs.items():
                with self.subTest(language=lang, key=key):
                    self.assertTrue(key in items or nav_key in items)

    def test_navigation_fallback_is_available_for_shared_labels(self):
        manager = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        self.assertIn('if "nav." + source in catalog:', manager)
        self.assertIn('return label("nav." + source)', manager)

    def test_calendar_display_preserves_stored_appointment_types(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('format_func=display_option)', app)
        self.assertIn('escape(display_option(ap["kind"]))', app)
        self.assertIn('"kind":kind', app)

    def test_ui_labels_are_present_in_english_catalog(self):
        # Detect typos and missing source keys before expanding the whitelist.
        import ast
        manager = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        tree = ast.parse(manager)
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "SAFE_UI_LABELS"
                for target in node.targets
            ):
                whitelist = ast.literal_eval(node.value.args[0])
                break
        else:
            self.fail("SAFE_UI_LABELS not found")
        english = self.catalogs["en"]
        for source in whitelist:
            with self.subTest(source=source):
                self.assertTrue(
                    "ui." + source in english or "nav." + source in english,
                    f"Missing English translation key for {source!r}",
                )

    def test_performance_fix_is_retained(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("new MutationObserver(", app)

    def test_medical_content_still_requires_review(self):
        manager = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        self.assertIn("CLINICAL_PREFIXES", manager)
        self.assertIn('return label(key, "en")', manager)


if __name__ == "__main__":
    unittest.main()
