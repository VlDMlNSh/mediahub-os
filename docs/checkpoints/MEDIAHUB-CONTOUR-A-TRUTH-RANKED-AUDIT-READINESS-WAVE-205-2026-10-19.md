# MediaHub OS Contour A — truth-ranked audit and readiness (Wave 205)

- Date: 2026-10-19
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Disposition: bounded static hardening and evidence refresh; no governance gate promoted.

## Current refs and exact-head CI

- PR #375 was read back as OPEN / Draft / unmerged at head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.
- Immediately before the Wave 205 change, the PR branch compared as 11 commits ahead, 0 behind `main`, merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. Re-run compare before any integration decision.
- Test file blob at exact head: `2c5fae2d431ca765bb548f4a2b5d70874961a438`.
- [Astra Verify run 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907), job `118206367053`: SUCCESS. Compile, Worker workflow credential policy regression tests, Cloud admission unit tests and Signed command smoke test succeeded.
- [Astra Cloud Runtime Validation run 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833), job `118206368089`: SUCCESS.
- The earlier commit `40ca9a2eabf69949134c941babd2624559f0cb1f` and its green runs remain historical exact-SHA evidence; Wave 205 evidence is bound to `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.

## Work completed

Reviewed the Wave 204 YAML oracle and found that PyYAML's default `safe_load` silently accepts duplicate mapping keys, allowing an ambiguous permissions mapping to be collapsed before policy checks. Added a safe loader that rejects duplicate mapping keys, including unhashable keys, and negative tests for duplicate workflow-level and job-level permission keys. The workflow test suite now includes these cases, and the repository's exact-head CI passed.

This is a focused hardening of the static oracle. It is not a full formal model of GitHub Actions permission evaluation. The tests do not prove server-side authorization, publisher provenance, runtime credential isolation, output validation, or the security of a future trusted publisher.

## Truth-ranked gaps

### P0 — must remain gating
1. **Issuer/capability authority:** Issue #301 and Waves 189–191 record an enforcement gap around signed capability envelopes, issuer lifecycle, exact operation/resource binding, expiry, revocation and replay. Governance must settle the contract; do not invent issuer/key semantics.
2. **Trusted output publication:** worker workflow uses `contents: read` and checkout `persist-credentials: false`, but direct `git push` behavior remains in the worker workflow path. Separate worker-produced artifacts from a publisher that independently reconstructs from an immutable base, validates repository/ref/path/diff, obtains a narrowly scoped write grant, records provenance, and verifies remote SHA.
3. **Independent security/governance disposition:** PR #375 remains Draft/unmerged; Issue #301 remains open. Green CI is not review approval or qualification evidence.

### P1 — required before qualification
4. **Semantic YAML oracle:** duplicate-key ambiguity is now rejected. Further review should cover GitHub-specific schema semantics, permission inheritance, reusable workflows, composite actions, expression contexts and pinning policy.
5. **Isolation and FCC propagation:** accepted runner/workspace/network target manifest and secret-boundary evidence are still required.
6. **Supply chain and additional agents:** Gemini parity/workflow presence is not proof of authorized identity, live availability, safe provider routing or persistent autonomous operation.
7. **Documentation / provenance:** this report, map and checkpoint must remain cross-linked with read-back blob SHA evidence.

### P2 — integration discipline
8. **Branch protection and ancestry:** branch protection/review settings have previously been inaccessible through API (403); do not infer they are enabled. Re-check settings and current ancestry before merge. Keep changes isolated and avoid broad sync/rebase until the integration path is proven safe.

## Architecture options, ranked

1. **Preferred:** isolated worker emits a quarantined artifact/patch; trusted publisher validates authority and diff and publishes from immutable source using narrowly scoped credentials. Worker receives no write credential.
2. **Conditional implementation:** GitHub App or equivalent short-lived publisher credential, only after governance-approved issuer/capability and key lifecycle contracts, path/ref constraints, audit, revocation and recovery tests.
3. **Rejected as default:** direct model-controlled worker `git push` with ambient write authority.

## Readiness

- YAML semantic oracle hardening: **CI-verified at exact candidate SHA**.
- PR integration readiness: **NOT READY / Draft** pending independent review, governance disposition, branch-protection evidence, ancestry and full diff review.
- Contour A: **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
- Contour B: **GATED**.

No worker dispatch, Gemini/provider call, secret access, host command, merge, deployment, qualification or acceptance occurred in this wave.

## Next action

Obtain independent review of the oracle and output publication design. Resolve issuer/capability semantics through governance; then design/test a publisher boundary and adversarial cases (wrong repo/ref/SHA, expired/revoked/replayed grants, forbidden paths, symlink/binary/oversized patches, forged Git metadata, race/cancel, audit outage, remote SHA mismatch). Re-read PR head and exact-head CI before every subsequent integration decision.
