# Architecture Decision Record (ADR) 0004 — AI review is the shipping gate

Date: 2026-10-24 · Status: accepted · Owner decision

## Context

ADRs 0001–0003 and the lexicon, schema, and roadmap docs gate
shipping on fluent-signer review. No signer is on the team and
none is coming. Holding shipping on that gate blocks the project
permanently.

## Decision

`ai-reviewed` (six checks in [docs/ai-review.md](docs/ai-review.md)) is the shipping
gate. The `reviewed` mark stays defined for a future signer; nothing waits
on it. Lexicon entry notes saying "reviewer to confirm" are
superseded by this record.

## Consequences

- Ship rule everywhere reads `ai-reviewed` ships: lexicon,
  gloss-schema, architecture, cookbook, README, CONTRIBUTING,
  roadmap, reviewer-guide (signer path kept as fallback).
- What machine review cannot certify (thumb nuance, movement,
  location, face grammar, meaning preservation, variation) stays
  listed in `docs/ai-review.md` as open risk on every pose.
- Re-review triggers unchanged: joint, fixture, rig, Blender, or
  reference-URL changes lapse `ai-reviewed` to `authored`.
