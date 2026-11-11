"""Export multilingual strings for qualified linguistic and healthcare review.

Usage:
    python scripts/export_translation_review.py
    python scripts/export_translation_review.py --output translation_review.csv

The CSV is a review worksheet, NOT an approval record. It includes the English
source and all translations. Clinical review is needed for health and safety
messages regardless of the catalog key prefix.
"""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "ha", "yo", "ig")
CLINICAL_PREFIXES = ("preg.", "post.", "baby.", "mama.", "well.", "learn.", "safety.")
HEALTH_TERMS = (
    "urgent", "emergency", "bleeding", "seizure", "vaccine",
    "immuniz", "symptom", "clinic", "medical", "doctor",
    "maternity", "hospital", "pregnan", "postpartum",
    "birth", "health", "feeding", "breast", "pain",
    "medicine", "screening", "diagnos", "referral",
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", default="translation_review.csv",
        help="Output CSV path; default is translation_review.csv",
    )
    args = parser.parse_args()
    catalogs = {
        lang: json.loads((ROOT / "locales" / f"{lang}.json").read_text(encoding="utf-8"))
        for lang in LANGUAGES
    }
    keys = set(catalogs["en"])
    for lang in LANGUAGES[1:]:
        if set(catalogs[lang]) != keys:
            raise SystemExit(f"Catalog key mismatch: {lang}")
    columns = [
        "key", "review_priority", "english_source",
        "hausa", "yoruba", "igbo",
        "hausa_linguistic_approved", "yoruba_linguistic_approved",
        "igbo_linguistic_approved", "clinical_approved_for_all_languages",
        "reviewer", "review_date", "notes",
    ]
    output = Path(args.output)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for key in sorted(keys):
            source = catalogs["en"][key]
            searchable = (key + " " + source).lower()
            priority = (
                "HEALTH_SAFETY_REVIEW"
                if key.startswith(CLINICAL_PREFIXES)
                or any(term in searchable for term in HEALTH_TERMS)
                else "LANGUAGE_REVIEW"
            )
            writer.writerow({
                "key": key,
                "review_priority": priority,
                "english_source": source,
                "hausa": catalogs["ha"][key],
                "yoruba": catalogs["yo"][key],
                "igbo": catalogs["ig"][key],
                "hausa_linguistic_approved": "",
                "yoruba_linguistic_approved": "",
                "igbo_linguistic_approved": "",
                "clinical_approved_for_all_languages": "",
                "reviewer": "",
                "review_date": "",
                "notes": "",
            })
    print(f"Exported {len(keys)} entries to {output}")
    print("All approval fields are blank until a reviewer signs off.")


if __name__ == "__main__":
    main()
