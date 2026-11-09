"""Brand Streamlit's initial HTML/favicon during the DigitalOcean build.

Run after pip install, before the application starts. Only installed
Streamlit web assets are modified; no HerMamaAI application data is touched.
"""
from pathlib import Path
import re
from PIL import Image, ImageOps

import streamlit

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "HerMamaAI Mother and Baby Emblem.png"
WEB = Path(streamlit.__file__).resolve().parent / "static"
HTML = WEB / "index.html"
ICON = WEB / "favicon.png"

if not LOGO.is_file() or not HTML.is_file():
    raise SystemExit("Branding failed: official logo or Streamlit index.html missing")

# Streamlit's initial page normally links to ./favicon.png before app.py runs.
# Replacing the packaged favicon handles Safari's first document load.
with Image.open(LOGO) as source:
    source = source.convert("RGBA")
    square = Image.new("RGBA", (64, 64), "#fff2fa")
    fitted = ImageOps.contain(source, (60, 60), Image.Resampling.LANCZOS)
    square.alpha_composite(fitted, ((64 - fitted.width) // 2, (64 - fitted.height) // 2))
    square.save(ICON, format="PNG")
html = HTML.read_text(encoding="utf-8")
icon_link = '<link rel="icon" type="image/png" href="./favicon.png?v=hermamaai-tab-20261109c" />'
html, count = re.subn(
    r"""<link\s+[^>]*rel=["'](?:shortcut\s+)?icon["'][^>]*>""",
    icon_link,
    html,
    flags=re.IGNORECASE,
)
if not count:
    # Insert a link in the initial head even if the installed Streamlit
    # version has changed its default favicon markup.
    if "</head>" not in html:
        raise SystemExit("Branding failed: Streamlit index.html has no </head>")
    html = html.replace("</head>", f"  {icon_link}\n</head>", 1)
# Streamlit may rewrite the favicon after its frontend initializes.
# Install this guard in the *top-level* HTML, not in a Streamlit component iframe.
# Preserve the initial branded favicon and restore it if Streamlit changes it.
guard = """<script data-hermamaai-tab-icon>
(() => {
  const href = '/favicon.png?v=hermamaai-tab-20261109c';
  let syncing = false;
  function apply() {
    if (syncing) return;
    syncing = true;
    try {
      let primary = document.head.querySelector('link[data-hermamaai-tab-icon]');
      if (!primary) {
        primary = document.createElement('link');
        primary.setAttribute('data-hermamaai-tab-icon', 'true');
        document.head.appendChild(primary);
      }
      if (primary.rel !== 'icon') primary.rel = 'icon';
      if (primary.type !== 'image/png') primary.type = 'image/png';
      if (primary.getAttribute('href') !== href) primary.setAttribute('href', href);
      document.head.querySelectorAll('link[rel~="icon"]').forEach(link => {
        if (link !== primary) link.remove();
      });
    } finally { syncing = false; }
  }
  apply();
  const observer = new MutationObserver(() => apply());
  observer.observe(document.head, {childList: true, subtree: true, attributes: true,
    attributeFilter: ['href', 'rel']});
})();
</script>"""
if 'data-hermamaai-tab-icon' not in html:
    html = html.replace('</head>', guard + '\\n</head>', 1)
HTML.write_text(html, encoding="utf-8")
print(f"HerMamaAI initial favicon installed: {ICON}; HTML links updated: {count}")
