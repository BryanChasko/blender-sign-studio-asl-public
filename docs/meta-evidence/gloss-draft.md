# Gloss draft: host line "Hello! Yes, thank you for coming."

New host line, no existing sequence. Both drafts use only ai-reviewed
signs from `data/lexicon/lexicon.v1.json` (unknown words as fingerspell).

## Spark draft (this file's author runs on Muse Spark via Muse Code: this IS the Spark contribution)

Machine-readable copy: `docs/meta-evidence/gloss-draft-spark.json`.

```json
{
  "line_id": "host-hello-thanks-01",
  "host": "fiona",
  "text": "Hello! Yes, thank you for coming.",
  "duration_ms": 3200,
  "tokens": [
    { "gloss": "HELLO", "type": "sign", "start_ms": 0, "hold_ms": 500 },
    { "gloss": "YES", "type": "sign", "start_ms": 650, "hold_ms": 400 },
    { "gloss": "THANK-YOU", "type": "sign", "start_ms": 1200, "hold_ms": 600 },
    {
      "gloss": "C-O-M-I-N-G",
      "type": "fingerspell",
      "start_ms": 1950,
      "hold_ms": 1000
    }
  ]
}
```

Choices: HELLO / YES / THANK-YOU cover the signed content; "for" is
dropped as an ASL function word and "coming" is fingerspelled hyphenated
per gloss convention. Passed validation on the first pass, so there is
no failed first pass to record.

## Glimmer draft (local model, `http://127.0.0.1:8181/v1`)

Raw response: `docs/meta-evidence/gloss-glimmer-raw.json`.
Requested via `POST /v1/completions` (primed JSON prefix, `n_predict: 85`).

Verbatim continuation returned (`finish_reason: length`, truncated at 85 tokens):

```json
{"gloss":"YES","type":"sign","start_ms":500,"hold_ms":400},
{"gloss":"THANK-YOU","type":"sign","start_ms":900,"hold_ms":600},
{"gloss":"FOR","type":"fingerspell","start_ms":1500,"hold_ms":300},
{"gloss":"COMING","type":"fingerspell","start_ms":1800," ...
```

Glimmer token choices: HELLO (primed), YES, THANK-YOU, FOR (fingerspell),
COMING (fingerspell, timing cut off). Draft is incomplete: no closing
brackets, no final hold/duration, so it was not run through the validator.

## Comparison

- Same sign core: both drafts choose HELLO, YES, THANK-YOU in order.
- Function word: Spark drops "for"; Glimmer fingerspells FOR.
- "coming": Spark hyphenates C-O-M-I-N-G; Glimmer emits unhyphenated COMING.
- Timings: both monotonic so far; Glimmer packs tighter (500/900/1500/1800
  vs 0/650/1200/1950) but never states a duration (truncated).
- Completeness: Spark is a complete validatable sequence; Glimmer is a
  fragment limited by endpoint throughput (see note).

Endpoint note: two `POST /v1/chat/completions` attempts (250-300 tokens)
died with HTTP 502 because the supervisor's 300 s idle reaper tears the
backend down mid-generation (backend ~0.35 tok/s, journal shows
"idle 300s — tearing down" during active inference; supervisor not
modified). The short `/v1/completions` call (85 tokens, ~242 s) fit and
returned HTTP 200.

## Validation evidence (one line per fact)

- Spark draft tokens: HELLO sign, YES sign, THANK-YOU sign, C-O-M-I-N-G fingerspell.
- `python3 scripts/validate_gloss.py docs/meta-evidence/gloss-draft-spark.json` -> GLOSS PASS, 4 tokens, 0 failures (ship=False), exit 0.
- `python3 scripts/validate_gloss.py --ship docs/meta-evidence/gloss-draft-spark.json` -> GLOSS PASS, 4 tokens, 0 failures (ship=True), exit 0.
- `python3 scripts/lint_lexicon.py` -> LEXICON PASS, 58 entries, 0 failures, exit 0.
- Glimmer raw: 85 completion tokens, finish_reason length, HTTP 200 via supervisor 8181.
- Files: `docs/meta-evidence/gloss-draft.md`, `docs/meta-evidence/gloss-draft-spark.json`, `docs/meta-evidence/gloss-glimmer-raw.json`.
