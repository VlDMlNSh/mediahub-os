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

## Wave 430 — refreshed Ruflo upstream and admission reconciliation (2026-10-23)

### Exact MediaHub state

- MediaHub `main` target inspected: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- PR #572 remains **OPEN / DRAFT / NOT MERGED** at code head `50656c40ba9fa4008f18a831309efd20ebdcb202`: [PR #572](https://github.com/VlDMlNSh/mediahub-os/pull/572).
- Exact-head contract/policy CI succeeded: FCC admission/profile [39967316229](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39967316229) (jobs 120460466214, 120460466572, 120460466601, 120460466625 SUCCESS; dispatch gate 120460468143 and bounded worker 120460470377 SKIPPED as expected on pull_request); AI Factory [39967316349](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39967316349) / job 120460464792 SUCCESS; provider contract [39967316694](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39967316694) / job 120460466294 SUCCESS; Cloud Runtime Validation [39967316428](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39967316428) / job 120460464956 SUCCESS; Astra Verify [39967316045](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39967316045) / job 120460462447 SUCCESS.
- Formal PR reviews: **NONE**. These CI results verify contracts only. They do not verify a cloud provider call, Ruflo's runtime, or model review; no such dispatch took place.
- Canonical map remains on `docs/mediahub-chat-tree-map-20261012`: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md). This report is on a working PR branch, not canonical or accepted.

### Re-check against current Ruflo upstream

Current upstream main observed in this refresh is `88349655ebc2de8f9bf702aaf31d6be768e1ea11`; the task profile still pins the older immutable review snapshot `f6c6a32432e74e36c17b91b96e51ba218783e122`. Do not silently treat the two snapshots as equivalent.

- Root `package.json` at current main: blob `00adf9205546dd88762d96ea2a264b45a567a11c`, package `claude-flow@3.59.17`.
- `LICENSE`: blob `5c4718198a4156beacc780980077043a98b0dd6a`, MIT.
- `README.md`: blob `52944afd32ffbbea3a92bfcf02befe904d9b9597`; current recommended native Claude Code plugin flow requires Claude Code `2.1.287+`. MediaHub's pinned Claude Code in the FCC worker is `2.1.282`, so native plugin installation compatibility is **NOT SATISFIED**.
- Legacy `.claude-plugin/plugin.json`: blob `60717b542fb2436c7342d66e2e9f4ec9906b9387`; it independently reports version `2.5.0` and declares a non-optional MCP server via mutable `npx claude-flow@alpha`, plus optional mutable package references including `flow-nexus@latest`. This does not match root package version `3.59.17`; this path is not acceptable as an immutable production install contract.
- `SECURITY.md`: blob `1e4d66fdcf22d51855fe012e62920cd3aae9338b`; its supported-version table lists `3.5.x` as supported while the root manifest says `3.59.17`. Treat the project's support policy as ambiguous/stale until upstream reconciles it.
- `v3/@claude-flow/cli/src/mcp-tools/hooks-tools.ts` at current main: blob `7c7e219a5eba4d699ee6d89cc931d3a8097bfc65`. The source does not contain the `realCanonical()` hardening described in upstream issue [#4346](https://github.com/ruvnet/ruflo/issues/4346); `resolveTargets` still uses a lexical `abs.startsWith(cwd + sep)` containment check (source line 5442). This is a source-level unresolved/NOT-VERIFIED symlink-containment concern. The issue describes a candidate fix, but this pass did not reproduce an exploit and does not claim a runtime vulnerability test.
- Upstream issue [#4384](https://github.com/ruvnet/ruflo/issues/4384) records a direct-dependency CVE finding and two test timeouts on older commit `6250c920367a7309efec7fc694da3eb5328998e5`. The current main's dependency audit and CI result at `88349655ebc2de8f9bf702aaf31d6be768e1ea11` were not independently executed/retrieved here; current supply-chain status therefore remains **NOT VERIFIED**, rather than asserted still failing.
- Upstream capability counts vary even between current README/plugin documentation (314 vs 380+ MCP tools). These are un-reproduced vendor claims, not qualification evidence. Ruflo's hooks, policy/routing mods, memory, workers, daemons and federation overlap with the existing ECC and Astra boundaries.

### Decision and phase gate

**NO-GO** for installing Ruflo as a MediaHub runtime dependency or enabling its full plugin/MCP/hooks/mods/swarm/federation path. **CONDITIONAL** only for a source-only, read-only, immutable-checkout evaluation with no package installation or scripts, no MCP/hooks/daemon/network/federation, no write capability and no alternative controller or memory source of truth.

The new `ruflo_static_review` profile in PR #572 would still invoke a cloud model. Issue #568 currently prohibits model/provider calls during this evaluation phase. Therefore the profile remains **NOT DISPATCHED** even though the workflow's contract CI passes. Do not treat PR #572's existence or green tests as an exception to the issue's phase gate. Any later live static-review inference requires the evaluation phase to be explicitly advanced by the owner, the PR to be accepted, the trusted-main exact-SHA admission gate to pass, and independent review.

No Ruflo installation, package execution, hooks/MCP enablement, provider request, model inference, local FCC coding task, merge or qualification was performed in this refresh.

### Next bounded step

Complete static evidence review and independent security sign-off for Issue #568. In parallel, keep the local FCC lane blocked: prior host evidence shows the active FCC listener on `0.0.0.0:8082` with proxy auth disabled, so no local task may use it until loopback binding, auth, model alias and the actual effective managed configuration are verified.
