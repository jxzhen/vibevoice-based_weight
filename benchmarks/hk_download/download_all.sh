#!/usr/bin/env bash
# HK-server-only download pipeline.
#
# PURPOSE: pull all HuggingFace audio editing models that the local
# small-model experiment will need, into the HK lightweight server.
# After this, run rsync_to_local.sh ONCE to copy the cache to the local
# machine, then release the HK rental.
#
# This script is intentionally tuned for the HK server environment:
#   - no mirror throttle (HK has clean HF egress)
#   - 50 GB cache by default
#   - explicit allow-list so we never accidentally pull unrelated stuff
#
# Run on the HK server:
#   bash benchmarks/hk_download/download_all.sh
#
set -euo pipefail

CACHE="${HF_CACHE:-/root/vibevoice-cache}"
mkdir -p "${CACHE}"
echo "[hk] cache = ${CACHE}"

# ---- core audio editing base + side models ----
python - <<'PY'
import os
from huggingface_hub import snapshot_download

CACHE = os.environ.get("HF_CACHE", "/root/vibevoice-cache")
TARGETS = [
    # Microsoft VibeVoice family
    "microsoft/VibeVoice-ASR",
    "microsoft/VibeVoice",
    # ModelBest MiniCPM-o (omni-modal LLM)
    "openbmb/MiniCPM-o-2_6",
    # StepFun EditX (the official submission's base model -- for local
    # comparison; weights are NOT redistributed in this repo)
    "stepfun-ai/Step-Audio-EditX",
    # CosyVoice vocoder (used by EditX)
    "FunAudioLLM/CosyVoice-300M-25Hz",
    # Open ASR baselines (for the ASR benchmark)
    "openai/whisper-large-v3",
    "openai/whisper-large-v3-turbo",
    # Chinese ASR baseline
    "FunAudioLLM/Paraformer-v2",
]

for t in TARGETS:
    print(f"[hk] downloading {t} -> {CACHE}")
    snapshot_download(
        repo_id=t,
        cache_dir=CACHE,
        allow_patterns=[
            "*.json", "*.txt", "*.md",
            "*.safetensors", "*.bin", "*.pt",
            "*.py", "tokenizer.*", "vocab.*",
        ],
        max_workers=8,
    )
print("[hk] all downloads done")
PY

echo "[hk] cache size:"
du -sh "${CACHE}" || true
echo "[hk] next step: bash benchmarks/hk_download/rsync_to_local.sh <user>@<host>"