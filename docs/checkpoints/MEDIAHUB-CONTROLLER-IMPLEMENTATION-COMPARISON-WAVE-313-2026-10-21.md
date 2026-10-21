# Wave 313 — Controller implementation comparison and gate decision (2026-10-21)

## Decision

**Select PR #432 as the safer candidate; keep it Draft and unmerged. Do not dispatch Gemini.** PR #431 restores the requested GitHub API transport but lacks the separate signed child authorization envelope visible in #432. Neither PR has a formal independent review recorded. This is a source/CI comparison, not security acceptance or qualification.

- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap blob SHA: `c6ae5c09b95e708f547b8eaae1aab3913bf10288`
- Canonical map blob SHA read-back: `8c526be39a7d58e009862b9eca2f350d3d948d8f` (Contents API returned empty body; not treated as evidence of empty file)
- Documentation branch HEAD at inspection: `888a79352be5c4f2701d754cb16e1c75f881864f`
- `main` HEAD/base SHA: `f16e5bae202a78584f273132e7f88c6e25d3142e`

## PR comparison

- [PR #431](https://github.com/VlDMlNSh/mediahub-os/pull/431), head `8177cce6859624e7740db204e0c19cb2bcdfe7ca`, open, non-draft, mergeable according to PR metadata. Implements controller-only `MEDIAHUB_GITHUB_TOKEN` and fixed child `workflow_dispatch` calls, but does not include #432's separate HMAC-signed envelope and child-side signature verification. No formal reviews are recorded. Combined commit status query returned no classic status entries; this alone is not proof of successful CI.
- [PR #432](https://github.com/VlDMlNSh/mediahub-os/pull/432), head `ea637eb55c87d44f0ce22730588e744c7470ee1d`, open, Draft, unmerged, mergeable according to PR metadata. Uses `MEDIAHUB_GITHUB_TOKEN` only in the controller, distinct `MEDIAHUB_DISPATCH_HMAC_KEY`, fixed child workflows, allowlisted scope/base, common full target SHA, and default non-launching probe. No formal reviews are recorded.
- Exact-head CI for #432 reports SUCCESS:
  - [Workflow contract validation #39604609734](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609734)
  - [Astra Verify #39604609752](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609752) — report states 444 tests passed
  - [Non-launching caller-context probe #39604609755](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609755)
  - [Controller probe #39604609766](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609766) — dispatch job skipped
  - [Astra Cloud Runtime Validation #39604609921](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609921)
- The no-secret probe exercised PR context only; it is not proof that trusted-main workflow dispatch works end-to-end.

## Governance and safety state

- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains the governing Contour A tracker; schema validation, authority and runtime admission gates described there remain distinct.
- Gemini Agent 1/2/3: **NOT RUN**. No controller dispatch run ID and no child run IDs exist for this pass. No secret values were read.
- Formal independent security review: **NOT RECORDED** for either PR. Effective `MEDIAHUB_GITHUB_TOKEN` permissions and branch-protection/governance evidence: **NOT VERIFIED**. `MEDIAHUB_DISPATCH_HMAC_KEY` configuration/separation: **NOT VERIFIED**.
- Claude Code on Alamo/server 3 and browser automation: **NOT RUN** in this pass; no verified host/capability/approved free-route evidence was gathered.
- Do not merge, configure/consume secrets as part of this pass, or launch agent mode before independent review, effective permission evidence, governance acceptance and a reviewed no-secret trusted-context probe.

## Acceptance criteria for next gate

1. Independent reviewer reviews exact PR #432 head `ea637eb55c87d44f0ce22730588e744c7470ee1d`, specifically HMAC canonicalization, task input boundaries, fixed workflow IDs, immutable target checkout, token isolation, correlation uniqueness/ambiguity, partial-dispatch failure behavior, permissions and artifact/log leakage.
2. Record effective token permission scope without reading or printing its value.
3. Verify secret presence/separation through an approved non-disclosing mechanism; do not expose secret contents.
4. Verify branch protection and governance decisions for Issue #301.
5. Re-run checks on the exact updated head; only then decide whether a non-launching trusted-main probe is permitted.
6. Keep all Gemini children **NOT RUN** until the above gates are evidenced and accepted.

## Provenance and limitations

- PR metadata, branch refs, file contents and Actions run metadata were read from GitHub during Wave 313.
- No code was changed in either controller PR by this pass; no PR was merged; no workflow was dispatched; no tests were run locally.
- This report is evidence of comparison and gate status, not qualification, release or acceptance.
