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
