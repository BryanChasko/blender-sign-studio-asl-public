# ASL Gloss core rules

ASL Gloss is the written, uppercase label for a sign — the standard
linguistics notation used to name signs (for example HELLO, QUESTION,
WORK). It is the intermediate representation between English host text
and the chereme animation clips. It is hand-authorable and requires no
model.

## Core rules

1. ASL Gloss labels are uppercase and unique within the lexicon file.
2. Every `sign` token must exist in the lexicon at `ai-reviewed`
   status before it ships (`proposed` is dev-build only).
3. Unknown or out-of-lexicon words are emitted as fingerspell tokens —
   the service never invents a new sign.
4. Token timings are monotonic and fit inside the host line's speech
   duration; transitions stretch, holds never overlap.
5. Face-layer clips are additive and optional per token; a missing
   face clip degrades to neutral and never blocks playback.
6. Fingerspelling uses the 26 alphabet poses (A–Z) spelled letter by
   letter; proper nouns and names are fingerspelled by design.
7. Lexicon growth is additive — append new signs, start a new versioned
   file for a breaking contract change, never rewrite a shipped entry's
   meaning.

## Fixed lexicon, not open translation

The build signs only a fixed 58-sign seed lexicon covering everyday
host dialogue, not open-ended English-to-ASL translation (which is an
unsolved research problem and would be misleading if claimed).
Everything outside the fixed set is fingerspelled.

## See also

- [gloss-schema.md](gloss-schema.md) — machine schema for ASL Gloss
  sequences and lexicon entries
- [lexicon.md](lexicon.md) — the sign list (58 signs, categories)
- [decisions/0001-closed-domain-lexicon.md](decisions/0001-closed-domain-lexicon.md) —
  architecture decision record for the fixed-lexicon approach
