# Architecture Decision Record (ADR) 0001 — Fixed seed lexicon, fingerspelling fallback

Date: 2026-10-18 · Status: accepted

## Decision

The build signs only a 58-sign seed lexicon covering everyday host
dialogue plus basic cloud/AI vocabulary. All other words are
fingerspelled from 26 alphabet poses. The ASL Gloss service is schema-validated against the lexicon and
may not emit an unlisted sign.

## Why

- General English-to-American Sign Language (ASL) translation is an
  open research problem; a build claiming it would be
  inaccurate and misleading.
- A fixed seed lexicon is authorable in Blender and fully
  reviewable by one fluent signer.
- Fingerspelling covers everything outside the lexicon: slower,
  always available, and native to ASL for names and borrowings.

## Consequences

- Demo script lines must be written to the lexicon, not vice versa.
- Host names and proper nouns are fingerspelled by design.
- Lexicon growth is additive versioning (a new lexicon file),
  never edits to shipped entries' meanings.
