"""Brand Streamlit's initial HTML/favicon during the DigitalOcean build.

Run after pip install, before the application starts. Only installed
Streamlit web assets are modified; no HerMamaAI application data is touched.
"""
from pathlib import Path
import re
import shutil

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
shutil.copyfile(LOGO, ICON)
html = HTML.read_text(encoding="utf-8")
icon_link = '<link rel="icon" type="image/png" href="./favicon.png?v=hermamaai-20261109" />'
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
HTML.write_text(html, encoding="utf-8")
print(f"HerMamaAI initial favicon installed: {ICON}; HTML links updated: {count}")
