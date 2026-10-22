# Wave 356 — PR #437 CI recovery and local executor requalification (2026-10-22)

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
Current checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
Governing issue: [#301 — Contour A](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## GitHub source refs and PR recovery

- Repository default branch `main): `909d2ba6caeb2a84508978925126a074f3a934da`.
- PR #437: [Repair Gemini HMAC contract tests and execute child authorization](https://github.com/VlDMlNSh/mediahub-os/pull/437), open, mergeable, base SHA `909d2ba6caeb2a84508978925126a074f3a934da`, current head `2e23f9a99e655369672340329c4c1b6de25f1576). Compare status is `ahead`, 11 ahead / 0 behind. Formal reviews and inline review threads remain empty.
- Merge commit `6ab685f4b2f7fc7a65b85447c3edc4b8971d4527` joins previous PR head `5bf128bb357fced3283631b6b066021cc23b9d19` with main `909d2ba6caeb2a84508978925126a074f3a934da`. Two conflicts were resolved without dropping either side's intent: the contract-validation workflow now runs both child HMAC and trigger-path tests; the child HMAC test helper uses the canonical signed-field names from `SIGNED_FIELDS`. Conflict markers are absent and commit diff-check passed.
- Current head includes one-line assertion correction `2e23f9a99e655369672340329c4c1b6de25f1576`: the regression test now checks `recorded a successful Pull Request`, matching the actual validator's successful message. The commit metadata author is `Astra Node Agent <astra-node@localhost>`; this pass did not recover an individual controller/job ID for that commit, so it is not attributed to the local Claude-FCC invocation.

## Exact-head CI evidence

All listed runs correspond to current PR head `2e23f9a99e655369672340329c4c1b6de25f1576` and completed successfully after the assertion correction:

- [Gemini workflow contract validation — run 39757948715](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39757948715), job `119754631139`, **SUCCESS**. Actionlint and all contract suites passed, including child HMAC authorization and controller trigger-path coverage.
- [Controller no-secret probe — run 39757948751](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39757948751), probe job `119754632409` **SUCCESS**, context assertion job `119754679567` **SUCCESS**. `dispatch_and_monitor` job `119754634242` and readiness gate job `119754634688` were **SKIPPED**, as expected for a pull-request probe. No Gemini children were dispatched.
- [Astra Cloud Runtime Validation — run 39757948849](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39757948849), job `119754631433`, **SUCCESS**.
- [Astra Verify — run 39757948759](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39757948759), job `119754631035`, **SUCCESS**.

The prior exact-head runs `39757807179` and `39757807255` failed only because the new test expected the phrase `successfully created a Pull Request` while the validator intentionally prints `recorded a successful Pull Request`. The one-line assertion correction matches the existing validator wording; the subsequent exact-head runs above passed. Combined-status API still returns an empty `statuses` array, so workflow-run/job evidence above is the authoritative CI evidence, not an inferred status.

## Local executor — Voktors-Mini.Dlink

- Remote Desktop Commander device ID: `e264f341-2e21-4dfc-9f97-9b95cd08bcd3`; macOS 14.7.4, ARM64.
- Local autonomous worktree `/Users/voktor/dev/mediahub-os-df3`: HEAD `d7274c28e49e30864b81ea4fd5c7754c85966a5c`, branch `engineering/mh21-sandbox-lifecycle-20260910`, clean. Its control-plane log repeatedly reports `LOCAL_AGENT_IDLE`: canonical queue encoded, no bounded task currently eligible; no queue injection was performed.
- The existing local model endpoint at `127.0.0.1:8081/v1/chat/completions` reports model `/Users/voktor/Library/Application Support/MediaHub/models/qwen2.5-coder-1.5b-instruct/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf`. Three direct, loopback-only requests used the production chat-completions message schema, `max_tokens=256`, `temperature=0`, and a 15-second timeout. Results: HTTP 200 and valid response schema for all three; exact response marker for all three; latencies `3252.6 ms` (cold), `82.3 ms`, `81.6 ms` (warm). This is a small latency sample, not autonomous code execution or a broad performance qualification.
- Ollama is running as PID `98752` bound only to `127.0.0.1:11434`, started with `OLLAMA_NO_CLOUD=1`; startup log states cloud is disabled. Available local models observed: `qwen2.5-coder:1.5b`, `qwen2.5-coder:3b`, `qwen3:4b`.
- FCC server is running as PID `7306` bound only to `127.0.0.1:8082`. Read-back of effective settings confirms `MODEL` and all four Claude model aliases map to `ollama/qwen2.5-coder:3b`, `MODEL_FALLBACKS=null`, `REASONING_POLICY=off`, `OLLAMA_BASE_URL=http://127.0.0.1:11434`, `HOST=127.0.0.1`, `PROXY_AUTH_ENABLED=false`. This configuration has no paid-provider fallback and is loopback-only.
- Inference smoke test via `fcc-claude --print --tools '' --model claude-fable-5` returned exact marker `LOCAL_FCC_OLLAMA_OK`, exit code 0, runtime 14.29 s; FCC logs record an Ollama upstream HTTP 200. This verifies local inference routing only.
- **Tool execution remains NOT VERIFIED.** A prior tool-enabled Qwen2.5-Coder 3B Claude-Code invocation emitted fabricated terminal/latency output rather than reliable tool evidence. A Qwen3:4b tool-enabled attempt stalled for 112.24 seconds and was terminated with exit 143. Neither is counted as a successful autonomous task. The local model is therefore qualified for a smoke inference only, not for autonomous engineering.
- `agent-browser` 0.27.0 was found and its core skill instructions were retrieved. Browser navigation was not performed.
- During setup, invoking `fcc-server --help` unexpectedly launched the server with its default wildcard bind. That instance was terminated after the bind was detected; the final active instance was restarted and verified on `127.0.0.1:8082` only. No model request was made through the wildcard-bound instance; external access was not independently audited.

## Gate disposition

- PR #437 exact-head CI: **VERIFIED / PASS** for the four runs above.
- Trusted no-secret pull-request probe: **VERIFIED / PASS**; launch/readiness jobs skipped as intended.
- Independent formal review: **NOT VERIFIED** (zero submitted reviews; zero review threads).
- Controller-owned three-Gemini batch: **NOT RUN**. No controller dispatch was issued; no child IDs/artifacts exist for a new batch.
- Local FCC/Ollama inference: **VERIFIED**; local Claude-Code tool execution: **NOT VERIFIED**.
- Contour A: **NOT QUALIFIED / NOT ACCEPTED**.

## Next steps

1. Obtain an independent formal review of PR #437's HMAC signing/verification semantics, fail-closed output validation, trigger coverage, and merge commit.
2. Verify remaining Issue #301 gates (issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, authoritative target manifest, standards-compliant schema validation and negative fixtures, effective token scope/readiness).
3. Only after all gates pass, run one controller-owned batch on a single immutable target SHA and record controller run ID, all three child run/job IDs, terminal statuses, reports, artifact IDs/digests, and independent verification.
4. Requalify local Claude tool calling using a demonstrably tool-capable local/free route or a verified harness. Do not accept model-generated terminal output as execution evidence; do not enable paid fallback, cloud Ollama, or Gemini on the physical host.

**Status: CI VERIFIED / INDEPENDENT REVIEW NOT VERIFIED / GEMINI BATCH NOT RUN / LOCAL INFERENCE VERIFIED BUT TOOL EXECUTION NOT VERIFIED / CONTOUR A NOT ACCEPTED.**
