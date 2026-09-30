"""
Run InstructSpeech (ICML 2024, Huang et al.) -- LLM-driven speech editing.

Skeleton. Requires upstream https://github.com/ali-vilab/InstructSpeech
(or similar). Use the official inference script.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=str, required=True)
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--region_start", type=float, default=0.2)
    parser.add_argument("--region_end", type=float, default=0.6)
    parser.add_argument("--instruct_dir", type=str,
                        default="tools/InstructSpeech")
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        sys.exit(f"Audio not found: {audio_path}")
    instruct_dir = Path(args.instruct_dir)
    if not instruct_dir.exists():
        print(f"[instructspeech] WARNING: {instruct_dir} does not exist.")
        print(f"  Run benchmarks/hk_download/download_all.sh to clone upstream.")

    print(f"[instructspeech] Skeleton -- would call upstream inference in {instruct_dir}.")
    result = {
        "system": "instructspeech-icml2024",
        "audio": str(audio_path),
        "text_instruction": args.text,
        "region_start": args.region_start,
        "region_end": args.region_end,
        "output_audio": None,
        "n_params_B_total": None,
        "device": args.device,
        "dtype": None,
        "notes": "skeleton: requires upstream InstructSpeech clone",
        "si_sdr": float("nan"),
        "pesq": float("nan"),
        "stoi": float("nan"),
        "mel_l1": float("nan"),
        "lsd": float("nan"),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[instructspeech] Wrote {args.out}")


if __name__ == "__main__":
    main()