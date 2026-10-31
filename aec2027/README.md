# `aec2027/` -- model component manifest for the ICASSP 2027 AEC agent

This directory is the **Track 2 Rule 3 audit artifact** for the
audio-editing agent described by the `vibevoice-based-plus` project:
model versions, links to model weights, evidence of their public release
dates, and per-file SHA-256 checksums.

## What this directory is NOT

1. **It contains no model weights.** Not a single binary byte. The weights
   live on their upstream platforms, and this manifest points at them and
   pins them.
2. **It is not a second submission entry.** The one official entry is
   [`jxzhen/aec-2027-editx-lora`](https://github.com/jxzhen/aec-2027-editx-lora).
   The three side repositories (`vibevoice-based_weight` = this one,
   `AEC-2027-transfer-agent`, `vibevoice-based_AudioEditing.html`) are
   supporting material only.
3. **It is not a claim of any benchmark score.** Every number in this
   repository comes from the unmodified official evaluator, or it is not
   here at all.

## Why there are no binaries here (the timing argument)

Track 2 Rule 1 reads:

> The specific versions and weights of **all model components** in the agent
> system must have been publicly released **before November 1, 2026**.
> **This extends the previous cutoff of October 1, 2026.**

Source: <https://audio-editing-challenge.github.io/track2/> (Rule 1), and the
same wording in the FAQ at <https://audio-editing-challenge.github.io/faqs/>.
The official page states that November 1, 2026 *extends* the previous cutoff
of October 1, 2026, i.e. October 1 is the superseded cutoff and the
operative one is November 1, 2026.

The rule constrains the **public release date of the weights**. The release
date of a weight file is a property of *where and when that file was first
made public*, and the hosting platform is the only authority that records
it. If a copy of those same bytes were re-uploaded here, this repository
would gain a second, later public exposure of the same weights, and an
auditor could no longer tell which exposure is the authoritative one -- and
the later one would sit exactly on the cutoff. So:

- the weights stay upstream, where their release date is already recorded;
- this manifest pins each one to an exact 40-hex revision and publishes the
  platform's own SHA-256 for every LFS-tracked file;
- the deployment was verified **byte-identical** to those published digests,
  which is what links "the weights we ran" to "the version that was public
  before November 1, 2026".

## How the binding between "what we ran" and "what is public" works

The checkpoints were fetched by branch name without an explicit revision
lock, so the Hub snapshot metadata left on the host does not by itself prove
which commit was downloaded. The binding is cryptographic instead:

> every LFS-tracked file that was deployed hashes to exactly the
> `lfs.sha256` that the Hub publishes for the pinned revision.

A file carrying that digest **is** that revision's file, so the bytes we
ran and the bytes that were publicly released are the same bytes. Measured
on the compute host: `dots.tts.edit` 5/5 LFS files identical, `AuK` 2/2,
`Qwen2.5-Omni-3B` 5/5, zero mismatches.

That is why no re-download and no re-run is needed to close the audit chain
-- re-downloading the same revision would only reproduce the same digests.

## The components

Full machine-readable detail: [`MANIFEST.json`](MANIFEST.json).
Human-readable notes: [`COMPONENTS.md`](COMPONENTS.md).

| Role | Model | Pinned revision | Public release (UTC) | License | Gated |
|---|---|---|---|---|---|
| router LLM | `Qwen/Qwen2.5-Omni-3B` | `f75b40e3da20…` | 2025-04-30 | Apache-2.0 | no |
| speech edit | `dots-studio/dots.tts.edit` (V1.1) | `cc4d5d382157…` | 2026-10-30 | Apache-2.0 | no |
| generative edit | `tencent/AuK` | `790742b71a44…` | 2026-08-18 | MIT | no |
| source separation | `facebook/sam-audio-large` | `5f2cd3a9471a…` | 2025-12-12 | *not verified* | **manual** |
| ASR (in AuK route) | `iic/SenseVoiceSmall` | *(ModelScope)* | pre-cutoff | *not verified* | no |
| DSP tools (speed / volume / pitch) | numpy / soundfile / ffmpeg | -- | -- | no weights | -- |

The most recent component release is **2026-10-30**, i.e. inside the
cutoff. This system **trains no weights of its own**, so there is no
self-trained checkpoint whose publication would have to be scheduled
against the deadline.

## How to verify

```bash
# 1. the manifest's own integrity
sha256sum -c SHA256SUMS.txt

# 2. every LFS-tracked file against the platform's published digest
python verify_components.py            # needs network
python verify_components.py --offline  # uses only the local evidence files
```

`verify_components.py` re-reads the HuggingFace Hub API for each pinned
revision and compares the published `lfs.sha256` against the digests in
`MANIFEST.json` and against the locally computed digests recorded in
`LOCAL_SHA256_*.txt`.

## Known caveats, stated up front

- `facebook/sam-audio-large` is a **gated** repository
  (`gated = "manual"`): an anonymous request for its model card returns
  HTTP 401, and the weights require an individual access approval. The
  challenge FAQ acknowledges this because the official baseline uses the
  same model, but it does mean this one component is not unconditionally
  downloadable, and its license text could not be read without an approved
  token. It was used on 19 of 127 samples in the reference run.
- `iic/SenseVoiceSmall` is distributed on ModelScope and has no
  HuggingFace record, so it cannot be cross-checked against the Hub. The
  digests recorded for it are locally computed and pin the bytes that ran.
- The `dots.tts` **code** checkout used at run time carries no `.git`
  directory, so its revision is reconstructed from the upstream release
  that matches the deployed weight revision plus the `pyproject.toml`
  version string. The 45 hashed source files are listed in
  `LOCAL_SHA256_dots_tts_code.txt`.
- "not verified" in the license column means exactly that: the license
  text could not be read from a primary source and is therefore not
  asserted here. It is not a synonym for "permissive".

## Relationship to the official entry

| | Official entry | This directory |
|---|---|---|
| Repository | `jxzhen/aec-2027-editx-lora` | `jxzhen/vibevoice-based_weight/aec2027` |
| Weight carrier | HF mirror + GitHub Release v1.0 | none (pointer only) |
| First public | 2026-09-28 | 2026-11-01 (documentation only) |
| Role | the submission | audit material for a sibling agent project |

## License

MIT for the manifest text and scripts in this directory. The upstream model
licenses apply separately to the weights they cover.

## Contact

Jianxi Zheng - `hunan08182026@126.com`
