"""Generate unreviewed offline speech candidates for Calm Corner Activity 1.

Run only on a developer machine, never in the Streamlit request path.
Yoruba: verified Meta MMS model (CC BY-NC 4.0, research evaluation only).
Igbo: community Soro-TTS Igbo VITS checkpoint for research evaluation only.
Do not register output in approved_manifest.json automatically.
"""
import argparse
import os
from pathlib import Path

SCRIPTS = {
    "yo": "Gbin àwọn òdòdó, kí o sì wo ọgbà kékeré rẹ bí ó ṣe ń dàgbà.",
    "ig": "Kụọ okooko osisi ma lelee obere ubi gị ka ọ na-eto.",
}
VERIFIED_MODELS = {"yo": "facebook/mms-tts-yor", "ig": "Shinzmann/soro-tts-ibo"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=["yo", "ig"], required=True)
    parser.add_argument("--model-id", help="Explicitly selected Igbo VITS model after license and compatibility review")
    parser.add_argument("--offline", action="store_true", help="Use cached model files only")
    args = parser.parse_args()
    if args.model_id:
        parser.error("Model overrides are disabled; use the explicitly reviewed checkpoint for this language.")
    model_id = args.model_id or VERIFIED_MODELS[args.language]
    if args.offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    import numpy as np
    import torch
    from scipy.io.wavfile import write
    from transformers import AutoTokenizer, VitsModel

    print("Evaluation only. Do not publish or approve without language and rights review.")
    tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=args.offline)
    model = VitsModel.from_pretrained(model_id, local_files_only=args.offline)
    model.eval()
    torch.manual_seed(42)
    inputs = tokenizer(SCRIPTS[args.language], return_tensors="pt")
    with torch.no_grad():
        waveform = model(**inputs).waveform.squeeze().cpu().numpy()
    waveform = np.clip(waveform, -1, 1)
    output = Path(f"assets/calm_audio/candidates/{args.language}_activity_1_UNREVIEWED.wav")
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, model.config.sampling_rate, (waveform * 32767).astype(np.int16))
    print(f"UNREVIEWED candidate saved: {output}")
    print("Not approved for app playback. Confirm language accuracy, quality and distribution rights.")


if __name__ == "__main__":
    main()
