"""Generate installable Android icons from HerMamaAI's existing official emblem.

The original artwork remains the authoritative brand asset. These icon crops
exclude its tiny wordmark, which is unreadable on phone home screens.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "HerMamaAI Mother and Baby Emblem.png"
STATIC = ROOT / "static"


def ensure_official_mobile_icons():
    if not SOURCE.is_file():
        return False
    STATIC.mkdir(exist_ok=True)
    sizes = [
        (192, "hermamaai-official-192.png", 0.79),
        (512, "hermamaai-official-512.png", 0.79),
        (512, "hermamaai-official-maskable-512.png", 0.63),
    ]
    if all((STATIC / filename).is_file() for _, filename, _ in sizes):
        return True
    try:
        with Image.open(SOURCE) as original:
            art = original.convert("RGBA")
            # Trim transparency around the original artwork.
            alpha_bbox = art.getchannel("A").getbbox()
            if alpha_bbox:
                art = art.crop(alpha_bbox)
            w, h = art.size
            # The official graphic has the mother-and-baby symbol at the top
            # and a wordmark below. Keep only the recognizable emblem.
            region = art.crop((
                round(w * 0.16), 0,
                round(w * 0.84), max(1, round(h * 0.64))
            ))
            symbol_bbox = region.getchannel("A").getbbox()
            if symbol_bbox:
                region = region.crop(symbol_bbox)
            for size, filename, scale in sizes:
                icon = Image.new("RGBA", (size, size), "#fff2fa")
                max_symbol = round(size * scale)
                resized = ImageOps.contain(
                    region, (max_symbol, max_symbol),
                    method=Image.Resampling.LANCZOS
                )
                icon.alpha_composite(
                    resized,
                    ((size - resized.width) // 2,
                     (size - resized.height) // 2)
                )
                icon.convert("RGB").save(STATIC / filename, "PNG", optimize=True)
        return True
    except (OSError, ValueError):
        # Mobile icons are non-critical: never interrupt the maternal wellness app.
        return False
