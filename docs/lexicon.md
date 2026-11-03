# Lexicon — closed host-dialogue domain

The lexicon is deliberately small: only signs host dialogue
needs, each one authored from American Sign Language Lexicon Video
Dataset (ASLLVD) citation form and AI-reviewed
(`docs/ai-review.md`) before use.
Anything outside this list is fingerspelled — never improvised.

Machine-readable source of truth: `data/lexicon/lexicon.v1.json`
(the `.v1` names the current additive series — see
[gloss-schema.md](gloss-schema.md)).
Schema and entry fields: [ASL Gloss schema](gloss-schema.md).

## Categories (58 signs)

| Category           | Slug             | Signs (gloss)                                                                              | Count |
| ------------------ | ---------------- | ------------------------------------------------------------------------------------------ | ----- |
| Greetings / social | `greetings`      | HELLO, THANK-YOU, GOODBYE, PLEASE, SORRY, WELCOME                                          | 6     |
| Dialogue flow      | `dialogue-flow`  | HELP, FINISH, UNDERSTAND, REPEAT (+AGAIN alias), QUESTION, ANSWER, YOUR-TURN, MY-TURN      | 8     |
| Truth / response   | `truth-response` | YES, NO, RIGHT, WRONG, MAYBE, TRUE, FALSE                                                  | 7     |
| Numbers            | `numbers`        | ONE–NINE, FIRST, SECOND, HOW-MANY                                                          | 12    |
| Reference          | `reference`      | ME, YOU, THIS, WHAT, WHERE, WHO, THAT, HERE                                                | 8     |
| Emotion            | `emotion`        | HAPPY, SAD, FUN                                                                            | 3     |
| Subjects           | `subjects`       | TIME, DAY, PEOPLE, WORK                                                                    | 4     |
| Cloud / AI         | `cloud-ai`       | COMPUTER, LEARN, INTERNET, VIDEO (signs); CLOUD, AWS, DATA, AI, APP, ROBOT (fingerspelled) | 10    |

Final list is the owner's call; this table is a draft. Open
calls: SORRY placement, REPEAT-vs-AGAIN citation form,
YOUR-TURN/MY-TURN construction, FALSE vs F-A-L-S-E, FUN vs FUNNY,
THAT form, HERE vs THIS.

## Rules

1. A sign enters the lexicon as `proposed`. It becomes
   `ai-reviewed` by passing `docs/ai-review.md`, with the
   checklist output recorded in the PR.
2. Only `ai-reviewed` signs may appear in the shipped demo. The ASL Gloss
   service must refuse or fingerspell anything else. The `reviewed`
   mark is reserved for a future signer; entry notes saying
   "reviewer to confirm" are superseded by ADR 0004.
3. Fingerspelling (26 alphabet poses) covers proper nouns and every
   out-of-lexicon word. Slow, clear, and correct beats fast and wrong.
4. Regional/dialect variation is noted in the entry when found;
   the build ships one citation form per gloss.
5. Generic host `gesture.glb` clips (wave, heart, big, ...) are body
   language, not American Sign Language (ASL), and are never entered
   in this lexicon.

## Technical vocabulary (v2, proposed)

100 tech-domain signs for cloud/developer host dialogue. Additive v2
per `docs/asl-gloss-core-rules.md` — all entries are `proposed`,
pending AI review. Ships only after passing `docs/ai-review.md`.

Sources:

- CNCF Cloud Native Glossary (https://github.com/cncf/glossary) —
  cloud-native terminology
- Sign Language Tech Interview (https://github.com/signlanguagetech/sign-tech-interview) —
  developer skill domains (JavaScript, TypeScript, React, Angular,
  Node, Flutter, programming paradigms, component lifecycle)

### v2 categories

| Category             | Slug                   | Count |
| -------------------- | ---------------------- | ----- |
| Cloud Native         | `cloud-native`         | 22    |
| Architecture         | `architecture`         | 19    |
| Dev Workflow         | `dev-workflow`         | 21    |
| Tech Verbs           | `tech-verbs`           | 20    |
| Security             | `security`             | 10    |
| Languages/Frameworks | `languages-frameworks` | 8     |

### v2 type breakdown

| Type        | Count |
| ----------- | ----- |
| sign        | 56    |
| fingerspell | 24    |
| compound    | 20    |

Machine-readable source: `data/lexicon/lexicon.v2.json`

## Review workflow

Per clip: author in Blender from ASLLVD reference ->
segmentation visibility quality assurance (QA) (MediaPipe default,
Segment Anything Model 3 (SAM 3) swap) -> AI review
(`docs/ai-review.md`) -> status change in the JSON (one PR per
batch, checklist output in the PR). Signer path, if one ever
joins: [reviewer-guide.md](reviewer-guide.md).
