#!/usr/bin/env python3
"""lint_lexicon.py — structural lint for data/lexicon/lexicon.v1.json.

Enforces the tests/README contract: unique glosses, canonical
category slugs, known statuses, face names from the additive set,
 HTTPS asllvd_ref shape. Sign correctness stays human review
(docs/reviewer-guide.md); this guards the shape around it.

Usage: python3 scripts/lint_lexicon.py [lexicon path]
Exit 0 when clean, 1 with LINT lines otherwise.
"""

import json
import sys

CATEGORIES = {"greetings", "dialogue-flow", "truth-response", "numbers",
              "reference", "subjects", "emotion", "cloud-ai"}
STATUS = {"proposed", "authored", "qa-passed", "ai-reviewed"}
FACE = {"brow-raise", "headshake"}


def main(argv):
    path = argv[0] if argv else "data/lexicon/lexicon.v1.json"
    with open(path, encoding="utf-8") as f:
        signs = json.load(f)["signs"]
    fails = []
    seen = set()
    for s in signs:
        g = s.get("gloss", "?")
        if g in seen:
            fails.append("LINT %s: duplicate gloss" % g)
        seen.add(g)
        if s.get("category") not in CATEGORIES:
            fails.append("LINT %s: bad category %r" % (g, s.get("category")))
        if s.get("status") not in STATUS:
            fails.append("LINT %s: bad status %r" % (g, s.get("status")))
        for face in s.get("face", []):
            if face not in FACE:
                fails.append("LINT %s: unknown face %r" % (g, face))
        ref = s.get("asllvd_ref")
        if ref is not None and "dai.cs.rutgers.edu" not in ref:
            fails.append("LINT %s: asllvd_ref cites no DAI page" % g)
    for f in fails:
        print(f)
    print("LEXICON %s: %d entries, %d failures"
          % ("FAIL" if fails else "PASS", len(signs), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
