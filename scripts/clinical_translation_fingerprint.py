"""Create a deterministic inventory of current clinical translation text.

Run:
    python scripts/clinical_translation_fingerprint.py
    python scripts/clinical_translation_fingerprint.py --output docs/clinical_translation_fingerprints.json

Hashes identify the *current repository wording*, not practitioner approval.
Compare the exported entries against the reviewed material before enabling
translated medical instructions. Non-prefixed clinical text needs manual review.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "ha", "yo", "ig")
PREFIXES = ("preg.", "post.", "baby.", "mama.", "well.", "learn.", "safety.")


def fingerprint(entries):
    payload = json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()
    result = {
        "purpose": "Current text fingerprint for reviewed-version comparison; NOT approval",
        "clinical_prefixes": list(PREFIXES),
        "languages": {},
        "requires_manual_review_of_non_prefixed_health_content": True,
    }
    for lang in LANGUAGES:
        catalog = json.loads((ROOT / "locales" / (lang + ".json")).read_text(encoding="utf-8"))
        entries = {key: value for key, value in catalog.items() if key.startswith(PREFIXES)}
        result["languages"][lang] = {
            "key_count": len(entries),
            "sha256": fingerprint(entries),
        }
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
