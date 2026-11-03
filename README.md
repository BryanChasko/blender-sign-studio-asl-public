# Extending Amazon Sumerian Hosts with American Sign Language

3D hosts that don't just talk — they sign. This repo adds an
American Sign Language layer to Sumerian-style hosts: one host
line performed three ways at once (spoken, captioned, signed).
Fiona, the female rig, is the worked example throughout.

No Blender, Sumerian, or ASL background assumed. Every step below
is a command you can paste.

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

## Built with Meta

Every row below ran in this project's dev loop (evidence: the
upstream pull-request history). No Meta model runs in
production on the demo page — the site serves banked audio and
prebuilt clips, so there is nothing to bill at request time.

| Model                                                         | What it did here                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Muse Spark](https://dev.meta.ai/models/muse-spark)           | orchestrated the build: pose recipes, citations, and renders kept consistent across every sign                                                                                                                                                                                                            |
| [Muse Glimmer 30B](https://dev.meta.ai/models/muse-glimmer)   | local judge: close-looking render-vs-citation checks (the chin-contact catch came out of this loop), served on-device                                                                                                                                                                                     |
| [Muse Code](https://dev.meta.ai/lp/muse-code)                 | the coding agent that wrote it all: scripts, checks, pull requests with evidence attached                                                                                                                                                                                                                 |
| [Meta Model API](https://dev.meta.ai/products/meta-model-api) | staged path for hosted calls (event credits): [Image](https://dev.meta.ai/models/muse-image) for neutral stage backgrounds, [Voice Transcribe](https://dev.meta.ai/models/muse-voice-transcribe) for speech/clock drift measurement, [SAM 3.1](https://dev.meta.ai/models/sam-3-1) for hand-visibility QA |
| [Muse Spark Open](https://dev.meta.ai/models/muse-spark-open) | self-hosted gloss-sequencing fallback next to the local-model rows in the architecture doc                                                                                                                                                                                                                |

Live demo: <https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing>
