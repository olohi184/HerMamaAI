"""Report translation wiring coverage without treating translated medical copy as approved.

Run: python scripts/localization_coverage.py
This is a static inventory, not a clinical or linguistic quality assessment.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ("app.py", "babycare.py", "find_care.py", "mamacare.py", "adaptivecare.py")
CATALOG = json.loads((ROOT / "locales" / "en.json").read_text(encoding="utf-8"))


def approved_labels():
    tree = ast.parse((ROOT / "localization" / "language_manager.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "SAFE_UI_LABELS"
            for target in node.targets
        ):
            return set(ast.literal_eval(node.value.args[0]))
    raise RuntimeError("SAFE_UI_LABELS not found")


def main():
    safe = approved_labels()
    total = 0
    approved = 0
    missing = []
    deferred = []
    for filename in FILES:
        tree = ast.parse((ROOT / filename).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            if node.func.id != "ui" or not node.args:
                continue
            arg = node.args[0]
            if not isinstance(arg, ast.Constant) or not isinstance(arg.value, str):
                continue
            total += 1
            value = arg.value
            location = f"{filename}:{node.lineno}"
            if "ui." + value not in CATALOG and "nav." + value not in CATALOG:
                missing.append((location, value))
            elif value in safe:
                approved += 1
            else:
                deferred.append((location, value))
    print(f"Literal ui() calls: {total}")
    print(f"Allowlisted for interface localization: {approved}")
    print(f"Deferred / English fallback: {len(deferred)}")
    print(f"Missing catalog entries: {len(missing)}")
    for title, items in (("Missing entries", missing), ("Deferred for review", deferred)):
        print(f"\\n{title}:")
        for location, value in items:
            print(f"  {location}: {value[:140]}")
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
