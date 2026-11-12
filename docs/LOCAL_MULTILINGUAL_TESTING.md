# Test HerMamaAI without GitHub Actions

The GitHub Actions runner is currently blocked by an account billing restriction. This does **not** establish whether the application's Python code passes or fails. The steps below run independently on your own computer.

## macOS / Linux (Python 3.11 recommended)

1. Download the **development branch** ZIP from:
   https://github.com/olohi184/HerMamaAI/archive/refs/heads/feature/full-content-localization-foundation-20261109.zip
2. Unzip it, open Terminal and change directory into the extracted folder.
3. Run:

```bash
python3 --version
python3 scripts/run_local_tests.py --report 2>&1 | tee local-test-results.txt
```

The runner checks Python syntax, translation catalog consistency, and localization unit tests. The optional inventory lists possible untranslated text. The test process does **not** require GitHub Actions, a GitHub account, or an internet connection after the ZIP is downloaded.

If the command reports **3/3 checks passed**, that means these static/unit checks passed; it does **not** prove the interactive Streamlit app works or that maternal-health translations are clinically safe.

## Optional: manually test the interface

Create an isolated environment and install the application's dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

In the opened browser, switch between English, Hausa, Yoruba and Igbo and verify the main content, navigation, forms and conditional messages on every page. Do not enter real personal or health information. Clinical emergency guidance remains in English pending qualified review.

## Share results in GitHub without Actions

- Keep `local-test-results.txt` as a local test record. Review it before sharing: logs may contain computer paths or other information.
- Open PR #5: https://github.com/olohi184/HerMamaAI/pull/5
- Comment with the date, Python version, the three PASS/FAIL results, and any error text. You can attach a sanitized log or link to a manually uploaded report.
- Do not claim automated CI success or merge to production solely on the basis of these tests.

GitHub Actions can remain blocked while this independent testing and PR review continue.
