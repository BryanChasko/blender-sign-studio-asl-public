# Blender Sign Studio (ASL)

Build signing game characters, tutors, VTubers. Base: open
source Amazon Sumerian Hosts SDK, Babylon.js. Contents:
158-sign ASL dictionary (58 validated v1 + 100 v2), 23
reviewed engine clips on the Fiona rig, headless Blender
scripts that rebuild every still and clip.
[Watch it run](https://bryanchasko.com/blender-sign-studio/?host=fiona&shot=signing):
live page, host signing.
[All 23 clips](https://github.com/bryanchasko/blender-sign-studio-asl-public/releases/tag/v0.2-batch5):
finished .glb files. The tutorial builds them below — start
there, skip ahead only to compare.
[Issues](https://github.com/bryanchasko/blender-sign-studio-asl-public/issues):
report breaks, request ports.
Apache-2.0 (code/docs), CC BY-SA 4.0 (meshes).

Status: 23 reviewed clips ship as starting references, not
final ASL. Hand-adjust in Blender or fine-tune
programmatically before calling any sign correct. Breadth is
the win: 158 labeled, close signs as in-Blender references
(58 validated v1 + 100 v2). No starting from scratch.

Method: Muse Code workflows split the work across focused
subagents — renders, lexicon, evidence tables, site — while
the team bakes hero signs upstream. Same pattern scales to
new sign packs.

One host line plays three ways at once: spoken, captioned,
signed. All three share one clock. Path: watch it, play it in
Blender, export one clip.

<img src="docs/assets/live-fiona-face.png" width="760" alt="Fiona on the live signing page: face camera, sign deck with practice rings, lineup strip, transport bar">

The live page: face camera on Fiona, sign deck with practice
rings, lineup strip with up/down/remove, transport with
timeline blocks, quiz mode. Shot 2026-11-05, ?host=fiona&shot=face.

## Requirements

Three things: Blender 5.2 Long Term Support (LTS),
Python 3, a rig file (see Get a rig). Install Blender once:

```bash
mkdir -p ~/opt && cd ~/opt
curl -sSO https://download.blender.org/release/Blender5.2/blender-5.2.3-linux-x64.tar.xz
tar xf blender-5.2.3-linux-x64.tar.xz
ln -sfn ~/opt/blender-5.2.3-linux-x64/blender ~/.local/bin/blender-5.2
blender-5.2 --version   # Blender 5.2.3 LTS
```

The installer creates `~/.local/bin/blender-5.2`. Put it on
PATH (`export PATH="$HOME/.local/bin:$PATH"`), or the Try-it
commands fail with `command not found`.

## Concepts in 60 seconds

| Word          | Meaning                                                             |
| ------------- | ------------------------------------------------------------------- |
| host          | One animated 3D character. Fiona hosts Blender signing here.        |
| gloss         | Written label for one sign, capitals. Example: `THANK-YOU`.         |
| chereme       | One dictionary sign as one short animation. Handshape, place,       |
|               | movement, palm direction baked in.                                  |
| clip          | One exported chereme file (`.glb`, 72 frames at 24 fps). The engine |
|               | plays it.                                                           |
| rig           | Skeleton file the clip is built on. Rigs live outside this repo     |
|               | (see Get a rig).                                                    |
| citation form | The dictionary performance of a sign. Every compared row links      |
|               | its Lifeprint page.                                                 |

- **Kinematics.** A pose is three joint angles per arm
  (shoulder/elbow/wrist, radians) plus a named handshape. All 23
  live in `SIGNS`/`SIGNS_END` in
  `scripts/blender/render_host_shots.py`. Per-gloss values sit in
  [`docs/ai-vs-rig/scorecards.md`](docs/ai-vs-rig/scorecards.md) —
  read it before touching a number.
- **Engine.** Binary glTF (.glb) holds an action: bone angles
  per frame. The engine retargets each clip onto the host
  skeleton. It bakes the clip additive.
- **Meta Model API.** Base URL `https://api.meta.ai/v1` plus a
  `MODEL_API_KEY` from dev.meta.ai. Used here: Muse Image
  (comparison set, poster, round-2 edits), Muse Voice
  Transcribe (turn 0.140–0.380 s lands inside the gesture
  in-phase), Segment Anything Model 3.1 (SAM 3.1) for
  segmentation QA (rate-limited during development, so verdicts
  are inspected, not segmented), Muse Spark
  (gloss drafts via Muse Code). No model runs in production.
  The page serves committed outputs.

A rig is mesh over an armature: bones move, mesh follows.
(Muse Image's idea of one lives in
[`docs/assets/concepts-illustration.webp`](docs/assets/concepts-illustration.webp) —
portrait poster, kept out of this flow.)

## Get a rig

**Option A — upstream open source.** The canonical rigs live in
[aws-samples/amazon-sumerian-hosts](https://github.com/aws-samples/amazon-sumerian-hosts)
at `109baefef53cc18ef3e2e2340170c44078d011b91`, under
`packages/demos-babylon/src/character-assets/characters/adult_female/fiona/`.
Take the whole folder: `.gltf`, its `.bin`, `textures/`.

**Option B — sibling checkout (only if you already work with
both repos).** A checkout of the sibling `sumerian-hosts`
repository keeps the same files at `fixtures/hosts/<id>/<id>.glb`:
`fiona`, `cristine`, `grace`, `maya`, `jay`, `luke`, `preston`,
`wes`, `alien`. Same upstream commit, same license. Use this
option only if that checkout already exists next to this repo;
otherwise use Option A.

**Tell the scripts where the rigs live.** Every script in this
repo resolves a rig through the `RIG_DIR` environment variable
plus a `--rig <id>` flag, as `RIG_DIR/<id>/<id>.glb`. Set it
once per shell:

```bash
export RIG_DIR=/path/to/rig-root
```

Replace `/path/to/rig-root` with the directory that directly
contains the per-rig folders: the `fixtures/hosts` directory
for Option B, or the directory holding your Option A download.
Skip the export and the scripts look next to this repo for a
sibling checkout with fixtures — set `RIG_DIR` to be explicit.
This guide uses `--rig fiona`, which resolves to
`RIG_DIR/fiona/fiona.glb`. Any rig with the same bone names
works with any clip. Rig files are CC BY-SA
4.0 (Amazon Web Services, Inc.). Scripts and docs here are
Apache-2.0. The rig license requires attribution when you ship.

## Try it: THANK-YOU in three commands_T_

Prerequisite: a rig folder from Get a rig above, with `RIG_DIR`
exported so `RIG_DIR/fiona/fiona.glb` exists.

The commands below call a Blender 5.2 Long Term Support (LTS)
binary as `blender-5.2`. Any Blender 5.2 LTS binary works under
any name; adjust the command if yours is named differently. Run
every command from the repo root.

Render the citation still. Run from the repo root:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-thank-you --rig fiona
# RENDER_OK out/spike-sign-thank-you.png posed=36_T_
```

Export the 72-frame engine clip:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/export_sign_clip.py -- \
  --sign thank-you --rig fiona --out out/sign-thank-you-fiona.glb
# CLIP_OK out/sign-thank-you-fiona.glb action=thank-you_T_
```

Play the clip in Blender: open Blender, delete the cube,
import `fiona.glb` via `File > Import > glTF 2.0`, import
`sign-thank-you-fiona.glb` the same way, open a Dope Sheet,
switch it to Action Editor, select Fiona's armature, pick the
`thank-you` action, drag to frame 36, press **Spacebar**.
The full tour with screenshots sits in
[Press play in the Blender window](#press-play-in-the-blender-window)
below.

The first script reports `RENDER_OK` and `posed=36`: 36
bones posed. The second reports `CLIP_OK`: it exported only the
`thank-you` action. Skip the export step: grab ready-made clips
from the
[release assets](https://github.com/bryanchasko/blender-sign-studio-asl-public/releases).
Release files travel through the asset pipeline, never git.

<table>
<tr><th>citation start</th><th>end hold</th></tr>
<tr><td><img src="docs/assets/spike-sign-thank-you.png" width="380" alt="THANK-YOU citation still, start"></td><td><img src="docs/assets/spike-sign-thank-you-end.png" width="380" alt="THANK-YOU citation still, end hold"></td></tr>
</table>

Flat hand at the chin, fingertips at the lips. Forward-down arc
to the palm-down end hold (frames 44–52 of 72). Re-render these
exact pixels any time with the first command above.

## The signs: 158 glosses, 23 reviewed and clipped

![Fiona's five compared signs: hello, thank-you, yes, eight, first](docs/assets/fiona-five-strip.webp)

The lexicons hold 158 glosses: 23 reviewed with engine clips,
the rest proposed ([v1 JSON](data/lexicon/lexicon.v1.json),
[v2 JSON](data/lexicon/lexicon.v2.json)). All 58 v1 glosses
pose in Blender today — 23 reviewed, 35 UNSCORED drafts you
can render, correct in the UI, and promote. The
full per-sign table — reference, Muse Image call, rig still,
clip, verdict — lives in
[`docs/reviewed-signs.md`](docs/reviewed-signs.md).

Signs move — stills are citations. Each loop below is a 48-frame
excerpt at 24 fps rendered by `scripts/blender/render_host_shots.py`
(the engine clip stays 72 frames; the loop excerpts 48). Render
any loop the same way — hello shown here, change only `--shot` for
the other signs — then assemble it:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-hello-move --rig fiona
# RENDER_OK out/sign-hello-move frames=48
ffmpeg -framerate 24 -i out/sign-hello-move/frame_%04d.png \
  -vf scale=480:-1 -loop 0 hello.webp
```

<table>
<tr><th>hello</th><th>thank-you</th><th>yes</th><th>eight</th><th>first</th></tr>
<tr><td><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-hello-move.webp" width="200"></td><td><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-thank-you-move.webp" width="200"></td><td><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-yes-move.webp" width="200"></td><td><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-eight-move.webp" width="200"></td><td><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-first-move.webp" width="200"></td></tr>
</table>

Stance between signs: neutral idle, arms slightly out (left) vs
arms down (right). Rest is part of the idle base pose, built
upstream — these two stills are ported from the upstream repo's
asset batch for reference. Rest-idle export tooling is tracked in
[issue #2](https://github.com/bryanchasko/blender-sign-studio-asl-public/issues/2).

<table>
<tr><th>stand idle rest</th><th>rest arms down</th></tr>
<tr><td><img src="docs/assets/upstream-stand-idle-rest-fiona.png" width="300"></td><td><img src="docs/assets/upstream-rest-arms-down-fiona.png" width="300"></td></tr>
</table>

## Press play in the Blender window_T_

<img src="docs/assets/ui-fiona-viewport.webp" width="760" alt="Fiona in the Blender window: mesh framed in the 3D viewport, armature in the outliner">

Expected window layout: mesh framed in the 3D viewport, armature
listed in the Outliner, timeline along the bottom. Every
screenshot in this section is a committed output of the steps
below — reproduce each one with the same commands on any Linux
box with Blender 5.2.

Build the window file headless (no display needed for this
step). Run from the repo root:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/prepare_ui_blend.py -- \
  --rig <path-to-fiona.glb> --out out/ui-fiona.blend
# window file ready: out/ui-fiona.blend_T_
```

`<path-to-fiona.glb>` is the rig fixture from Get a rig above
(the scripts default to the `RIG_DIR` fixture; pass `--rig
fiona` for this guide's rig). Then open `out/ui-fiona.blend`
in Blender 5.2 on any Linux desktop and work the steps below.

1. Open `out/ui-fiona.blend`. (Without it: open Blender,
   delete the default cube — `X`, then `Enter`.)
2. Import `fiona.glb` via `File > Import > glTF 2.0`. The
   Outliner shows the rig's meshes plus one armature. The
   armature is the skeleton every clip moves. Expected output
   — imported full-body rest:

   ![Fiona imported, full-body rest render](docs/assets/gui-step1-imported.png)

3. Select the armature. Switch to Pose Mode (mode dropdown in
   the viewport header). Rotate a bone. Try the right wrist.
4. Compare the viewport against the citation still in Try it.
   The numbers live in `SIGNS`. The headless commands above set
   exactly this pose. Expected output — citation start pose:

   ![THANK-YOU citation start, same pose as a render](docs/assets/gui-step2-posed.png)

5. Import `sign-thank-you-fiona.glb` the same way (exported to
   `out/` in Try it, or grab it from the
   [release assets](https://github.com/bryanchasko/blender-sign-studio-asl-public/releases)).
   The clip file carries its own armature; ignore it — only
   Fiona's armature drives the mesh. Open a Dope Sheet
   (editor-type selector, top-left icon). Switch it to Action
   Editor. Select Fiona's armature. Pick the `thank-you`
   action. Drag the playhead to frame 36. Expected output —
   action open, frame 36:

   ![The thank-you action on Fiona, frame 36 render](docs/assets/gui-step3-playing.png)

6. Press **Spacebar**. Spacebar plays 72 frames: rest, chin
   hold, forward-down arc, palm-down end hold, return.
7. Tweak: in Pose Mode rotate the right wrist, note the new
   angles, copy them into `SIGNS`, re-run the export. The
   validators re-check the draft.

<img src="docs/assets/ui-fiona-action.webp" width="760" alt="Action open in the Blender window: rest mesh in the viewport, thank-you keys in the Dope Sheet, playhead at 36">

Frame 36 in the window: rest mesh up top, `thank-you` keys in
the Dope Sheet, playhead at 36. The clip poses the mesh only on
the engine's gesture-queue base, so Blender shows the setup
while the render shows the pose.

An animation is an action: bone angles over frames, assigned to
an armature. The headless scripts set steps 4–5 with numbers
instead of mouse drags. Same pose either way.

## How a sign is built_T_

Four parts combine into each sign, like sounds combine into a
spoken word:

- **Handshape** — which fingers extend and how the rest fold.
  A fist with the thumb alongside is A. A flat hand held
  together is B. A thumb-index circle is F. The joint angles
  for each shape live in the handshape table at
  `scripts/spike-finger-articulation/pose_handshapes.py`.
- **Place** — where the sign happens: chin (THANK-YOU), beside
  the forehead (HELLO), chest (YOU), mouth (WHO).
- **Movement** — the path the hand travels: forward-down arc
  (THANK-YOU), pinwheel (HELLO), forward point (YOU).
- **Palm direction** — which way the palm faces. Presets cover
  nearly every case. When a preset looks wrong, open the
  [cookbook](docs/cookbook.md) ("How to read a pose") before
  changing anything.

### The authoring loop

You need three things: a Blender 5.2 install available as
`blender-5.2`, Python 3, and one character rig file (see Get a
rig above; point the scripts at it with the `RIG_DIR`
environment variable and select it with `--rig`). Run every
command from the repo root. Outputs go to `out/`.

1. Write the line as a gloss sequence: one token per sign, in
   sign order. Fingerspell words the lexicon does not have yet:

```json
["YOU", "THANK-YOU", "FINGERSPELL:H-E-L-P"]
```

2. Check that the tokens are legal with the repo's two
   validation scripts:

```bash
python3 scripts/validate_gloss.py data/examples/gloss-demo.json
python3 scripts/lint_lexicon.py
```

The token rules are defined in
[`docs/gloss-schema.md`](docs/gloss-schema.md). Read them
before drafting new entries.

3. Set the pose. Start and end poses for all 58 glosses
   live in the `SIGNS` and `SIGNS_END` tables in
   `scripts/blender/render_host_shots.py` — 23 reviewed, 35
   UNSCORED drafts. The
   [cookbook](docs/cookbook.md) shows worked pose examples, so
   start there when a pose looks off. Edit the numbers in those
   tables, then drop the DRAFT tag once the still matches its
   citation.

4. Render a still and compare it against the dictionary
   reference for that sign (each reviewed row in
   [`docs/reviewed-signs.md`](docs/reviewed-signs.md) links its
   reference):

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-thank-you --rig fiona
# RENDER_OK out/spike-sign-thank-you.png posed=36_T_
```

5. Export the 72-frame clip once the still matches the
   reference:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/export_sign_clip.py -- \
  --sign thank-you --rig fiona --out out/sign-thank-you-fiona.glb
# CLIP_OK out/sign-thank-you-fiona.glb action=thank-you_T_
```

To watch the clip, import the rig file and the exported clip
into Blender, open a Dope Sheet in Action Editor mode,
select the character's armature, pick the `thank-you`
action, and press Spacebar.

6. Submit the clip for review before calling it correct. The
   bar is defined in [`docs/ai-review.md`](docs/ai-review.md):
   every clip labeled as a real sign must pass review against
   its dictionary reference. You may propose any lexicon entry,
   but never improvise a sign and never label a generic gesture
   as a real sign.

At runtime the engine needs nothing new. Each sign is one short
clip on the same skeleton. It queues in/hold/out beside the
gesture queue. It runs on the same clock as banked audio and
visemes.

## Docs route map

- [`docs/architecture.md`](docs/architecture.md) — pipeline and host foundations, so speech, captions, and signs share one clock in your head.
- [`docs/cookbook.md`](docs/cookbook.md) — joint values and code samples, so you author exact poses.
- [`docs/gloss-schema.md`](docs/gloss-schema.md) — token rules, so entries validate.
- [`docs/asl-gloss-core-rules.md`](docs/asl-gloss-core-rules.md) — plain-language gloss primer, so lines stay legal.
- [`docs/ai-review.md`](docs/ai-review.md) — the review gate, so you know the bar before starting.
- [`docs/reviewer-guide.md`](docs/reviewer-guide.md) — signer path, so a fluent signer can join review.
- [`docs/reviewed-signs.md`](docs/reviewed-signs.md) — full per-sign table, so every verdict stays inspectable.
- [`docs/roadmap.md`](docs/roadmap.md) — build plan, so you see what is done and next.
- [`docs/decisions/`](docs/decisions/) — architecture records, so choices stay learnable.
- [`docs/credits.md`](docs/credits.md) — reference attribution, so sources stay cited.
- [`docs/lexicon.md`](docs/lexicon.md) — the v1 seed list, so you pick a real gloss (machine-readable truth: `data/lexicon/lexicon.v1.json`).
- [`docs/asset-licensing.md`](docs/asset-licensing.md) — dataset and asset terms, so you stay legal.
- [`docs/ai-vs-rig/scorecards.md`](docs/ai-vs-rig/scorecards.md) — per-gloss rig values, so you never hand-tune blind.
- [`docs/game-ui-scorecard.md`](docs/game-ui-scorecard.md) — 12-row UI rubric, so your game screen stays playable.
- [`docs/screenshot-rounds.md`](docs/screenshot-rounds.md) — four pixel-graded sign feedback rounds, so verdicts stay honest.
- [`docs/asset-pipeline.md`](docs/asset-pipeline.md) — Meta Image + SAM procedures and the icon backlog, so site art stays reproducible.

## Built with Meta

Every row ran while building this project. The table links the
evidence. The reproducible core stays the headless scripts:
same numbers in, same pixels out. No model renders a frame. The
page serves banked audio and prebuilt clips. Nothing bills per
request.

| Model                       | What it did here                                                                                                                           | Evidence                                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Muse Spark (via Muse Code)  | orchestration; drafted the gloss for "Hello! Yes, thank-you for coming." — validators pass (GLOSS PASS 20 tokens, LEXICON PASS 58 entries) | [`gloss-draft.md`](docs/meta-evidence/gloss-draft.md), [`gloss-draft-spark.json`](docs/meta-evidence/gloss-draft-spark.json) |
| Muse Wonder (via Muse Code) | planned the work, set the verdict rubric, reviewed every evidence table                                                                    | [`wonder-notes.md`](docs/meta-evidence/wonder-notes.md), [`verdicts.md`](docs/ai-vs-rig/verdicts.md)                         |
| Muse Image (API)            | 5-sign comparison set (prompts + payloads verbatim), demo poster, round-2 edits (both pass), round-3 (hello fixed, eight resists)          | [`prompts.md`](docs/ai-vs-rig/prompts.md), [`demo-poster.webp`](docs/assets/demo-poster.webp)                                |
| Muse Voice Transcribe (API) | timing audit: banked "thank you" turn 0.140–0.380 s inside the gesture in-phase                                                            | [`transcribe-audit.md`](docs/meta-evidence/transcribe-audit.md)                                                              |
| SAM 3.1 (API)               | hand-segmentation QA on all 10 images; capacity 429s, zero masks — verdicts inspected, rerun queued                                        | [`verdicts.md`](docs/ai-vs-rig/verdicts.md)                                                                                  |
| Muse Glimmer (local)        | same gloss task on-device; too slow to finish (fragment recorded as a limitation)                                                          | [`gloss-glimmer-raw.json`](docs/meta-evidence/gloss-glimmer-raw.json)                                                        |
| Muse Code                   | the agent that wrote it all                                                                                                                | commit history                                                                                                               |

### Demo 1 — Muse Spark drafts gloss, validators gate it

A gloss is one written token per sign, in ASL order — the
script the engine bakes into clips. Spark read the English
line and proposed the token sequence. The validators decide:
every token must exist in the lexicon. The model proposes,
the validators dispose.

Run the validators on the committed draft:

```bash
python3 scripts/validate_gloss.py docs/meta-evidence/gloss-draft-spark.json
# GLOSS PASS: 20 tokens across 1 files, 0 failures (ship=False)
python3 scripts/lint_lexicon.py
# LEXICON PASS: 58 entries, 0 failures
```

The draft lives in
[`gloss-draft-spark.json`](docs/meta-evidence/gloss-draft-spark.json)
(`HELLO YES THANK-YOU C-O-M-I-N-G` for "Hello! Yes, thank-you for
coming."). The model proposes. The validators dispose.

### Demo 2 — Muse Wonder plans, the rubric reviews

Read the plan, delegation, and verdict rubric in
[`wonder-notes.md`](docs/meta-evidence/wonder-notes.md) — it
decided what counts as a PASS. The sign-off sits in
[`verdicts.md`](docs/ai-vs-rig/verdicts.md).

### Demos 3–6 — hosted calls, one key

One key (`MODEL_API_KEY`). Same base URL:
`https://api.meta.ai/v1`. Get a key at dev.meta.ai: sign up,
open API keys, create one, then `export MODEL_API_KEY=...`.
Outputs are committed above. Rerun a call only when you change
its inputs.

The Image column below is the foil, never the reference.
Each side is judged against the Lifeprint citation first.

Right hand, wrong sign: the AI failures are chereme errors
(palm, handshape), none anatomical. Segment Anything Model 3.1
(SAM 3.1) masks rate-limited out, so these verdicts are
inspected, not segmented.

Second and third attempts: the bare gloss prompt failed
THANK-YOU, HELLO, and EIGHT. The pose knowledge went in with the
image. THANK-YOU and HELLO pass corrected. EIGHT fails twice:
the model cannot close the middle-to-thumb circle. No
ControlNet-style pose conditioning exists on the Meta Model API.
The edits endpoint is the lever, and it has a limit. There is no
video generation endpoint on the Meta Model API (video is
input-only). Motion
still comes from the Blender pipeline. Full calls in
[`docs/ai-vs-rig/prompts.md`](docs/ai-vs-rig/prompts.md),
verdicts in
[`docs/ai-vs-rig/verdicts.md`](docs/ai-vs-rig/verdicts.md).

<table>
<tr><th>fix thank-you: PASS</th><th>photoreal rig still: PASS</th><th>fix hello: PASS</th><th>fix eight: FAIL ×2</th></tr>
<tr><td><img src="docs/ai-vs-rig/edit-thank-you-fix-ai.webp" width="220"></td><td><img src="docs/ai-vs-rig/edit-thank-you-from-rig.webp" width="220"></td><td><img src="docs/ai-vs-rig/edit-hello-fix-ai.webp" width="220"></td><td><img src="docs/ai-vs-rig/edit-eight-fix-ai2.webp" width="220"></td></tr>
</table>

#### Demo 3 — Muse Image generates (exact comparison call)

This call made the comparison set. [`prompts.md`](docs/ai-vs-rig/prompts.md)
logs model and prompt. It does not log size and aspect, so
exact pixels may differ. Run from the repo root:

```bash
curl -X POST "https://api.meta.ai/v1/images/generations" \
  -H "Authorization: Bearer $MODEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"muse-image-1.0",
       "prompt":"photorealistic adult woman signing ASL THANK-YOU, hands clearly visible, neutral background"}' \
  -o img.json
python3 -c "import json,base64;open('img.webp','wb').write(base64.b64decode(json.load(open('img.json'))['data'][0]['b64_json']))"
# img.webp — 1280x1920
```

#### Demo 4 — Muse Image edits with a reference (exact round-2 call — the one that fixed the palm)

Convert the source first (the repo stores webp). Run from the
repo root:

```bash
ffmpeg -y -i docs/ai-vs-rig/ai-thank-you.webp edit-ai-input.png
curl -X POST "https://api.meta.ai/v1/images/edits" \
  -H "Authorization: Bearer $MODEL_API_KEY" \
  -F 'model=muse-image-1.0' \
  -F 'image=@edit-ai-input.png' \
  -F 'prompt=Keep the same woman, framing and neutral background. Fix
      only her signing hand: flat hand at the chin, fingertips touching
      the chin, palm facing toward her, the ASL sign for thank-you.' \
  -o edit.json
python3 -c "import json,base64;open('edit.webp','wb').write(base64.b64decode(json.load(open('edit.json'))['data'][0]['b64_json']))"
# edit.webp — palm corrected, rest intact
```

#### Demo 4b — Fingerspelling stress test (same model, nine words)

Nine words, one frame each, same prompt shape with the word
swapped in. Read every image below as labeled AI slop: only
MUSE and SUMERIAN pass, WONDERFUL is unscored, the other six
fail (wrong hands, an extra limb, burned-in text). The rig sets the standard here, never the
model. These failures are why this repo builds programmatic 3D
references first: pose references (ControlNet-style
conditioning, which the Model API lacks) are the future lever
that could make image models stop failing signs. Full calls and
per-word verdicts in
[`docs/ai-vs-rig/fingerspell.md`](docs/ai-vs-rig/fingerspell.md):

![Nine fingerspelling attempts: amazon, sumerian, hosts, meta, wonderful, glimmer, model, api, muse](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/fp-grid.webp)

#### Demo 5 — Transcribe times the turn (`ENDPOINTING` returns turns; `PUSH_TO_TALK` returns none)

Run from the repo root:

```bash
curl -X POST "https://api.meta.ai/v1/asr/transcribe" \
  -H "Authorization: Bearer $MODEL_API_KEY" \
  -H "Accept: application/json" \
  -F 'request={"model":"muse-voice-transcribe-1.0","audioEncoding":"WAV","mode":"ENDPOINTING"};type=application/json' \
  -F "audio=@docs/meta-evidence/thank-you.wav;type=audio/wav"
# {"transcript":"Thank you","audioDurationMs":880,
#  "turns":[{"turnId":0,"startMs":140,"endMs":380,...}]}
```

#### Demo 6 — SAM segments hands (expect 429s until capacity recovers — every attempt here did)

```bash
curl -X POST "https://api.meta.ai/v1/responses" \
  -H "Authorization: Bearer $MODEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"sam-3.1","stream":false,
       "input":[{"role":"user","content":[
         {"type":"input_text","text":"hands"},
         {"type":"input_image","image_url":"https://raw.githubusercontent.com/bryanchasko/blender-sign-studio-asl-public/main/docs/ai-vs-rig/cmp/cmp-yes-ai.webp"}]}]}'
# masks arrive as <|box;...|> + <|mask;...|> tokens in output_text
```

### Demo 7 — Glimmer and Ollama run local

- **An open-weights model on your own hardware** (Glimmer 30B,
  self-hosted behind an OpenAI-compatible endpoint — the attempt
  here ran at `http://127.0.0.1:8181/v1` on a workstation-class
  GPU): asked to score EIGHT (rig vs AI) from the citation. A
  40-token reply returns 200 with the verdict still in
  reasoning; the full reply times out past 280 s under GPU
  contention; a 387 KB image payload returns nothing in 180 s.
  Text works, vision hangs, long answers starve. Send it the
  same requests the API takes. Keep the validators as the gate,
  not the model's word. Attempt log:
  [`glimmer-verdict-attempt.md`](docs/meta-evidence/glimmer-verdict-attempt.md).
- **A vision model for second opinions** (we used Ollama vision
  models for render-vs-citation checks): install Ollama, the
  free local model runner, from [ollama.com](https://ollama.com).
  Pull a vision model. Show it the render next to the citation
  still. Ask what differs. It catches pose drift a tired eye
  misses. The human reviewer still decides.

(Muse Code drives all of this — see Demo 8. Muse Spark via API is the
same model without the agent loop.)

### Demo 8 — Muse Code drives, bridge inspects

Install the agent on any Mac or Linux box:

```bash
curl -fsSL https://dev.meta.ai/install.sh | sh
```

Then run `muse` in the project folder and sign in.
Non-interactive use takes `MODEL_API_KEY` instead.

The `blender-mcp` bridge (v1.29.1 answered here) exposes the open
Blender file as tools over the Model Context Protocol (MCP).
Replicate it: open your `.blend` in a Blender with the MCP addon
enabled and connected. It listens on `127.0.0.1:8190/mcp`.
Every call below is read-only. The bridge answers about whatever
file that Blender has open.

Run the handshake. It returns a session id. A real reply looks
like this:

```bash
curl -X POST http://127.0.0.1:8190/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize",
       "params":{"protocolVersion":"2025-06-18","capabilities":{},
       "clientInfo":{"name":"my-probe","version":"0.1"}}}'
# 200, serverInfo: {"name":"blender-mcp","version":"1.29.1"},
# header mcp-session-id: <SID>
```

List tools, then ask what is in the scene:

```bash
curl -X POST http://127.0.0.1:8190/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <SID>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
# tools include: get_objects_summary, get_object_detail_summary,
# render_viewport_to_path, search_api_docs, execute_blender_code ...

curl -X POST http://127.0.0.1:8190/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <SID>" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call",
       "params":{"name":"get_objects_summary","arguments":{}}}'
# {"status":"ok","scene_name":"Scene","active_object":"Cube",
#  "collections":[{"name":"Scene Collection", ...,"objects":
#   [{"name":"Camera","type":"CAMERA",...},
#    {"name":"Cube","type":"MESH",...},
#    {"name":"Light","type":"LIGHT",...}] ...}]}
```

That reply came from a default scene. Open Fiona's file in the
bridged Blender. Rerun the same call. It lists her mesh,
armature, and bones. `get_object_detail_summary` drills into one
bone. `render_viewport_to_path` snapshots the viewport. Both skip
the headless scripts.

Watch it run: <https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing>
