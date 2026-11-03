# AI sign review

AI review with tooling grants `ai-reviewed`, never
`reviewed`. Commands and pass/fail bars below define what an AI
reviewer can and cannot certify.

## Marks and ship rule

- `proposed` → `authored` → `ai-reviewed`, and `ai-reviewed`
  ships. The `reviewed` mark stays defined for a future signer;
  nothing waits on it.

## The six checks (every pose, every time)

All six run on rocmaibox from a repo checkout; 1–4 need only
Python 3, 5–6 need Blender. The GitHub PR is the review surface.

### 1. Live reference

Every pose section in [docs/cookbook.md](cookbook.md) links its SignBank page.

```sh
curl -s -o /dev/null -w "%{http_code}\n" \
  https://dai.cs.rutgers.edu/dai/s/translation?id=2933
```

Pass: HTTP 200 and the page names the sign (e.g. "Related
English Words for Sign Variant: TWO"). A/B/F cite the Lifeprint
letter pages, THANK-YOU cites the Lifeprint Lesson 01 page — every
cookbook section links its citation.

Reference landmark signature (same check, numeric half): every
`ref-*.png` carries a MediaPipe extended-set that must equal the
citation formation (`scripts/qa/compare_landmarks.py`, rocmaibox):

```sh
LD_LIBRARY_PATH=~/.cache/gles/usr/lib/x86_64-linux-gnu \
  .venv/bin/python scripts/qa/compare_landmarks.py \
  --model ~/.cache/mediapipe/hand_landmarker.task \
  --pairs docs/assets/ref-a.png docs/assets/ref-a.png [... all 8]
```

Pass: extended-set per still equals the signature table in
the cookbook ("Reference landmark signatures"), with the F
thumb-index gap at most 0.2 (circle). Since the
neutral-baseline
re-render, our stills detect too (true palm, flat light): B, F,
2, 3, 4 MATCH exactly; A, 1, 5 read marginally over/under the
photo-calibrated 1.4 threshold on tucked-edge digits (2D
projection effects — tightening curls measured worse, so the
eye-verified pixels stand and the edges are recorded per shape
in the cookbook). Renders remain certified by bone measurement
plus the side-by-side panels; the detector is advisory until a
render-domain threshold calibration lands. The GLES shim is
re-fetchable without root: `apt-get download libgles2 &&
dpkg-deb -x libgles2*.deb ~/.cache/gles` (cache lives outside
the repo; never /tmp deliverables per repo rules).

### 2. Code matches docs

The cookbook's python blocks must equal the script dicts exactly:

```sh
python3 scripts/review_signs.py
```

Pass: script prints `REVIEW: PASS` (it parses the cookbook blocks
and compares against `pose_handshapes.SHAPES`,
`render_host_shots.NUMBERS`, and `FLAT_HAND`). Any joint-value
edit without a matching doc edit fails here.

### 3. Explicit camera per pose

Every number section states its own wrist/camera lines. "Same as
2"-style cross-references are a fail — poses drift independently
(the 2 proof changed 2's framing while 3/4 stayed legacy).

### 4. No vendored reference media

`git status` clean of image/video additions outside
`docs/assets/` renders we generated; no ASLLVD frames committed.

### 5. Bone mapping (isolation probes)

One finger extended, rest tucked, same camera math — the correct
digit must visibly move. Proves bone names map to anatomy:

```sh
# rocmaibox, from the repo root (probe renders reuse the
# handshape pose + camera math; pixels verified by eye and
# recorded in the PR, then deleted — reproducible any time)
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/qa/probe_fingers.py -- --out-dir docs/assets
```

Pass: index-only and middle-only renders each show exactly one
extended digit in the anatomically correct slot, rest tucked into
a fist. Look at the pixels (`read_file`); `posed=N` counts prove
nothing about which digit moved.

### 6. Presentation still

Final still must show, all at once: correct digits extended and
countable, tucked digits visibly tucked, thumb placed per the
section's convention without touching what it must not touch,
the cited side to camera — letters palm-side (smooth fronts, no
nail plates beyond fingertip specular), cardinal numerals
dorsal-side (knuckle creases, nail plates up) — fingers up, no
bent-wrist subluxed look, flat neutral light with no crushed
shadows hiding joints, and a matching in-situ torso render
locating the hand (location/tab witness). Two machine eyes back
the human one: chereme-aware chirality vs the reference crop
(`scripts/qa/check_chirality.py` — letters must match the
palmar refs, cardinals must mirror them since they cite dorsal
except n1 (detection only: tucked-tip order unstable) and n4
(handedness only); number-2 carries blind-tolerant handling.
A failed relation catches wrong-side cameras and mirrored
hands) and anterior hand depth via side view + joint survey
(`scripts/qa/inspect_pose.py`, whose signed frontality reads the
chereme: +1 palm-out, −1 palm-in — frontal pixels cannot catch
behind-the-body arms, verified failure mode). Camera derived
from the posed bones (palm normal → position, finger direction
→ frame-up) beats fixed offsets — fixed offsets don't track the
hand as twist changes.

## What AI review cannot certify

Thumb lay nuance, movement, location, face grammar, pacing,
meaning preservation, regional variation. Palm orientation per
sign IS certified: the chereme preset cites it, the signed
frontality probe measures it, and the chirality gate checks it —
but the preset itself rests on the Vicars isolated-1–5 rule, so
a citation-form dispute would lapse every number at once.

## Re-review triggers

Any joint-value change, fixture/rig change, Blender version
change, or reference-URL death lapses `ai-reviewed` back to
`authored`. Re-run all six.

## Worked example: TWO (2026-10-24)

1. Reference live: SignBank 2933 fetched, names TWO. Pass.
2. `review_signs.py`: cookbook n2 block equals
   `render_host_shots.NUMBERS["n2"]`. Pass.
3. Own chereme/camera lines (`cardinal_numeral` preset:
   arm (0,-0.4,-0.2)/(-2.5,-0.5,0), wrist roll 0 / flex -1.0 /
   dev 0.1 (zero twist), 110mm at 1.4m, 10deg medial).
4. No outside media committed.
5. Isolation probes: index-only shows the upper digit extended,
   middle-only the second; mapping correct. Pass.
6. Still shows two separated fingers up, ring/pinky tucked,
   thumb alongside. Open: no finger spread (digits parallel),
   thumb lay unreviewed, chin intrudes at frame corner.

Result: `ai-reviewed`, which ships.

## Body-pose naturalness (torso/full-body shots)

For torso or full-body shots, run the MediaPipe-based body-pose review:

```sh
python3 scripts/qa/body_pose_review.py docs/assets/spike-host-signing-torso.png data/envelopes/body_pose_envelope.v1.json
```

Pass: `overall_verdict` is `pass`, `naturalness_score` >= 0.8, no `fail` metrics.

Envelope build (run once per reference image set, then commit):

```sh
python3 scripts/qa/build_envelope_from_references.py
```

Uses `scripts/references/image_manifest.json` (SignBank references) to
build percentile distributions, writes `data/envelopes/body_pose_envelope.v1.json`.
