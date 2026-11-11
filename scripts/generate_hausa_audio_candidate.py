"""Generate an UNAPPROVED local Hausa Calm Corner WAV candidate.

Run separately from the HerMamaAI app. Requires an initial internet download
of the Meta MMS Hausa model; inference works offline after caching.
Model: facebook/mms-tts-hau (CC BY-NC 4.0, noncommercial restrictions).
Do NOT add output to approved_manifest.json without linguistic and rights review.
"""
import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="Use cached model only")
    args = parser.parse_args()
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    import numpy as np
    import torch
    from scipy.io.wavfile import write
    from transformers import AutoTokenizer, VitsModel

    model_id = "facebook/mms-tts-hau"
    text = "Shuka furanni ka ga ƙaramin lambunka yana bunƙasa."
    tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=args.offline)
    model = VitsModel.from_pretrained(model_id, local_files_only=args.offline)
    model.eval()
    torch.manual_seed(42)
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        waveform = model(**inputs).waveform.squeeze().cpu().numpy()
    waveform = np.clip(waveform, -1, 1)
    output = Path("assets/calm_audio/candidates/ha_activity_1_UNREVIEWED.wav")
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, model.config.sampling_rate, (waveform * 32767).astype(np.int16))
    print(f"UNREVIEWED audio candidate saved: {output}")
    print("Do not approve or deploy before fluent Hausa and licensing review.")


if __name__ == "__main__":
    main()
