# Component notes

Machine-readable version: [`MANIFEST.json`](MANIFEST.json).
Everything below was collected first-hand on 2026-11-01 from the HuggingFace
Hub API (`/api/models/<repo>`, `/api/models/<repo>/commits/main`,
`/api/models/<repo>?blobs=true`) and from the deployment host, and can be
re-derived by anyone with the same commands.

## Summary

| Role | Model | Revision | Revision commit (UTC) | Repo created (UTC) | License | Gated |
|---|---|---|---|---|---|---|
| router LLM | `Qwen/Qwen2.5-Omni-3B` | `f75b40e3da2003cdd6e1829b1f420ca70797c34e` | 2025-04-30 | 2025-04-30 | Apache-2.0 | no |
| speech edit | `dots-studio/dots.tts.edit` (V1.1) | `cc4d5d3821577ccf40e7ff0d997161219a16b1c9` | 2026-10-30 | 2026-07-28 | Apache-2.0 | no |
| generative edit | `tencent/AuK` | `790742b71a4430120daf2b2099192abae449eb9f` | 2026-09-10 | 2026-08-18 | MIT | no |
| source separation | `facebook/sam-audio-large` | `5f2cd3a9471a08c7282c06036be6893e18de8b70` | 2025-12-30 | 2025-12-12 | SAM License (Meta) | **manual** |
| ASR inside the AuK route | `iic/SenseVoiceSmall` | *(ModelScope only)* | -- | -- | not asserted | no |
| speed / volume / pitch | numpy, soundfile, ffmpeg | -- | -- | -- | no weights | -- |

Every dated component was released before 2026-11-01. The latest is
`dots.tts.edit` V1.1 at **2026-10-30**, two days inside the cutoff.

## 1. Router LLM -- `Qwen/Qwen2.5-Omni-3B`

- Revision `f75b40e3da2003cdd6e1829b1f420ca70797c34e`, commit
  "upload" dated **2025-04-30T04:01:19Z**. The repo has exactly two commits.
- License: Apache-2.0 (the Hub tag reads `other`; the model card and the
  repository's `LICENSE` file state Apache-2.0).
- Deployed locally on the AutoDL Beijing-B host and served over a loopback
  OpenAI-compatible endpoint (`http://127.0.0.1:8000/v1`). No API key, no
  cloud endpoint. This satisfies Track 2 Rule 2 (an LLM may be served
  locally or through an API as long as the served version corresponds to
  publicly released weights; closed-source LLMs are prohibited).
- 18 deployed files hashed on the host; all 5 LFS-tracked files are
  byte-identical to the digests published for this revision.

## 2. Speech editing -- `dots-studio/dots.tts.edit`

- Revision `cc4d5d3821577ccf40e7ff0d997161219a16b1c9`, commit
  "Release dots.tts.edit V1.1" dated **2026-10-30T12:06:24Z**. The repo has
  exactly two commits: V1.0 at `e2aea9cab95a802a63f1a491702a1cc8bf796b30`
  (2026-08-10) and V1.1.
- License: Apache-2.0. The dots.tts `LICENSE` reads
  "Copyright 2026 dots.tts Team, RedNote"; the dots.tts README states that
  "dots.tts code and released checkpoints are licensed under Apache-2.0".
  The Hub tag reads `other` because the model card delegates the terms to
  the project repository.
- Code: `github.com/studio-dots-ai/dots.tts`. The deployed checkout carries
  no `.git` directory, so the revision is reconstructed from the upstream
  release that matches the deployed weight revision (both
  2026-10-30T12:0x UTC) plus `pyproject.toml` `version = "0.3.1"`. The 45
  hashed source files are listed in `LOCAL_SHA256_dots_tts_code.txt`; the
  digest of that list is
  `d8b00ef490a70c1879b9b2c0335d5d10fc7e006c559749dd80ec8c628e4e51fb`.
  The code bytes are therefore pinned by digest even though the git
  revision label is inferred.
- If a pre-2026-10-01 code revision is ever needed, the correct target is
  **`3cb6f94a5710`** (2026-09-28T13:51:59Z, "docs: announce doteBench V1.0
  release (#54)") -- the last commit before that date. `32407a55`
  (2026-08-17) is its ancestor and is **not** the last pre-cutoff commit;
  an earlier draft of this document named it and was corrected on
  2026-11-01 after a cross-check against the GitHub commits API.
- 15 deployed files hashed on the host; all LFS-tracked files are
  byte-identical to the digests published for this revision.

## 3. Generative editing -- `tencent/AuK`

- Revision `790742b71a4430120daf2b2099192abae449eb9f`, repo created
  **2026-08-18T07:08:36Z**, last modified 2026-09-10. The model's own
  citation block gives a release date of 2026-09-09.
- License: MIT (Hub tag `mit`; a `LICENSE` file is committed in the same
  repository, upload commit `ca50bbd34b28`).
- Deployed locally, served over loopback `http://127.0.0.1:8010`.
- 5 deployed files hashed; both LFS files (`auk_base.safetensors`,
  `vae.safetensors`) are byte-identical to the published digests.

## 4. Source separation -- `facebook/sam-audio-large`

**This is the one component with a caveat, and it is stated plainly.**

- Revision `5f2cd3a9471a08c7282c06036be6893e18de8b70`, repo created
  **2025-12-12T21:24:20Z**, last modified 2025-12-30. The Hub tag
  `arxiv:2512.18099` points at the SAM Audio paper.
- License: the **SAM License** (Meta Platforms), last updated 2025-11-19,
  published at
  <https://raw.githubusercontent.com/facebookresearch/sam-audio/main/LICENSE>.
  It is a custom research license, **not** an OSI-approved open-source
  license. It grants a non-exclusive, worldwide, non-transferable,
  royalty-free limited license to use, reproduce, distribute and modify the
  SAM Materials, and it requires that published research acknowledge the use
  of SAM Materials. Redistribution must follow the same terms. Reverse
  engineering is disallowed. Trade-control clauses apply.
- **Access gate**: the Hub reports `gated = "manual"`. The weights require
  an individual access approval, and an anonymous request for the model
  card at the pinned revision returns **HTTP 401**. The challenge FAQ
  acknowledges exactly this ("Access remains subject to the model
  provider's approval and license terms") because the official baseline also
  uses SAM Audio Large -- so this component is no less available to us than
  to the baseline, but it is not unconditionally downloadable.
- Single LFS file `checkpoint.pt`, 14,861,356,211 bytes, Hub digest
  `ca55418b1d23e8c8a4dcc55f259d9801c8f79da0131a66e525d862c1289e3c4f`.
- **Usage share**: 19 of the 127 samples in the reference run took the
  `separate` route. The remaining 108 took `speech_edit` or a DSP route, so
  a submission that dropped this component would change only those 19
  samples.
- The local copy of these weights was removed from the compute host after
  the reference run (disk pressure); the Hub digest above is therefore the
  authoritative checksum for them.

## 5. ASR inside the AuK route -- `iic/SenseVoiceSmall`

- Distributed on ModelScope (<https://www.modelscope.cn/models/iic/SenseVoiceSmall>);
  the HuggingFace Hub has **no record** for this repo id, so no Hub-side
  digest or release date can be asserted.
- The 7 deployed files were hashed on the host; the digests are in
  `LOCAL_SHA256_SenseVoiceSmall.txt` and pin the exact bytes that ran.
- Its license is **not asserted** here: it could not be read from a primary
  source during this collection. This row is deliberately left as
  "not asserted" rather than guessed.

## Not part of the submitted system

| Role | Model | Revision | Created (UTC) |
|---|---|---|---|
| official judge | `Qwen/Qwen3-Omni-30B-A3B-Instruct` | `26291f793822fb6be9555850f06dfe95f2d7e695` | 2025-09-20 |

Used only to score locally with the unmodified official evaluator
(`python -m eval.score`). It is not a component of the submitted agent.

## Self-trained weights

**None.** This system trains no weights of its own, so there is no
self-trained checkpoint whose publication would have to be scheduled against
the November 1, 2026 deadline. The self-developed part is code:
the router, the DSP tools, the tool-call plumbing, the audio utilities, and
the evaluation harness.

## Official entry (reference only)

| | Value |
|---|---|
| Repository | `jxzhen/aec-2027-editx-lora` |
| HuggingFace | `jxzhen/aec-2027-editx-lora` |
| HF created | 2026-09-28T16:28:59Z |
| HF last modified | 2026-09-30T04:02:15Z |
| GitHub Release v1.0 `published_at` | 2026-09-28T17:11:35Z |
| Base model | `stepfun-ai/Step-Audio-EditX` @ `5fe2f8a05c23...`, repo created 2025-10-29 |
| License | Apache-2.0 |

This is the single official entry. The three side repositories are
supporting material, not competing submissions.
