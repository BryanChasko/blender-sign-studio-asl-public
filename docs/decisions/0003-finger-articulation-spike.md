# Architecture Decision Record (ADR) 0003 — Finger-articulation spike result (GO with tuning)

Date: 2026-10-22 · Status: accepted · Decides ADR 0002 go/no-go

## Decision

GO on 3D signing. The humanoid host rig articulates all 10 fingers and
renders a legible close-up hand still. Exact A/B/F/1/5 handshape angles
need tuning against ASLLVD citation form plus fluent-signer review;
the signing-inset fallback stays available per ADR 0002 but is not the
current path.

## Method (rocmaibox only)

Macmini has no Blender. The spike ran on `rocm-aibox` (Blender 4.4.0)
against the sibling `sumerian-hosts` fixture
`fixtures/hosts/cristine/cristine.glb`, using the rebuildable script
`scripts/spike-finger-articulation/build_hand_proof.py`:

```
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/spike-finger-articulation/build_hand_proof.py -- \
  --host cristine --out docs/assets/spike-finger-v2.png
```

## Findings

One armature, 134 bones. Hand rig per side: wrist, carpal, and
5 fingers x 3 joints (Thumb/Index/Mid/Ring/Pinky A/B/C).

| Side  | Wrist              | Carpal                 | Finger joints posed | Total hand bones |
| ----- | ------------------ | ---------------------- | ------------------- | ---------------- |
| Left  | `char:def_l_wrist` | `char:def_l_fngCarpal` | 15 (5 x A/B/C)      | 17               |
| Right | `char:def_r_wrist` | `char:def_r_fngCarpal` | 15 (5 x A/B/C)      | 17               |
| Both  | —                  | —                      | 30                  | 34               |

Run output: `TOTAL_BONES: 134`, `HAND_BONES: 34`, `POSED_BONES: 30`,
`RENDER_OK docs/assets/spike-finger-v2.png`, `PROOF: PASS`.
Pose values stick (verified `char:def_r_fngIndexA = (0.9, 0.0, 0.0)`).
Render: right hand fully in frame, well-exposed at 640x360 with Blender's EEVEE renderer, no
occlusion. See `docs/assets/spike-finger-v2.png`.

## Handshape drafts v0 (unreviewed, for ASLLVD + reviewer tuning)

Built by `scripts/spike-finger-articulation/pose_handshapes.py`, rendered
on rocmaibox, committed at `docs/assets/spike-hand-{a,b,f,n1,n5}.png`.
Values are flexion amounts (0.0 extended, 1.0 full flex) applied about
local Z, negative toward the palm.

| Shape | Thumb (A/B/C) | Index       | Mid         | Ring        | Pinky       | Render reads as                                                 |
| ----- | ------------- | ----------- | ----------- | ----------- | ----------- | --------------------------------------------------------------- |
| A     | 0.2/0.1/0.1   | 1.0/1.0/0.8 | 1.0/1.0/0.8 | 1.0/1.0/0.8 | 1.0/1.0/0.8 | fist, thumb alongside                                           |
| B     | 0.4/0.2/0.1   | 0.05 x3     | 0.05 x3     | 0.05 x3     | 0.05 x3     | flat hand; thumb-across needs reviewer check (reads close to 5) |
| F     | 0.6/0.5/0.3   | 0.7/0.6/0.4 | 0.05 x3     | 0.05 x3     | 0.05 x3     | thumb-index approximate circle; touching needs tuning           |
| 1     | 0.9/0.7/0.5   | 0.05 x3     | 1.0/1.0/0.8 | 1.0/1.0/0.8 | 1.0/1.0/0.8 | index up, rest tucked                                           |
| 5     | 0.05 x3       | 0.05 x3     | 0.05 x3     | 0.05 x3     | 0.05 x3     | open hand                                                       |

Two rig facts found while proving this, recorded so no one re-derives
them: the imported host carries a `bindpose_offset` action on a
Non-Linear Animation (NLA) strip that overrides pose bones at render
time (the script clears
animation data first), and X is the bone roll axis (0.5 rad moves the
fingertip 2 mm) while local Z negative is the flexion axis (Z-0.9
closed fingertip-to-palm distance from 0.1365 to 0.0546).

Remaining gap, stated plainly: the above are drafts. Per-handshape
tuning for A/B/F/1/5 against ASLLVD multi-angle reference plus
fluent-signer approval is still required before any clip is marked
`reviewed`.

## Consequences

- 3D signing is the v1 path; chereme batches proceed on rocmaibox.
- Macmini validates schema, timing, slugs, and contracts without
  Blender; rocmaibox owns authoring, renders, and segmentation QA.
- Inset fallback stays contracted but unbuilt unless a clip fails
  review (see `docs/asset-licensing.md` for licensed-video terms).
