# Asset pipeline — Meta Image + SAM via Model API

Live-site rule: this repo never edits the site. It produces
assets and procedures the site team pulls in.

## Host icons: provenance gap

The live page's host icons (fiona, cristine, maya, jay,
grace, luke, preston, wes) were built by the site team with
Muse Image edits over live refs. That pipeline is NOT
documented here — no prompts, no seeds, no style spec. Do
not claim otherwise. The icon below proves the public repo
can replicate the style from scratch; the backlog issues
track the rest.

## Replicated: category icon (proof)

`docs/assets/icon-say-hi.webp` — generated 2026-11-06, one
call, first attempt, 105 KB webp:

```
POST https://api.meta.ai/v1/images/generations
Authorization: Bearer $MODEL_API_KEY  # providers.meta.api_key in ~/.config/muse/auth.json
Content-Type: application/json
{"model": "muse-image-1.0",
 "prompt": "flat vector app icon, waving hand, teal background, gold ring border, minimal, no text, kid-friendly signing game UI asset"}
```

Usage: 17838 in / 1622 out. Verdict: on-style (teal, gold
ring, no text). The style lever is adjectives, not pose
control — there is no pose conditioning on this endpoint;
`/v1/images/edits` carries reference images when a pose
must survive.

## Backlog for the site team

- Category icons: DONE 2026-11-06, all seven in
  `docs/assets/icon-*.webp` (say-hi, numbers,
  people-places, spell-it, make-build, quiz, practice).
  Eyeballed: all on-style. One note: make-build drifts
  off-palette (pale-blue wrench, orange block) — one
  regen with "teal and gold only" if the team wants it
  strict. Per-call usage ~10–29k tokens; total under
  150k for the set.
- Caption window skin: DONE 2026-11-06,
  `docs/assets/caption-skin.webp` — dark glass, gold
  border, tail down-left, empty center, no text. Slice
  in CSS.
- Camera/footer treatments: OPEN — preset thumbnails per
  view (signing, face, torso, hands, full body) rendered
  from the rig, not generated. Needs new Blender framings.
- Sprites + webp loops: PROOF DONE 2026-11-06,
  `docs/assets/sign-goodbye-move.webp` — 48 rendered
  frames collapse to 25 distinct (12 rest-hold + 13
  end-hold are byte-identical; encoders dedupe exact
  duplicates). Motion fully covered: 23-frame arc intact.
  `--shot sign-<gloss>-move` now resolves for every gloss
  (auto-registry in render_host_shots.py).
- Shader-layer art: gradient backdrops per shelf (jungle
  set exists on-site; this repo does not author scenes).

## SAM joint labeling: scope and status

SAM 3.1 segments named regions (boxes + masks), not
skeleton keypoints. It cannot return joint angles. Its QA
use is region verification: segment "hand" + "face" on a
citation still, then check containment/overlap numbers
against the claim (e.g. chin contact = hand mask touching
face mask). Procedure:

```
POST https://api.meta.ai/v1/responses
{"model": "sam-3.1", "stream": false,
 "input": [{"role": "user", "content": [
   {"type": "input_text",
    "text": "the signing hand and the face: return one box per object"},
   {"type": "input_image",
    "image_url": "<raw.githubusercontent URL of the still>"}]}]}
```

Status 2026-11-06: `rate_limit_exceeded` on three
attempts — same capacity wall as every prior try.
Verdicts stay author-inspected until a call succeeds; the
rerun is queued, not assumed.
