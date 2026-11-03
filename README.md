# Fiona ASL signs for Sumerian-style hosts

Open American Sign Language sign clips and Blender authoring scripts for
the Fiona female host rig. This is the reproducible signing slice of
the [signing-hosts demo](https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing):
everything needed to pose, render, and export the THANK-YOU sign on
Fiona in Blender, plus the seed lexicon it belongs to.

Upstream build work continues in the private
`sumerian-signing-hosts` repo; this fork holds the files a stranger
needs to redo the signing half, nothing else.

## The rig (not vendored here)

Fiona's mesh is not in this repo. Fetch it yourself from either source:

- Upstream open source: [aws-samples/amazon-sumerian-hosts](https://github.com/aws-samples/amazon-sumerian-hosts)
  at commit `109baefef53cc18ef3e2e340170c44078d011b91`
  (`packages/demos-babylon/.../adult_female/fiona/`), or
- The sibling vendored fixtures: `sumerian-hosts`
  repo, `fixtures/hosts/fiona/fiona.glb`.

Mesh terms: 3d character assets are Creative Commons
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0), original
author Amazon Web Services, Inc. — see `fixtures/LICENSE` and
`fixtures/ATTRIBUTION.md` in the sibling repo. The SDK side is
Apache-2.0. This repo's own files (scripts, angles, docs) are
Apache-2.0 (see LICENSE); signs played on the mesh follow the
mesh terms for combined builds.

## Setup

Blender 5.2 LTS (current long-term support, verified on 5.2.3) or
4.4. Scripts run headless:

```bash
blender -b --factory-startup --python-exit-code 1 -P <script> -- <args>
```

The scripts default to the `cristine` male rig at the sibling
fixtures path. Point `--rig fiona` at the female rig:

```bash
# THANK-YOU citation start still, Fiona
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot signing-torso --rig fiona

# 72-frame movement clip, armature-only .glb for the engine
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/export_sign_clip.py -- \
  --sign thank-you --rig fiona --out out/sign-thank-you-fiona.glb
```

Verified outputs: `RENDER_OK ... posed=36` on the still (right flat
hand at the chin, fingertips at the lips), `CLIP_OK` on the export
(72 frames at 24 fps: rest, chin hold 12-20, forward-down arc,
palm-down end hold 44-52, return). A ready-made export ships as a
release asset (see Releases) since `.glb` files travel through the
asset pipeline, not git.

Every still in `docs/cookbook.md` reproduces the same way —
"Reproducing any pose" has the one-liners. Joint values are baked
into `SIGNS` / `SIGNS_END` in `render_host_shots.py` and the
handshape dicts in `pose_handshapes.py`; Blender 5.x layered
actions are handled by `_all_fcurves` in both files.

## Repo map

```
scripts/blender/   render + clip-export scripts (--rig cristine/fiona)
scripts/spike-finger-articulation/  handshape dicts, single source of truth
data/lexicon/      versioned sign lexicon (v1 reviewed set, v2 in progress)
data/examples/     validated gloss sequence the adapter consumes
docs/              poses, schema, review gate, architecture, licensing, credits
```

## Accuracy bar

Nothing here ships as ASL without passing `docs/ai-review.md`,
and sign correctness is human review (see `docs/reviewer-guide.md`) —
scripts guard the contracts, never substitute for it. Poses cite
Bill Vicars' lessons; a pose that does not match the citation does
not ship. The voice half (banked speech audio, engine sync) lives
with the demo sources, not here.

Live demo: <https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing>
