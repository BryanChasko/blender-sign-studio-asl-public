# Gloss schema

Contracts between the ASL Gloss service, the lexicon, and the host
runtime. The ASL Gloss service accepts any compatible provider —
hand-authored ASL Gloss needs no model; versioned self-hosted options
are in the README provider table. Schema and lexicon share one
series: the `.v1` in `lexicon.v1.json` names the current additive
series. New signs are appended to the same file; a breaking contract
change starts a new file rather than rewriting entries in place.

## Lexicon entry (`data/lexicon/lexicon.v1.json`)

```json
{
  "gloss": "QUESTION",
  "category": "dialogue-flow",
  "type": "sign",
  "status": "proposed",
  "asllvd_ref": null,
  "clip": null,
  "face": ["brow-raise"],
  "reviewer": null,
  "notes": ""
}
```

| Field        | Meaning                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `gloss`      | Uppercase gloss label, unique in the file                                                                                                      |
| `category`   | Canonical slug from docs/lexicon.md: `greetings`, `dialogue-flow`, `truth-response`, `numbers`, `reference`, `subjects`, `emotion`, `cloud-ai` |
| `type`       | `sign` \| `fingerspell` \| `number` \| `letter`                                                                                                |
| `status`     | `proposed` -> `authored` -> `qa-passed` -> `ai-reviewed`; only `ai-reviewed` ships                                                             |
| `asllvd_ref` | American Sign Language Lexicon Video Dataset (ASLLVD) sign identifier used as authoring reference                                              |
| `clip`       | Path/URL of the authored animation clip, once built                                                                                            |
| `face`       | Additive face-layer clips that accompany the sign                                                                                              |
| `reviewer`   | Approver of record: set by the automated review for `ai-reviewed`, named signer for `reviewed`                                                 |
| `notes`      | Dialect, variation, or formation notes from review                                                                                             |

## ASL Gloss sequence (ASL Gloss service output)

One host line becomes an ordered, timed token list on the same clock
as the speech/viseme track:

```json
{
  "line_id": "host-welcome-01",
  "host": "host-a",
  "text": "Welcome Alex. Your turn.",
  "duration_ms": 2600,
  "tokens": [
    { "gloss": "WELCOME", "type": "sign", "start_ms": 0, "hold_ms": 600 },
    {
      "gloss": "A-L-E-X",
      "type": "fingerspell",
      "start_ms": 750,
      "hold_ms": 900
    },
    { "gloss": "YOUR-TURN", "type": "sign", "start_ms": 1800, "hold_ms": 600 }
  ]
}
```

## Validation rules (enforced by tests, not prompts)

1. Every `sign` token must exist in the lexicon with status
   `ai-reviewed` at ship time (`proposed` allowed in dev builds only).
2. Unknown words must be emitted as `fingerspell` tokens — the
   service may not invent an ASL Gloss.
3. Token timings must be monotonic and fit inside the line's speech
   duration; the runtime stretches transitions, never overlaps holds.
4. `face` clips are additive and optional per token; a missing face
   clip degrades to neutral, never blocks playback.
