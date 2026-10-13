# HerMamaAI branded Android PWA shell (pilot)

This static frontend displays the existing HerMamaAI Streamlit educational prototype inside an iframe using Streamlit's documented `?embed=true` mode. The original Streamlit deployment remains unchanged.

## Deployment
1. In the HerMamaAI GitHub repository, configure GitHub Pages to publish a static site from the appropriate folder, or deploy this `mobile-app/` directory through another static HTTPS host.
2. Confirm that the Streamlit iframe loads, navigation works, and the toolbar is absent on Android.
3. Check the install prompt and Android launcher icon. The existing mother-and-baby logo is used provisionally; generate dedicated **square 192x192 and 512x512** icon assets and update the manifest before claiming full install readiness.
4. Do not uninstall the current Streamlit installation until the new frontend has passed testing.

## Safety and limitations
- Functional research and innovation prototype, **not clinically validated**.
- Not a medical device, emergency service or source of individualized medical advice.
- No persistent secure health-record storage; use fictional demo data only.
- The service worker caches only the static shell; it does not provide offline clinical guidance.
- Streamlit Community Cloud may sleep or fail to load in some embedded environments; test on target phones before launch.
- A branded PWA is **not** a native Android APK or Google Play Store release.
