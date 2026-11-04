# ai-vs-rig prompts

model: muse-image-1.0
endpoint: POST https://api.meta.ai/v1/images/generations
template: photorealistic adult woman signing ASL <GLOSS>, hands clearly visible, neutral background

- thank-you: photorealistic adult woman signing ASL THANK-YOU, hands clearly visible, neutral background
- hello: photorealistic adult woman signing ASL HELLO, hands clearly visible, neutral background
- yes: photorealistic adult woman signing ASL YES, hands clearly visible, neutral background
- eight: photorealistic adult woman signing ASL EIGHT, hands clearly visible, neutral background
- first: photorealistic adult woman signing ASL FIRST, hands clearly visible, neutral background

selection: fixed slugs thank-you, hello, yes plus first two alphabetically by gloss
among lexicon.v1.json entries with status ai-reviewed, non-null clip, and existing
docs/assets/spike-sign-<slug>.png: EIGHT (eight), FIRST (first).

hosted (public-read via bucket-policy Sid PublicReadAiVsRig on ai-vs-rig/*):

- https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ai-thank-you.webp
- https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ai-hello.webp
- https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ai-yes.webp
- https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ai-eight.webp
- https://bryanchasko-amazon-sumerian-hosts-asl-webp.s3.us-east-2.amazonaws.com/ai-vs-rig/ai-first.webp

## request log (reproducibility)

5 production calls + 1 shape probe, 2026-11-04, model muse-image-1.0:

```
POST https://api.meta.ai/v1/images/generations
Authorization: Bearer $MODEL_API_KEY   # oauth key, ~/.config/muse/auth.json
Content-Type: application/json
{"model": "muse-image-1.0", "prompt": "<per-sign prompt above>"}
```

measured outputs: 1280x1920 webp, 211–477 KB. unrecorded gap: the
producer logged the prompt but not the size/aspect params it sent —
whether 1280x1920 was requested or the default is unknown. all five
succeeded first attempt, zero retries.

demo poster call (owner, same session), exact payload:

```
POST https://api.meta.ai/v1/images/generations
{"model": "muse-image-1.0",
 "prompt": "wide video thumbnail, stylized 3D animated woman host signing American Sign Language on a dark stage, glowing caption bar and sound-wave icons beside her, cinematic, title space at top, no text"}
```

response: `{"data": [{"b64_json": "..."}]}`, saved to
docs/assets/demo-poster.webp (RIFF webp). one call, first attempt ok.
