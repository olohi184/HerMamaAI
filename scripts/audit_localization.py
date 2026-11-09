"""Static quality gate for HerMamaAI four-language development.

Run from repository root: python scripts/audit_localization.py
Checks Python syntax, locale parity, interpolation placeholders and literal UI references.
Does not verify clinical accuracy, translation quality, or rendered Streamlit behavior.
"""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "ha", "yo", "ig")
PYTHON_FILES = ("app.py", "mamacare.py", "adaptivecare.py", "adaptive_engine.py",
                "babycare.py", "find_care.py", "localization/language_manager.py")
PLACEHOLDER = re.compile(r"(?<!{){([a-zA-Z_][a-zA-Z_0-9]*)}(?!})")


def main():
    failures = []
    catalogs = {}
    for language in LANGUAGES:
        path = ROOT / "locales" / (language + ".json")
        try:
            catalog = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            failures.append(f"{path}: {exc}")
            continue
        if not isinstance(catalog, dict):
            failures.append(f"{path}: expected a JSON object")
            continue
        catalogs[language] = catalog
    if len(catalogs) != len(LANGUAGES):
        raise SystemExit("\n".join(failures))
    keys = set(catalogs["en"])
    for language, catalog in catalogs.items():
        missing, extra = keys - set(catalog), set(catalog) - keys
        if missing:
            failures.append(f"{language}: missing {len(missing)} keys: {sorted(missing)[:12]}")
        if extra:
            failures.append(f"{language}: unexpected {len(extra)} keys: {sorted(extra)[:12]}")
        for key, value in catalog.items():
            if not isinstance(value, str) or not value.strip():
                failures.append(f"{language}:{key}: empty or non-string translation")
            elif key in catalogs["en"]:
                source = catalogs["en"][key]
                if isinstance(source, str) and set(PLACEHOLDER.findall(source)) != set(PLACEHOLDER.findall(value)):
                    failures.append(f"{language}:{key}: interpolation placeholders differ")
    referenced = set()
    for name in PYTHON_FILES:
        path = ROOT / name
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=name)
        except (OSError, SyntaxError) as exc:
            failures.append(f"{name}: {exc}")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not node.args:
                continue
            function = node.func
            if isinstance(function, ast.Name) and function.id in ("ui", "t"):
                arg = node.args[0]
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    key = ("ui." if function.id == "ui" else "") + arg.value
                    referenced.add(key)
    missing_references = referenced - keys
    for key in sorted(missing_references):
        failures.append(f"Referenced translation missing: {key}")
    print(f"Checked {len(PYTHON_FILES)} Python files and {len(keys)} translation keys across {len(LANGUAGES)} languages.")
    print(f"Literal translation references: {len(referenced)}")
    if failures:
        print("\n".join(failures[:100]))
        raise SystemExit(f"Localization audit failed with {len(failures)} issue(s)")
    print("Static localization checks passed. Clinical, linguistic and interactive testing still required.")


if __name__ == "__main__":
    main()
