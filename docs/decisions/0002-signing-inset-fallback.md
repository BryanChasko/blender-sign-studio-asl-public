# Architecture Decision Record (ADR) 0002 — Signing-inset fallback if finger rig fails the articulation spike

Date: 2026-10-18 · Status: accepted

## Decision

Phase 1 runs a finger-articulation spike (alphabet
poses A, B, F, numbers 1 and 5 on one humanoid host). If handshapes
cannot reach reviewer-acceptable quality, the build ships a synchronized
signing inset — licensed signer video driven by the same ASL Gloss
tokens — and chereme rigging continues as stretch work.

## Why

- Finger-level articulation on rigs built for coarse gesture clips
  is the project's single largest technical risk.
- The ASL Gloss service, lexicon, timing, and QA contracts are identical
  in both modes; only the performer changes. Deciding in Phase 1
  protects downstream work.

## Consequences

- Inset video must be licensed for this use (see
  docs/asset-licensing.md); no scraped signing video.
- The README describes whichever mode shipped, plainly.
- A fallback ship is a successful release, not a failed chereme project:
  the roadmap continues to 3D signing.
