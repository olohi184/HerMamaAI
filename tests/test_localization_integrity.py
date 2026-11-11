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

    def test_every_ui_call_has_a_catalog_entry(self):
        # This does not imply clinical approval: untranslated health copy may
        # deliberately remain in English until separately reviewed.
        import ast
        sources = ("app.py", "babycare.py", "find_care.py", "mamacare.py", "adaptivecare.py")
        english = self.catalogs["en"]
        for filename in sources:
            tree = ast.parse((ROOT / filename).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                    continue
                if node.func.id != "ui" or not node.args:
                    continue
                arg = node.args[0]
                if not isinstance(arg, ast.Constant) or not isinstance(arg.value, str):
                    continue
                with self.subTest(file=filename, line=node.lineno):
                    self.assertTrue(
                        "ui." + arg.value in english or "nav." + arg.value in english,
                        f"Missing locale entry for ui() text in {filename}:{node.lineno}: {arg.value!r}",
                    )

    def test_calm_corner_descriptions_are_localized_in_every_catalog(self):
        descriptions = (
            "Plant flowers and watch your little garden bloom.",
            "Find a calm scene and enjoy a quiet pause.",
            "Match cheerful pictures at your own pace.",
            "Unscramble gentle, encouraging words.",
            "Collect small moments worth remembering.",
            "Create a colourful bouquet of flowers.",
        )
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        manager = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        self.assertIn("escape(ui(description))", app)
        for description in descriptions:
            self.assertIn(description, app)
            self.assertIn(repr(description).replace("'", '"'), manager)
            for lang, items in self.catalogs.items():
                with self.subTest(language=lang, description=description):
                    self.assertTrue(items["ui." + description].strip())

    def test_unreviewed_clinical_prefixes_stay_english(self):
        manager = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        import ast
        tree = ast.parse(manager)
        funcs = {
            node.name: node for node in tree.body
            if isinstance(node, ast.FunctionDef)
        }
        self.assertIn("t", funcs)
        t_func = funcs["t"]
        self.assertTrue(any(
            isinstance(node, ast.Return)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "label"
            and len(node.value.args) >= 2
            and isinstance(node.value.args[1], ast.Constant)
            and node.value.args[1].value == "en"
            for node in ast.walk(t_func)
        ), "Clinical fallback to English was removed without documented review")

    def test_audio_is_opt_in_and_nonclinical(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        # A speech synthesis implementation is present, but availability
        # depends on the browser and installed voices.
        self.assertIn("SpeechSynthesisUtterance", app)
        self.assertIn("getVoices()", app)
        self.assertIn("No matching language voice is available", app)
        self.assertIn("addEventListener('click'", app)
        self.assertIn("Only Calm Corner activity descriptions are eligible", app)
        self.assertNotIn("synth.speak(utterance);\\n    });\\n    synth.speak", app)

    def test_clinical_review_is_not_equated_with_release_approval(self):
        report = (ROOT / "docs" / "multilingual_release_review.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("directly on the live HerMamaAI website", report)
        self.assertIn("Release reconciliation still required", report)

    def test_performance_fix_is_retained(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("new MutationObserver(", app)

    def test_medical_content_still_requires_review(self):
        manager = (ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8")
        self.assertIn("CLINICAL_PREFIXES", manager)
        self.assertIn('return label(key, "en")', manager)


if __name__ == "__main__":
    unittest.main()
