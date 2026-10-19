# MediaHub OS Contour A — truth-ranked gaps and execution blueprint (Wave 203)

Date: 2026-10-19. This is a research/sequence proposal, not an accepted governance decision.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
Security candidate: https://github.com/VlDMlNSh/mediahub-os/pull/375
Related candidates: https://github.com/VlDMlNSh/mediahub-os/pull/374 and https://github.com/VlDMlNSh/mediahub-os/pull/376

## Executive truth

Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains gated. Generated qualification truth on main, blob 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731, reports G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED. G11 is HUMAN_ONLY.

The map content was successfully retrieved by blob SHA 2eb9717ed8194b4a0a07391bd8acad20dbc0a7da after the path fetch returned empty content. Its latest inventory marker appears older than the Wave 202 entry near the map tail, so map freshness/reconciliation remains open.

## Ranked gaps (risk priority, not approval)

| Rank | Gap | Evidence | Closure evidence | Fail-closed rule |
|---|---|---|---|---|
| P0 | Issuer/capability authorization and lifecycle | Waves 189–191 report mesh admission does not yet prove signed capability-envelope verification, exact operation/resource binding, expiry, revocation and replay protection across one authority boundary. | Governance-selected issuer/key lifecycle and versioned envelope; cross-layer contract; positive and adversarial tests; independent review. | No capability-bound execution until authority and envelope are approved and verified. |
| P0 | Trusted publisher and output provenance | PR #375 limits workflow token to contents:read and sets three checkouts to persist-credentials:false, while worker code retains direct git-push behavior. | Separate trusted publisher; clean reconstruction from immutable base SHA; repo/ref/path/diff validation; least-privilege short-lived write grant; audit record and remote SHA read-back. | Keep PR #375 Draft/unmerged; do not restore ambient worker write credentials. |
| P0 | Independent security/governance disposition | Issue #301 remains open; PR #375 review list was empty in the checked response. | Explicit independent review and governance disposition tied to immutable contract/test revisions. | CI is not approval. |
| P1 | Exact-head CI and static oracle validity | Wave 202 records CI at 5ed32d0cc1375aa2cd524d1963183497cc0ff6eb; this evidence cannot be transferred to a later head. Regex oracle is not a YAML semantic parser. | Refresh head; verify exact-SHA runs; use YAML parser to inspect workflow/job effective permissions and quoted/flow forms. | Do not claim current-head CI without matching SHA. |
| P1 | Runner/workspace/network isolation and FCC propagation | Earlier Wave 181 reported no connected SentinelX hosts at that time; freshness is not implied. Isolation and subprocess secret propagation remain unresolved in prior reports. | Current host inventory; bounded workspace and egress; secret non-inheritance proof; negative tests and audit/recovery evidence. | No host dispatch/provider call while readiness and isolation are unproven. |
| P1 | Gemini workflow supply chain and dispatch | PR #376 parity tests do not prove valid credentials, a successful live run, or safe output publication. Prior reports note mutable action/dependency pins and unresolved MCP image tag-to-digest provenance. | Immutable pins, OCI digest/provenance, server-side ref/path restrictions, controlled run evidence, trusted publisher. | Do not describe workflow_dispatch agents as permanently running. |
| P1 | Canonical map/checkpoint freshness | Path fetch failed with 404/empty response; blob retrieval worked. Map header/inventory and tail need reconciliation. | Read-back report, map and checkpoint by blob SHA; align index/header with latest wave and preserve historical IDs/Baseline 2.0. | A successful blob fetch does not prove index freshness. |
| P2 | Branch divergence/integration hygiene | Comparison reported docs branch diverged from main: 2471 ahead, 27 behind; merge base f0f406feb9f9816b009f4e6e756813541e53b9bc. PR #374 is Draft and connector previously reported mergeable=false. | Refresh refs, inspect ancestry/diff/branch protections, explain divergence before any integration. | No force push or broad merge while ancestry/protection is unresolved. |

## Architecture blueprint

1. Freeze evidence: current PR #375 head SHA, PR-triggered runs and statuses for that exact SHA, reviews, latest Issue #301 comments, main/docs refs and generated truth.
2. Close static-oracle gap offline: YAML-parser-based tests for workflow-level and job-level effective permissions; no worker dispatch.
3. Resolve authority contract before coding: issuer, principal, operation, repository, base ref, target SHA, allowed paths, expiry/revocation/replay, output digest and audit evidence. If governance has not selected semantics, record decision questions; do not invent them.
4. Only after contract review, implement isolated publication: worker submits patch/result artifact; trusted publisher checks out immutable base, validates and reconstructs the candidate, and performs the only scoped write. No write credentials enter model-controlled processes.
5. Adversarial tests: wrong issuer/repo/ref/SHA; expired/revoked/replayed grant; forbidden path; binary/symlink; oversized output; forged Git metadata; race/cancel; publisher or audit outage; remote SHA mismatch. All invalid cases must fail closed without unauthorized writes.
6. Run focused tests and CI on frozen exact SHA, preserve job evidence, obtain independent security review. CI is necessary, not sufficient.
7. Integrate only after protection, approval, ancestry, diff and data-loss checks pass. Keep Draft/unmerged until gates are met.
8. Read back the report, map and checkpoint after updates, recording blob/commit SHAs. Keep Master Roadmap unchanged unless a reviewed sequencing/authority change requires it.

## Evidence snapshot

- PR #375: OPEN, Draft, unmerged; updated 2026-10-19T17:03:22Z. Current head SHA was not exposed in the normalized response, so current-head CI is unverified in this wave.
- Candidate workflow blob: c24ad16ab8ed59fd4dbad9538063f63a933eab2c.
- Candidate test blob: 1046b59acf4a97390b64162dcbbb81e458ec26c2.
- Prior CI evidence for commit 5ed32d0cc1375aa2cd524d1963183497cc0ff6eb: Astra Verify run https://github.com/VlDMlNSh/mediahub-os/actions/runs/39290847516 and Astra Cloud Runtime Validation run https://github.com/VlDMlNSh/mediahub-os/actions/runs/39290847553. Do not transfer these results to a different head.
- Issue #301 has 42 comments in the fetched history; latest inspected Wave 192 comment says PR #376 is Draft/unmerged and branch-protection API returned 403, leaving protection/review settings unverified.
- No worker dispatch, Gemini dispatch, provider call, secret access, host command, merge, deployment, qualification, or Contour B work was performed.

## Next action

Execute evidence freeze and offline YAML semantic-oracle work. Do not implement the trusted publisher or choose issuer/key semantics before governance resolves the authority contract.

Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains gated.
