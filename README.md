# Extending Amazon Sumerian Hosts with American Sign Language

You reproduce 23 American Sign Language signs as engine clips,
starting with Fiona.
[Watch it run](https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing):
the live page plays the host signing.
[All 23 clips](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/tag/v0.2-batch5):
every .glb, no Blender needed.
[Issues](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/issues):
report a break, request a port.
Apache-2.0 (code/docs), CC BY-SA 4.0 (meshes).

![Fiona signs THANK-YOU, looped](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-thank-you-move.webp)

## Requirements

You need three things: Blender 5.2 Long Term Support (LTS),
Python 3, and a rig file (see Get a rig). Install Blender once:

```bash
mkdir -p ~/opt && cd ~/opt
curl -sSO https://download.blender.org/release/Blender5.2/blender-5.2.3-linux-x64.tar.xz
tar xf blender-5.2.3-linux-x64.tar.xz
ln -sfn ~/opt/blender-5.2.3-linux-x64/blender ~/.local/bin/blender-5.2
blender-5.2 --version   # Blender 5.2.3 LTS
```

The installer creates `~/.local/bin/blender-5.2`.

## Concepts in 60 seconds

- **ASL.** Cheremes: handshape, place, movement, palm direction.
  Meaningless parts combine into signs, like phonemes in speech.
  Gloss: one token per sign, ASL order
  (`["YOU","THANK-YOU","FINGERSPELL:H-E-L-P"]`). Citation form:
  the dictionary performance of a sign. Every row below links
  its Lifeprint page.
- **Kinematics.** A pose is three joint angles per arm
  (shoulder/elbow/wrist, radians) plus a named handshape. All 23
  live in `SIGNS`/`SIGNS_END` in
  `scripts/blender/render_host_shots.py`. Per-gloss values sit in
  [`docs/ai-vs-rig/scorecards.md`](docs/ai-vs-rig/scorecards.md) —
  read it before touching a number.
- **3D files.** The rig is GL Transmission Format (glTF): mesh
  plus armature. One clip is a binary glTF (.glb) file: an
  action, or bone angles per frame. The engine retargets each
  clip onto the host skeleton. It bakes the clip additive. It
  queues in/hold/out beside the gesture queue.
- **Meta Model API.** Base URL `https://api.meta.ai/v1` plus a
  `MODEL_API_KEY` from dev.meta.ai. Used here: Muse Image
  (comparison set, poster, round-2 edits), Muse Voice
  Transcribe (turn 0.140–0.380 s lands inside the gesture
  in-phase), Segment Anything Model 3.1 (SAM 3.1) for
  segmentation QA (capacity-blocked all day), Muse Spark
  (gloss drafts via Muse Code). No model runs in production.
  The page serves committed outputs.

## Get a rig

**Option A — upstream open source.** The canonical rigs live in
[aws-samples/amazon-sumerian-hosts](https://github.com/aws-samples/amazon-sumerian-hosts)
at `109baefef53cc18ef3e2e2340170c44078d011b91`, under
`packages/demos-babylon/src/character-assets/characters/adult_female/fiona/`.
Take the whole folder: `.gltf`, its `.bin`, `textures/`.

**Option B — vendored fixtures.** The sibling `sumerian-hosts`
repository keeps the same files at `fixtures/hosts/<id>/<id>.glb`:
`fiona`, `cristine`, `grace`, `maya`, `jay`, `luke`, `preston`,
`wes`, `alien`. Same upstream commit, same license.

Scripts default to the sibling fixtures path. Pass `--rig fiona`
for this guide's rig. You can use any rig with the same bone
names. Same skeleton, same names. Character files are CC BY-SA
4.0 (Amazon Web Services, Inc.). Scripts and docs here are
Apache-2.0. You must keep the attribution if you ship.

## Try it: THANK-YOU in three commands

You need the rig file from Get a rig above. Run every command
with `blender-5.2` from Requirements. A system `blender` is
usually the wrong version.

You render the citation still:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-thank-you --rig fiona
# RENDER_OK out/spike-sign-thank-you.png posed=36
```

You export the 72-frame engine clip:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/export_sign_clip.py -- \
  --sign thank-you --rig fiona --out out/sign-thank-you-fiona.glb
# CLIP_OK out/sign-thank-you-fiona.glb action=thank-you
```

You play the clip in Blender: open Blender, delete the cube,
import `fiona.glb` via `File > Import > glTF 2.0`, import
`sign-thank-you-fiona.glb` the same way, open a Dope Sheet,
switch it to Action Editor, select Fiona's armature, pick the
`thank-you` action, drag to frame 36, press **Spacebar**.
The full tour with screenshots sits in
[Open Fiona in Blender and press play](#open-fiona-in-blender-and-press-play)
below.

The first script reports `RENDER_OK` and `posed=36`: you posed
36 bones. The second reports `CLIP_OK`: it exported only the
`thank-you` action. Skip the export step: grab ready-made clips
from the
[release assets](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases).
Release files travel through the asset pipeline, never git.

![THANK-YOU citation still, start](docs/assets/spike-sign-thank-you.png)
![THANK-YOU citation still, end hold](docs/assets/spike-sign-thank-you-end.png)

Flat hand at the chin, fingertips at the lips. Forward-down arc
to the palm-down end hold (frames 44–52 of 72).

## The 23 signs

This fork ships 23 ai-reviewed signs with engine clips (23
of 58 v1 glosses). Upstream tracks more: 25 ai-reviewed on
main, and a greetings bake is in flight. Track it in
[issue #2](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/issues/2),
the upstream port queue.

Five signs carry the full comparison: human reference, Muse
Image output with its exact prompt, the rig still, and a
verdict. The table judges each side against the reference
first.

Reference photos: [ASL University /
Lifeprint](https://www.lifeprint.com/asl101) (© William G.
Vicars), mirrored to our Amazon Simple Storage Service (S3)
bucket so the page never scrapes them. Per-gloss kinematics
and both-sides scoring live in
[`docs/ai-vs-rig/scorecards.md`](docs/ai-vs-rig/scorecards.md) —
read it before disputing a verdict.

| sign      | real world                                                                                                                                                                                                  | Muse Image                                                                                                                                                                                                                                                                                                                                                                                    | Fiona                                                            | clip                                                                                                                                        | verdict                                                                                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| HELLO     | [no fixed form — any wave](https://www.lifeprint.com/asl101/pages-signs/h/hello.htm)                                                                                                                        | <img src="docs/ai-vs-rig/cmp/cmp-hello-ai.webp" width="220"><details><summary>prompt</summary>sent: POST /v1/images/generations, model muse-image-1.0<br>prompt: photorealistic adult woman signing ASL HELLO, hands clearly visible, neutral background<br>received: 1280x1920 webp, 267572 B, s3://bryanchasko-amazon-sumerian-hosts-asl-webp/ai-vs-rig/ai-hello.webp</details>             | <img src="docs/ai-vs-rig/cmp/cmp-hello-rig.png" width="220">     | [sign-hello-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-hello-fiona.glb)         | AI FAIL vs citation B salute at forehead (multi-dictionary; Lifeprint page notes wave latitude); rig PASS |
| THANK-YOU | <a href="https://www.lifeprint.com/asl101/pages-signs/t/thankyou.htm"><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ref-thank-you.jpg" width="220"></a> | <img src="docs/ai-vs-rig/cmp/cmp-thank-you-ai.webp" width="220"><details><summary>prompt</summary>sent: POST /v1/images/generations, model muse-image-1.0<br>prompt: photorealistic adult woman signing ASL THANK-YOU, hands clearly visible, neutral background<br>received: 1280x1920 webp, 477090 B, s3://bryanchasko-amazon-sumerian-hosts-asl-webp/ai-vs-rig/ai-thank-you.webp</details> | <img src="docs/ai-vs-rig/cmp/cmp-thank-you-rig.png" width="220"> | [sign-thank-you-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-thank-you-fiona.glb) | AI FAIL — palm down, not toward signer; rig PASS                                                          |
| YES       | <a href="https://www.lifeprint.com/asl101/pages-signs/y/yes.htm"><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ref-yes.jpg" width="200"></a>            | <img src="docs/ai-vs-rig/cmp/cmp-yes-ai.webp" width="220"><details><summary>prompt</summary>sent: POST /v1/images/generations, model muse-image-1.0<br>prompt: photorealistic adult woman signing ASL YES, hands clearly visible, neutral background<br>received: 1280x1920 webp, 349738 B, s3://bryanchasko-amazon-sumerian-hosts-asl-webp/ai-vs-rig/ai-yes.webp</details>                   | <img src="docs/ai-vs-rig/cmp/cmp-yes-rig.png" width="220">       | [sign-yes-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-yes-fiona.glb)             | PASS both — S fist at chest                                                                               |
| NO        | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-no.png" width="220">            | [sign-no-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-no-fiona.glb)               | —                                                                                                         |
| QUESTION  | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-question.png" width="220">      | [sign-question-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-question-fiona.glb)   | —                                                                                                         |
| TRUE      | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-true.png" width="220">          | [sign-true-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-true-fiona.glb)           | —                                                                                                         |
| ONE       | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-one.png" width="220">           | [sign-one-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-one-fiona.glb)             | —                                                                                                         |
| TWO       | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-two.png" width="220">           | [sign-two-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-two-fiona.glb)             | —                                                                                                         |
| THREE     | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-three.png" width="220">         | [sign-three-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-three-fiona.glb)         | —                                                                                                         |
| FOUR      | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-four.png" width="220">          | [sign-four-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-four-fiona.glb)           | —                                                                                                         |
| FIVE      | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-five.png" width="220">          | [sign-five-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-five-fiona.glb)           | —                                                                                                         |
| SIX       | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-six.png" width="220">           | [sign-six-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-six-fiona.glb)             | —                                                                                                         |
| SEVEN     | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-seven.png" width="220">         | [sign-seven-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-seven-fiona.glb)         | —                                                                                                         |
| EIGHT     | <a href="https://www.lifeprint.com/asl101/pages-signs/n/numbers1-10.htm"><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ref-eight.jpg" width="220"></a>  | <img src="docs/ai-vs-rig/cmp/cmp-eight-ai.webp" width="220"><details><summary>prompt</summary>sent: POST /v1/images/generations, model muse-image-1.0<br>prompt: photorealistic adult woman signing ASL EIGHT, hands clearly visible, neutral background<br>received: 1280x1920 webp, 265104 B, s3://bryanchasko-amazon-sumerian-hosts-asl-webp/ai-vs-rig/ai-eight.webp</details>             | <img src="docs/ai-vs-rig/cmp/cmp-eight-rig.png" width="220">     | [sign-eight-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-eight-fiona.glb)         | AI FAIL — open V is a 2; rig PASS (zoom verified)                                                         |
| NINE      | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-nine.png" width="220">          | [sign-nine-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-nine-fiona.glb)           | —                                                                                                         |
| ME        | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-me.png" width="220">            | [sign-me-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-me-fiona.glb)               | —                                                                                                         |
| YOU       | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-you.png" width="220">           | [sign-you-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-you-fiona.glb)             | —                                                                                                         |
| THIS      | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-this.png" width="220">          | [sign-this-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-this-fiona.glb)           | —                                                                                                         |
| WHERE     | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-where.png" width="220">         | [sign-where-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-where-fiona.glb)         | —                                                                                                         |
| WHO       | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-who.png" width="220">           | [sign-who-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-who-fiona.glb)             | —                                                                                                         |
| HOW-MANY  | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-how-many.png" width="220">      | [sign-how-many-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-how-many-fiona.glb)   | —                                                                                                         |
| FIRST     | <a href="https://www.lifeprint.com/asl101/pages-signs/f/first.htm"><img src="https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ref-first.jpg" width="200"></a>        | <img src="docs/ai-vs-rig/cmp/cmp-first-ai.webp" width="220"><details><summary>prompt</summary>sent: POST /v1/images/generations, model muse-image-1.0<br>prompt: photorealistic adult woman signing ASL FIRST, hands clearly visible, neutral background<br>received: 1280x1920 webp, 211078 B, s3://bryanchasko-amazon-sumerian-hosts-asl-webp/ai-vs-rig/ai-first.webp</details>             | <img src="docs/ai-vs-rig/cmp/cmp-first-rig.png" width="220">     | [sign-first-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-first-fiona.glb)         | PASS both — index up, palm forward                                                                        |
| SECOND    | —                                                                                                                                                                                                           | —                                                                                                                                                                                                                                                                                                                                                                                             | <img src="docs/assets/spike-sign-second.png" width="220">        | [sign-second-fiona.glb](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-second-fiona.glb)       | —                                                                                                         |

Right hand, wrong sign: the three AI failures are chereme errors
(palm, thumb, handshape), none anatomical. Read every row's
evidence in [`docs/ai-vs-rig/verdicts.md`](docs/ai-vs-rig/verdicts.md).
Copy any call from [`docs/ai-vs-rig/prompts.md`](docs/ai-vs-rig/prompts.md).
Segment Anything Model (SAM) 3.1 masks rate-limited out, so these
verdicts are inspected, not segmented.

Second attempt, same session: the bare gloss prompt failed
THANK-YOU. The pose knowledge went in with the image, and both
passes corrected it. No ControlNet-style pose conditioning exists
on the API. The edits endpoint is the lever. There is no video
generation endpoint on the Model API (video is input-only). Motion
still comes from the Blender pipeline. Full calls in
[`docs/ai-vs-rig/prompts.md`](docs/ai-vs-rig/prompts.md#round-2-edits-endpoint-same-session),
verdicts in
[`docs/ai-vs-rig/verdicts.md`](docs/ai-vs-rig/verdicts.md#round-2-edits-endpoint-same-session).

<table>
<tr><th>fix the AI image</th><th>photoreal the rig still</th></tr>
<tr><td><img src="docs/ai-vs-rig/edit-thank-you-fix-ai.webp" width="300"></td><td><img src="docs/ai-vs-rig/edit-thank-you-from-rig.webp" width="300"></td></tr>
</table>

Stance between signs: neutral idle, arms slightly out (left) vs
arms down (right). Rest bakes into the idle base upstream (pull
requests #107–111). The rest-idle export tooling lives there too.
Track the port in
[issue #2](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/issues/2),
the upstream port queue. Stills ported from upstream origin/main
`docs/assets/batch9/`. The upstream team eye-verified them there.

<table>
<tr><th>stand idle rest</th><th>rest arms down</th></tr>
<tr><td><img src="docs/assets/upstream-stand-idle-rest-fiona.png" width="300"></td><td><img src="docs/assets/upstream-rest-arms-down-fiona.png" width="300"></td></tr>
</table>

## Open Fiona in Blender and press play

You do this in the Blender window:

1. Open Blender. Delete the default cube (`X`).
2. Import `fiona.glb` via `File > Import > glTF 2.0`. The Outliner
   shows the rig's meshes plus one armature. The armature is
   the skeleton every clip moves.
3. Select the armature. Switch to Pose Mode. Rotate a bone. Try
   the right wrist.
4. Pose the citation start: flat hand at the chin, fingertips at
   the lips. The numbers live in `SIGNS`. The headless commands
   above set exactly this pose.
5. Import `sign-thank-you-fiona.glb` the same way. Export it
   above, or grab the release. Ignore the second armature. Open a
   Dope Sheet. Switch it to Action Editor. Select Fiona's
   armature. Pick the `thank-you` action. Drag to frame 36.
6. Press **Spacebar**. You play 72 frames: rest, chin hold,
   forward-down arc, palm-down end hold, return.

An animation is an action: bone angles over frames, assigned to
an armature. The headless scripts set steps 4–5 with numbers
instead of mouse drags. You reproduce the exact pose either way.

![Fiona imported, full-body rest render](docs/assets/gui-step1-imported.png)

![THANK-YOU citation start, same pose as a render](docs/assets/gui-step2-posed.png)

![The thank-you action on Fiona, frame 36 render](docs/assets/gui-step3-playing.png)

## How a sign is built

Four cheremes per sign. Meaningless parts combine into meaning,
like phonemes in speech:

- **Handshape** — which fingers extend, how the rest fold. A
  fist with thumb alongside is A. Flat hand together is B.
  Thumb-index circle is F. Every joint angle lives in
  `scripts/spike-finger-articulation/pose_handshapes.py`, one
  dict per shape.
- **Place** — chin (THANK-YOU), beside forehead (HELLO), chest
  (YOU), mouth (WHO).
- **Movement** — forward-down arc (THANK-YOU), pinwheel
  (HELLO), forward point (YOU).
- **Palm direction** — palm-out on letters, dorsal on isolated
  numbers 1–5. Presets cover nearly everything. The full table
  lives in the [cookbook](docs/cookbook.md) ("How to read a
  pose") — read it when a preset looks wrong.

You turn a host line into a gloss sequence. One token per sign,
ASL order. Fingerspell what the lexicon lacks:

```json
["YOU", "THANK-YOU", "FINGERSPELL:H-E-L-P"]
```

You check a draft with two commands:

```bash
python3 scripts/validate_gloss.py data/examples/gloss-demo.json
python3 scripts/lint_lexicon.py
```

The token rules live in
[`docs/gloss-schema.md`](docs/gloss-schema.md) — read them
before drafting. You author a sign like this: change the numbers
in `SIGNS` / `SIGNS_END`. Re-run the two commands. Compare
against the citation. The [cookbook](docs/cookbook.md) records
every still's numbers, so start there when a pose looks off.

At runtime the engine needs nothing new. Each sign is one short
clip on the same skeleton. It queues in/hold/out beside the
gesture queue. It runs on the same clock as banked audio and
visemes.

## Built with Meta

Every row ran while building this project. The table links the
evidence. The reproducible core stays the headless scripts. Same
numbers in, same pixels out. No model renders a frame. The page
serves banked audio and prebuilt clips. Nothing bills per
request.

| Model                       | What it did here                                                                                                                  | Evidence                                                                                                                     |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Muse Spark (via Muse Code)  | orchestration; drafted the gloss for "Hello! Yes, thank-you for coming." — validators pass (GLOSS PASS 4 tokens, LEXICON PASS 58) | [`gloss-draft.md`](docs/meta-evidence/gloss-draft.md), [`gloss-draft-spark.json`](docs/meta-evidence/gloss-draft-spark.json) |
| Muse Wonder (via Muse Code) | planned the work, set the verdict rubric, reviewed every evidence table                                                           | [`wonder-notes.md`](docs/meta-evidence/wonder-notes.md), [`verdicts.md`](docs/ai-vs-rig/verdicts.md)                         |
| Muse Image (API)            | 5-sign comparison set (prompts + payloads verbatim), demo poster, 2 round-2 edits — both pass                                     | [`prompts.md`](docs/ai-vs-rig/prompts.md), [`demo-poster.webp`](docs/assets/demo-poster.webp)                                |
| Muse Voice Transcribe (API) | timing audit: banked "thank you" turn 0.140–0.380 s inside the gesture in-phase                                                   | [`transcribe-audit.md`](docs/meta-evidence/transcribe-audit.md)                                                              |
| SAM 3.1 (API)               | hand-segmentation QA on all 10 images; capacity 429s, zero masks — verdicts inspected, rerun queued                               | [`verdicts.md`](docs/ai-vs-rig/verdicts.md)                                                                                  |
| Muse Glimmer (local)        | same gloss task on-device; too slow to finish (fragment recorded as a limitation)                                                 | [`gloss-glimmer-raw.json`](docs/meta-evidence/gloss-glimmer-raw.json)                                                        |
| Muse Code                   | the agent that wrote it all                                                                                                       | commit history                                                                                                               |

### Demo 1 — Spark drafts gloss, validators gate it

Run the validators on the committed draft:

```bash
python3 scripts/validate_gloss.py docs/meta-evidence/gloss-draft-spark.json
# GLOSS PASS: 4 tokens, 0 failures
python3 scripts/lint_lexicon.py
# LEXICON PASS: 58 entries, 0 failures
```

The draft lives in
[`gloss-draft-spark.json`](docs/meta-evidence/gloss-draft-spark.json)
(`HELLO YES THANK-YOU C-O-M-I-N-G` for "Hello! Yes, thank-you for
coming."). The model proposes. The validators dispose.

### Demo 2 — Wonder plans, the rubric reviews

Read the plan, delegation, and verdict rubric in
[`wonder-notes.md`](docs/meta-evidence/wonder-notes.md) — it
decided what counts as a PASS. Every evidence table passed that
review before commit. The Wave-3 sign-off sits in
[`verdicts.md`](docs/ai-vs-rig/verdicts.md).

### Demo 7 — Glimmer and Ollama run local

- **A local open-weights model** (we used Glimmer 30B for gloss
  drafts): any OpenAI-compatible server on your own hardware —
  about 20 gigabytes free for a 30-billion-parameter quantized
  model (vLLM, SGLang, or llama.cpp all serve one). Query it the
  same way you would the API. Keep the validators as the gate,
  not the model's word.
- **A vision model for second opinions** (we used Ollama vision
  models for render-vs-citation checks): install Ollama, the
  free local model runner, from [ollama.com](https://ollama.com).
  Pull a vision model. Show it the render next to the citation
  still. Ask what differs. It catches pose drift a tired eye
  misses. The human reviewer still decides.

(Muse Code drives all of this — see Demo 8. Spark via API is the
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

Run the handshake. It returns a session id. This is a real reply
from this box:

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

### Demos 3–5 — hosted calls, one key

One key (`MODEL_API_KEY` from dev.meta.ai). Same base URL:
`https://api.meta.ai/v1`. Outputs are committed above. Rerun a
call only when you change its inputs.

#### Demo 3 — Image generates (exact comparison call)

This call made the comparison set. Model and prompt are logged
in [`prompts.md`](docs/ai-vs-rig/prompts.md). Size and aspect
were not, so exact pixels may differ:

```bash
curl -X POST "https://api.meta.ai/v1/images/generations" \
  -H "Authorization: Bearer $MODEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"muse-image-1.0",
       "prompt":"photorealistic adult woman signing ASL THANK-YOU, hands clearly visible, neutral background"}'
# {"data":[{"b64_json":"..."}]} — 1280x1920 webp
```

#### Demo 4 — Image edits with a reference (exact round-2 call — the one that fixed the palm)

```bash
curl -X POST "https://api.meta.ai/v1/images/edits" \
  -H "Authorization: Bearer $MODEL_API_KEY" \
  -F 'model=muse-image-1.0' \
  -F 'image=@ai-thank-you.png' \
  -F 'prompt=Keep the same woman, framing and neutral background. Fix
      only her signing hand: flat hand at the chin, fingertips touching
      the chin, palm facing toward her, the ASL sign for thank-you.'
# {"data":[{"b64_json":"..."}]} — palm corrected, rest intact
```

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
         {"type":"input_image","image_url":"https://.../ai-vs-rig/cmp/cmp-yes-ai.webp"}]}]}'
# masks arrive as <|box;...|> + <|mask;...|> tokens in output_text
```

Watch it run: <https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing>
