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

- Category icons: numbers, people-places, spell-it,
  make-build, quiz, practice — same style string, swap the
  subject noun. One call each, eyeball each.
- Caption window skin: dark glass bubble, gold border,
  comic tail — generate as a 9-patch-style backdrop, slice
  in CSS.
- Camera/footer treatments: preset thumbnails per view
  (signing, face, torso, hands, full body) rendered from
  the rig, not generated.
- Sprites + webp loops: 24 fps move excerpts, 480px wide,
  same ffmpeg line as the five compared loops in the README.
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

Status 2026-11-06: `rate_limit_exceeded` on two attempts
(an hour apart) — same capacity wall as every prior try.
Verdicts stay author-inspected until a call succeeds; the
rerun is queued, not assumed.
