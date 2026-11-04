# Wonder planning notes (Meta Global AI Developer Hackathon entry)

Planned under Muse Wonder Full via Muse Code. Wonder owns planning,
delegation structure, and the evidence rubric below; Spark (also via Muse
Code) authors implementation tasks such as gloss drafts. The Meta Model API
is used only for the non-conversation models: Muse Image, Muse Voice
Transcribe, SAM 3.1.

## Verdict rubric (applied to every sign in docs/ai-vs-rig/)

- Visible finger count correct for the lexicon handshape (B hand = 4 extended
  fingers + thumb placement; S fist = 0 extended).
- Handshape matches the lexicon `notes` + `SIGNS`/`SIGNS_END` pose spec.
- Anatomically possible (no extra joints, no fused/displaced digits).
- One line per sign: PASS or FAIL with the failing dimension named.

## Wave 0 findings (locked)

- Lexicon v1 has no handshape/location/movement fields; formation lives in
  `notes` prose + the `SIGNS`/`SIGNS_END` dict in
  `scripts/blender/render_host_shots.py`.
- Per-sign timing is the shared 72f@24fps layout in `export_sign_clip.py`
  (f1 rest, f12-20 citation hold, f20-44 arc, f44-52 end hold, f52-72
  return); envelopes are population stats, not phase windows.
- PLEASE and SORRY are `proposed` (no pose, clip, or stills) and stay out of
  the comparison. Replacement rule: thank-you, hello, yes, plus the first two
  alphabetically by gloss among v1 entries with status ai-reviewed, a
  non-null clip, and an existing `docs/assets/spike-sign-<slug>.png`.
- SAM 3.1: POST `https://api.meta.ai/v1/responses`, model `sam-3.1`,
  `input_image` with public `image_url` (or Files API `POST /v1/files`
  ID reuse), `input_text` concept noun phrase, geometry tokens
  `<|box;...|>` + `<|mask;...|>` in `output_text`.
- Voice Transcribe: POST `https://api.meta.ai/v1/asr/transcribe`
  (multipart `request` JSON + `audio`), model `muse-voice-transcribe-1.0`,
  WAV input, turn-level timestamps only (no word-level), 10-min / 32 MB max.
- Upstream drift (read-only scan): private `sumerian-signing-hosts`
  origin/main is ahead (rest-arms-down PRs #107-109, 4-file diff:
  2 batch9 pngs, `export_rest_clip.py`, `verify_sign_clip_bake.py`).
  Filed as public-fork issues at publish time; private tree untouched.

## Spend log

| Wave     | Calls                                                                              | Running total    |
| -------- | ---------------------------------------------------------------------------------- | ---------------- |
| 1 (done) | 6 image calls (5 gens + 1 probe), gloss drafts (no API cost)                       | 6 paid calls     |
| 2 (done) | transcribe fixed + CONFIRMED (4 calls: 2 shape-400, 2 ok); SAM blocked (see below) | 4 transcribe     |
| 3 (done) | 1 poster image + 1 clean SAM probe (429) + README gallery/table                    | 1 image, 0 masks |

Actuals. Image: 6 (Wave 1) + 1 poster = 7 generations. Transcribe: 4
calls, 2 transcripts. SAM: ~23 first-pass + ~121 paced rerun attempts

- 2 owner probes, every one HTTP 429 rate_limit_exceeded, 0 masks —
  no further SAM attempts today; error responses carry no usage charge.
  Total paid-content calls: 7 image + 2 transcripts. Wonder/Spark ran on
  the Muse Code route at no API cost.

Hard stop at ~14 paid calls. Wonder/Spark via Muse Code consume no API
credits. Retries: max one per sign/image call, then the gap is recorded.
