# ai-vs-rig verdicts (Wave 2, 2026-11-04; reference-grounded 2026-11-04)

SAM 3.1 status: 0 masks. All 20 segmentation calls (10 images x "hands" + 1 retry x "person signing") returned HTTP 429 rate_limit_exceeded ("Service temporarily unavailable"). Rerun 2026-11-04 ~16:50 UTC: 10 images x up to 12 paced attempts each (retry-after honored, 12 s spacing, "hands" + "person signing", stream true and false variants) still all HTTP 429; no masks, no agreement scores. Owner probe after the window: 429. No further attempts today.
Raw error bodies saved verbatim in sam-\<slug\>-ai.json / sam-\<slug\>-still.json with result NO-MATCH.
Verdicts below are inspected against the reference spec, not segmented.

## reference basis (Lifeprint, linked not vendored — third-party photos stay off this repo)

- THANK-YOU: [ASL "thank you"](https://www.lifeprint.com/asl101/pages-signs/t/thankyou.htm) — flat hand, fingertips start at lips/chin, palm toward signer, forward-down toward addressee. Reference photo viewed: fingertips at lips, palm facing signer.
- HELLO: [ASL "hello"](https://www.lifeprint.com/asl101/pages-signs/h/hello.htm) — no fixed form: "just wave", side-to-side, "no one specific type of wave". The lexicon pins one variant (B-hand salute beside forehead).
- YES: [ASL "yes"](https://www.lifeprint.com/asl101/pages-signs/y/yes.htm) — "S" hand, wrist nod (fist = head nodding).
- EIGHT: [ASL numbers 1-10](https://www.lifeprint.com/asl101/pages-signs/n/numbers1-10.htm) — 8 = index/ring/pinky up, middle bent down to thumb contact (chart photo viewed).
- FIRST: [ASL "first"](https://www.lifeprint.com/asl101/pages-signs/f/first.htm) — "many right versions"; general form index up with wrist-twist variants.

## verdicts (AI and rig each judged against the reference, not against each other)

| sign      | reference says                                       | Muse Image vs reference                                                                                          | Fiona rig vs reference                                                               | verdict                                                              |
| --------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| thank-you | flat hand at lips/chin, palm to signer, forward-down | flat hand at chin, palm DOWN, static                                                                             | fingertips at lips, palm-to-signer, clip arcs forward-down                           | AI FAIL (palm), rig PASS                                             |
| hello     | no fixed form — any natural wave                     | open 5-hand held static at forehead height; inside the reference's latitude as a wave, but posed high and frozen | B-hand salute beside forehead (one pinned variant)                                   | AI FAIL vs authored spec (latitude noted), rig PASS vs authored spec |
| yes       | S fist, wrist nod                                    | S fist at chest, 0 extended (left hand; lexicon sets no dominance)                                               | S fist at chest                                                                      | PASS both                                                            |
| eight     | index/ring/pinky up, middle-to-thumb contact         | open V = index+middle spread, no thumb contact: a 2, not an 8                                                    | index up, middle-to-thumb circle, ring+pinky extended (zoom-eight-hand.png verified) | AI FAIL (handshape), rig PASS                                        |
| first     | many right versions; index up + wrist twist          | index up, palm forward, rest curled                                                                              | index up, palm forward                                                               | PASS both                                                            |

Right hand, wrong sign: the three AI failures are chereme errors (palm, thumb, handshape), none anatomical — every hand shown has the correct digit count.

Evidence (comparison crops, 720px, same framing per sign):

- cmp/cmp-\<slug\>-ai.webp: AI crop (face + signing hand, hand fully visible).
- cmp/cmp-\<slug\>-rig.png: rig crop (face + signing hand from the citation still).
- cmp/zoom-eight-hand.png: rig eight hand close-up (middle-to-thumb circle, ring+pinky extended).
- Full frames: docs/ai-vs-rig/ai-\<slug\>.webp + docs/assets/spike-sign-\<slug\>.png, sha256-identical to the segmented URLs.
- All 10 segmented URLs verified HTTP 200 before the SAM pass.
- SAM request shape that passed validation: {"model":"sam-3.1","input":[{"role":"user","content":[{"type":"input_text","text":...},{"type":"input_image","image_url":...}]}],"stream":true}; parameters input_image and include_confidence rejected as unknown (HTTP 400).
- Key used read-only from ~/.config/muse/auth.json providers.meta.api_key; never printed or logged.

## Wave 3 review (Wonder, owner session)

- Viewed all 5 AI images and the thank-you/eight reference photos; verdicts above confirm the table. Reference grounding added after review; no silent edits to scores.
- Viewed still-thank-you.png (fingertips at chin, palm-to-signer) and still-eight.png + zoom (index up, middle-to-thumb circle, ring+pinky extended): both match their Lifeprint pages. Control side stands.
- SAM: clean single-image probes after the rerun window also returned 429. No further attempts today; verdicts stay labeled inspected-not-segmented.
