# Screenshot rounds — sign feedback plan

Each round produces pixels a human grades. No verdict without
a screenshot. Rounds run in order; a round can reopen any
earlier sign.

## Round 0 — baseline (done)

Live-site audit: `docs/site-audit/` screenshots 01–26,
`docs/interaction-matrix.md` 18/24. Per-sign stills:
`docs/assets/`, AI comparison set: `docs/ai-vs-rig/`,
scorecards: `docs/ai-vs-rig/scorecards.md`,
`docs/reviewed-signs.md`.

## Round 1 — citation correctness, 58 glosses

1. All 58 v1 glosses pose since the DRAFT scaffold: render
   frame-36 citation stills in one command
   (`--shot sign-<gloss>` works for every gloss; hand-written
   entries keep their exact filenames). 35 stills are
   UNSCORED drafts awaiting grading.
2. Build contact sheets, 6 signs per sheet, elbow + top of
   head in frame.
3. Compare each still against its Lifeprint citation.
   Record PASS / FAIL / UNSCORED in `docs/reviewed-signs.md`
   with the still filename as evidence.
4. Exit: zero UNSCORED. Every FAIL names the wrong chereme
   (handshape, place, movement, palm).

## Round 2 — card crops, live page

1. Screenshot every deck card on the live page at card size
   (?host=fiona&shot=signing and &shot=face).
2. Fail any card where the thumb cuts the elbow or the top
   of the head. Fail any gloss label that wraps mid-word.
3. Exit: all shipped cards pass; fails filed with crops.

## Round 3 — integration flows

1. Screenshot: quiz prompt (answer must NOT be visible),
   lineup build, trash + undo toast, quiz verdicts
   (right/wrong readable in grayscale).
2. Screenshot: 390 px and 768 px widths, same flows.
3. Exit: quiz unspoiled, verdicts pass grayscale, zero
   overlap at either width.

## Round 4 — motion

1. Capture 24 fps strips for the 5 compared signs plus any
   Round 1 FAILs. Signs move; stills are citations.
2. Grade emphasis frame + full arc per sign.
3. Exit: every reviewed sign has a graded motion strip.

## Standing rules

- One command per still. Same command, same pixels.
- Verdicts stay author-inspected until a signer confirms.
  Say so on every sheet.
- New glosses enter at UNSCORED. They earn a verdict only
  from a screenshot.
