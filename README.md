# Fiona ASL signs for Sumerian-style hosts

Blender scripts and open ASL clips reproducing the
[signing-hosts demo](https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing)'s
Fiona THANK-YOU sign, plus its seed lexicon.

Build continues in private `sumerian-signing-hosts`; this fork
keeps signing-half files only.

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

Verified outputs: `RENDER_OK ... posed=36` on the still,
`CLIP_OK` on the export (frame table in
`docs/cookbook.md` "Runtime playback"). A ready-made export ships
as a release asset (see Releases) since `.glb` files travel
through the asset pipeline, not git.

![THANK-YOU citation start](docs/assets/spike-sign-thank-you.png)
![THANK-YOU end hold](docs/assets/spike-sign-thank-you-end.png)

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

Ship rule and review gate: [`docs/ai-review.md`](docs/ai-review.md).
Poses cite Bill Vicars' lessons; a pose that does not match the
citation does not ship. The voice half (banked speech audio,
engine sync) lives with the demo sources, not here.

Live demo: <https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing>
