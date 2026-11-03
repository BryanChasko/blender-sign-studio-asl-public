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
