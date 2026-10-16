# MediaHub OS — Post-Merge Gemini Diagnostic and Cloud-Agent Portability, Wave 37

- Date: 2026-10-17
- Repository: `VlDMlNSh/mediahub-os`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **SOURCE-BOUND DIAGNOSTIC / PROPOSED / PROVIDER SMOKE TEST PENDING / FABRIC NOT QUALIFIED**
- Scope: reconcile current Gemini MCP dispatch evidence, establish a portable cloud-agent reference path, and prioritize the existing admission backlog.
- Authority: Baseline 2.0, the Master Development Roadmap, accepted domain contracts, A0 issuer/lifecycle, MH-12 secret handling, R-06 audit/privacy, and MH-21 egress rules retain their authority.

## 1. Executive disposition

PR #305 and PR #306 are already merged into `main`. The latest retrieved `main` HEAD is `6c2e8dbdee81c798b64e65546e7ded07093f100a`; the current `.github/workflows/gemini-autonomous-engineering.yml` blob is `9be13613ae79f316ca410c16c6e69e2aea7283a4`. The latest recorded `Astra Verify` run at that HEAD succeeded, but that CI run does not establish that a fresh Gemini MCP tool call and PR creation succeed after the merge.

The existing autonomous engineering workflow has a more recent fail-closed output validator. Evidence from earlier runs shows why the distinction is essential: a green wrapper/action step can coexist with a malformed model-tool stream, and the job can only be classified by inspecting the structured output and the final validation result.

This wave is an evidence and architecture update. It has not changed the live workflow, provider settings, secrets, agent registry, queue implementation, or infrastructure. No new provider invocation, workflow dispatch, test suite, qualification, or deployment occurred here.

## 2. Revision-bound evidence

| Evidence | Observed result | Scope limit |
|---|---|---|
| PR [#305](https://github.com/VlDMlNSh/mediahub-os/pull/305) | Merged 2026-10-16 22:28:35Z; head `76bf37e87e1cb041cd4487a3f8a14fa3025a4bc9` | Source change merged; merge itself is not provider runtime evidence |
| PR [#306](https://github.com/VlDMlNSh/mediahub-os/pull/306) | Merged 2026-10-16 22:34:48Z; head `1af3037570268cf5ab6b97502a5ac3165af3d134` | Source change merged; post-merge Gemini dispatch remains unverified |
| Current `main` | `6c2e8dbdee81c798b64e65546e7ded07093f100a` | Live ref observed through GitHub API |
| Current Gemini workflow blob | `9be13613ae79f316ca410c16c6e69e2aea7283a4` | Current YAML readback; no execution in this wave |
| [Astra Verify run 38976598150](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976598150) | Success at current `main` HEAD | CI evidence only |
| [Astra Verify run 38976332250](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976332250) | Success on the Wave 16 pull-request head | CI evidence only |
| [Astra Cloud Runtime Validation run 38976332054](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976332054) | Success on the Wave 16 pull-request head | CI evidence only |
| [Gemini dispatch run 38976095754](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976095754) | Failed final output validation; artifact `gemini-output`, ID `12079316446` | Reproduced in historical artifacts; no provider call made during this pass |
| [Earlier dispatch run 38972774167](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167) | Wrapper reported success, while its uploaded structured output contained empty response / invalid stream and tool errors | Treat as a false-positive workflow outcome, not successful agent execution |
| [Historical read-only audit run 38952885501](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38952885501) | Previously recorded as successful for that bounded read-only run | It proves only that run and its provided context, not the full development fabric |

### Artifact-level failure classification

The archived `gemini-output` for run `38976095754` shows:

- `response` is empty.
- The model stream reports `INVALID_STREAM` and `MALFORMED_FUNCTION_CALL`.
- Tool invocation attempts for `mcp_github_get_me`, `github:get_me`, and `get_me` returned “Tool ... not found”.
- The Gemini CLI action step itself reached its post-action artifact upload, then the workflow validator rejected the empty response.

The evidence supports **tool registration/name mismatch followed by malformed function-call stream and fail-closed validation**. It does not independently identify a bad API key. PR #305 addresses registered MCP tool names; PR #306 addresses credential/token interpolation. The merged sources need a fresh provider smoke test before the end-to-end dispatch can be marked working.

## 3. Reference topology: account-scoped credentials, portable workers

The preferred execution path is a GitHub-hosted ephemeral runner that retrieves a narrowly scoped credential at job runtime, invokes the explicitly admitted provider, and returns a revision-bound artifact or pull request. The runner is compute placement, not the identity owner, queue authority, or permanent API-key home.

| Plane | Preferred responsibility | Hard boundary |
|---|---|---|
| Identity and credential custody | Provider/account/project or approved repository/environment identity; secret reference and rotation metadata | Raw key values stay out of Git, task JSON, prompts, logs, artifacts, and issue text |
| Admission/control plane | One authorized A0 lifecycle issues a task-bound decision with audience, repo, source SHA, path scope, provider/model, data class, limits, expiry, and revocation status | Catalog membership, route selection, or a model response alone never grants execution capability |
| Cloud compute | Fresh hosted runner for one bounded task; immutable checkout; minimal workspace; short lifetime | No dependency on the user's phone or an owner-operated always-on server; no permanent broad token on disk |
| Provider route | A task-bound adapter uses an approved provider/model destination | Direct runner egress has a real network origin; provider region, account, policy, quota, and terms still apply |
| Output and provenance | Sanitized structured result, changed-path manifest, source SHA, artifact digest, tool-call outcome, audit reference | Output stays untrusted proposal data until an independent verifier and the authorized PR/promotion path accept it |
| Local three-node fabric | Mac mini 2018 / macOS; Mac mini 2011 / Linux; remote video server, with current roles preserved | Cloud execution is additive; no hardware role or target profile is inferred from this design |

### Credential resolution choice

1. Prefer short-lived OIDC federation where the destination explicitly supports a trust relationship and validates repository, ref, environment and workflow claims.
2. For API providers requiring static keys, use the provider/account-scoped secret store supported by the platform, with job/environment restrictions, just-in-time injection, rotation and revocation. Select the actual store through an accepted ADR; its identity and operation must be evidence-bound.
3. Keep secret references separate from task data; never allow an agent to list, print, copy or broaden secrets.
4. Do not pin a provider key to the Mac mini or the video server solely to make remote requests work.
5. Treat the selected runner's egress IP/location as an actual infrastructure attribute. A portable credential model removes a permanent-host dependency; it does not make request origin invisible or override provider eligibility and regional requirements.

## 4. Agent admission and immediate queue semantics

The existing catalog, role registry, provider schemas and 23-lane manifest are the starting components. Reuse them; do not create a parallel registry or scheduler. The JSON queue with 16 entries remains a **documentary queue**, not a live worker scheduler.

Admission remains fail-closed until the relevant gates have accountable decisions and revision-bound proof:

`DISCOVERED → REVIEW_PENDING → WAITING_AUTH → AUTH_VERIFIED → READ_ONLY_ADMITTED → PATCH_ADMITTED → QUALIFIED → ACTIVE`

`BLOCKED`, `QUARANTINED`, `REVOKED`, `EXPIRED` and `DEGRADED` are stop states. Provider adapter health and provider selection are separate fields; neither implies admission or qualification.

Every admitted task must bind at minimum: queue ID, owner/issuer, repo, base and immutable source SHA, allowed paths, task purpose, data classification, agent/provider/model, tool capabilities, budget/quota ceiling, allowed fallback destinations, lease/expiry, cancellation/replay policy, output schema, expected evidence, independent reviewer and promotion rule. Missing/unknown fields that affect trust, egress or authority block dispatch.

### Priority order for the existing activation queue

| Priority | Existing queue work | Required closure evidence |
|---|---|---|
| P0 | CAF-Q-001 — A0 issuer/ingress/lease/cancel/recovery | Accepted issuer and lifecycle contract, state authority, fencing/idempotency and recovery cases |
| P0 | CAF-Q-002 — R-06 privacy/audit | Accountable approval path; event schema, integrity, retention, access controls and audit-unavailable behavior |
| P0 | CAF-Q-003 — workflow-source remediation | Exact-SHA source review, least privilege, action pinning, fail-closed errors and PR-only change route |
| P0 | CAF-Q-004 — task envelope and agent registry | Versioned schemas plus standards validation, negative fixtures and semantic reference checks |
| P1 | CAF-Q-005 — evidence manifest | Source SHA, workflow/run/job/artifact identity, digests, timestamps and distinct execution/verification/qualification states |
| P1 | CAF-Q-007 — runner/workspace/network target manifest | Accepted node roles, hosted/self-hosted lane boundaries, workspace cleanup, egress and storage profile |
| P1 | CAF-Q-008 — PR promotion and independent review | Protected-branch/ruleset evidence, required checks, independent verifier and no-auto-merge proof |
| P1 | CAF-Q-009 — provider quota/privacy/failover | Per-destination permission before first invocation; no silent paid fallback; privacy/retention eligibility |
| P2 | CAF-Q-010 — concurrency/retry/cancel/recovery | Atomic claim across runners, fencing, bounded retry, ambiguous-outcome reconciliation and cancellation |

The queue ordering is an execution proposal. Actual task dispatch still requires the accepted A0 and R-06 gates, exact target manifest and provider-specific approval.

## 5. Reuse-first component disposition

- **Reuse now as source candidates:** existing `profiles/agent-registry.json`, `.github/agent-system/registry.yaml`, provider registry/adapter schemas, the 23-lane manifest, the current cloud-agent v0.2 schema candidates, and existing GitHub Actions workflow infrastructure.
- **Keep provider adapters behind an admission boundary:** Gemini CLI is already represented in GitHub Actions; its post-merge tool contract needs a provider smoke test. OpenRouter/Groq or another free route may be candidates only after provider/model/data-policy review and quota approval.
- **Keep OpenHands as a pinned SDK/Agent Server candidate:** it provides reusable agent, tool, workspace and remote execution abstractions. Its Agent Server performs file/command operations inside a configured workspace; its own security and ingress requirements must be applied before any network exposure or integration.
- **Avoid a second scheduler or authority database** until source-bound evidence shows a concrete capability gap in the existing queue/claim subsystem.
- **Keep patch workers separate from read-only auditors and independent verifiers.** The worker must lack a direct protected-branch merge or deploy capability.

## 6. Workflow hardening review backlog

This wave makes no workflow edits. The next implementation-bound review should evaluate:

1. Pin third-party actions to verified full-length commit SHAs; in particular, replace floating action references only after verifying the exact trusted upstream commit and release lineage.
2. Recheck the minimum GitHub token permissions and scope write-capable MCP tools to the one job that needs them; never reuse the broad write token for read-only discovery.
3. Preserve the final outcome validator, but classify empty response, malformed JSON, invalid model stream, MCP tool resolution, authorization failure, quota exhaustion and PR-creation failure as separate statuses.
4. Always retain sanitized diagnostic artifacts and a compact job summary containing source SHA, provider/model alias, successful/failed tool-call counts, final disposition and artifact digests. Exclude raw secrets and sensitive prompts.
5. Verify that an action-step success can never override a failed/missing response, absent successful tool call, missing PR, or evidence-manifest mismatch.
6. Test stale SHA, unexpected branch, path escape, prompt injection, unapproved provider, quota exhaustion, cancellation, replay and malformed-output denial paths in a separately authorized qualification wave.
7. Review workflow inputs and external text as untrusted data; agent-generated content must never change its own authority scope.

## 7. Public source basis

- GitHub Actions secure use and immutable action pinning: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub-hosted runners and dynamic egress address ranges: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub Actions OIDC / cloud trust: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments
- Official Gemini CLI GitHub Action: https://github.com/google-github-actions/run-gemini-cli
- Official OpenHands Software Agent SDK source: https://github.com/OpenHands/software-agent-sdk
- OpenHands Agent Server security/configuration: https://github.com/OpenHands/docs/blob/main/sdk/arch/agent-server.mdx
- Jules task lifecycle and separate VM workspaces: https://jules.google/docs/tasks-repos/
- OpenRouter current pricing and privacy references: https://openrouter.ai/pricing/ and https://openrouter.ai/privacy/
- Groq data retention and Zero Data Retention controls: https://console.groq.com/docs/your-data
- Gemini API Additional Terms, including account eligibility, region and free-tier data-use conditions: https://ai.google.dev/gemini-api/terms

These sources describe platform features or provider terms at their own revisions. Availability, quota, terms and privacy posture can change. A provider must be evaluated for the exact model, account/project and data class before admission.

## 8. Acceptance boundary and next action

This wave records the current source state and a portable topology. It does not mark the Gemini dispatch fixed, the free-agent routes activated, the queue live, or Contour A qualified.

Next: complete source-bound static review of the current Gemini workflow and the actual OpenHands Agent Server workspace/tool boundary; reconcile these with A0, MH-12 and R-06; then prepare a narrowly scoped implementation/qualification proposal. The fresh post-merge provider smoke test remains pending an authorized eligible run.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md


## 9. Latest post-merge diagnostic and Wave 38 PR (2026-10-17)

### Fresh run evidence

- Latest retrieved main SHA: `6c2e8dbdee81c798b64e65546e7ded07093f100a`.
- [Gemini Autonomous Engineering Dispatch run 38977205621](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38977205621) completed with `failure` at the final “Validate Gemini produced an actionable PR result” step. The Gemini CLI wrapper step itself concluded `success`.
- Artifact `gemini-output`, ID `12079328104`, is 1,714 bytes with GitHub-reported digest `sha256:2411b20d32d6e68ce21f9bae75282416f101df55028e7b052fbb931a73e0854a`.
- Its JSON response is non-empty and records 3 model requests, 0 API errors, 2 tool calls, 0 successful calls, 2 failed calls, no branch, no PR and no commit.
- The stderr log shows registration/overwrite warnings for the allowed `mcp_github_*` tools, followed by “Tool ... not found” for `mcp_github_get_me` and `mcp_github_get_file_contents`.

### Refined root-cause classification

The current workflow sets `"tools": { "core": [] }` while selecting Gemini CLI `0.64.0`. Upstream [run-gemini-cli issue #532](https://github.com/google-github-actions/run-gemini-cli/issues/532) and Gemini CLI issue [#28361](https://github.com/google-gemini/gemini-cli/issues/28361) document that an explicitly empty `tools.core` allowlist emits a wildcard deny that also excludes MCP tools in Gemini CLI versions from 0.41.0 onward. The observed MediaHub configuration and the failed runtime tool lookup match that documented mechanism. This is stronger evidence than the earlier naming-only hypothesis.

The direct task prompt already uses fully qualified tool names, in accordance with the official Gemini CLI MCP naming reference. The action also copies upstream custom command prompts into the workspace; those templates contain stale/unqualified MCP references, as documented in issue #510. That is an adjacent defect surface for slash-command-driven tasks, while the latest failing task used its own direct prompt.

### Bounded source change prepared

PR [#307 — allowlist GitHub MCP tools without enabling core tools](https://github.com/VlDMlNSh/mediahub-os/pull/307) proposes a one-line workflow change:

- Before: `"tools": { "core": [] }`
- Proposed: `"tools": { "core": ["mcp_github_*"] }`

The server-side `includeTools` allowlist, workflow permissions, output validator, provider/model settings and PR-only behavior are unchanged. This preserves the core-tool deny-by-default stance while admitting only GitHub MCP tools by fully qualified prefix.

- Branch: `fix/gemini-mcp-core-allowlist-wave-38`
- Head commit: `5ae969763ff7ccbd22052efbd2661cf7bbdd7fd3`
- Workflow blob after read-back: `ed1ec965abc70041024afd4a1fc6ab17c6594fe7`
- PR base is `main` at `6c2e8dbdee81c798b64e65546e7ded07093f100a`.
- PR #307 remains open and unmerged. Standard pull-request checks and reviewer acceptance are pending. This report does not claim runtime repair until successful MCP calls, final output validation and an actual PR artifact are independently evidenced.

### Independent CI state

[Astra Verify run 38976598150](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976598150), attempt 2, completed successfully on the same main SHA. All 11 workflow steps passed, including compilation, cloud admission unit tests and signed command smoke test. This validates that CI workflow only; it does not qualify Gemini provider interaction or the cloud-agent fabric.

### Boundary

No fresh Gemini/model-provider call or Gemini dispatch was initiated by this continuation. The existing failed run was inspected as evidence. No secret value was accessed. No merge, deployment, infrastructure mutation, agent activation or qualification occurred. PR #307 is a source-level remediation proposal pending CI/review and a separately authorized provider-runtime acceptance event.

Next: review PR #307 checks and inspect its resulting merge-free source tree; then reconcile Google Action's copied command templates with the current fully-qualified tool names as a distinct follow-up, while preserving the least-privilege allowlist.
