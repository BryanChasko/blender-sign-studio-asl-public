# Animation clips

Short looping clips of the Fiona rig. Every clip below: make
it with the render command, play it in the Blender window,
check the sidecar for frame counts. Binaries live on S3 —
binaries stay outside git.

Play any clip in Blender: open Blender, delete the cube,
`File > Import > glTF 2.0` > `fiona.glb`, import the sign's
`.glb` from the [release assets](https://github.com/bryanchasko/blender-sign-studio-asl-public/releases)
the same way, Dope Sheet > Action Editor, pick the action,
drag the playhead, press **Spacebar**. Full tour in the README
Press-play section.

## THANK-YOU movement (48 frames, 24 fps)

Fingertips at the chin, forward-down arc, palm-down end hold:

![Fiona signs THANK-YOU](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-thank-you-move.webp)

Make it:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-thank-you-move --rig fiona
# RENDER_OK out/sign-thank-you-move frames=48
ffmpeg -framerate 24 -i out/sign-thank-you-move/frame_%04d.png \
  -vf scale=480:-1 -loop 0 thank-you.webp
```

Play it in Blender: import `fiona.glb` +
`sign-thank-you-fiona.glb`, Action Editor > `thank-you`,
frame 36, **Spacebar**.
Sidecar (frames, fps, bytes):
[`plays/fiona-thank-you-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-thank-you-move.sidecar.json)

## Posture transition (51 frames, 12 fps)

Rest → neutral → active → neutral → rest, the between-signs
stance flow:

![Fiona posture transition](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-posture-transition.webp)

Make it:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot posture-transition --rig fiona
```

Play it in Blender: no clip file ships for this one — it
stitches rest/neutral/active poses. Re-run the shot above to
replay it.
Sidecar:
[`plays/fiona-posture-transition.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-posture-transition.sidecar.json)

## HELLO movement (48 frames, 24 fps)

B salute beside the forehead, shoulder-abduction travel:

![Fiona signs HELLO](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-hello-move.webp)

Make it:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-hello-move --rig fiona
# RENDER_OK out/sign-hello-move frames=48
ffmpeg -framerate 24 -i out/sign-hello-move/frame_%04d.png \
  -vf scale=480:-1 -loop 0 hello.webp
```

Play it in Blender: import `fiona.glb` +
`sign-hello-fiona.glb`, Action Editor > `hello`, **Spacebar**.
Sidecar:
[`plays/fiona-hello-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-hello-move.sidecar.json)

## YES movement (48 frames, 24 fps)

S fist nods at the chest:

![Fiona signs YES](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-yes-move.webp)

Make it:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-yes-move --rig fiona
# RENDER_OK out/sign-yes-move frames=48
ffmpeg -framerate 24 -i out/sign-yes-move/frame_%04d.png \
  -vf scale=480:-1 -loop 0 yes.webp
```

Play it in Blender: import `fiona.glb` +
`sign-yes-fiona.glb`, Action Editor > `yes`, **Spacebar**.
Sidecar:
[`plays/fiona-yes-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-yes-move.sidecar.json)

## EIGHT movement (48 frames, 24 fps)

Index up, middle-to-thumb circle, ring and pinky extended:

![Fiona signs EIGHT](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-eight-move.webp)

Make it:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-eight-move --rig fiona
# RENDER_OK out/sign-eight-move frames=48
ffmpeg -framerate 24 -i out/sign-eight-move/frame_%04d.png \
  -vf scale=480:-1 -loop 0 eight.webp
```

Play it in Blender: import `fiona.glb` +
`sign-eight-fiona.glb`, Action Editor > `eight`, **Spacebar**.
Sidecar:
[`plays/fiona-eight-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-eight-move.sidecar.json)

## FIRST movement (48 frames, 24 fps)

Index up, palm forward, shoulder travel:

![Fiona signs FIRST](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-first-move.webp)

Make it:

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-first-move --rig fiona
# RENDER_OK out/sign-first-move frames=48
ffmpeg -framerate 24 -i out/sign-first-move/frame_%04d.png \
  -vf scale=480:-1 -loop 0 first.webp
```

Play it in Blender: import `fiona.glb` +
`sign-first-fiona.glb`, Action Editor > `first`, **Spacebar**.
Sidecar:
[`plays/fiona-first-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-first-move.sidecar.json)

## Labeled strip (five rig stills, one image)

Built with Python Pillow (DejaVu Sans Bold labels on a dark
bar), committed as webp:

![Fiona's five compared signs](../docs/assets/fiona-five-strip.webp)

## UI screenshots

The Blender window, captured: mesh framed, dope sheet,
timeline.

Make it in two commands. Build the `.blend` headless
([`prepare_ui_blend.py`](../scripts/blender/prepare_ui_blend.py)
imports the rig, hides the 2 m proxy mesh, sets STICK bones):

```bash
blender-5.2 -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/prepare_ui_blend.py -- \
  --rig /path/to/fiona.glb --out out/ui-fiona.blend
```

Open it on a virtual display and hold the window
([`screenshot_ui.py`](../scripts/blender/screenshot_ui.py)
hides the armature, frames the mesh, waits for capture):

```bash
Xvfb :98 -screen 0 1600x900x24 &
LIBGL_ALWAYS_SOFTWARE=1 DISPLAY=:98 blender-5.2 \
  out/ui-fiona.blend --factory-startup \
  -P scripts/blender/screenshot_ui.py -- --hold 75 &
sleep 40
DISPLAY=:98 import -window root docs/assets/ui-fiona-viewport.webp
```

Notes: hide the armature for mesh views (hundred-unit bones
fill the viewport under software GL; renders never draw
bones). The internal screenshot operator returns black here,
so capture from outside with ImageMagick. Kill stale sessions
by PID — with no window manager the first-mapped window stays
on top.

![Fiona in the Blender window](../docs/assets/ui-fiona-viewport.webp)

## Live site capture

The README header shows the real page. Capture it again with:

```bash
chromium-browser --headless --disable-gpu --no-sandbox \
  --window-size=1280,800 --virtual-time-budget=20000 \
  --screenshot=signing-hosts.png \
  "https://bryanchasko.com/signing-hosts/?host=fiona&shot=signing"
ffmpeg -y -i signing-hosts.png -q:v 85 signing-hosts-live.webp
aws s3 cp signing-hosts-live.webp \
  s3://bryanchasko-amazon-sumerian-hosts-asl-webp/webp/signing-hosts-live.webp
```

![The live signing page](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/signing-hosts-live.webp)
