# ASR Comparison Benchmarks

Goal: place **microsoft/VibeVoice-ASR** (the model referenced by this
side-project repo) in context. Where it shines, where it lags.

This is a **side-project benchmark**, NOT part of the official
ICASSP 2027 AEC submission at <https://github.com/jxzhen/aec-2027-editx-lora>.

## Why compare VibeVoice-ASR

VibeVoice-ASR (Microsoft Research Asia, 2026) advertises:
- 60-minute single-pass long-form transcription (others slice 30s)
- Joint ASR + speaker diarization + timestamps
- 50+ language support
- Customized hotwords
- DER 3.42% / tcpWER 14.81% on AISHELL-4, AMI, AliMeeting

The interesting questions for a side-project:

1. **How much better is 7B on long-form TED-style English than Whisper-large-v3?**
2. **How does VibeVoice compare to open Chinese ASR (Paraformer, FunASR)?**
3. **What is the real-time factor (RTF) on consumer GPUs?**
4. **Does the speaker diarization actually work on multi-speaker podcast audio?**
5. **Hotword injection: measurable WER improvement on technical jargon?**

## Compared ASR systems

| System | Params | Open | Long-form | Multilingual | Diarization |
|---|---|---|---|---|---|
| **microsoft/VibeVoice-ASR** | 7B | ✅ | ✅ 60 min | ✅ 50+ langs | ✅ |
| openai/whisper-large-v3 | 1.5B | ✅ | ⚠️ via chunking | ✅ 99 langs | ❌ |
| openai/whisper-large-v3-turbo | 0.8B | ✅ | ⚠️ | ✅ | ❌ |
| alibaba/Paraformer-v2 | ~220M | ✅ | ⚠️ | ❌ (CN-only) | ❌ |
| pyf98/canary-1b-v2 | 1B | ✅ | ⚠️ | ✅ | ❌ |
| nvidia/Parakeet-TDT-0.6B | 0.6B | ✅ | ⚠️ | ❌ (EN) | ❌ |

## Datasets

| Dataset | Language | Length | Why |
|---|---|---|---|
| TED-LIUM 3 (test) | EN | long | classic lecture English |
| AISHELL-1 (test) | CN | short | Chinese benchmark |
| Earnings-21 | EN | long | noisy financial call |
| VoxConverse (dev) | EN | long | multi-speaker podcast |

## Metrics

- **WER** (word error rate, lower is better) — primary metric
- **CER** (character error rate) — for Chinese
- **DER** (diarization error rate) — for multi-speaker
- **RTF** (real-time factor, lower is faster than 1.0)
- **Peak GPU memory** (GB)

## Reproducing

Each model has its own runner:

```bash
python benchmarks/run_vibevoice.py --audio test.wav --out benchmarks/results/vibevoice.json
python benchmarks/run_whisper.py   --audio test.wav --out benchmarks/results/whisper.json
python benchmarks/run_paraformer.py --audio test.wav --out benchmarks/results/paraformer.json

python benchmarks/aggregate.py --results benchmarks/results/ --out benchmarks/summary.md
```

`aggregate.py` builds the comparison table that powers the web demo.

## Status

This folder is intentionally left empty of results until the AutoDL run
completes. The runners are skeletons that load each model and dump JSON;
the numbers are filled in manually after the runs.