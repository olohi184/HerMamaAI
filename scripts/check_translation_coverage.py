"""Audit translation completeness without pretending that untranslated medical text is safe.

Run: python scripts/check_translation_coverage.py
Exit nonzero if the four catalogs do not share required UI keys.
This is a structural check, not a clinical or linguistic review.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "locales"
LANGS = ("en", "ha", "yo", "ig")

def main():
    catalogs = {lang: json.loads((ROOT / f"{lang}.json").read_text(encoding="utf-8")) for lang in LANGS}
    english = catalogs["en"]
    missing = {lang: sorted(set(english) - set(catalogs[lang])) for lang in LANGS}
    empty = {lang: sorted(k for k, v in catalogs[lang].items() if not isinstance(v, str) or not v.strip()) for lang in LANGS}
    for lang in LANGS:
        print(f"{lang}: {len(catalogs[lang])} keys; missing={len(missing[lang])}; empty={len(empty[lang])}")
        for key in missing[lang][:30]:
            print(f"  missing: {key}")
        for key in empty[lang][:30]:
            print(f"  empty: {key}")
    if any(missing.values()) or any(empty.values()):
        raise SystemExit(1)
    print("Catalog keys aligned. Medical translation review and UI testing still required.")

if __name__ == "__main__":
    main()
