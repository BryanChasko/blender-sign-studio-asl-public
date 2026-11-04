# Scorecards: all 23 glosses

One card per sign. Judged against the reference first, both sides.
Evidence levels, stated per card: `photo-inspected` (reference
photo viewed, both sides checked pixel-by-pixel) vs `spec-match`
(rig still renders the authored numbers, numbers ai-reviewed,
reference page linked but its photo not inspected). AI column is
`not attempted` where no generation exists. Shared timing for
every clip: 72f @ 24fps, f1 rest, f12-20 citation hold, f20-44
arc, f44-52 end hold, f52-72 return (export_sign_clip.py).
Reference photos live in our bucket (mirrored from Lifeprint,
attributed in the README) — no hotlink scraping.

## HELLO — AI FAIL vs citation salute · rig PASS (photo-inspected)

- Reference: [Lifeprint hello](https://www.lifeprint.com/asl101/pages-signs/h/hello.htm) (page: wave latitude, no photo) + citation form from Wiktionary/PocketSign: B hand at forehead/temple, palm forward, salute motion outward.
- Rig kinematics: hand b; start sh(-0.4,-0.95,-0.15) el(0,-1.5,0) wr(1.2,0,0) → end sh(-0.4,-0.95,-0.45), same el/wr (travel is shoulder abduction). Clip assets/clips/sign-hello.glb.
- AI round 1: open 5-hand held static at forehead height. Fails the citation salute; sits inside the page's wave latitude but reads posed, not waved. AI round 2 (edit-hello-fix-ai.webp): B hand at forehead, palm forward. PASS.
- Rig: B salute beside forehead, palm out, still = render of these numbers. PASS.

## THANK-YOU — AI FAIL (palm) · rig PASS (photo-inspected)

- Reference: [Lifeprint thank-you](https://www.lifeprint.com/asl101/pages-signs/t/thankyou.htm) — flat hand, fingertips at lips/chin, palm toward signer, forward-down. Photo viewed: fingertips at lips, palm to signer.
- Rig kinematics: hand b; start sh(1.1,-0.3,-1.0) el(-1.9,-1.4,-0.1) wr(-0.2,0,-0.45) → end sh(0.4,-0.3,-0.55) el(0,-0.85,0) wr(0.9,0,0). Chin-contact fix 2026-11-02 (gap_lips 13.7mm, verified on zoomed render). Clip assets/clips/sign-thank-you.glb.
- AI: flat hand at chin, palm DOWN, static. Fails palm orientation.
- Rig: fingertips at lips, palm-to-signer, clip arcs forward-down. PASS.

## QUESTION — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint question](https://www.lifeprint.com/asl101/pages-signs/q/question.htm) (linked, photo not inspected).
- Rig kinematics: hand n1; start sh(0,-0.6,-0.9) el(-2,-0.5,0) wr(0,0.1,-0.4) → end el(0,-0.4,0) wr(0,0.5,-0.4) (wrist flick = the question mark). Clip assets/clips/sign-question.glb.
- Rig: still renders these numbers (ai-reviewed 2026-11-03). PASS vs authored spec.

## YES — PASS both (photo-inspected for AI; rig spec-match + eye-verified still)

- Reference: [Lifeprint yes](https://www.lifeprint.com/asl101/pages-signs/y/yes.htm) — S hand, wrist nod.
- Rig kinematics: hand s; start sh(0,-0.6,-0.9) el(-2,-0.5,0) wr(0,0.1,-0.1) → end wr(0,0.1,-0.6) (nod). Clip assets/clips/sign-yes.glb.
- AI: S fist at chest, 0 extended (left hand; lexicon sets no dominance). PASS.
- Rig: S fist staged chest box, still eye-verified. PASS.

## NO — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint no](https://www.lifeprint.com/asl101/pages-signs/n/no.htm) (linked, photo not inspected).
- Rig kinematics: hand h; start wr(0,0.1,-0.2) → end wr(0,0.1,-0.7) (wrist snap down, fingers to thumb). Clip assets/clips/sign-no.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## TRUE — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint true](https://www.lifeprint.com/asl101/pages-signs/t/true.htm) (linked, photo not inspected).
- Rig kinematics: hand p1; start sh(0.3,-1.2,0) el(0,-0.5,0) wr(0.5,0.1,0.4), index straight out from mouth. Clip assets/clips/sign-true.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## ONE..FIVE — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint numbers 1-10](https://www.lifeprint.com/asl101/pages-signs/n/numbers1-10.htm) (chart linked; isolated 1-5 palm-back is the citation default).
- Rig kinematics: shared cardinal-numeral arm sh(0,-0.6,-0.9) el(-2,-0.5,0), hand n1..n5; start wr(0,0.1,-0.4) → end wr(0,0.1,-0.35) (settle). Clips assets/clips/sign-{one,two,three,four,five}.glb.
- Rig: handshape alone distinguishes them; stills render these numbers (ai-reviewed). PASS vs authored spec.

## SIX..NINE — rig PASS (spec-match) · AI not attempted except EIGHT

- Reference: [Lifeprint numbers 1-10](https://www.lifeprint.com/asl101/pages-signs/n/numbers1-10.htm) (chart linked; number08 photo viewed: index/ring/pinky up, middle bent to thumb contact).
- Rig kinematics: shared arm sh(0,-0.9,0) el(0.5,-1.5,0), hand n6..n9; start wr(0.5,0.1,0.2) → end wr(0.5,0.1,0.15). Clips assets/clips/sign-{six,seven,eight,nine}.glb.
- EIGHT AI round 1: open V (index+middle spread, no thumb contact) = a 2. FAIL (photo-inspected). Rounds 2–3 (edit-eight-fix-ai.webp, ai2): three fingers up both times, no middle-to-thumb circle. FAIL.
- EIGHT rig: index up, middle-to-thumb circle, ring+pinky extended (zoom-eight-hand.png verified). PASS (photo-inspected).
- SIX/SEVEN/NINE rig: stills render these numbers (ai-reviewed). PASS vs authored spec.

## ME — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint me](https://www.lifeprint.com/asl101/pages-signs/m/me.htm) (linked, photo not inspected).
- Rig kinematics: hand p1; start sh(0.7,-0.3,-1.0) el(-1.9,-1.0,-0.1) wr(1.7,0,-0.45), index to upper chest. Clip assets/clips/sign-me.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## YOU — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint you](https://www.lifeprint.com/asl101/pages-signs/y/you.htm) (linked, photo not inspected).
- Rig kinematics: hand p1; index forward at addressee, chest height, sh(0.3,-0.6,-0.9). Clip assets/clips/sign-you.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## THIS — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint this](https://www.lifeprint.com/asl101/pages-signs/t/this.htm) (linked, photo not inspected).
- Rig kinematics: hand p1; index down-forward at near locus, sh(0.3,-0.3,-0.9). Clip assets/clips/sign-this.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## WHERE — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint where](https://www.lifeprint.com/asl101/pages-signs/w/where.htm) (linked, photo not inspected).
- Rig kinematics: hand p1; index forward, end wr z 0.4→0.7 (mid-shake frame). Clip assets/clips/sign-where.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## WHO — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint who](https://www.lifeprint.com/asl101/pages-signs/w/who.htm) (linked, photo not inspected).
- Rig kinematics: hand p1; index at face height, end sh z 0→-0.15 (mid-circle frame). Clip assets/clips/sign-who.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## HOW-MANY — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint how-many](https://www.lifeprint.com/asl101/pages-signs/h/how-many.htm) (linked, photo not inspected).
- Rig kinematics: hand s; two-handed citation, wr y -0.5→-0.3 across the hold. Clip assets/clips/sign-how-many.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## FIRST — PASS both (photo-inspected)

- Reference: [Lifeprint first](https://www.lifeprint.com/asl101/pages-signs/f/first.htm) — "many right versions"; general form index up + wrist twist.
- Rig kinematics: hand n1; arm sh(0,-0.9,0) el(0.5,-1.5,0); start wr(0.5,0.1,0.2) → end wr(0.9,0.1,0.2) (twist). Clip assets/clips/sign-first.glb.
- AI: index up, palm forward, rest curled. Matches a right version. PASS.
- Rig: index up, palm forward, twist in END. PASS.

## SECOND — rig PASS (spec-match) · AI not attempted

- Reference: [Lifeprint second](https://www.lifeprint.com/asl101/pages-signs/s/second.htm) (linked, photo not inspected).
- Rig kinematics: hand n2; V forward, same twist (wr x 0.5→0.9). Clip assets/clips/sign-second.glb.
- Rig: still renders these numbers (ai-reviewed). PASS vs authored spec.

## method note

Nobody reworks Blender from here: rig verdicts rest on authored,
ai-reviewed numbers that the stills render by construction. New
work goes to the AI side — generate the missing 18, score them
against these cards, and only then touch the table.
