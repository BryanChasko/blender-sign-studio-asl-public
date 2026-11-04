# Meta models in this repo: active, parked, blocked

Honest map, 2026-11-04. Supersedes the 2026-11-03 edition: the API
key works now, and every active row below ran with committed
evidence. Each row names the exact proof.

## Active (ran, committed)

- Muse Spark (via Muse Code) — gloss drafts; validators gate.
  Proof: `docs/meta-evidence/gloss-draft-spark.json` (GLOSS PASS 4
  tokens), `lint_lexicon.py` LEXICON PASS 58.
- Muse Wonder (via Muse Code) — planning, delegation, verdict
  rubric, evidence review. Proof:
  `docs/meta-evidence/wonder-notes.md`, Wave-3 sign-off in
  `docs/ai-vs-rig/verdicts.md`.
- Muse Image (API) — 5-sign comparison set, demo poster, 2
  round-2 edits (both pass). Proof:
  `docs/ai-vs-rig/prompts.md` (endpoint, prompts, payloads,
  byte counts), images beside it.
- Muse Voice Transcribe (API) — timing audit CONFIRMED: banked
  "thank you" turn 0.140–0.380 s lands inside the gesture
  in-phase. Proof: `docs/meta-evidence/transcribe-audit.md`,
  `transcribe-response-ok.json`.
- SAM 3.1 (API) — hand-segmentation QA attempted on all 10
  images; capacity 429s all day, zero masks. Proof:
  `docs/ai-vs-rig/verdicts.md`, `sam-*.json` (error bodies).
  Rerun queued (issue #3).
- Muse Glimmer (local) — same gloss task on-device; too slow to
  finish, fragment recorded as a limitation. Proof:
  `docs/meta-evidence/gloss-glimmer-raw.json`.
- Ollama vision (local) — render-vs-citation second opinions.
  No committed transcript; advisory only, human reviewer decides.

## Parked (specced, not wired)

- SAM 3 weight-gated swap (needs an approved HuggingFace
  request + token). Offline path unchanged; QA-stats collection
  is the same either way.
- Direct API batch gloss drafting (no agent in the loop). Spark
  drafted once through Muse Code; raw API batching is unspecced.

## Deliberately not Meta

- Voice banking is Amazon Polly neural (Kendra); the demo's voice
  path stays Polly so lip-sync marks match the shipped audio byte
  for byte.
- Landmark detection is MediaPipe (advisory only). Renders are
  certified by bone measurement, never by the detector.
- The host runtime is Amazon Sumerian Hosts (aws-samples
  upstream).

## Hackathon intake

Judging angles this map supports: Build for Your World (ASL
access to host dialogue work), Technical Depth (every shipped
sign carries machine-checkable provenance, not vibes), Demo
(playable clips with speak-while-signing on one clock).
