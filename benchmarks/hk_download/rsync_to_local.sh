#!/usr/bin/env bash
# One-time transfer: HK cache -> local machine.
#
# Run on the LOCAL machine (or via SSH port-forward), NOT on HK.
# After this succeeds, the HK rental can be released.
#
# Usage:
#   bash benchmarks/hk_download/rsync_to_local.sh <hk_user>@<hk_host>
#
# The HK cache is mounted at /root/vibevoice-cache by download_all.sh.
# We pull it down to ./models/ inside this repo's working directory
# (which is excluded by .gitignore).
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <hk_user>@<hk_host>"
    echo "Example: $0 root@hk.ali.example.com"
    exit 1
fi
HK_TARGET="$1"
LOCAL_DIR="${LOCAL_DIR:-./models}"
mkdir -p "${LOCAL_DIR}"

echo "[local] pulling HK cache (${HK_TARGET}:/root/vibevoice-cache) -> ${LOCAL_DIR}/"
rsync -avz --progress \
    --include='*/' \
    --include='*.safetensors' --include='*.bin' --include='*.pt' \
    --include='*.json' --include='*.txt' --include='*.md' \
    --include='tokenizer*' --include='vocab.*' --include='*.py' \
    --exclude='*' \
    "${HK_TARGET}:/root/vibevoice-cache/" "${LOCAL_DIR}/"

echo "[local] done. Verify with:"
echo "  du -sh ${LOCAL_DIR}"
echo "  ls ${LOCAL_DIR}/models--microsoft--VibeVoice-ASR/snapshots/"
echo ""
echo "When verified, release the HK rental instance."
echo "The next phase is the local MiniCPM-o + VibeVoice fine-tune."