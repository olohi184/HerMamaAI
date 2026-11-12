# HerMamaAI Calm Corner: approved offline recordings

The six Calm Corner activity descriptions are **non-medical**. No recording is currently approved or bundled. The app deliberately shows an unavailable-audio notice in Hausa, Yoruba and Igbo until recordings have been reviewed and registered.

## Adding one reviewed recording

1. Have a fluent speaker review the exact translated activity description and record it naturally. Confirm consent and rights to distribute the recording; do not include identifying or private user data.
2. Save as `assets/calm_audio/<language>/activity_<number>.mp3` (or `.wav`). Language codes: `ha`, `yo`, `ig`; numbers: 1–6 in the existing Calm Corner order.
3. Compute its SHA-256 digest: `shasum -a 256 assets/calm_audio/ha/activity_1.mp3` (adjust path).
4. In `approved_manifest.json`, add under the language and activity number: `"1": {"format": "mp3", "sha256": "<64 lowercase hex digits>"}`.
5. Verify the spoken words, language, sound quality, duration, Stop/pause behaviour, mobile playback, and offline playback after the app has loaded. Browser and PWA offline access require separate caching validation.

Only manifest-approved files with matching hashes are playable. No cloud speech service, automatic translation, or cross-language voice fallback is used. English continues using its existing browser speech feature. Do not add medical instructions or generated audio without separate qualified review.
