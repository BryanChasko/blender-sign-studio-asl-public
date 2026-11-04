# ai-vs-rig verdicts (Wave 2, 2026-11-04)

SAM 3.1 status: 0 masks. All 20 segmentation calls (10 images x "hands" + 1 retry x "person signing") returned HTTP 429 rate_limit_exceeded ("Service temporarily unavailable"). Rerun 2026-11-04 ~16:50 UTC: 10 images x up to 12 paced attempts each (retry-after honored, 12 s spacing, "hands" + "person signing", stream true and false variants) still all HTTP 429; no masks, no agreement scores.
Raw error bodies saved verbatim in sam-\<slug\>-ai.json / sam-\<slug\>-still.json with result NO-MATCH.
Verdicts below rest on direct eyeball inspection of local copies byte-identical (sha256) to the segmented URLs.
Rubric: docs/meta-evidence/wonder-notes.md section Verdict rubric.

Lexicon refs (data/lexicon/lexicon.v1.json notes): THANK-YOU = B hand, fingertips on chin, palm toward signer.
HELLO = B hand beside forehead, palm out. YES = S fist, chest signing space.
EIGHT = dominant-hand 8 handshape (index up, middle bent to thumb), non-dominant uninvolved.
FIRST = index up, palm forward, slight wrist twist.

| slug      | AI fingers (R/L visible)                                                         | still fingers (R/L visible)                                    | handshape vs lexicon (AI)                                     | anatomy AI R/L | anatomy still R/L | verdict                       |
| --------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------- | -------------- | ----------------- | ----------------------------- |
| thank-you | R4+thumb flat under chin / L not visible                                         | R4 together at chin / L relaxed open, uninvolved               | B hand at chin yes, palm faces down not toward signer         | yes / n/a      | yes / yes         | FAIL (pose: palm orientation) |
| hello     | R4 extended + thumb stuck out sideways beside forehead, palm out / L not visible | R raised beside head, loose B, small in frame / L out of frame | 4 fingers yes, B thumb placement no (thumb abducted = 5-hand) | yes / n/a      | yes / n/a         | FAIL (thumb placement)        |
| yes       | L0 fist + thumb across at chest / R not visible                                  | R0 fist + thumb at chest side / L relaxed open                 | S fist at chest matches                                       | n/a / yes      | yes / yes         | PASS                          |
| eight     | R2 (index+middle V, no thumb contact) / L not visible                            | R1 up + middle-to-thumb circle (8) / L relaxed                 | shows 2, not 8                                                | yes / n/a      | yes / yes         | FAIL (handshape: 2 for 8)     |
| first     | R1 index up, palm forward, rest curled, thumb across / L not visible             | R1 index up, palm forward / L relaxed                          | matches index-up palm-forward                                 | yes / n/a      | yes / yes         | PASS                          |

Evidence, one line per fact:

- ai-thank-you.webp: single flat hand under chin, 4 fingertips + thumb nail visible, no extra digits.
- ai-thank-you.webp: fingertips point sideways, palm faces down toward neck, not toward face.
- still-thank-you.png (= spike-sign-thank-you.png sha256-identical): right fingertips contact chin/lip area, fingers together.
- ai-hello.webp: 4 fingers spread beside forehead, thumb extended outward to frame-left, palm toward camera.
- ai-hello.webp: 5 digits total extended on the signing hand.
- still-hello.png (= spike-sign-hello.png sha256-identical): right hand raised lateral to head, fingers loosely together.
- ai-yes.webp: left fist at chest height, 0 fingers extended, thumb folded across front, knuckles intact.
- still-yes.png (= spike-sign-yes.png sha256-identical): right S fist at chest side, thumb up across fingers.
- ai-eight.webp: right hand V shape, index + middle extended spread, ring/pinky folded, thumb hidden, no finger-thumb circle.
- still-eight.png (= spike-sign-eight.png sha256-identical): right index extended up, middle bent down to thumb forming circle.
- ai-first.webp: right index extended up, middle/ring/pinky curled, thumb across them, palm facing camera.
- still-first.png (= spike-sign-first.png sha256-identical): right index up palm-forward, others curled.
- No image on either side shows fused, missing, or supernumerary digits; all hands anatomically possible.
- All 10 segmented URLs verified HTTP 200 before the SAM pass; local copies sha256-identical to remote bytes.
- SAM request shape that passed validation: {"model":"sam-3.1","input":[{"role":"user","content":[{"type":"input_text","text":...},{"type":"input_image","image_url":...}]}],"stream":true}; parameters input_image and include_confidence rejected as unknown (HTTP 400).
- Key used read-only from ~/.config/muse/auth.json providers.meta.api_key; never printed or logged.

## Wave 3 review (Wonder, owner session)

- Viewed all 5 AI images: thank-you FAIL (palm down under chin),
  hello FAIL (thumb abducted = 5-hand), yes PASS (S fist),
  eight FAIL (V = 2), first PASS (index up palm forward).
  Confirms the table above; no silent edits made.
- Viewed still-thank-you.png (fingertips at chin, B hand,
  palm-to-signer) and still-eight.png (index up,
  middle-to-thumb circle): both match their lexicon notes.
  Control side stands.
- SAM: one clean single-image probe after the rerun window also
  returned 429. No further attempts today; masks remain a gap,
  verdicts stay labeled inspected-not-segmented.
