# Audio Editing SOTA Comparison

Goal: place a small-model hybrid (`MiniCPM-o` + `VibeVoice` fine-tune)
in context against the published ICASSP 2027 Audio Editing Challenge SOTA.
**Final objective: exceed SOTA on SI-SDR / PESQ / STOI / Mel L1 / LSD.**

This is **research**, NOT the official submission
(<https://github.com/jxzhen/aec-2027-editx-lora>).

## Compared methods

| ID | Repo / reference | How we run it here |
|---|---|---|
| **Mask-only** | baseline (silence the masked region) | `run_mask_only.py` |
| **Zero-copy** | upper bound (return original) | `run_zero_copy.py` |
| **AudioEditor** | ICASSP 2025 (Jia et al.) | `run_audioeditor.py` |
| **Audit** | NeurIPS 2023 (Wang et al.) | `run_audit.py` |
| **InstructSpeech** | ICML 2024 (Huang et al.) | `run_instructspeech.py` |
| **MiniCPM-o + VibeVoice (ours)** | local fine-tune | `run_minicpm_vibevoice.py` |

## Evaluation metrics

Aligned with the ICASSP 2027 AEC protocol:

- **SI-SDR** (dB, higher better) -- primary
- **PESQ** (wide-band, higher better)
- **STOI** (0-1, higher better)
- **Mel L1** (lower better)
- **LSD** (log-spectral distance, lower better)

## Datasets

For the AEC evaluation we target the official test set, which uses a
held-out 100-clip subset with synthetic region annotations:

- AudioCaps test split (English short captions)
- ESC-50 (environmental)
- ESC-50 + noise (MUSAN mix)

The official ICASSP submission tested on a smaller (12-pair) self-distilled
LibriSpeech subset for emotional editing; this side-project uses a broader
AudioCaps + ESC-50 mix to give the small-model hybrid more headroom.

## How to reproduce

```bash
# 1. Pull all baseline repos via HK (one-time, see hk_download/)
bash benchmarks/hk_download/download_all.sh

# 2. Run each baseline
python benchmarks/audio_editing/run_mask_only.py     --audio_dir data/test --out results/mask_only.json
python benchmarks/audio_editing/run_audioeditor.py   --audio_dir data/test --out results/audioeditor.json
python benchmarks/audio_editing/run_audit.py         --audio_dir data/test --out results/audit.json
python benchmarks/audio_editing/run_instructspeech.py --audio_dir data/test --out results/instructspeech.json
python benchmarks/audio_editing/run_minicpm_vibevoice.py --audio_dir data/test --out results/ours.json

# 3. Aggregate
python benchmarks/audio_editing/aggregate.py --results benchmarks/audio_editing/results/ --out benchmarks/audio_editing/summary.md
```

## Status

Skeleton only. Numbers come after the local fine-tune finishes.