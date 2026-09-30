# vibevoice-based_weight

**Side-project weight manifest and download pipeline for an audio editing
research effort that combines `MiniCPM-o` (ModelBest, "MianBian XiaoGangPao")
with `microsoft/VibeVoice` and evaluates against ICASSP 2027 AEC SOTA.**

This is NOT the official ICASSP 2027 AEC submission.

The official submission lives in a separate repository and was authored
earlier, without overlap:

> **Official ICASSP 2027 AEC submission:**
> <https://github.com/jxzhen/aec-2027-editx-lora>
>
> A LoRA adapter on top of `stepfun-ai/Step-Audio-EditX`. The submission
> weight carrier of record is the HF mirror
> `huggingface.co/jxzhen/aec-2027-editx-lora` (commit
> `b6d1621d583e6109ccc09f3e2dbe67b8d1820494`, 2026-09-28).
>
> The ICASSP 2027 AEC organizer should grade only the official submission.
> **This side-project repo is for research experimentation and explicitly
> does not affect the grading chain.**

## Why this side-project exists

After the official submission was finalized, the author reserved a
one-month lightweight HK server for the following purpose:

1. **Download** a curated set of HuggingFace audio editing models
   (and related base models / tokenizers) **without** relying on
   mainland-China mirrors that occasionally throttle or break.
2. **Transfer** those weights **once** to the author's local machine
   for long-term storage. The HK server is ephemeral -- it will be
   released after the one-month rental ends.
3. **Run** small-model experiments locally that combine
   `ModelBest/MiniCPM-o` (a ~2-4B omni-modal LLM with audio I/O) with
   `microsoft/VibeVoice` (a 7B long-form ASR / audio LLM) to see if a
   small-model hybrid can match or exceed the published SOTA on the
   ICASSP 2027 Audio Editing Challenge evaluation metrics
   (SI-SDR / PESQ / STOI / Mel L1 / LSD).

## Relationship at a glance

```
                       ephemeral (1 month)
   +-----------------------------+
   |  HK lightweight server      |   downloads:
   |  - HF, no mirror throttle   |    - microsoft/VibeVoice-ASR  (7B)
   |  - rsync endpoint           |    - microsoft/VibeVoice        (TTS)
   |  - 1 month rental           |    - openbmb/MiniCPM-o          (omni)
   +-------------+---------------+
                 | rsync / scp (one-time)
                 v
   +-----------------------------+      long-term storage
   |  local machine (this repo)  |      - D:/models/...
   |  - mini experiments         |      - bench harness
   |  - SOTA comparison          |
   +-------------+---------------+
                 |
                 v
            (no further action;
             this is not a submission)
```

## Layout

```
.
+- README.md                          this file
+- LICENSE                            MIT
+- manifest.json                      machine-readable manifest
+- benchmarks/
|   +- README.md                      ASR comparison overview
|   +- run_vibevoice.py               VibeVoice-ASR inference dump
|   +- run_whisper.py                 Whisper inference dump
|   +- run_paraformer.py              Paraformer inference dump
|   +- aggregate.py                   combine JSON -> summary.{md,json}
|   +- results_template.md            fill-in template
|   +- audio_editing/                 SOTA comparison for AEC
|       +- README.md
|       +- run_audioeditor.py
|       +- run_audit.py
|       +- run_instructspeech.py
|       +- run_minicpm_vibevoice.py   the local small-model hybrid
|       +- aggregate.py
|       +- results_template.md
|   +- hk_download/                   HK download pipeline
|       +- download_all.sh            pulls HF models into HK cache
|       +- rsync_to_local.sh          one-time transfer from HK -> local
+- .gitignore
```

## Integrity / SHA-256

This repo does not store binary weights. Integrity is verified against
upstream HuggingFace commit hashes at download time. The official
ICASSP submission's `SHA256SUMS.txt` lives in
`jxzhen/aec-2027-editx-lora` and is unchanged.

## Use

Research only. The ICASSP organizer should not consult this repo when
grading `jxzhen/aec-2027-editx-lora`.

## Contact

Jianxi Zheng · `hunan08182026@126.com`