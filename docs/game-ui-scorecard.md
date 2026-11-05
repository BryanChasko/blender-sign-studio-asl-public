# Game UI Scorecard

Grade any game screen in one pass. Score each row 0 (fail), 1
(partial), or 2 (pass). Total out of 24.

Ship bar: no zeros on rows 1, 4, 5. Total 20 or higher.

## Score it

| #   | Check                                                           | How to verify                                                   | 0 / 1 / 2 |
| --- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------- |
| 1   | Every input confirms in ~100 ms with sight + sound              | Press each control once. Note any silent press.                 |           |
| 2   | Screen shows at most ~4 live items; the rest hides until needed | Count persistent elements. Open menus only on demand.           |           |
| 3   | Text readable at couch distance; size adjustable                | Step back 3 m. Check size control exists.                       |           |
| 4   | No critical info by color alone                                 | Turn on a grayscale filter. Replay one round.                   |           |
| 5   | All speech and critical audio cues captioned, on by default     | Mute the game. Finish one objective.                            |           |
| 6   | All inputs remappable, menus included                           | Rebind jump/select. Check sensitivity and hold/toggle.          |           |
| 7   | First success lands in ~90 s with no manual                     | Hand to a new player. Time to first win.                        |           |
| 8   | In-world displays stay readable under worst light               | Stand in the brightest scene. Read every diegetic element.      |           |
| 9   | Damage source and next objective visible without reading        | Take a hit. Ask where to go next. No text allowed.              |           |
| 10  | Controls, icons, menu order match on every screen               | Map each verb. Check focus order with keyboard only.            |           |
| 11  | Mistakes undo free; only destructive acts confirm               | Misclick through shop/delete flows. Count lost progress.        |           |
| 12  | Per-axis assists exist; pause always available                  | Turn on one assist. Pause mid-combat. Check comms alternatives. |           |

## Fix in order

Fix zeros before ones. Fix rows 1, 4, 5 before anything
else — those lock players out entirely. Then fix by row
number; the list already ranks by player impact.

## Not scored yet

Motion/photosensitivity toggles, touch target size and
safe-area HUD, lobby and scoreboard flows, localization.
Add rows when your game ships those surfaces.
