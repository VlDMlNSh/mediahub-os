# MediaHub OS — Wave 429: Claude FCC fixed task profiles, local Llama status, Ruflo evaluation

- Date: 2026-10-23
- Status: **IMPLEMENTED ON DRAFT PR #572 / EXACT-HEAD CI PASS / INDEPENDENT REVIEW NOT VERIFIED / NOT DISPATCHED**
- Base main SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Working branch: `contour-a/claude-fcc-ruflo-review-task-wave429-20261023`
- PR #530: [merged](https://github.com/VlDMlNSh/mediahub-os/pull/530), merge SHA `4fe1486e2062d276c4dba2ab8c9ed97f261e9086`
- Pending-check repair: [PR #563 merged](https://github.com/VlDMlNSh/mediahub-os/pull/563), merge SHA `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Ruflo evaluation tracker: [Issue #568](https://github.com/VlDMlNSh/mediahub-os/issues/568)

## Fix for PR #530 not fully green

The root cause was the stale `FreeLLMAPI Live Qualification` push-triggered job `39959271970`, queued for a self-hosted runner and unrelated to the Claude FCC route. PR #563 separated deterministic tests onto GitHub-hosted runners and gated live qualification behind owner-confirmed `workflow_dispatch`, `confirm=true`, exact `target_sha == github.sha`, trusted `main`, and repository-owner actor.

Post-fix evidence:
- Old queued run [39959271970](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39959271970): **CANCELLED**.
- New post-merge run [39963718640](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39963718640): hosted adapter/workflow contract tests **SUCCESS**; live dispatch gate and `qualify` **SKIPPED** because this was a push event.
- Astra Verify [39963718803](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39963718803): **SUCCESS**.
- PR #564 was closed as superseded by the stronger merged #563 contract; no provider inference ran.

The current main commit is `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`. Branch protection is disabled on `main`; exact checks must therefore continue to be audited manually.

## Cloud Claude FCC + ECC — fixed, bounded additional task profile

This branch extends `.github/workflows/mediahub-fcc-free-claude-worker.yml` with a closed enumeration for `task_profile`:
- `connectivity_smoke`: the existing fixed-marker connectivity smoke.
- `ruflo_static_review`: the same free-only route plus one bounded source-only review of a fully pinned Ruflo checkout.

The caller cannot send arbitrary task text. The source-review profile pins Ruflo commit `f6c6a32432e74e36c17b91b96e51ba218783e122`, verifies the MIT license blob `5c4718198a4156beacc780980077043a98b0dd6a`, package metadata blob `00adf9205546dd88762d96ea2a264b45a567a11c`, and security policy blob `1e4d66fdcf22d51855fe012e62920cd3aae9338b`. The checkout is made read-only. The model receives only `Read`, `Glob`, and `Grep`; Bash, web tools, notebooks, installation, package execution, MCP tools, hooks, daemons, federation, and file writes are disallowed. The source-only report must mark runtime execution as **NOT RUN** and return an explicit GO/NO-GO/CONDITIONAL recommendation. No Ruflo install or model request occurred during this implementation pass.

The cloud admission gate remains: repository owner dispatch from `refs/heads/main`, `confirm=true`, exact full SHA equality, `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE=true`, and `OPENROUTER_API_KEY` presence; OpenRouter must return a concrete model ID ending in `:free`; paid fallback stays disabled. ECC remains guidance-only with pinned source/skill hashes; no second controller is introduced.

- Workflow source blob before Wave 429 changes: `384eee5209d2ec129ff2d0e92e953d3cad0fa863`
- Current branch workflow blob: `8f2da8eead76ce4a62e502e220999164d4029083`
- Current branch contract-test blob: `08ab003462e4f048f93eb9ef011efc0ea3fab4fc`
- Current branch verifier blob: `82918e0de254b4265817816e796b146ca5914d1e`
- PR #572 exact-head SHA: `5c3209e36f0089b450baf853be588eb1844ca513`; five workflows all **SUCCEEDED**:
  - [FCC admission/profile workflow 39966545981](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39966545981): FCC managed-auth preflight job 120457779025, workflow contract tests job 120457778845, install-smoke job 120457778798, ECC profile preflight job 120457778473 all PASS; dispatch-gate and bounded-worker SKIPPED on the pull_request event as expected.
  - [AI Factory verifier 39966545806](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39966545806) PASS.
  - [Provider contract 39966546027](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39966546027) PASS.
  - [Cloud Runtime Validation 39966545883](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39966545883) PASS.
  - [Astra Verify 39966546085](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39966546085) PASS.
- Formal PR reviews: **NONE**. Branch protection on main is disabled, so green CI alone is not acceptance.
- Cloud route provider invocation / Ruflo profile dispatch: **NOT RUN** pending independent review and merge. Do not treat the contract test, install-smoke, or ECC preflight as cloud Claude execution.

## Local Claude-FCC-Llama on Voktors-Mini.Dlink

Last verified evidence:
- Host ID `host_5f7264034bdf0b51` (`Voktors-Mini.Dlink`); SentinelX intermittently disconnects during interactive sessions.
- Ollama model `llama3.2:3b` was pulled; direct Ollama inference returned exact marker `MEDIAHUB_LOCAL_LLAMA_OK`, `done=true`, `eval_count=8`, elapsed total duration `10305270834 ns` (~10.3 s).
- Active FCC `/health` and `/v1/models` on port 8082 previously returned HTTP 200; `llama3.2:3b` did not appear in FCC's model list.
- A process on `0.0.0.0:8082` was observed, and effective FCC settings previously reported `proxy_auth_enabled=False`. Port 18093 was unavailable. That is a **SECURITY BLOCKER** until the external listener is positively contained and FCC's local route/model/auth are verified. Do not send a coding task through the current FCC instance. Do not treat direct Ollama inference as FCC/Claude qualification.

The current branch's desired route policy is `fcc_ollama` / `llama3.2:3b` on `Voktors-Mini.Dlink`; actual FCC-routed execution remains **NOT RUN** pending a healthy loopback-only, authenticated FCC endpoint with a verified Llama model alias.

## Next steps

1. Run exact-head CI for this branch and read back every changed blob SHA.
2. Obtain independent security review of the new task profile before merge or live cloud invocation.
3. Dispatch `ruflo_static_review` only after the PR is accepted and from current `main` with the exact SHA; record controller/run IDs, job IDs, selected free model, request ID and artifact digests. Do not claim completion before checking the run.
4. Restore SentinelX connectivity and contain FCC's non-loopback listener. Inspect the supported FCC Admin config contract; set a loopback-only bind, auth enabled, and `ollama/llama3.2:3b`; then verify `/health`, authenticated `/v1/models`, and one marker inference through FCC/Claude Code.
5. Ruflo remains **PLANNED / NOT INSTALLED / NOT QUALIFIED** under Issue #568 pending the independent static report and security review.

## Wave 429 further Ruflo source-only findings

Commented the preliminary security findings to [Issue #568 comment 6366843638](https://github.com/VlDMlNSh/mediahub-os/issues/568#issuecomment-6366843638). At pinned upstream commit `f6c6a32432e74e36c17b91b96e51ba218783e122`:
- root package metadata reports version 3.59.17 (blob `00adf9205546dd88762d96ea2a264b45a567a11c`), while legacy `.claude-plugin/plugin.json` reports 2.5.0 (blob `60717b542fb2436c7342d66e2e9f4ec9906b9387`) and configures a non-optional MCP server via mutable `npx claude-flow@alpha`.
- Legacy plugin hooks (blob `86e57d404ae08eaa70387c6fd86f261bdc80413a`) intercept Bash/Write/Edit and post-command/post-edit/session hooks; it describes itself as a legacy unaudited shim. The legacy installer (blob `436026ea3ac0205bccfee105811036fb205c7bf6`) modifies `~/.claude` and can install unpinned MCP package tags.
- MCP policy blob `8a5ce77df7cbe44df0925ef31c95446c38dc49e3` is scoped to MCP-layer actions and explicitly says native Claude tools are outside its jurisdiction. Upstream README blob `52944afd32ffbbea3a92bfcf02befe904d9b9597` requires Claude Code 2.1.287+, while the current MediaHub pin is 2.1.282.
- Preliminary recommendation: **NO-GO for installation/use as a runtime dependency now; CONDITIONAL for a pinned source-only static review pilot**. No Ruflo installation or runtime execution took place.

