# Wave 318 — Per-/next Gemini trigger and Alamo executor readiness (2026-10-21)

## Executive status

The latest Draft PR #432 contains the controller-side building blocks for a GitHub-triggered per-`/next` Gemini batch and has green non-launching CI at exact HEAD `269b57b8b9c412261c97c4811bd49cbb4122ba03`. This does **not** make the route operational yet: the PR is unmerged and still Draft, no independent review is recorded, the default-closed repository variable and required secret presence/scope cannot be verified through the available GitHub integration, and the Alamo server is not connected to the available host inventory.

## Immutable refs and provenance

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Current `main` HEAD observed: `1f9fe47f986376a733fb0ddfa5e3b567b2613d5c`.
- Current canonical documentation branch at the start of this pass: `docs/mediahub-chat-tree-map-20261012`, HEAD `b7a59fb5e2b408cfd22f02ba3d1d38d9c72a2ebe`.
- PR #432: https://github.com/VlDMlNSh/mediahub-os/pull/432 — OPEN / DRAFT / UNMERGED. Latest head observed: `269b57b8b9c412261c97c4811bd49cbb4122ba03`. PR metadata still reports base SHA `f16e5bae202a78584f273132e7f88c6e25d3142e`, whereas `main` has advanced to `1f9fe47f986376a733fb0ddfa5e3b567b2613d5c`; refresh/reconcile the base before integration.
- Controller workflow blob on PR branch: `9453403bba899a2400ee3fb874d32badd034c704`.
- Controller transport contract test blob: `2806962ef90a892b49288cadf56925b60d39e224`.
- Wave 292 controller contract test blob: `84a92e514c930c55d411bf74ad390109b7ed0d4b`.
- The same controller path on `main` is blob `4cec1aa234fd9ccb0d41533b37248fff079c79c5` and does not contain the new `issue_comment` bridge. The bridge is PR-only until a reviewed integration.

## Per-/next Gemini controller contract in PR #432

The controller source currently provides the following:

1. `issue_comment` trigger; accepts only an exact `/next` comment on normal Issue #301 authored by an OWNER. PR comments and other issues do not satisfy the dispatch condition.
2. `MEDIAHUB_GEMINI_BATCH_ENABLED` repository variable is a closed-by-default admission gate. If it is not exactly `true`, the controller reports that no child dispatch will occur.
3. One immutable full 40-hex target SHA is resolved once and sent to all three children. The controller holds `MEDIAHUB_GITHUB_TOKEN` for GitHub API workflow dispatch and run monitoring only; the value is not passed to child workflows. Provider keys remain separate and scoped to the respective child workflow. No `secrets: inherit`.
4. Three complementary tasks are encoded for each batch: Agent 1 bounded implementation against the canonical map/Bootstrap/checkpoint/roadmap and Issue #301; Agent 2 independent contract/test verification; Agent 3 security, authority, credential-separation and provenance audit. Agent 2 is specifically prohibited from claiming review of concurrent Agent 1 changes as independent review.
5. Each intended child dispatch is recorded before POST. Definite 4xx failures are terminal failures; ambiguous network/5xx/408 outcomes are reconciled by unique dispatch ID. An ambiguous accepted child that is discovered and reaches completion becomes `RECONCILED`; all three child outcomes must still conclude successfully for the batch to pass.
6. Controller run-name includes the source comment ID and a replay check suppresses a duplicate trigger if a prior run with that marker is visible in the most recent 100 runs. This is bounded history-based idempotency, not a durable ledger.
7. Agent-mode controller job is not invoked from the PR probe. The PR-context probe remains credential-free and non-launching.

**Important integration boundary:** GitHub Actions cannot receive an ordinary ChatGPT message as an `issue_comment` event. To bridge a ChatGPT `/next` after the controller has passed gates and been integrated, the ChatGPT-side action must create a separate owner-authored `/next` comment on Issue #301 (or an equivalent authenticated dispatcher must send the event). This PR does not by itself create that ChatGPT event binding, and the code is not active on `main` yet.

## Exact-head CI evidence

These runs all reference PR head `269b57b8b9c412261c97c4811bd49cbb4122ba03` and completed SUCCESS:

- [Astra Cloud Runtime Validation #39647070609](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070609)
- [Controller non-launching PR probe #39647070682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070682) — dispatch job skipped as intended.
- [Astra Verify #39647070683](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070683)
- [Workflow contract validation #39647070718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070718)
- [Reusable workflow caller-context probe #39647070781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070781)

There is no controller agent-mode run ID for this pass, and no Gemini child run IDs or artifacts were produced. Successful static CI and negative/PR-context probes do not qualify actual secret-backed transport or trusted-main execution.

## Governance, settings and launch-gate status

- Formal PR #432 reviews: zero returned by the review API.
- Repository branch-protection endpoint returned HTTP 403 (`Resource not accessible by integration`). Repository rulesets endpoint returned an empty array; this does not establish absence of organization-level or classic branch-protection controls.
- Attempts to inspect repository Actions variables/secrets metadata through the available GitHub connector were not authorized by the connector. Therefore the existence, values, dates and effective scope of `MEDIAHUB_GEMINI_BATCH_ENABLED`, `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, and `GEMINI_API_KEY` / `GEMINI_API_KEY_2` / `GEMINI_API_KEY_3` are **NOT VERIFIED**. No secret values were read.
- Required gates before activation: independent security review at exact PR HEAD; latest-base reconciliation and exact-head CI; effective minimum transport-token permissions; separate HMAC key presence; provider-key scope; branch/org/Actions governance; and an authorized trusted-main no-secret positive-context probe.

## Alamo / Free Claude Code executor

Live inventories from SentinelX and Desktop Commander do not identify an Alamo host:

- SentinelX connected host: `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, operational, version `0.22.0`.
- SentinelX reports Free plan, one active-host slot, one active host; `mh-dev-01` and `mh-dev-02` are disabled.
- Desktop Commander reports `Voktors-Mini.Dlink` online, but `mh-dev-01` and `mh-dev-02` offline. No device named Alamo is available.
- No Alamo Claude session/job ID or browser evidence exists; the local executor was **NOT RUN**.
- `ops/agent-fabric/providers/local-executor-routing-v2.yaml` on `main` has blob SHA `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` and declares `ASTRA_GOLD_QUALIFICATION_GATED`. Its FCC Claude candidate is not route qualification evidence: required admission includes exact executable/provider identity, immutable source SHA, a non-mutating marker probe, isolated workspace, 23-round pass record and independent A3 verification.
- Wave 272 hard requirements prohibit Anthropic API/paid API auth and paid fallback. The exact FCC upstream, permission/terms status, auth/cost class, billing behavior, version, egress and Alamo binding must be verified before Claude can be enabled.

## Disposition

- Gemini dispatch correction and partial/ambiguous-result reconciliation: IMPLEMENTED on Draft PR #432.
- Exact-head non-launching CI at the listed SHA: VERIFIED.
- Per-/next automation integrated into `main`: NOT ACTIVE.
- Independent security review, governance/secret/variable scope: NOT VERIFIED.
- Gemini Agent 1/2/3 actual invocation in this pass: NOT RUN.
- Alamo Free Claude Code executor: NOT RUN.
- Qualification or acceptance: NOT CLAIMED.

Next safe step is to obtain independent review and current-base reconciliation for PR #432, verify settings through an authorized repository-admin view, then run only the approved non-launching trusted-main probe. In parallel, establish Alamo host connectivity without routing Gemini through it, and complete the documented non-paid Claude route qualification.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Governance issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
