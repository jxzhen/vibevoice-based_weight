"""
Run Alibaba Paraformer-v2 on an audio file, dump transcript + timing to JSON.

Usage:
    pip install funasr modelscope
    python benchmarks/run_paraformer.py --audio <path.wav> --out <path.json>

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
    parser.add_argument("--model", type=str, default="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch")
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        sys.exit(f"Audio not found: {audio_path}")

    duration = audio_duration_seconds(audio_path)
    print(f"[paraformer] Loading {args.model} ...")
    from funasr import AutoModel

    model = AutoModel(
        model=args.model,
        device=args.device,
        disable_update=True,
    )
    # Paraformer model param count is reported by ModelScope; load manually
    n_params_B = 0.220  # ~220M as published

    print(f"[paraformer] Transcribing {audio_path.name} ({duration:.2f}s) ...")
    t0 = time.time()
    result = model.generate(
        input=str(audio_path),
        batch_size_s=300,  # 5-minute chunks
    )
    gen_seconds = time.time() - t0
    rtf = gen_seconds / max(duration, 0.01)

    if not result:
        text, lang = "", "unknown"
    else:
        text = result[0].get("text", "").strip()
        lang = "zh" if any('\u4e00' <= ch <= '\u9fff' for ch in text) else "unknown"

    out = {
        "system": "paraformer-v2",
        "model_id": args.model,
        "audio": str(audio_path),
        "audio_seconds": round(duration, 3),
        "transcript": text,
        "language": lang,
        "generation_seconds": round(gen_seconds, 3),
        "rtf": round(rtf, 3),
        "n_params_B": n_params_B,
        "device": args.device,
        "dtype": "float32",
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[paraformer] Wrote {args.out} (rtf={rtf:.2f})")


if __name__ == "__main__":
    main()