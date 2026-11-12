"""Batch-generate UNREVIEWED Calm Corner audio candidates (activities 2-6).

Uses existing draft UI translations verbatim; does not invent translations.
Local research evaluation only. Model weights may download on first use.
Do not publish audio or modify approved_manifest.json without language,
clinical-scope and licensing review. No runtime inference in the web app.
"""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGLISH = [
    "Plant flowers and watch your little garden bloom.",
    "Find a calm scene and enjoy a quiet pause.",
    "Match cheerful pictures at your own pace.",
    "Unscramble gentle, encouraging words.",
    "Collect small moments worth remembering.",
    "Create a colourful bouquet of flowers.",
]
MODELS = {
    "ha": "facebook/mms-tts-hau",
    "yo": "facebook/mms-tts-yor",
    "ig": "Shinzmann/soro-tts-ibo",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=sorted(MODELS), required=True)
    parser.add_argument("--offline", action="store_true", help="Use already cached weights only")
    parser.add_argument("--start", type=int, default=2, choices=range(2, 7))
    args = parser.parse_args()
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
    language = args.language
    translations = json.loads((ROOT / "locales" / f"{language}.json").read_text(encoding="utf-8"))
    texts = []
    for index in range(args.start - 1, 6):
        source = ENGLISH[index]
        translated = translations.get("ui." + source)
        if not isinstance(translated, str) or not translated.strip() or translated.strip() == source:
            raise SystemExit(f"Missing distinct {language} translation for activity {index+1}: {source}")
        texts.append((index + 1, translated))

    import numpy as np
    import torch
    from scipy.io.wavfile import write
    from transformers import AutoTokenizer, VitsModel

    model_id = MODELS[language]
    tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=args.offline)
    model = VitsModel.from_pretrained(model_id, local_files_only=args.offline)
    model.eval()
    destination = ROOT / "assets" / "calm_audio" / "candidates"
    destination.mkdir(parents=True, exist_ok=True)
    print("Research candidates only. Do not publish or register in approved manifest.")
    for activity, script in texts:
        path = destination / f"{language}_activity_{activity}_UNREVIEWED.wav"
        if path.exists():
            print(f"Skipping existing file: {path.name}")
            continue
        print(f"Generating {language} activity {activity}: {script}", flush=True)
        inputs = tokenizer(script, return_tensors="pt")
        torch.manual_seed(42 + activity)
        with torch.no_grad():
            waveform = model(**inputs).waveform.squeeze().cpu().numpy()
        waveform = np.clip(waveform, -1, 1)
        write(path, model.config.sampling_rate, (waveform * 32767).astype(np.int16))
        print(f"Saved UNREVIEWED: {path.name}", flush=True)
    print("Finished candidate generation. Fluent-speaker and rights review still required.")


if __name__ == "__main__":
    main()
