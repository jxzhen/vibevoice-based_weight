"""
Run Audit (NeurIPS 2023, Wang et al.) -- latent diffusion audio editing.

Skeleton. Requires upstream https://github.com/zwx898/AudioEditingTrees
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
    parser.add_argument("--audit_dir", type=str,
                        default="tools/AudioEditingTrees",
                        help="Path to the cloned Audit repo (via HK download)")
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        sys.exit(f"Audio not found: {audio_path}")
    audit_dir = Path(args.audit_dir)
    if not audit_dir.exists():
        print(f"[audit] WARNING: {audit_dir} does not exist.")
        print(f"  Run benchmarks/hk_download/download_all.sh to clone upstream.")

    print(f"[audit] Skeleton -- would call the upstream inference script in {audit_dir}.")
    result = {
        "system": "audit-neurips2023",
        "audio": str(audio_path),
        "text_instruction": args.text,
        "region_start": args.region_start,
        "region_end": args.region_end,
        "output_audio": None,
        "n_params_B_total": None,
        "device": args.device,
        "dtype": None,
        "notes": "skeleton: requires upstream Audit clone + AudioLDM weights",
        "si_sdr": float("nan"),
        "pesq": float("nan"),
        "stoi": float("nan"),
        "mel_l1": float("nan"),
        "lsd": float("nan"),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[audit] Wrote {args.out}")


if __name__ == "__main__":
    main()