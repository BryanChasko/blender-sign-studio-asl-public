# Extending Amazon Sumerian Hosts with American Sign Language

Sign clips for Sumerian-style hosts. Fiona is the worked example.
Commands run headless; the GUI path is covered too.

## How a Sumerian host works (60 seconds)

A host is a rigged 3D character: a mesh (the visible body) bound
to a skeleton of named bones, plus a library of short animation
clips. At runtime the Babylon.js engine loads the mesh file, then
plays clips on the skeleton — a wave, a blink, lips moving with
speech. Speech comes from banked audio files plus viseme data
(mouth shapes over time). Signing rides the same rails: each sign
is one short clip on the same skeleton, queued with an
in / hold / out shape (move in, hold the meaning, move out), on
the same clock as the voice. Nothing about the engine changes —
signing is a parallel clip queue beside the gesture queue.

## What you need

- Blender 5.2 LTS (free, open source). No Blender experience
  needed: everything here runs headless, one command per step.
- A host rig file (`.glb` — one file holding mesh, skeleton,
  and textures). Get it below.
- Python 3 for the repo's check scripts. That is all.

Install Blender (user-local, no sudo needed):

```bash
mkdir -p ~/opt && cd ~/opt
curl -sSO https://download.blender.org/release/Blender5.2/blender-5.2.3-linux-x64.tar.xz
tar xf blender-5.2.3-linux-x64.tar.xz
ln -sfn ~/opt/blender-5.2.3-linux-x64/blender ~/.local/bin/blender-5.2
blender-5.2 --version   # Blender 5.2.3 LTS
```

## Get a rig (Fiona first, others the same way)

A rig is just files. Two ways to fetch them; both give you the
same signed-by-Amazon open-source hosts:

**Option A — upstream open source.** The canonical source is
[aws-samples/amazon-sumerian-hosts](https://github.com/aws-samples/amazon-sumerian-hosts)
at commit `109baefef53cc18ef3e2e2340170c44078d011b91`.
Fiona lives under
`packages/demos-babylon/src/character-assets/characters/adult_female/fiona/`.
You need the whole folder: the `.gltf`, its `.bin`, and the
`textures/` folder next to it. (The `.glb` is the same content
packed into one file with textures embedded — the form the
engine loads.)

**Option B — vendored fixtures.** The sibling `sumerian-hosts`
repo keeps the same files ready-made at
`fixtures/hosts/<id>/<id>.glb`: `fiona`, `cristine`, `grace`,
`maya` (female rigs), `jay`, `luke`, `preston`, `wes` (male),
`alien`. Same upstream commit, same license.

Either way, point the scripts at the folder. They default to the
sibling fixtures path; `--rig fiona` picks the female rig used
through this guide. Any rig with the same bone names works —
that is what "compatible" means here: same skeleton, same names.

Mesh license: the character files are CC BY-SA 4.0 (Amazon Web
Services, Inc.). The scripts, angles, and docs in this repo are
Apache-2.0 (see LICENSE). Keep the attribution if you ship.

## Run your first sign (Fiona signs THANK-YOU)

THANK-YOU in ASL: fingertips start at the chin, hand moves out
and slightly down. Flat hand throughout. (Reference: Vicars
[Lesson 01](https://www.lifeprint.com/asl101/pages-signs/t/thankyou.htm).)

Still first — the citation start frame:

```bash
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot signing-torso --rig fiona
# RENDER_OK out/spike-host-signing-torso.png posed=36
```

Then the movement clip — 72 frames the engine can play:

```bash
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/export_sign_clip.py -- \
  --sign thank-you --rig fiona --out out/sign-thank-you-fiona.glb
# CLIP_OK out/sign-thank-you-fiona.glb action=thank-you
```

`posed=36` means 36 bones posed; `CLIP_OK` means the armature-only
clip exported with its `thank-you` action. A ready-made export
ships as a [release asset](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases)
since `.glb` files travel through the asset pipeline, not git.

What the motion looks like:

![THANK-YOU citation start](docs/assets/spike-sign-thank-you.png)
![THANK-YOU end hold](docs/assets/spike-sign-thank-you-end.png)

Start: flat hand at the chin, fingertips at the lips. Then the
forward-down arc to the palm-down end hold (frames 44–52 of 72).
Animated versions live under [`assets/`](assets/) as hosted
webp clips.

## Open Fiona in Blender and press play (the GUI way)

Prefer windows over terminals? Same result, by hand:

1. Open Blender. Delete the default cube (select it, press `X`).
2. `File > Import > glTF 2.0`, pick `fiona.glb`. Fiona appears;
   the Outliner (top right) shows one mesh plus one armature —
   that armature, a skeleton of named bones, is what every
   animation moves. The mesh is just the skin on top.

![Fiona imported, full-body rest render](docs/assets/gui-step1-imported.png)

3. Select the armature, switch the editor from Object Mode to
   **Pose Mode** (dropdown, top left of the 3D view). Now
   rotating a bone poses the body — try the right wrist.
4. Pose the citation start: flat hand at the chin, fingertips at
   the lips (the numbers behind this pose live in `SIGNS` in the
   scripts — the headless commands above set exactly this).

![THANK-YOU citation start, same pose as a render](docs/assets/gui-step2-posed.png)

5. Load the animation: `File > Import > glTF 2.0`, pick
   `sign-thank-you-fiona.glb` (export it with the headless
   command above, or grab it from the release). It arrives as a
   second armature — ignore that armature; what you want is its
   **action**. Open a Dope Sheet editor, switch it to Action
   Editor mode: the `thank-you` action is in the dropdown.
   Select Fiona's armature, pick `thank-you` in that dropdown,
   drag the timeline to frame 36.

![The thank-you action on Fiona, frame 36 render](docs/assets/gui-step3-playing.png)

6. Press **Spacebar**. Fiona signs. The playhead runs 72 frames:
   rest, chin hold, forward-down arc, palm-down end hold, return.

That is all "playing an animation" ever is here: an action (a
bag of bone angles over frames) assigned to an armature, played
back. The headless scripts do steps 4–5 with numbers instead of
mouse drags, so anyone can reproduce the exact pose.

## Cheremes: the four building blocks of a sign

Linguists break signs into cheremes — meaningless parts that
combine into meaning, like phonemes in speech. Every sign in
this repo is four cheremes:

- **Handshape** — which fingers are extended and how the rest
  fold. A fist with the thumb alongside is A; a flat hand with
  fingers together is B; thumb-index circle is F. The exact
  curl of every finger joint lives in
  `scripts/spike-finger-articulation/pose_handshapes.py`, one
  dict per shape.
- **Place** — where the sign happens: chin (THANK-YOU), beside
  the forehead (HELLO), chest height (YOU), mouth height (WHO).
- **Movement** — what travels: forward-down arc (THANK-YOU),
  pinwheel (HELLO), forward point (YOU).
- **Palm direction** — palm-side toward the addressee on letters,
  dorsal (back of hand) on isolated numbers 1–5.

Two presets cover the wrist and camera for nearly everything:
`letter_or_digit` (palm-out) and `cardinal_numeral` (palm-in,
dorsal). Full table in the [cookbook](docs/cookbook.md) ("How
to read a pose").

## Gloss: how a line becomes signs

Nobody animates sentences by hand. A host line is first rewritten
as an ASL gloss sequence — one token per sign, in ASL order, with
fingerspelling marked where the lexicon has no entry:

```json
["YOU", "THANK-YOU", "FINGERSPELL:H-E-L-P"]
```

`data/examples/gloss-demo.json` is a validated sequence the
adapter consumes. The rules live in
[`docs/gloss-schema.md`](docs/gloss-schema.md); two repo scripts
enforce them:

```bash
python3 scripts/validate_gloss.py data/examples/gloss-demo.json
python3 scripts/lint_lexicon.py
```

Out-of-lexicon words are fingerspelled, never improvised — a
missing sign degrades to letters, not to a made-up gesture.

## How the parts fit

```
scripts/blender/   pose + render + clip-export (works headless, see above)
scripts/spike-finger-articulation/  handshape joint values, one dict per shape
data/lexicon/      versioned sign list (v1 reviewed set, v2 in progress)
data/examples/     a validated gloss sequence the adapter consumes
docs/              per-pose recipes (cookbook), schema, review gate, credits
assets/            animation clips hosted for embedding (webp)
```

A sign is four things: a handshape, a place (chin), a movement
(forward-down), and a palm direction. Those four are baked into
the clip as joint angles — `SIGNS` / `SIGNS_END` in
`render_host_shots.py`, fingers in `pose_handshapes.py`. Change
the numbers, re-run the two commands, compare against the
citation. That loop is the whole authoring process; the
[cookbook](docs/cookbook.md) records every still's numbers.

## AI signs vs Blender signs

Right hand, wrong sign. Each row judges both sides against the
linked reference first — verdicts in
[`docs/ai-vs-rig/verdicts.md`](docs/ai-vs-rig/verdicts.md) with the
reference basis. Image calls (endpoint, model, prompts, payloads)
in [`docs/ai-vs-rig/prompts.md`](docs/ai-vs-rig/prompts.md).
Reference photos are linked, not vendored. Crops match (720px,
face + signing hand). SAM 3.1 masks rate-limited out, so these are
inspected, not segmented.

<table>
<tr><th>sign (reference)</th><th>Muse Image</th><th>Fiona rig</th><th>verdict</th></tr>
<tr><td><a href="https://www.lifeprint.com/asl101/pages-signs/t/thankyou.htm">THANK-YOU</a></td><td><img src="docs/ai-vs-rig/cmp/cmp-thank-you-ai.webp" width="300"></td><td><img src="docs/ai-vs-rig/cmp/cmp-thank-you-rig.png" width="300"></td><td>AI FAIL — palm down, not toward signer. Rig PASS.</td></tr>
<tr><td><a href="https://www.lifeprint.com/asl101/pages-signs/h/hello.htm">HELLO</a></td><td><img src="docs/ai-vs-rig/cmp/cmp-hello-ai.webp" width="300"></td><td><img src="docs/ai-vs-rig/cmp/cmp-hello-rig.png" width="300"></td><td>AI FAIL vs authored B salute (reference allows wave variants). Rig PASS.</td></tr>
<tr><td><a href="https://www.lifeprint.com/asl101/pages-signs/y/yes.htm">YES</a></td><td><img src="docs/ai-vs-rig/cmp/cmp-yes-ai.webp" width="300"></td><td><img src="docs/ai-vs-rig/cmp/cmp-yes-rig.png" width="300"></td><td>PASS both — S fist at chest.</td></tr>
<tr><td><a href="https://www.lifeprint.com/asl101/pages-signs/n/numbers1-10.htm">EIGHT</a></td><td><img src="docs/ai-vs-rig/cmp/cmp-eight-ai.webp" width="300"></td><td><img src="docs/ai-vs-rig/cmp/cmp-eight-rig.png" width="300"></td><td>AI FAIL — open V is a 2. Rig PASS (zoom verified).</td></tr>
<tr><td><a href="https://www.lifeprint.com/asl101/pages-signs/f/first.htm">FIRST</a></td><td><img src="docs/ai-vs-rig/cmp/cmp-first-ai.webp" width="300"></td><td><img src="docs/ai-vs-rig/cmp/cmp-first-rig.png" width="300"></td><td>PASS both — index up, palm forward.</td></tr>
</table>

Signs move — stills are citations. THANK-YOU looped, the rest as
engine clips:

![Fiona signs THANK-YOU, looped](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-thank-you-move.webp)

[thank-you](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-thank-you-fiona.glb) ·
[hello](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-hello-fiona.glb) ·
[yes](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-yes-fiona.glb) ·
[eight](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-eight-fiona.glb) ·
[first](https://github.com/bryanchasko/amazon-sumerian-hosts-asl/releases/download/v0.2-batch5/sign-first-fiona.glb)

## Built with Meta

Every row ran in this repo's dev loop; evidence linked. No Meta
model runs in production on the demo page — the site serves banked
audio and prebuilt clips.

| Model                       | What it did here                                                                                                                  | Evidence                                                                                                                     |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Muse Spark (via Muse Code)  | orchestration; drafted the gloss for "Hello! Yes, thank-you for coming." — validators pass (GLOSS PASS 4 tokens, LEXICON PASS 58) | [`gloss-draft.md`](docs/meta-evidence/gloss-draft.md), [`gloss-draft-spark.json`](docs/meta-evidence/gloss-draft-spark.json) |
| Muse Wonder (via Muse Code) | planned the work, set the verdict rubric, reviewed every evidence table                                                           | [`wonder-notes.md`](docs/meta-evidence/wonder-notes.md), [`verdicts.md`](docs/ai-vs-rig/verdicts.md)                         |
| Muse Image (API)            | generated the 5-sign comparison set (prompts verbatim) + the demo poster                                                          | [`prompts.md`](docs/ai-vs-rig/prompts.md), [`demo-poster.webp`](docs/assets/demo-poster.webp)                                |
| Muse Voice Transcribe (API) | timing audit: banked "thank you" turn 0.140–0.380 s confirmed inside the gesture in-phase                                         | [`transcribe-audit.md`](docs/meta-evidence/transcribe-audit.md)                                                              |
| SAM 3.1 (API)               | hand-segmentation QA attempted on all 10 images; capacity 429s all day, zero masks — verdicts are inspected, rerun queued         | [`verdicts.md`](docs/ai-vs-rig/verdicts.md)                                                                                  |
| Muse Glimmer (local)        | same gloss task on-device; too slow to finish (fragment recorded as a limitation, not a result)                                   | [`gloss-glimmer-raw.json`](docs/meta-evidence/gloss-glimmer-raw.json)                                                        |
| Muse Code                   | the coding agent that wrote it all                                                                                                | repo history                                                                                                                 |

Full model map (active, parked, blocked): [`docs/meta-models.md`](docs/meta-models.md).

### Where the models actually run

Budget matters here, so be precise: nothing above bills per
request on the demo page. The heavy models ran (and run) in the
dev loop on this workstation; the site serves their outputs.

- **Local and free:** Muse Spark (orchestration), Glimmer 30B
  (render judging), and the ollama vision models (render-vs-still
  checks) run on rocmaibox hardware. Muse Code is the agent that
  drives them. This is where every still and clip was reviewed.
- **On credits, then committed:** the Meta Model API calls —
  Image comparison set + poster, Transcribe timing audit, SAM
  segmentation attempts — ran during development and their outputs
  are committed above. The page serves those outputs; nothing
  bills per request.
- **Blender MCP:** a live-Blender bridge (`blender-mcp-http`)
  runs on this workstation for scene inspection during authoring
  — ask it what is in the scene instead of guessing. The
  reproducible core stays the headless scripts in this repo: same
  numbers in, same pixels out, no model in the loop at render
  time.

Live demo: <https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing>
