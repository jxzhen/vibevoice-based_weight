"""
Run VibeVoice-ASR on an audio file, dump the transcript + timing to JSON.

Usage:
    python benchmarks/run_vibevoice.py --audio <path.wav> --out <path.json>

Output JSON:
    {
        "system": "vibevoice-asr",
        "model_id": "microsoft/VibeVoice-ASR",
        "audio": "<path>",
        "audio_seconds": 12.3,
        "transcript": "...",
        "language": "auto",
        "generation_seconds": 5.4,
        "rtf": 0.44,
        "n_params_B": 7.0,
        "device": "cuda",
        "dtype": "bfloat16"
    }
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
    parser.add_argument("--model_path", type=str, default="microsoft/VibeVoice-ASR")
    parser.add_argument("--out", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--dtype", type=str, default="bfloat16",
                        choices=["float32", "float16", "bfloat16"])
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        sys.exit(f"Audio not found: {audio_path}")

    duration = audio_duration_seconds(audio_path)
    print(f"[vibevoice] Loading {args.model_path} on {args.device} ...")

    import torch
    from vibevoice.modular.modeling_vibevoice_asr import (
        VibeVoiceASRForConditionalGeneration,
    )
    from vibevoice.processor.vibevoice_asr_processor import (
        VibeVoiceASRProcessor,
    )

    dtype = {"float32": torch.float32, "float16": torch.float16, "bfloat16": torch.bfloat16}[args.dtype]
    processor = VibeVoiceASRProcessor.from_pretrained(
        args.model_path,
        language_model_pretrained_name="Qwen/Qwen2.5-7B",
    )
    model = VibeVoiceASRForConditionalGeneration.from_pretrained(
        args.model_path,
        dtype=dtype,
        attn_implementation="sdpa",
        trust_remote_code=True,
    ).to(args.device)
    model.eval()
    n_params = sum(p.numel() for p in model.parameters()) / 1e9

    print(f"[vibevoice] Transcribing {audio_path.name} ({duration:.2f}s) ...")
    inputs = processor(
        audio=[str(audio_path)],
        sampling_rate=None,
        return_tensors="pt",
        padding=True,
        add_generation_prompt=True,
    )
    inputs = {k: v.to(args.device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}

    t0 = time.time()
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=2048,
            pad_token_id=processor.pad_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            do_sample=False,
        )
    gen_seconds = time.time() - t0
    rtf = gen_seconds / max(duration, 0.01)

    input_len = inputs["input_ids"].shape[1]
    text = processor.tokenizer.decode(output_ids[0, input_len:], skip_special_tokens=True).strip()

    result = {
        "system": "vibevoice-asr",
        "model_id": args.model_path,
        "audio": str(audio_path),
        "audio_seconds": round(duration, 3),
        "transcript": text,
        "language": "auto",
        "generation_seconds": round(gen_seconds, 3),
        "rtf": round(rtf, 3),
        "n_params_B": round(n_params, 3),
        "device": args.device,
        "dtype": args.dtype,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[vibevoice] Wrote {args.out} (rtf={rtf:.2f})")


if __name__ == "__main__":
    main()