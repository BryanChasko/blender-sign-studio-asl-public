# Interaction Matrix — live-site audit method

Score from pixels and clicks, never from code reads. Each row
is one user action: what you do, what you expect, what you see.

## How to run it

1. Load the URL in a real browser. Screenshot load state.
2. Work each action top to bottom. Screenshot each result.
3. Score the game-UI scorecard row only from what the
   screenshots and DOM state show. Mark the rest unobserved.
4. File issues only for screenshot-grounded findings. Link the
   screenshot. Name what you did not test.

## Audit 2026-11-05 — blender-sign-studio (COMPLETE, pixel-grounded)

Target: `https://bryanchasko.com/blender-sign-studio/`.
Method: headless Chromium, real clicks, one screenshot per
step (`docs/site-audit/10`–`18`). The deck renders async
(~5 s, 59 cards) — wait for `button.deck-card` before acting.

Total: 13/24. Ship bar fails: rows 6 and 11 score 0.

| #   | Action                  | Expected                   | Actual (evidence)                                                                              |
| --- | ----------------------- | -------------------------- | ---------------------------------------------------------------------------------------------- |
| 0   | Open the URL            | App loads                  | 200 after outage (10). Earlier: 404 x3 + 301 into 404 (02, fixed)                              |
| 1   | Tap card, tap mid-play  | Confirm each tap           | First tap: gold outline + PLAYING + ring + xp + streak (11, 12). Mid-play: no busy cue (12). 1 |
| 2   | Count default surface   | ~4 live items              | Play mode: 8 cards + scrub + status. Builder: ~40 controls (15, 17). 1                         |
| 3   | Read smallest text      | 0.75 rem min, size control | 0/5 counters, 0.0s labels tiny; contrast good; no size control (10-13). 1                      |
| 4   | Grayscale verdicts      | Shape/icon twin            | Every observed state has a text twin (PLAYING/IDLE, streak N, n/5). No quiz surfaced. 2        |
| 5   | Finish by captions      | Caption track              | Zero caption-class nodes; two polite live regions ("watch..."). 1                              |
| 6   | Remap an input          | Rebind UI                  | No keybind UI; Tab reaches skip link, native focus works. 0                                    |
| 7   | New player, first win   | Success in ~90 s           | Zero gates; loader % + tips; first tap plays in seconds (10, 11). 2                            |
| 8   | Read timeline blocks    | Readable at a glance       | gather/hold/release blocks legible; host readable (17). 2                                      |
| 9   | Read state at a glance  | One consistent state       | "ready! tap a card." + IDLE/PLAYING coherent (15-17). Loader-vs-READY seen once (01). 1        |
| 10  | Same verb everywhere    | One label per action       | play / play sequence / preview / play sample sequence / replay; "moon"; "+/-" (15, 17). 1      |
| 11  | Clear a 2-item sequence | Confirm or undo            | One click wipes both; no dialog, toast, or undo button (17, 16). 0                             |
| 12  | Slow down, pause        | Granular assists           | slow-mo toggle, hold ms, pause, 5 camera presets, sound checkbox (15). 1                       |

## Standing rule

A row without a screenshot is a hypothesis, not a finding.
File it as "unconfirmed" or do not file it.

## Audit 2026-11-05 (evening) — evolved build (v0.074)

Same method. Screenshots `docs/site-audit/20`–`26`.

Total: 18/24 (was 13/24). One zero remains: row 6.

- Row 1 → 2: mid-play tap now queues the sign and counts
  practice (lineup grows, ring 2/5). #143 fixed.
- Row 5 → 2: now-signing chip + status lines
  ("sign 1 of 1: thank-you — hands down",
  "playing sign 1 of 1: thank-you"). #142 fixed.
- Row 8 → 1: quiz prompt shows the answer gloss in the
  top-center chip during "watch, then pick the sign..."
  (26-quiz-prompt.png). New issue.
- Row 10 → 2: playback collapsed to icon buttons;
  theme is an icon. #140 fixed.
- Row 11 → 2: trash clear now shows
  "cleared 2 signs — tap undo to bring it back."
  #138 fixed.
- Builder mode toggle gone; tap plays and queues; quiz
  entry exists ("guess the sign!"). #141 fixed.
- Unchanged: row 6 remap (no UI text found, #137),
  row 3 text size (no control, #139).
