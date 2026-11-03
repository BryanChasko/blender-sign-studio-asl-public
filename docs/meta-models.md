# Meta models in this pipeline: active, parked, blocked

Honest map, 2026-11-03. Nothing here claims an integration that does not
exist; each row names the exact script, doc, or issue that proves it.

## Active today (in the loop on every batch)

- Muse Spark (Meta, via this coding session) is the AI reviewer of
  record. docs/ai-review.md defines what "an AI reviewer with tooling"
  can and cannot certify; every ai-reviewed entry in
  data/lexicon/lexicon.v1.json carries reviewer ai-review-pipeline and a
  notes field recording the exact evidence (sweep numbers, BAKE_OK,
  world-space proofs, still names). Batches 1/2/5 (23/58 glosses) were
  authored and reviewed this way: model reasoning + deterministic local
  gates (lint_lexicon, validate_gloss, review_signs, Blender bakes),
  never model assertion alone.
- SAM 2.1 open weights, local, for hand-segmentation QA
  (scripts/qa/sam_segment.py, scripts/qa/sam_demo_app.py). SAM 2.1 is a
  Meta architecture run fully offline; no API key involved.

## Parked (specced, not wired)

- SAM 3 text prompts ("the signing right hand") in sam_demo_app.py: the
  text box is parked until the license-gated facebook/sam3 weights land
  (needs an approved HuggingFace request + HF_TOKEN). Drop-in when
  access arrives; QA stats collection is unchanged.
- docs/roadmap.md and docs/architecture.md already name the SAM 3 swap
  as the segmentation upgrade path.

## Blocked (needs a working Meta Model API key)

- Issue #72 (meta model mapping): the key on hand returns
  invalid_api_key, so nothing below has run yet.
- SAM 3.1 via API for clip-acceptance segmentation (replaces the local
  SAM 2.1 path with the hosted model).
- Muse Voice Transcribe for speak-while-signing timing QA: score
  banked Polly audio against performed signing instead of trusting the
  fixed hold-ms values in the demo.
- Muse Spark via API for batch gloss drafting (formation notes from
  Lifeprint citations) with the local gates as the approver, same as
  today but without a human in the typing loop.

## Deliberately not Meta

- Voice banking is Amazon Polly neural (Kendra); the demo's voice path
  stays Polly so lip-sync marks match the shipped audio byte for byte.
- Landmark detection is MediaPipe (advisory only, per ai-review).
  Renders are certified by bone measurement, never by the detector.
- The host runtime is Amazon Sumerian hosts (aws-samples upstream).

## Hackathon intake

- The demo's "improve this sign" button opens a prefilled
  [sign-feedback] issue (uploads ride along: kinematic datapoints,
  mocap stills, short video). That issue queue is the future training
  and eval set for the blocked rows above: real performer feedback
  paired with the exact clip, host, and demo version that produced it.
- Judging angles this map supports: Build for Your World (ASL access
  to cloud-native vocabulary work), Technical Depth (every shipped sign
  carries machine-checkable provenance, not vibes), Demo (live 23-sign
  playable demo with speak-while-signing).
