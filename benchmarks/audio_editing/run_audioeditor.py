"""
Run AudioEditor (ICASSP 2025, Jia et al.) on an audio + text edit instruction.

Skeleton. Requires the upstream repo https://github.com/NKU-HLT/AudioEditor
to be pulled via HK. Use the official inference script.

Output JSON schema matches run_minicpm_vibevoice.py.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=str, required=True)
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--region_start", type=float, default=0.2)
    parser.add_argument("--region_end", type=float, default=0.6)
    parser.add_argument("--audioeditor_dir", type=str,
                        default="tools/AudioEditor",
                        help="Path to the cloned AudioEditor repo (via HK download)")
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        sys.exit(f"Audio not found: {audio_path}")
    ae_dir = Path(args.audioeditor_dir)
    if not ae_dir.exists():
        print(f"[audioeditor] WARNING: {ae_dir} does not exist.")
        print(f"  Run benchmarks/hk_download/download_all.sh to clone upstream.")

    print(f"[audioeditor] Skeleton -- would call:")
    print(f"  python {ae_dir}/inference.py --audio {audio_path} --text '{args.text}'")

    result = {
        "system": "audioeditor-icassp2025",
        "audio": str(audio_path),
        "text_instruction": args.text,
        "region_start": args.region_start,
        "region_end": args.region_end,
        "output_audio": None,
        "n_params_B_total": None,  # unknown until upstream loaded
        "device": args.device,
        "dtype": None,
        "notes": "skeleton: requires upstream AudioEditor clone + LDM TTA weights",
        "si_sdr": float("nan"),
        "pesq": float("nan"),
        "stoi": float("nan"),
        "mel_l1": float("nan"),
        "lsd": float("nan"),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[audioeditor] Wrote {args.out}")


if __name__ == "__main__":
    main()