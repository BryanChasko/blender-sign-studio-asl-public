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

## Audit 2026-11-05 — blender-sign-studio (BLOCKED)

Target: `https://bryanchasko.com/blender-sign-studio/`.
Evidence: `docs/site-audit/01-loaded.png` (app, loading),
`docs/site-audit/02-ready.png` (404 page).

| #   | Action                  | Expected                        | Actual (evidence)                                                                                  |
| --- | ----------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------- |
| 0   | Open the URL            | App loads                       | App loaded once (01), then 404 x3 via curl; `/signing-hosts/` 301s into the 404 (02)               |
| 1   | Tap a sign card         | Plays in ~100 ms, sight + sound | BLOCKED — site down before interaction                                                             |
| 2   | Count default surface   | ~4 live items                   | 4 host cards + 6 sign cards + loader + tips + scrub + status visible in 01; shelves collapsed      |
| 3   | Read smallest text      | 0.75 rem min, size control      | 0/5 counters and 0.0s labels tiny in 01; no size control visible                                   |
| 4   | Grayscale quiz verdicts | Shape/icon twin                 | BLOCKED — never reached quiz                                                                       |
| 5   | Mute, finish objective  | Captions carry it               | BLOCKED — never played a sign                                                                      |
| 6   | Remap an input          | Rebind UI                       | BLOCKED — no interaction possible                                                                  |
| 7   | New player, first win   | Success in ~90 s, no manual     | Zero-gate path visible in 01 ("tap a card to play it now", loader % + tips); win itself unobserved |
| 8   | Long gloss caption      | Full text shows                 | BLOCKED — no caption rendered while loading                                                        |
| 9   | Read state at a glance  | One consistent state            | CONTRADICTION in 01: loader says "still loading", pill says READY                                  |
| 10  | Same verb everywhere    | One label per action            | "+/-", "reset", "views^", "play/pause" visible in 01; full map needs interaction                   |
| 11  | Clear the lineup        | Confirm or undo                 | BLOCKED — never reached lineup                                                                     |
| 12  | Pause mid-play          | Instant, granular               | BLOCKED — never played                                                                             |

## Standing rule

A row without a screenshot is a hypothesis, not a finding.
File it as "unconfirmed" or do not file it.
