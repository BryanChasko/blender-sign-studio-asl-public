# Spike: finger articulation proof (rocmaibox only)

Day-1 spike for architecture decision records (ADRs) 0002/0003. Macmini has no Blender; everything here
runs on rocmaibox (`rocm-aibox`, Blender 4.4.0) against the sibling
`sumerian-hosts` fixtures. Nothing in this directory writes to `/tmp`;
renders go to the asset pipeline or `docs/assets/`.

## Run

```sh
# from the repo root, on rocmaibox:
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/spike-finger-articulation/build_hand_proof.py -- \
  --host cristine --out docs/assets/spike-finger-v2.png
```

Expected output tail:

```
TOTAL_BONES: 134
HAND_BONES: 34
POSED_BONES: 30
RENDER_OK docs/assets/spike-finger-v2.png
PROOF: PASS posed=30 hand_bones=34
```

`POSED_BONES: 30` is 5 fingers x 3 joints x 2 hands. `HAND_BONES: 34`
adds left/right wrist plus carpal bones.

## What it proves

The humanoid rig articulates all 10 fingers and renders a legible
close-up hand still. Exact A/B/F/1/5 handshape angles still need tuning
against ASLLVD citation form plus fluent-signer review; see
`docs/decisions/0003-finger-articulation-spike.md`.

## Macmini side (no Blender)

Macmini validates everything except renders: lexicon lint, ASL Gloss
validation against `data/examples/gloss-demo.json`, timing checks,
category-slug checks. Rocmaibox owns authoring, renders, and
segmentation QA and returns `authored` or `qa-passed` per clip.
