#!/usr/bin/env python3
"""validate_gloss.py — enforce docs/gloss-schema.md validation rules.

Checks every demo line's token list:
  1. every `sign` token exists in the lexicon; with --ship it must be
     `ai-reviewed` (dev builds allow `proposed` and up, but fail on
     unknown glosses either way).
  2. `fingerspell` tokens must not shadow a lexicon sign gloss
     (unknown words come back as fingerspelling; invented ASL Gloss
     fails the build). A shadowing fingerspell is an error.
  3. token timings are monotonic, holds never overlap, and every
     token fits inside the line duration when the line states one.
  4. `face` names on lexicon entries come from the known additive
     set; unknown names fail (a missing clip degrades to neutral,
     an unknown name is a contract break).

Usage:
  python3 scripts/validate_gloss.py [--ship] [sequence files...]
Default files: data/examples/gloss-demo.json data/clip-batch-1.json.
Sequence files carry lines under `lines` or a single `demo_line`.
Exit 0 when every line passes, 1 with FAIL lines otherwise.
"""

import json
import sys

KNOWN_FACE = {"brow-raise", "headshake"}
KNOWN_STATUS = {"proposed", "authored", "qa-passed", "ai-reviewed"}
SHIP_ORDER = {"proposed": 0, "authored": 1, "qa-passed": 2, "ai-reviewed": 3}

DEFAULT_FILES = ["data/examples/gloss-demo.json",
                 "data/clip-batch-1.json"]


def load_lexicon(path="data/lexicon/lexicon.v1.json"):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {s["gloss"]: s for s in data["signs"]}


def lines_of(doc):
    if isinstance(doc.get("lines"), list):
        return [(L.get("line_id", "?"), L.get("tokens", []),
                 L.get("duration_ms")) for L in doc["lines"]]
    if isinstance(doc.get("demo_line"), dict):
        L = doc["demo_line"]
        return [(L.get("line_id", "demo_line"), L.get("tokens", []),
                 L.get("duration_ms"))]
    return []


def check_line(line_id, tokens, duration_ms, lex, ship):
    fails = []
    prev_end = None
    for i, t in enumerate(tokens):
        gloss, typ = t.get("gloss"), t.get("type")
        start, hold = t.get("start_ms", 0), t.get("hold_ms", 0)
        where = "%s token %d (%s)" % (line_id, i, gloss)
        entry = lex.get(gloss)
        if typ in ("sign", "number", "letter"):
            if entry is None:
                fails.append("%s: FAIL unknown sign gloss" % where)
            elif ship and SHIP_ORDER.get(entry.get("status"), -1) < 3:
                fails.append("%s: FAIL status %s ships only at "
                             "ai-reviewed" % (where, entry.get("status")))
            elif entry.get("status") not in KNOWN_STATUS:
                fails.append("%s: FAIL bad status %r"
                             % (where, entry.get("status")))
        elif typ == "fingerspell":
            if entry is not None and entry.get("type") == "sign":
                fails.append("%s: FAIL fingerspell shadows lexicon sign "
                             "(invented ASL Gloss)" % where)
        else:
            fails.append("%s: FAIL unknown token type %r" % (where, typ))
        if prev_end is not None and start < prev_end:
            fails.append("%s: FAIL overlaps previous hold (starts %d, "
                         "previous ends %d)" % (where, start, prev_end))
        if duration_ms is not None and start + hold > duration_ms:
            fails.append("%s: FAIL exceeds line duration %d" % (where,
                                                                 duration_ms))
        prev_end = start + hold
    return fails


def main(argv):
    ship = "--ship" in argv
    files = [a for a in argv if not a.startswith("--")] or DEFAULT_FILES
    lex = load_lexicon()
    bad_face = sorted({f for s in lex.values() for f in s.get("face", [])
                       if f not in KNOWN_FACE})
    fails = ["lexicon: FAIL unknown face names %s" % bad_face] if bad_face \
        else []
    n_tokens = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        for line_id, tokens, duration in lines_of(doc):
            n_tokens += len(tokens)
            fails.extend(check_line(line_id, tokens, duration, lex, ship))
    for f in fails:
        print(f)
    print("GLOSS %s: %d tokens across %d files, %d failures (ship=%s)"
          % ("FAIL" if fails else "PASS", n_tokens, len(files),
             len(fails), ship))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
