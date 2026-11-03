# Build roadmap

Ordered phases. Each phase lands as its own PRs per
[CONTRIBUTING.md](../CONTRIBUTING.md); a phase is done when its
checks are green and AI review has passed on
any signs it touches.

## Before build

- [ ] Teammate confirmed; roles and credit split written down in
      `docs/team.md` (create on confirmation)
- [ ] Provider paths confirmed (ASL Gloss: hand-authored or ollama
      `qwen3:8b` / `llama3.2` on rocmaibox, Llama 3.1 8B Instruct
      self-hosted; stage visuals: procedural or Stable Diffusion XL
      (SDXL) Base 1.0 self-hosted; segmentation: MediaPipe
      HandLandmarker + FaceLandmarker, swap Segment Anything Model 3
      (SAM 3) open weights); rocmaibox budget in
      `docs/architecture.md`
- [ ] American Sign Language Lexicon Video Dataset (ASLLVD) access and terms reviewed (docs/asset-licensing.md)
- [ ] Seed lexicon list agreed with owner (docs/lexicon.md)

## Phase 1 — kill the biggest risk first

- [x] **Spike: finger articulation (rocmaibox) — DONE, GO with tuning.**
      134-bone rig, 34 hand bones, 30 finger joints posed and sticking;
      legible close-up still at `docs/assets/spike-finger-v2.png`.
      Exact A/B/F/1/5 angles need ASLLVD + reviewer tuning.
      See `docs/decisions/0003-finger-articulation-spike.md`.
      Go/no-go on 3D signing vs. signing-inset fallback
      (architecture decision record (ADR) 0002):
      GO on 3D signing, inset stays fallback.
- [ ] Repo skeleton builds on macmini; ASL Gloss schema validator runs on
      `data/examples/gloss-demo.json` fixtures with no Blender needed.

## Phase 2

- [ ] ASL Gloss service: host line -> validated ASL Gloss tokens;
      fingerspelling fallback enforced by schema test.
- [ ] Chereme clips batch 1 (rocmaibox): greetings, YES/NO, QUESTION, numbers 1–9.
- [ ] Face layer: brow raise (question), headshake (negation) additive, paired per ASL Gloss token.

## Phase 3

- [ ] Sign playback synced to the existing speak cycle (speech +
      captions + signs on one clock).
- [ ] Chereme clips batch 2 (rocmaibox): host dialogue (YOUR-TURN, MY-TURN,
      REPEAT, HELP, TRUE, FALSE, FINISH, AGAIN).
- [ ] Segmentation quality assurance (QA) pass wired into clip acceptance (rocmaibox renders, macmini checks).

## Phase 4

- [ ] Stage-visual pass: neutral signing-stage visuals only with configurable image model (no game props, no hosted dependency).
- [ ] Full dialogue loop: welcome -> signed question -> signed
      answer -> acknowledgement -> closing, end to end in the host
      build.
- [ ] AI-review pass on every clip in the demo script; fix or cut.

## Phase 5

- [ ] Freeze lexicon. Demo script locked to ai-reviewed signs only.
- [ ] Performance: clip loading, Draco assets, mobile layout.

## Phase 6

- [ ] AI-review pass recorded per clip (checklist in the PR).
- [ ] Fallback inset integrated if any demo line failed review.

## Phase 7 — demo

- [ ] Demo video (signed + captioned), README demo section. No new
      features after the freeze.

## Stretch (only if the demo loop is green)

- Webcam sign-along: the segmentation model segments the viewer's
  hands for fingerspelling practice. Practice feedback only — no
  recognition claim.
- Second host signing a duet line (host + host exchange).
- Pose-matched stage visuals: Blender depth/OpenPose pass into SDXL
  via ControlNet, containerized. Path, costs, and open box-side
  checks in [docs/comfyui-container-path.md](comfyui-container-path.md).
- Clip driving via the running `blender-mcp-http` MCP server
  (rocmaibox port 8190; container Blender 5.1.2 vs host 4.4.0 —
  version match still open).

## Demo script (target, ~90 seconds)

1. Host welcomes the viewer — spoken, captioned, signed.
2. Host reads a question, signed, with brow-raise question face.
3. Host signs the answer with acknowledgement (REPEAT / HELP if needed).
4. Correct answer: signed TRUE + friendly emote; caption shows the fact.
5. Closing line signed. Close on lexicon/review credits.
