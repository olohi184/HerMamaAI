"""Audit multilingual release requirements without claiming unverified readiness.

Run: python scripts/audit_multilingual_release.py
Exit 0 means catalog parity and source checks passed, NOT that release is approved.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("en", "ha", "yo", "ig")
MODULES = ("app.py", "adaptivecare.py", "mamacare.py", "babycare.py", "find_care.py")


def main():
    catalogs = {
        code: json.loads((ROOT / "locales" / (code + ".json")).read_text(encoding="utf-8"))
        for code in LANGS
    }
    english = catalogs["en"]
    failures = []
    for code, catalog in catalogs.items():
        missing = sorted(set(english) - set(catalog))
        extra = sorted(set(catalog) - set(english))
        empty = sorted(key for key, value in catalog.items()
                       if not isinstance(value, str) or not value.strip())
        if missing or extra or empty:
            failures.append(f"{code}: missing={missing}, extra={extra}, empty={empty}")
    manager = (ROOT / "localization/language_manager.py").read_text(encoding="utf-8")
    if "CLINICAL_PREFIXES" not in manager or 'return label(key, "en")' not in manager:
        failures.append("Clinical English fallback could not be verified")
    for filename in MODULES:
        source = (ROOT / filename).read_text(encoding="utf-8")
        try:
            ast.parse(source, filename=filename)
        except SyntaxError as exc:
            failures.append(f"Python syntax error in {filename}: {exc}")
        if "new MutationObserver(" in source:
            failures.append(f"Persistent MutationObserver pattern found in {filename}")
    print("Languages:", ", ".join(LANGS))
    # A successful static audit is not a release authorization. In particular,
    # production practitioner review cannot be inferred from catalog parity.
    print("Clinical review: owner-reported in-app approval of four languages")
    print("Reviewed production wording vs this branch: NOT YET RECONCILED")
    print("Catalog keys:", len(english))
    print("Catalog parity:", "PASS" if not any("missing=" in f for f in failures) else "FAIL")
    print("Python syntax and English clinical fallback:", "PASS" if not failures else "CHECK")
    print()
    print("MANUAL RELEASE BLOCKERS (not automatically verified):")
    print("- Full-page visual review and localization coverage")
    print("- Spoken-language/audio feature implementation and device testing")
    print("- Qualified linguistic review in Hausa, Yoruba and Igbo")
    print("- Qualified maternal-health review of translated clinical and safety text")
    print("- Android, iPhone and desktop acceptance testing")
    if failures:
        for item in failures:
            print("FAIL:", item)
        raise SystemExit(1)
    print("Static source checks passed; release approval is NOT implied.")


if __name__ == "__main__":
    main()
