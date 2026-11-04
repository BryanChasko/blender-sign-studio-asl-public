# Glimmer 30B on-device verdict attempt (EIGHT)

Endpoint: `http://127.0.0.1:8181/v1` (supervisor, OpenAI-compat
`POST /v1/chat/completions`, cold-start spawns llama-server).
Model: `/home/bryanchasko/models/muse-glimmer-30b/Muse-Glimmer-30B-Q4_K_M.gguf`.
Same requests as the API. Box was under GPU contention throughout.

1. Liveness: `{"messages":[{"role":"user","content":"Reply with
exactly: GLIMMER_OK"}],"max_tokens":10}` → 200, 10 completion
   tokens, ~48 s. Reasoning echoed the prompt, content empty.
2. Vision: hello still (960x540 PNG, 387 KB base64 `image_url`)
   - "PASS or FAIL plus one clause" → 0 bytes in 180 s. Vision
     path hangs here; not retried.
3. Verdict micro (40 tokens): citation vs rig vs AI described in
   ~100 prompt tokens → 200, 40 completion tokens, verdict still
   in `reasoning_content`, `content` empty. Full reply in
   `glimmer-verdict-micro.json`.
4. Verdict full (150 tokens): same prompt, room to answer →
   timeout at 280 s and again at 290 s. Throughput under
   contention cannot finish a scored answer in-session.

Conclusion: text path works, vision hangs, long answers starve.
The on-device judge only fits tiny prompts while the GPU is
shared. Gloss-draft history stays in `gloss-glimmer-raw.json`.
