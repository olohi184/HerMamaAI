# HerMamaAI multilingual mobile verification

## Test environment
Use a preview deployment built from `feature/multilingual-adaptivecare`, **not** the production URL. Test on an Android Chrome browser and iPhone Safari, including the installed PWA if applicable.

## Manual acceptance checklist
- [ ] Page loads without Python exceptions at 320px, 375px, and 390px viewport widths.
- [ ] Language selector is visible, usable by touch, and has English/Hausa/Yorùbá/Igbo.
- [ ] Switching language updates the section navigation labels immediately.
- [ ] Selecting each localized section opens the correct underlying page.
- [ ] Switching language does not reset the current care page unexpectedly.
- [ ] The English-only medical-content warning is visible in all non-English modes.
- [ ] No clinical text is represented as translated.
- [ ] AdaptiveCare, MamaCare, BabyCare, CareCalendar and Find Care still load.
- [ ] No horizontal overflow, clipped dropdowns or unreadable text.
- [ ] VoiceOver (iPhone) and TalkBack (Android) announce language options.
- [ ] A reload defaults to English unless persistent preference storage is added.
- [ ] Slow 3G simulation does not prevent access to core text navigation.

## Evidence to record
Device model, OS/browser versions, viewport width, screenshots of each selected language, test date, failed steps and console/server errors.

## Release gate
Do not merge or deploy until CI is green, native speakers review navigation translations, and device checks pass. Audio and clinical translations are out of scope for Phase 1.
