# Wave 352 — OmniRoute/Claude historical evidence and remaining effort (2026-10-22)

- Status: **HISTORICAL OMNIROUTE/Ollama RUNTIME EVIDENCE CONFIRMED / EXACT CLAUDE SUCCESSFUL RUN NOT LOCATED / GEMINI CURRENT BATCH NOT RUN / LOCAL CURRENT EXECUTION NOT VERIFIED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior evidence: [Wave 351](MEDIAHUB-NEXT-CLAUDE-FCC-OLLAMA-HISTORICAL-EVIDENCE-WAVE-351-2026-10-22.md), [Wave 349](MEDIAHUB-NEXT-RECONCILED-EFFORT-AND-TRIGGER-COVERAGE-WAVE-349-2026-10-22.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301); controller PR [#437](https://github.com/VlDMlNSh/mediahub-os/pull/437); trigger coverage PR [#443](https://github.com/VlDMlNSh/mediahub-os/pull/443).

## 1. Historical OmniRoute/Claude/Ollama evidence

The existing [2026-10-02 hybrid component reconciliation](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/2026-10-02-astra-gold-hybrid-component-reconciliation.md), blob SHA `567ea108f5faee9d9176cb475ac8534ef19eb25d`, records on `Voktors-Mini.Dlink` (macOS Darwin 23.6 / arm64):
- Claude Code 2.1.282 discovered;
- OmniRoute 3.8.50 discovered, with a running OmniRoute process observed;
- Ollama 0.34.4 discovered, with a running Ollama server observed;
- Node.js 22.23.3 discovered.

This is a concrete timestamped positive runtime inventory. Combined with the owner's report, it supports retaining the historical Claude → OmniRoute/Ollama route as previously operational and not rebuilding it from scratch. It does **not** identify the exact successful Claude invocation/run ID, model-response artifact, or current service state. Historical component discovery alone does not prove a completed end-to-end task; that detail remains owner-reported pending a run artifact.

A separate historical transport health checkpoint (blob `18ca4708d67456fc6be8953cfe411fff8c007d67`) recorded `Voktors-Mini.Dlink PASS`, transport `self-reexec-v1`, worker SHA `cd7a83c6b6b8d6065a157274e79e315e2aa5012c0f8ee9466de92980570b9e1a`, and result commit `3a369037e99058d51e37eee3d26fb3941a6506f`. This is historical transport evidence, not today's runtime proof.

Existing implementations are to be reused:
- [three-Claude 23-wave workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/mh25-three-claude-23wave.yml), recorded blob SHA `3a7327135ea73c7a886c1c8b6dbbf7080aff421c`;
- [distributed local worker](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/qualification/run_distributed_local_worker.py), recorded blob SHA `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`;
- [local qualification result 2026-10-02](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/qualification/ASTRA-GOLD-LOCAL-QUALIFICATION-RESULT-2026-10-02.md), blob SHA `3b284dd211414da816af8fc4ac8addbc810a928d`.

The exact successful end-to-end Claude workflow run ID and aggregate evidence artifact digest remain **NOT LOCATED**. No historical run ID is invented. Current runtime availability and current exact-SHA qualification remain **NOT VERIFIED**.

## 2. Gemini evidence and exact current gates

Historical Gemini child runs are verified as completed/success:
- [39370191589](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370191589), job `118456086050`, artifact ID `12240818397`, digest `sha256:6ba571f563e38fd9df2be5d5ca23da0c59e446661528284ac22b428dfde93d3e`;
- [39370202615](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370202615), job `118456119718`, artifact ID `12241545147`, digest `sha256:a800276ca454550d19930b03a62169cdfe45786e96beabf59d9194b54098644f`;
- [39370217605](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370217605), job `118456166571`, artifact ID `12240363870`, digest `sha256:6d91dc54e57aebb3720674c86466e0fa37cc3f69c525a5c94bb0b5c14fceeccd`.

All three refer to historical source SHA `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`; artifacts were unexpired at lookup time. These are three historical individual runs, not a controller-correlated batch.

PR #443 is merged at `909d2ba6caeb2a84508978925126a074f3a934da`. PR #437 is still open/draft at head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; formal review endpoint returned zero reviews, exact-head status endpoint returned an empty list, and the associated comment explicitly says exact-head CI was not verified. The controller on main was read at blob SHA `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f`. No current controller-owned three-child batch was dispatched. Effective secret values were not read.

## 3. Remaining effort estimate — active work in this chat

Estimates are engineering effort, not elapsed wall-clock time; review queues and disconnected hosts can extend calendar time.

| Workstream | Expected active effort | Contingency | Definition of done |
|---|---:|---:|---|
| Gemini controller to first current 3-child batch | 1.5–3.5 h | +2.5 h (total 4–6 h) if a real gate/source defect appears | Exact-head CI and independent review; governance and no-secret probe gates; one controller run with common target SHA, three child run/job IDs, terminal states and artifact digests |
| Local Claude-fcc-Ollama execution, after host channel is available | 0.5–1.5 h | Additional time only if runtime/allowlist/free-route fails | Verify exact host/capabilities/allowlist, use existing runner, confirm free-only local model route and real bounded result; record session/job and evidence |
| **Combined expected active work** | **2.0–5.0 h** | **Approximately 4.5–7.5 h** if Gemini contingency is needed, excluding major local host repair | Both outcomes independently evidenced; Gemini never uses a physical server |

The Gemini estimate assumes historical transport and prior successful child executions are reused. It is not a promise of completion within this chat's wall-clock time. The local estimate is conditional: current Ollama API reachability was not verified in the last bounded check, so host reconnect could create external waiting or extra repair work.

## 4. Ordered next actions

1. Reconcile PR #437 against current main and exact-head CI; resolve the draft/review gate without weakening HMAC or authorization checks.
2. Verify required governance, effective readiness and trusted-main no-secret probe using permitted GitHub Actions paths; do not expose credentials.
3. Only after all gates pass, dispatch one controller-owned Gemini batch on a single immutable SHA. Capture controller/child run and job IDs, terminal results, reports and artifact digests.
4. Separately reconnect to the exact authorized Mac host and inspect existing Claude/Ollama/FCC route with bounded read-only checks. Reuse the existing worker/workflow; no paid fallback and no Gemini transport through the server.
5. Read back changed docs and record final blob/commit SHAs.

## 5. Disposition

- Historical OmniRoute/Ollama process presence: **VERIFIED AS HISTORICAL INVENTORY**.
- Owner-reported successful Claude-fcc-Ollama execution: **RETAINED; exact runtime run/artifact not located**.
- Current Claude runtime/qualification: **NOT VERIFIED**.
- Historical Gemini individual child runs and artifact metadata: **VERIFIED**.
- Current controller-owned Gemini three-child batch: **NOT RUN**.
- Overall Contour A acceptance: **NOT ACCEPTED**.

No secret values were read. No workflow was dispatched, no host service started, no local model invoked, and no browser task repeated during this pass.


## Wave 352 follow-up — live SentinelX reconnect result (2026-10-22)

- SentinelX host registry lists `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, agent `0.22.0`, connected timestamp `2026-10-22T09:08:33.511522+00:00`, operational=true at list time. Bounded `sentinel_ping` and `sentinel_capabilities(detail=summary)` then both failed `agent_disconnected / read_loop_ended` (hub request IDs `hreq_15ae01dc4214449a` and `hreq_9744f2fb60854759`). This establishes registry presence but not an executable live session. No runtime commands or model calls were made.
- Updated local lane estimate remains 0.5–1.5 active hours after reconnection; current access failure may add external waiting. Do not reinstall or change allowlists based on this result.
