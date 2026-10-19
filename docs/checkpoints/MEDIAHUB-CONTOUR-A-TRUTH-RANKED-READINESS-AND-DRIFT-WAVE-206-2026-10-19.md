# MediaHub OS Contour A — truth-ranked readiness and drift audit (Wave 206)

- Date: 2026-10-19
- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Disposition: bounded evidence refresh and architecture readiness assessment; no gate promoted.

## Verified current state

- PR #375 currently reports OPEN / Draft / unmerged at head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.
- Branch compare against `main`: **12 ahead / 1 behind**, status `diverged`, merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. This is a change from the prior Wave 205 snapshot (11 ahead / 0 behind). Do not integrate until the new base-side commit and full diff are reviewed.
- Exact-head workflow evidence for this PR head:
  - [Astra Verify run 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907) — completed / success.
  - [Astra Cloud Runtime Validation run 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833) — completed / success.
  - The combined-status endpoint returned no status entries; the two completed workflow runs are the positive evidence. Do not infer required-review or branch-protection status from this.
- Issue #301 remains OPEN and explicitly says it is a tracker, not authorization for credential access, provider calls, workflow dispatch, infrastructure changes, merge or deployment.
- Generated truth on main, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`, still lists G0–G11 BLOCKED and overall `NOT_PROVEN / BLOCKED`; G11 is HUMAN_ONLY.

## Review of the YAML semantic oracle

The candidate test file at commit `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`, blob `2c5fae2d431ca765bb548f4a2b5d70874961a438`, uses a PyYAML SafeLoader subclass that rejects duplicate mapping keys. It includes negative fixtures for duplicate contents permission keys at workflow and job scopes. The exact-head CI above passes.

Boundaries of this evidence:
- This is an offline static test; it does not execute the worker workflow or exercise GitHub's server-side authorization.
- PyYAML's YAML 1.1 interpretation of unquoted `on` can differ from GitHub Actions' YAML handling; current tests do not prove full workflow-schema equivalence.
- The permission checker is purpose-built and must be independently reviewed for inheritance, reusable workflows, action-level behavior, expression contexts, unknown permission keys, aliases/merge keys and all accepted permission syntaxes.
- Green CI does not establish publisher provenance, runtime isolation or governance acceptance.

## Truth-ranked gaps

### P0 — gating
1. **Issuer/capability contract:** signed capability-envelope verification and exact operation/resource binding remain unresolved in the reviewed admission path. Governance must define issuer trust, expiry, revocation, replay handling, audience, repository/ref/resource scope and key lifecycle before implementation.
2. **Trusted publisher boundary:** worker workflow still has a direct `git push` behavior in its code path. `contents: read` and `persist-credentials: false` reduce ambient checkout credentials but do not by themselves make a write-capable path safe. Prefer worker-produced quarantined artifacts and independent publisher reconstruction from immutable base SHA with validated diff/path/ref, scoped short-lived credentials, audit and remote SHA readback.
3. **Independent disposition:** PR remains Draft and Issue #301 open. Independent security review, branch-protection settings and approval evidence are not established by green CI.

### P1 — qualification prerequisites
4. Full GitHub Actions semantic validation and dependency/action pinning.
5. Runner/workspace/network isolation and FCC/secret-boundary evidence.
6. Provider/Gemini execution provenance and routing evidence; workflow presence does not prove agents are available or autonomously running.
7. Adversarial publisher tests: wrong repo/ref/base SHA, forbidden paths, symlinks/binaries/oversized artifacts, forged Git metadata, expiry/revocation/replay, races/cancellation, audit failure and remote SHA mismatch.

### P2 — integration discipline
8. Refresh refs and inspect the one-commit main-side drift; establish branch-protection/review requirements with evidence before rebase/merge. No broad sync or force push.

## Architecture options ranked

1. **Preferred:** isolated model-controlled worker emits a quarantined patch/artifact; a separate trusted publisher validates source SHA, authority, repository/ref/path/diff, reconstructs the change and performs a constrained publication with auditable short-lived credentials.
2. **Conditional:** GitHub App or equivalent publisher identity, only after governance approves issuer/capability and key lifecycle semantics and tests expiry/revocation/replay.
3. **Not recommended:** direct model-controlled worker `git push` with ambient or persistent write credentials.

## Readiness disposition

- YAML oracle at current PR head: **CI-verified; independent semantic review still required**.
- PR #375 integration: **NOT READY** — Draft, branch diverged 12 ahead / 1 behind, governance and independent review unresolved.
- Contour A: **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
- Contour B: **GATED**.

No worker/Gemini/provider dispatch, secret access, host command, merge, deployment, qualification or acceptance occurred in this wave.

## Next action

Inspect the single main-side commit and current full PR diff, refresh exact-head CI after any change, and obtain independent review. In parallel, resolve issuer/capability semantics through governance before implementing the trusted publisher. Keep PR #375 Draft until the evidence and mandatory gates are satisfied.
