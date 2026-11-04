# Animation clips

Short looping clips of the Fiona rig, rendered headless in
Blender 5.2.3 and hosted on S3 (binaries live outside git — see
the asset pipeline rule in the private build repo).

Base URL: `https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/`

## THANK-YOU movement (48 frames, 24 fps)

Fingertips at the chin, forward-down arc, palm-down end hold:

![Fiona signs THANK-YOU](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-thank-you-move.webp)

Made with:

```bash
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot sign-thank-you-move --rig fiona
```

Then downscaled to 480px and encoded to looping webp.
Sidecar (frames, fps, bytes):
[`plays/fiona-thank-you-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-thank-you-move.sidecar.json)

## Posture transition (51 frames, 12 fps)

Rest → neutral → active → neutral → rest, the between-signs
stance flow:

![Fiona posture transition](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-posture-transition.webp)

Made with:

```bash
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/blender/render_host_shots.py -- \
  --out-dir out --shot posture-transition --rig fiona
```

Sidecar:
[`plays/fiona-posture-transition.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-posture-transition.sidecar.json)

## HELLO movement (48 frames, 24 fps)

B salute beside the forehead, shoulder-abduction travel:

![Fiona signs HELLO](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-hello-move.webp)

Made with `--shot sign-hello-move --rig fiona`.
Sidecar:
[`plays/fiona-hello-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-hello-move.sidecar.json)

## YES movement (48 frames, 24 fps)

S fist nods at the chest:

![Fiona signs YES](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-yes-move.webp)

Made with `--shot sign-yes-move --rig fiona`.
Sidecar:
[`plays/fiona-yes-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-yes-move.sidecar.json)

## EIGHT movement (48 frames, 24 fps)

Index up, middle-to-thumb circle, ring and pinky extended:

![Fiona signs EIGHT](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-eight-move.webp)

Made with `--shot sign-eight-move --rig fiona`.
Sidecar:
[`plays/fiona-eight-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-eight-move.sidecar.json)

## FIRST movement (48 frames, 24 fps)

Index up, palm forward, shoulder travel:

![Fiona signs FIRST](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/webp/fiona-first-move.webp)

Made with `--shot sign-first-move --rig fiona`.
Sidecar:
[`plays/fiona-first-move.sidecar.json`](https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/plays/fiona-first-move.sidecar.json)

## Labeled strip (five rig stills, one image)

Built with Python Pillow (DejaVu Sans Bold labels on a dark
bar), committed as webp:

![Fiona's five compared signs](../docs/assets/fiona-five-strip.webp)

## True UI screenshots (Xvfb, no display)

`bpy.ops.screen.screenshot` returns black under Xvfb, so the
protocol splits in two: `prepare_ui_blend.py` builds the
`.blend` headless (imports the rig, hides the 2 m proxy
`Icosphere`, sets STICK bones), `screenshot_ui.py` opens it in
a GUI Blender under Xvfb, hides the armature, frames the mesh,
and holds the window while ImageMagick captures the X screen:

```bash
Xvfb :98 -screen 0 1600x900x24 &
LIBGL_ALWAYS_SOFTWARE=1 DISPLAY=:98 blender-5.2 \
  out/ui-fiona.blend --factory-startup \
  -P scripts/blender/screenshot_ui.py -- --hold 75 &
sleep 40
DISPLAY=:98 import -window root docs/assets/ui-fiona-viewport.webp
```

Findings that cost an evening: the fixture's hundred-unit bones
render as a solid blob in the viewport even in STICK mode under
software GL (renders never draw bones, so stills stay clean);
hide the armature for mesh screenshots. With no window manager,
the first-mapped window stays on top — kill stale Blenders by
PID before capturing, never by broad `pkill -f` from the same
shell (the pattern matches your own command line).

![Fiona in the Blender window](../docs/assets/ui-fiona-viewport.webp)

## Live site capture (headless Chromium, S3-hosted)

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
