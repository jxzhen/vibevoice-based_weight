"""
Run Whisper (large-v3) on an audio file, dump transcript + timing to JSON.

Usage:
    pip install openai-whisper
    python benchmarks/run_whisper.py --audio <path.wav> --out <path.json>

Output: same shape as run_vibevoice.py.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import soundfile as sf


def audio_duration_seconds(path: Path) -> float:
    info = sf.info(str(path))
    return float(info.frames) / float(info.samplerate)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=str, required=True)
    parser.add_argument("--model", type=str, default="large-v3",
                        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3", "turbo"])
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        sys.exit(f"Audio not found: {audio_path}")

    duration = audio_duration_seconds(audio_path)
    print(f"[whisper] Loading {args.model} on {args.device} ...")
    import whisper

    model = whisper.load_model(args.model, device=args.device)
    n_params = sum(p.numel() for p in model.parameters()) / 1e9

    print(f"[whisper] Transcribing {audio_path.name} ({duration:.2f}s) ...")
    t0 = time.time()
    result_whisper = model.transcribe(
        str(audio_path),
        language=None,  # auto-detect
        verbose=False,
        fp16=(args.device == "cuda"),
    )
    gen_seconds = time.time() - t0
    rtf = gen_seconds / max(duration, 0.01)

    text = result_whisper.get("text", "").strip()
    lang = result_whisper.get("language", "unknown")

    out = {
        "system": f"whisper-{args.model}",
        "model_id": f"openai/whisper-{args.model}",
        "audio": str(audio_path),
        "audio_seconds": round(duration, 3),
        "transcript": text,
        "language": lang,
        "generation_seconds": round(gen_seconds, 3),
        "rtf": round(rtf, 3),
        "n_params_B": round(n_params, 3),
        "device": args.device,
        "dtype": "float16" if args.device == "cuda" else "float32",
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[whisper] Wrote {args.out} (rtf={rtf:.2f}, lang={lang})")


if __name__ == "__main__":
    main()