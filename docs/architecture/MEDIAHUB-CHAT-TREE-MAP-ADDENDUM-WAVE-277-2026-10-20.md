# Map addendum — Wave 277: branch-tree drift and A0 authority crosswalk

## Status
Source-bound audit only. No runtime/host action, provider call, secret read, agent dispatch, merge, deployment, release, qualification or acceptance occurred. Contour A remains NOT_PROVEN / BLOCKED; Contour B remains gated pending deployment and independent acceptance of Contour A.

## Canonical navigation
- [Canonical project map](MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 277 report](../checkpoints/MEDIAHUB-CONTOUR-A-TREE-DRIFT-AND-A0-AUTHORITY-CROSSWALK-WAVE-277-2026-10-20.md)
- [Wave 275 legacy workflow drift audit](../checkpoints/MEDIAHUB-CONTOUR-A-WAVE-275-LEGACY-WORKFLOW-RETIREMENT-DRIFT-AUDIT-2026-10-20.md)
- [Wave 271 A0 issuer/task crosswalk](../checkpoints/MEDIAHUB-A0-ISSUER-TASK-CONTRACT-RECONCILIATION-WAVE-271-2026-10-20.md)
- [Wave 274 Alamo Claude route guards](../checkpoints/MEDIAHUB-ALAMO-CLAUDE-ROUTER-CANDIDATE-IDENTITY-AND-NONPAID-ROUTE-GUARD-WAVE-274-2026-10-20.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421 — controller-only reusable workflows](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- [PR #423 — legacy workflow retirement proposal](https://github.com/VlDMlNSh/mediahub-os/pull/423)

## Findings recorded
- Snapshot refs: `main` `80be45a70732b1d568164571d4273a6397792c3b`, tree `9ca2461bd2ee3028e43016089cdb39d08802ba52`; docs branch `51d2c0b6e917abb44f11a655aa4c7e68669c4eda`, tree `aac37fffd343fdcb782d6815179386003e065f06`.
- Exhaustive recursive tree comparison (`truncated=false` on both sides): 704 blob paths docs-only, 29 main-only and 14 same-path content deltas. Commit compare reports 2,835 ahead / 44 behind from merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`; its 300-file list is not exhaustive. Do not integrate the docs branch wholesale.
- Main-only entries include six Gemini/controller workflows, two obsolete old-host migration workflows and `tests/test_worker_security_gate.py`. The docs version of `ops/qualification/run_distributed_local_worker.py` has an over-escaped secret-assignment regex relative to main; tests from main are absent from docs. Audit exact source hashes in the linked Wave 277 report before resolving deltas.
- PR #423 was based directly on the current main SHA and deletes only the two retired workflows. Exact-head Astra Cloud Runtime Validation #39451818985 and Astra Verify #39451818611 report SUCCESS; PR remains Draft/unmerged and review API is empty.
- PR #421 remains Draft/unmerged at `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`. Exact-head Astra Cloud Runtime Validation #39425009654 and Astra Verify #39425009644 report SUCCESS; no submitted independent review. Caller-guard/secret-boundary review, non-launching negative caller-context test and governance/protection evidence remain open.
- The existing `mediahub.ai.astra-task@1.0.0` ingress, principal+capability authorization seam, local claims/leases, provider registry schema and node attestation do not yet compose into the required authenticated A0 hybrid mission/issuer/destination/DAG contract. The issuer/writer and trusted approval-verification lifecycle remains to be traced.
- Preserve A0 mission scheduling vs MediaHub Product State Authority separation. Alamo Claude is local executor-only; no Anthropic API, paid/unknown fallback or silent reroute. FCC, FreeLLMAPI, OmniRoute, OpenFlux remain unqualified candidates until upstream/auth/cost/terms/egress/version/Alamo evidence exists.

## Next
Trace the actual task producer/writer and trusted approval/attestation verifier; resolve authority ownership; then draft the versioned envelope and destination responsibility matrix before any static/mock-only negative contract tests. Do not wire the Wave 269 candidate into runtime or invoke any live route.
