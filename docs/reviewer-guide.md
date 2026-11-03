# Reviewer guide — teammate review, signer path if one joins

This project signs with a small, closed lexicon, and nothing ships
as American Sign Language (ASL) without passing review. Shipping
review is automated review ([docs/ai-review.md](docs/ai-review.md), grants
`ai-reviewed`). This guide defines the signer path below in case
one joins; until then the teammate shapes the lexicon.

## Your role

- Co-own the seed lexicon list ([docs/lexicon.md](docs/lexicon.md)): add, cut, or replace
  any proposed sign. Host dialogue serves the signing, not the reverse.
- Review authored clips (Blender renders / in-scene captures) for
  handshape, location, movement, orientation, and face grammar.
- Record approval directly: your name goes in the lexicon entry's
  `reviewer` field via PR approval, recording a `reviewed` mark
  for the future. Nothing waits on it.
- Credit is shared as agreed by teammates (to be recorded in
  [docs/team.md](docs/team.md) once the team is confirmed, per [docs/roadmap.md](docs/roadmap.md)).
  This is a teammate role, not a review-for-hire role.

## What to review against

- American Sign Language Lexicon Video Dataset (ASLLVD) citation
  form was the authoring reference (multi-angle video). Flag any
  deviation that changes meaning.
- In-scene legibility: hands inside frame, no occlusion by stage UI,
  signing space consistent per host.
- Face layer: brow raise on questions, headshake on negation, mouth
  morphemes where the sign requires them.
- Pacing: holds long enough to read at dialogue speed; fingerspelling
  spelled at learner-readable speed.

## How review happens

1. Author opens a PR with a clip batch + updated lexicon entries
   (`status: authored` from rocmaibox or `qa-passed` after
   segmentation visibility check). Macmini checks schema and timing;
   rocmaibox supplies renders.
2. Reviewer comments per gloss: approve, fix (with note), or cut.
3. Fixes re-render; cuts fall back to fingerspelling automatically.
4. If the signer path is active: reviewer approves the PR; entries move to `reviewed`.

## Labeling rules we all follow

- Generic host gestures are body language, never presented as signs.
- If a demo line cannot be signed with ai-reviewed signs, it is
  rewritten or fingerspelled. The script bends; the signing doesn't.
