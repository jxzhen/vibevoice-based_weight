"""
Run the local MiniCPM-o + VibeVoice hybrid on an audio + text edit instruction.

Skeleton. The local fine-tune is the planned next step; for now this
script loads the base models and produces a placeholder transcript so
that the comparison harness has a uniform JSON output schema.

Usage:
    python benchmarks/audio_editing/run_minicpm_vibevoice.py \\
        --audio test.wav --text "replace with a soft pad synth" --out results/ours.json

Output JSON schema (uniform across all baselines):
    {
        "system": "minicpm-o-vibevoice",
        "audio": "<path>",
        "text_instruction": "<prompt>",
        "region_start": 0.2,
        "region_end": 0.6,
        "output_audio": "<path-to-edited.wav>",
        "si_sdr": 12.5,             # higher is better
        "pesq": 2.9,                # higher is better (NaN if pesq not installed)
        "stoi": 0.91,               # higher is better (NaN if pystoi not installed)
        "mel_l1": 0.16,             # lower is better
        "lsd": 5.3,                 # lower is better
        "n_params_B_total": 9.2,    # combined MiniCPM-o (~4B) + VibeVoice (~7B), with sharing
        "device": "cuda",
        "dtype": "bfloat16",
        "notes": "skeleton: not yet fine-tuned; numbers are placeholder"
    }
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch


def placeholder_metrics() -> dict:
    """Return NaN metrics so the harness records a run without fake numbers."""
    return {
        "si_sdr": float("nan"),
        "pesq": float("nan"),
        "stoi": float("nan"),
        "mel_l1": float("nan"),
        "lsd": float("nan"),
    }


def compute_si_sdr(ref: np.ndarray, est: np.ndarray, eps: float = 1e-8) -> float:
    ref = ref - ref.mean()
    est = est - est.mean()
    alpha = np.dot(ref, est) / (np.dot(ref, ref) + eps)
    proj = alpha * ref
    noise = est - proj
    return float(10.0 * np.log10((np.sum(proj**2) + eps) / (np.sum(noise**2) + eps)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", type=str, required=True)
    parser.add_argument("--text", type=str, required=True,
                        help="text edit instruction, e.g. 'replace with violin'")
    parser.add_argument("--region_start", type=float, default=0.2)
    parser.add_argument("--region_end", type=float, default=0.6)
    parser.add_argument("--minicpm_path", type=str, default="openbmb/MiniCPM-o-2_6")
    parser.add_argument("--vibevoice_path", type=str, default="microsoft/VibeVoice-ASR")
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", type=str, default="bfloat16",
                        choices=["float32", "float16", "bfloat16"])
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        sys.exit(f"Audio not found: {audio_path}")

    print(f"[ours] Skeleton harness -- the local MiniCPM-o + VibeVoice "
          f"fine-tune is the next deliverable.")
    print(f"[ours] Audio:   {audio_path}")
    print(f"[ours] Prompt:  {args.text}")
    print(f"[ours] Region:  [{args.region_start:.2f}, {args.region_end:.2f}] s")

    # When the fine-tune is ready, this is where the actual call goes:
    #
    #   from minicpm.modeling_minicpm_o import MiniCPMOmniodelForCausalLM
    #   from vibevoice.modular.modeling_vibevoice_asr import VibeVoiceASRForConditionalGeneration
    #
    #   minicpm = MiniCPMOmniodelForCausalLM.from_pretrained(
    #       args.minicpm_path, torch_dtype=...)
    #   vibevoice = VibeVoiceASRForConditionalGeneration.from_pretrained(
    #       args.vibevoice_path, torch_dtype=...)
    #   # ... fuse via a small adapter that we will train on ICASSP data
    #   edited_audio = fused_model.edit(audio=audio_path, prompt=args.text)
    #   edited_audio.save(args.output_audio)
    #
    # For now we just dump NaN metrics so the harness records the entry.
    result = {
        "system": "minicpm-o-vibevoice",
        "audio": str(audio_path),
        "text_instruction": args.text,
        "region_start": args.region_start,
        "region_end": args.region_end,
        "output_audio": None,
        "n_params_B_total": 9.2,
        "device": args.device,
        "dtype": args.dtype,
        "notes": "skeleton: local MiniCPM-o + VibeVoice fine-tune not yet trained",
        **placeholder_metrics(),
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[ours] Wrote {args.out} (placeholder metrics, NaN)")


if __name__ == "__main__":
    main()