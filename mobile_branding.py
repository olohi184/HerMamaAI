"""Create Android installation images directly from HerMamaAI's official logo.

No tracing, stylization, emblem reconstruction, or partial cropping is applied.
The PNG images contain the original official artwork scaled proportionally.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "HerMamaAI Mother and Baby Emblem.png"
STATIC = ROOT / "static"


def ensure_official_mobile_icons():
    """Produce manifest images from the full original brand logo.

    Never let icon generation stop the educational Streamlit application.
    """
    if not SOURCE.is_file():
        return False
    STATIC.mkdir(exist_ok=True)
    specs = [
        (192, "hermamaai-original-brand-192.png", 0.89),
        (512, "hermamaai-original-brand-512.png", 0.89),
        (512, "hermamaai-original-brand-maskable-512.png", 0.76),
    ]
    if all((STATIC / filename).is_file() for _, filename, _ in specs):
        return True
    try:
        with Image.open(SOURCE) as original:
            image = original.convert("RGBA")
            # Only remove fully transparent padding; never crop the logo itself.
            alpha_box = image.getchannel("A").getbbox()
            if alpha_box:
                image = image.crop(alpha_box)
            for size, filename, fraction in specs:
                side = round(size * fraction)
                scaled = ImageOps.contain(
                    image, (side, side), method=Image.Resampling.LANCZOS
                )
                canvas = Image.new("RGBA", (size, size), "#fff2fa")
                canvas.alpha_composite(
                    scaled,
                    ((size - scaled.width) // 2, (size - scaled.height) // 2),
                )
                canvas.convert("RGB").save(
                    STATIC / filename, format="PNG", optimize=True
                )
        return True
    except (OSError, ValueError):
        return False
