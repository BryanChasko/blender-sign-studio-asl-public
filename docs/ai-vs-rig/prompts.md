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

measured outputs: 1280x1920 webp. per-sign bytes on S3:
thank-you 477090, hello 267572, yes 349738, eight 265104, first 211078. unrecorded gap: the producer logged the prompt but not the
size/aspect params it sent — whether 1280x1920 was requested or the
default is unknown. no seed recorded (not a param of this
endpoint's logged shape). all five succeeded first attempt, zero
retries. reference mirrors on S3: ref-thank-you.jpg 434914,
ref-yes.jpg 34748, ref-eight.jpg 10351, ref-first.jpg 35256.

demo poster call (owner, same session), exact payload:

```
POST https://api.meta.ai/v1/images/generations
{"model": "muse-image-1.0",
 "prompt": "wide video thumbnail, stylized 3D animated woman host signing American Sign Language on a dark stage, glowing caption bar and sound-wave icons beside her, cinematic, title space at top, no text"}
```

response: `{"data": [{"b64_json": "..."}]}`, saved to
docs/assets/demo-poster.webp (RIFF webp). one call, first attempt ok.

## round 2: edits endpoint (same session)

no ControlNet-style pose conditioning exists on the API; the lever
is `/v1/images/edits` (OpenAI-images compatible, multipart) plus the
Responses API's interleaved text+image input. test: feed the model
our knowledge (the failed AI image, the rig still) with a corrective
instruction. 2 calls, both HTTP 200 first attempt:

```
POST https://api.meta.ai/v1/images/edits  (multipart/form-data)
- model=muse-image-1.0
- image=@edit-ai-input.png   (ai-thank-you.webp converted to PNG)
- prompt="Keep the same woman, framing and neutral background. Fix
  only her signing hand: flat hand at the chin, fingertips touching
  the chin, palm facing toward her, the ASL sign for thank-you."
-> docs/ai-vs-rig/edit-thank-you-fix-ai.webp (RIFF webp)

- image=@edit-rig-input.png  (spike-sign-thank-you.png)
- prompt="Photorealistic adult woman signing ASL thank-you, same pose
  as the reference: flat hand at the chin, fingertips at the lips,
  palm facing toward her, neutral background."
-> docs/ai-vs-rig/edit-thank-you-from-rig.webp (RIFF webp)
```

both PASS the reference rubric on inspection (palm toward signer,
fingertips at chin/lips). verdicts in verdicts.md round-2 section.

## round 3: hello fix lands, eight resists (same key, $21.80 budget session)

same lever as round 2, two more failures. 4 calls, all HTTP 200
first attempt:

```
POST https://api.meta.ai/v1/images/edits  (multipart/form-data)
- model=muse-image-1.0
- image=@edit-hello-input.png  (ai-hello.webp converted to PNG)
- prompt="Keep the same woman, framing and neutral background. Fix
  only her signing hand: B hand, flat hand with fingers together,
  held at the forehead, palm facing forward, the ASL citation
  salute for hello."
-> docs/ai-vs-rig/edit-hello-fix-ai.webp (1280x1920 webp, 283120 B)
   PASS: B hand at forehead, palm forward.

- image=@edit-eight-input.png  (ai-eight.webp converted to PNG)
- prompt="Keep the same woman, framing and neutral background. Fix
  only her signing hand: index finger up, middle finger bent to
  touch the thumb, ring finger and pinky extended, the ASL number
  eight. Not a V shape."
-> docs/ai-vs-rig/edit-eight-fix-ai.webp (1280x1920 webp, 307640 B)
   FAIL: three fingers up, no middle-to-thumb contact.

- image=@edit-eight-input.png  (same source, sharper instruction)
- prompt="Keep the same woman, framing and neutral background. Fix
  only her signing hand, ASL number eight: index finger pointing
  straight up, ring finger and pinky pointing straight up, middle
  finger bent down so its tip touches the tip of the thumb forming
  a closed circle. Three fingers up plus a middle-to-thumb circle."
-> docs/ai-vs-rig/edit-eight-fix-ai2.webp (1280x1920 webp, 308836 B)
   FAIL: still three up, thumb misses the middle finger. the model
   cannot close a finger-contact circle. stop here; two attempts
   is the finding.

POST https://api.meta.ai/v1/images/generations
- model=muse-image-1.0
- prompt="Stylized 3D game character rig: smooth gray mannequin with
  a visible bone skeleton inside, one hand raised mid-sign, dark
  studio background, teal rim light, digital illustration, no text,
  no words, no letters"
-> docs/assets/concepts-illustration.webp (1280x1920 webp, 253348 B)
   illustration for the Concepts section, captioned as such.
```

verdicts updated in verdicts.md round-3 section.
