"""Opt-in, locally packaged Calm Corner recordings (non-medical content only).

Recordings are NOT generated, fetched, or shipped by this module. A reviewer must
approve each recording and explicitly register its SHA-256 digest in the manifest.
This prevents unreviewed or mismatched audio from being played accidentally.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "calm_audio" / "approved_manifest.json"
LANGUAGES = frozenset({"ha", "yo", "ig"})
ACTIVITY_COUNT = 6


def approved_audio_path(language: str, activity_index: int):
    """Return an approved local recording path or None; never use network/TTS."""
    if language not in LANGUAGES or type(activity_index) is not int:
        return None
    if not 0 <= activity_index < ACTIVITY_COUNT or not MANIFEST.is_file():
        return None
    try:
        entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
        entry = entries.get(language, {}).get(str(activity_index + 1), {})
        digest = entry.get("sha256", "")
        extension = entry.get("format", "")
        if extension not in ("mp3", "wav") or len(digest) != 64:
            return None
        if not all(c in "0123456789abcdef" for c in digest):
            return None
        path = ROOT / "assets" / "calm_audio" / language / (
            f"activity_{activity_index + 1}.{extension}"
        )
        if not path.is_file() or path.stat().st_size > 15 * 1024 * 1024:
            return None
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            return None
        return path
    except (OSError, ValueError, TypeError, AttributeError):
        return None
