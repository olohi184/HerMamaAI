#!/usr/bin/env python3
"""Independent HerMamaAI localization test runner (no GitHub Actions required)."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ["app.py", "mamacare.py", "adaptivecare.py", "adaptive_engine.py",
           "babycare.py", "find_care.py", "localization/language_manager.py",
           "scripts/audit_localization.py", "scripts/report_untranslated_ui.py"]


def run(label, command):
    print(f"\n=== {label} ===", flush=True)
    result = subprocess.run(command, cwd=ROOT, check=False)
    print(f"{label}: {'PASS' if result.returncode == 0 else 'FAIL'}", flush=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true",
                        help="Print inventory of remaining untranslated interface literals")
    args = parser.parse_args()
    checks = [
        ("Python syntax", [sys.executable, "-m", "py_compile", *MODULES]),
        ("Catalog and translation-reference audit",
         [sys.executable, "scripts/audit_localization.py"]),
        ("Localization unit tests",
         [sys.executable, "-m", "unittest", "discover", "-s", "tests",
          "-p", "test_*.py", "-v"]),
    ]
    passed = [run(name, command) for name, command in checks]
    if args.report:
        run("Untranslated interface inventory",
            [sys.executable, "scripts/report_untranslated_ui.py"])
    print(f"\nSUMMARY: {sum(passed)}/{len(passed)} checks passed.", flush=True)
    print("This does not certify clinical accuracy, translation quality, or rendered UI.")
    return 0 if all(passed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
