# HerMamaAI multilingual release review package (draft)

**Status:** Practitioner review reported for all four languages; technical release checks and reviewed-version reconciliation remain outstanding. Not release-ready. Development branch only. This document is an inventory and sign-off checklist, not evidence of clinical validation or completed testing.

## Practitioner review confirmation (reported by project owner, 11 November 2026)

The project owner confirms that a healthcare practitioner reviewed and approved the medical instructions in **English, Hausa, Yoruba and Igbo**, **directly on the live HerMamaAI website** (not using a separate review document). This is recorded as **owner-reported practitioner approval**, not independently verified clinical validation or a claim that the currently committed translation strings are identical to the reviewed versions.

**Release reconciliation still required:** use the live production version as the reported reviewed baseline; compare its medical guidance against the development branch's catalogs and hard-coded guidance. Record any differences for review. Only after confirming exact content correspondence should the English-only clinical fallback be lifted. This avoids publishing unreviewed edits made after approval.

## Scope and current implementation

- Languages: English (en), Hausa (ha), Yoruba (yo), Igbo (ig).
- Catalogs: `locales/{en,ha,yo,ig}.json`; currently 418 keys in the English catalog.
- Translation entry points: `localization/language_manager.py` (`t`, `ui`, `display_option`).
- Safety gate: `CLINICAL_PREFIXES` intentionally returns English. Non-allowlisted `ui()` text also stays in English.
- The current live production application is not this development branch. Do not merge until the acceptance criteria below are satisfied.

## Outstanding English medical and safety copy — qualified review required

The following source-code locations are *review candidates*, not an exhaustive clinical audit. Line numbers refer to the branch at the time this document was prepared and may shift.

| Module | Approximate lines | Subject |
| --- | --- | --- |
| `app.py` | 203, 269, 294 | App limitations, emergency symptoms, fetal movement |
| `app.py` | 305–337 | Postpartum recovery, feeding, emotional wellness, mental-health emergencies |
| `app.py` | 351, 711, 717 | Calm Corner medical disclaimer and urgent-care instructions |
| `babycare.py` | 60–61, 117–126, 191 | Immunization disclaimers, visit examples, eligibility and safety |
| `find_care.py` | 81, 116 | Emergency warning and directory limitations |
| `mamacare.py` | 24, 56 | Clinical disclaimer and urgent referral |
| `adaptivecare.py` | 23 | Medical disclaimer |

Also review all clinical catalog keys beginning with `preg.`, `post.`, `baby.`, `mama.`, `well.`, `learn.`, and `safety.`, as well as health-related `ui.` entries. Do not approve solely on key-prefix classification.

## Non-clinical content still to localize

- Calm Corner introductory captions, activity descriptions beyond the six cards, status strings and any embedded HTML text.
- Educational and directory page body text that is currently hard-coded.
- Text in dynamic expressions and helper functions that a literal-string checker may miss.
- Confirm all headings, button labels, accessibility text and placeholders on each page.

Use `python scripts/localization_coverage.py` to generate a preliminary inventory. It is static analysis and can miss dynamic or HTML-generated text.

## Release acceptance criteria

- [ ] All user-visible strings inventoried; each is translated, intentionally language-neutral, or explicitly documented as an English-only safety fallback.
- [ ] Hausa, Yoruba and Igbo language-quality review completed by qualified fluent reviewers; wording checked in context.
- [ ] Qualified maternal-health reviewer approves translated clinical guidance, warnings, disclaimers and referral instructions **for each language**.
- [ ] Medical content remains English-only until that language's review is documented; do not silently switch the safety gate off.
- [ ] Run `python -m unittest discover -s tests -p 'test_localization_integrity.py'` and `python scripts/localization_coverage.py`; investigate all failures.
- [ ] Browser testing: change language on Home, Pregnancy Care, Postpartum, BabyCare, MamaCare, AdaptiveCare, Find Care, Learning Hub and Calm Corner.
- [ ] Verify language switching preserves page navigation, calendar entries, demo records and form behavior.
- [ ] Test mobile Android and iPhone layouts, screen-reader labels where available, and text overflow in all languages.
- [ ] Confirm no persistent `MutationObserver` was reintroduced and production loading performance remains acceptable.
- [ ] Review privacy claims, external links and any audio/voice output in all languages; no claim of audio completion without testing.
- [ ] Obtain explicit release approval, then merge the development PR and monitor deployment; retain a rollback plan.

## Reviewer sign-off record

| Review | Reviewer | Language | Date | Findings / issues | Approved? |
| --- | --- | --- | --- | --- | --- |
| Linguistic | TBD | Hausa | TBD | Pending | No |
| Linguistic | TBD | Yoruba | TBD | Pending | No |
| Linguistic | TBD | Igbo | TBD | Pending | No |
| Maternal-health safety | TBD | Hausa | TBD | Pending | No |
| Maternal-health safety | TBD | Yoruba | TBD | Pending | No |
| Maternal-health safety | TBD | Igbo | TBD | Pending | No |
| Device and functional QA | TBD | All four | TBD | Pending | No |

**Do not describe HerMamaAI as fully multilingual, medically translated, or clinically validated until the relevant acceptance criteria are met.** The original application having undergone practitioner review does not establish approval of new translated content.
