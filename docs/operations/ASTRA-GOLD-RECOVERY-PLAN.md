# Astra Gold Recovery and Qualification Plan

## Objective

Prove one bounded, signed-SHA-bound autonomous development wave end to end before treating Astra Gold as qualified. A successful setup or workflow job is not a qualification pass; the controller must execute real tasks and preserve evidence from independent verification.

## Evidence from the latest completed wave

Run 38149541196 used source SHA aa2ea4281343c084d7f50f49a376be6d8a7d31b9. The Mac executor completed its bounded document task with deterministic acceptance PASS, the scoped Agent Fabric regression suite passing, an independent verifier returning ASTRA_VERDICT: PASS, and a pushed branch whose remote SHA matched the worker SHA. The mh-dev-01 and mh-dev-02 lanes were blocked before verifier execution: their no-tool Claude CLI invocation returned API Error 400: OpenAI chat conversion requires an inline Anthropic system message to contain text.

The failure was not proof of a bad task artifact or a verifier rejection. The --bare option removed the system message required by the node-local FCC OpenAI-compatible adapter. The no-tool artifact path already uses a temporary working directory and temporary CLAUDE_CONFIG_DIR, so --bare is unnecessary to isolate repository instructions.

## Rollout stages and hard gates

### Stage 0 — Freeze and preflight

Use a dedicated qualification branch and a single immutable target SHA. Do not update that branch while its qualification run is active. Verify the workflow source SHA, runner hostname/user, Claude CLI executable, FCC health, configured model binding, and expected local Ollama model before running a task. Do not merge to main.

### Stage 1 — Repair the executor transport

Run no-tool builder and verifier calls from an isolated temporary directory and isolated config directory, but retain the normal non-empty Claude system message required by FCC. Classify adapter errors into stable, non-sensitive failure codes. Keep raw stdout/stderr out of controller summaries.

### Stage 2 — Qualify each lane independently

Dispatch one bounded task at a time to mh-dev-01, mh-dev-02, and Voktors-Mac-mini.local, all pinned to the same target SHA. A lane passes only when its result proves:
- exact command/target-SHA/node/task/executor binding;
- a real Claude CLI execution produced the declared artifact;
- deterministic acceptance, scope, and security gates pass;
- the declared regression tests pass;
- a separate verifier process returns a canonical ASTRA_VERDICT: PASS;
- an isolated branch is pushed and the remote SHA equals the reported worker SHA.

Do not launch the three-lane wave until the three independent canaries pass. Limit retries to two per task and stop on a repeated failure code rather than starting another generic wave.

### Stage 3 — Run the integrated controller wave

Dispatch the signed controller command on the same frozen source SHA. Require fresh node attestations, provider qualification, all three lane results, and canonical aggregation. The final controller result must bind to the signed command and target SHA; report PASS only when the queue verdict is PASS, workers is at least one, and every selected result is VERIFIED. A successful preparation job or a successful child job alone is insufficient.

### Stage 4 — Prove actual autonomous development

The document-generation canaries prove execution, isolation, transport, and verification, but do not prove general code-writing ability. After the integrated wave passes, run a separate small, bounded code-change task on a non-production test boundary with a test that fails before the change and passes after it. Then run the full regression suite and inspect the pushed diff. This code task must use the same independent-verifier and exact-SHA evidence contract.

## Stop conditions

Stop the wave and diagnose instead of retrying when the same failure code recurs, source SHA changes during a run, the reported head and remote head differ, required evidence is missing, a task escapes its declared boundary, or the verifier output is not canonical. Keep all work on feature/task branches. Promotion to main remains a separate explicit decision after review.
