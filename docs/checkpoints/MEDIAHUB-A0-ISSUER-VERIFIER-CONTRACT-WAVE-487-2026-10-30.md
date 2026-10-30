# Wave 487 — A0 issuer/verifier contract candidate (2026-10-30)

## Outcome

**DRAFT NORMATIVE CANDIDATE CREATED / READ-BACK PENDING / INDEPENDENT A3 REVIEW NOT RUN / RUNTIME BLOCKED.**

Primary artifact: [A0 Issuer and Verifier Contract — Wave 487](../architecture/MEDIAHUB-A0-ISSUER-VERIFIER-CONTRACT-WAVE-487-2026-10-30.md).

This pass translated the owner-directed Wave 486 dispositions into a technology-neutral, testable contract. It specifies authority boundaries, principal/issuer lifecycle, capability semantic claims, delegation, mandatory verifier checks, 300-second lifetime and 30-second revocation freshness defaults, active-work fencing, durable idempotent A0 acceptance, lease lifecycle, R-06 audit/privacy, versioning and 40+ acceptance scenarios.

## Source evidence

- Wave 486 disposition re-read: blob `13e6745463dbc05a7c188423bb45ffb2b210c789`.
- Wave 485 skeleton re-read: blob `14cf0194504824a17569433d4478154eb44afc3f`.
- Canonical map blob rechecked: `75f62685459ec99ebf8be478f4e9096cdb842b1d`; Contents API returned empty content. No canonical-map rewrite attempted.
- Issue #301 re-read: objective and ordered steps still require A0 authority closure, runner/workspace/network manifest, Draft 2020-12 validation, independent schema review and cloud worker hardening.
- Master Roadmap blob re-read: `ea7e94e921045253f3e6494438e197c4bafae3a0`; Cloud Pool First priority remains in Wave 483 draft PR #595; server hardware stays second phase.
- Bootstrap blob re-read: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.

## Gemini controller feasibility check

Controller source on main:
- `.github/workflows/gemini-batch-dispatch-controller.yml` blob `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- It supports `probe`, `agents`, `review`; dispatch confirmation is explicit for workflow_dispatch; issue-comment /next triggers fixed `agents` mode.
- Required controller secrets in source: `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`; enable gate variable: `MEDIAHUB_GEMINI_BATCH_ENABLED`.
- Child credential refs in source: Agent 1 `GEMINI_API_KEY`, Agent 2 `GEMINI_API_KEY_2`, Agent 3 `GEMINI_API_KEY_3`; model variable `GEMINI_MODEL`; children also require `MEDIAHUB_DISPATCH_HMAC_KEY`.
- Exact presence/value/configuration of repository secrets and variables is NOT VERIFIED. No secret values were accessed.
- Controller's three task strings are fixed generic per-/next tasks. They do not accept this Wave 487 task packet as a caller-supplied per-agent task. Agent 2 is described as Research & Architecture; Agent 3 is Security & Verification Review. Therefore this controller version cannot prove it dispatched this exact contract task to the requested independent roles.
- Controller review mode is pinned to historical FCC target `074f20eb495666946a14410ab88d566aaa754f24` and fixed FCC diffs, not Wave 487. It is not suitable as an independent review route for this artifact.
- Result: Gemini roles **NOT RUN** for this Wave 487 packet. No probe, child run, provider call, secret access or workflow dispatch was initiated. A controller extension with authenticated, allowlisted task profiles and task-to-role acceptance criteria is a prerequisite before dispatching this exact packet.

## Current PR and branch governance

- Prior PR #599 remains Draft/Open/Unmerged and stacked on PR #598 branch; current recorded head `824bb2568b2ac8bb3dceb3608366668e99bab95e`.
- PR #599 exact-head workflow runs: empty; combined statuses: empty; formal reviews: 0; inline review threads: 0. CI and independent review NOT VERIFIED.
- New Wave 487 branch is stacked on Wave 486 head `824bb2568b2ac8bb3dceb3608366668e99bab95e`.
- No merge, runtime edits, tests, provider calls, secrets, server work, deployment, qualification or acceptance.

## Contract disposition

- Contract status: DRAFT NORMATIVE CANDIDATE / NOT ACCEPTED / NOT IMPLEMENTED.
- The requirements use MUST/SHOULD language as a proposed normative target; they are not yet binding.
- The 300-second/30-second defaults and retention targets are policy proposals requiring load, clock, revocation, privacy/legal and operational review.
- Protocol, token format, canonical serialization, crypto algorithm, KMS/HSM, identity source, database, audit sink, endpoint and named operational teams remain ADR/source-research items.
- Wave 482 A0-ISSUER-01 remains a HIGH source-level provenance gap, not a confirmed exploit. Runtime remediation remains blocked until independent review and implementation gates pass.

## Git evidence

- Parent: `824bb2568b2ac8bb3dceb3608366668e99bab95e`.
- Branch: `docs/wave487-a0-issuer-verifier-normative-contract-20261030`.
- Contract create commit: `6969de41410818a5a6b61ce90a32ee809aa803da`.
- Report blob SHA after PR reconciliation: `0cff710f93bda21eca3158c0b387afea4d16cfaa` (updated below in this final report revision); map addendum blob SHA: `81b95b2cf62ae06eebe0531f283dc90489fc546e`; checkpoint blob SHA: `8f692d2cda868eb17201d10b67f9539f6b07d91c`.

## Next

1. Obtain independent A3 review of Wave 486 decision + Wave 487 contract.
2. In parallel on the Contour A roadmap, identify and accept the authoritative runner/workspace/network target manifest; do not skip A0 security admission.
3. Complete standards-compliant Draft 2020-12 schema validation and positive/negative fixtures with tool/version/digests.
4. Design a controller extension so the three Gemini roles can receive a bounded task profile on one immutable target, while preserving signed inputs, allowlists, exact secret names, output quarantine and provenance.
5. Keep runtime issuer changes blocked until contract review, protocol ADR and required tests.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301


## Final PR reconciliation

- Draft PR [#600](https://github.com/VlDMlNSh/mediahub-os/pull/600) remains Open/Draft/Unmerged and stacked on PR #599.
- The latest exact PR head, ahead/behind counts and exact-head checks are recorded by GitHub and the finalization evidence in Issue #301; always re-read before integration.
- At the initial PR-head check, workflow runs and combined statuses were empty; formal reviews and inline threads were zero. CI and independent A3 review remain NOT VERIFIED.
- Do not merge directly to the canonical documentation branch; preserve the Wave 486 → Wave 487 stack.
