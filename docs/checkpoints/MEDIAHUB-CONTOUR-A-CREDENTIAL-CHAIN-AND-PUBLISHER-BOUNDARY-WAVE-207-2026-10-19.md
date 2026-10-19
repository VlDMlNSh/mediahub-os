# MediaHub OS Contour A — credential-chain and publisher-boundary audit (Wave 207)

- Date: 2026-10-19
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Scope: bounded read-only audit and evidence synchronization. No runtime worker/provider dispatch, credential use, merge, deployment or qualification.

## Fresh state

- PR #375: OPEN / Draft / unmerged; head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`; GitHub reports `mergeable: false`.
- Fresh compare against `main`: 12 commits ahead, 3 behind; merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. This supersedes the earlier Wave 206 12/2 snapshot. Do not merge/rebase based on stale ancestry.
- Exact-head CI remains green at this SHA: [Astra Verify 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907) and [Astra Cloud Runtime Validation 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833).
- Issue #301 OPEN. No PR review submissions returned. Branch protection/required-review configuration remains unverified; a prior API request returned 403.
- Generated current truth on `main`, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`: G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED.

## Credential-chain findings

Inspected worker program blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` and workflow blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`, both at PR head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.

1. Workflow permissions are `contents: read`; all three `actions/checkout@v4` steps set `persist-credentials: false`. The workflow's own YAML has no literal push command.
2. The worker script does contain direct publication logic: it creates a task branch, stages all workspace changes with `git add -A`, commits, pushes to `origin`, then checks remote SHA via `git ls-remote`. SHA equality only confirms remote branch matches that worker-created commit; it does not establish authorization correctness, artifact review or safe content scope.
3. Worker subprocess helper `run()` defaults to the process environment unless an explicit environment is passed. Model/FCC setup also starts from `os.environ.copy()`; the model token is loaded from a local FCC env file. Therefore, workflow permission and checkout credential settings alone do not prove the effective credential chain for a self-hosted runner. Ambient environment variables, runner-level Git configuration/credential helpers, remote URL configuration, OS account access and FCC process environment still need a controlled audit.
4. Static search of the worker source did not find explicit `git config`, `GITHUB_TOKEN`, `GH_TOKEN` or a dedicated Git credential source in the checked lines; absence in this file is not proof those sources are absent from the runner environment or Git configuration.
5. The local env path includes a user-home location in the worker's node configuration. This pass did not access that file or inspect any secret values; it is a path/configuration fact, not evidence that a credential is present or usable.

## Decision / architecture

**P0 — do not restore write permissions to the worker.** Treat the present direct-push path as an unresolved authority boundary, not as proven exploitable or proven harmless.

Preferred target:
- worker runs without repository write credentials and emits a quarantined patch/artifact plus immutable provenance (target SHA, repository, task/command IDs, file manifest, diff digest, tests, verifier identity);
- trusted publisher runs separately, independently checks issuer/capability, target repo/ref/base SHA, allowlisted paths, patch size/type/symlink rules, commit ancestry and replay/expiry/revocation, and publishes with narrowly scoped short-lived credentials;
- publisher records an auditable decision and fails closed on missing/revoked authority, audit outage, base drift or SHA mismatch.

Do not implement issuer semantics or credential minting ad hoc. Governance must first settle issuer/capability authority, resource and operation binding, expiry, revocation, replay protection, and recovery.

## Ranked gaps

### P0
1. Establish the complete self-hosted runner credential chain using non-secret metadata only; document token sources, Git config scopes, remote URL shape, credential helpers, inherited environment and process boundaries. Never print or copy secret values.
2. Replace direct worker publication with artifact-only output plus a separately trusted publisher.
3. Obtain independent security/governance review and verifiable branch-protection/required-review evidence.

### P1
4. Add isolated tests proving worker subprocesses do not inherit publisher credentials and that output is quarantined; test environment scrubbing without exposing secrets.
5. Validate publisher handling of wrong repo/ref/SHA, expired/revoked/replayed grants, forbidden paths, symlink/binary/oversized patches, forged Git metadata, cancellation races, audit outage and remote-SHA mismatch.
6. Continue semantic YAML policy review beyond duplicate-key rejection.

### P2
7. Resolve branch divergence only after governance and publication-boundary work, fresh diff/ancestry inspection and protection verification.

## Readiness

- Static policy tests / exact-head CI: verified green for the current PR SHA.
- Effective runner credential chain: NOT VERIFIED.
- Worker write-authority isolation: NOT PROVEN.
- Trusted publisher: NOT IMPLEMENTED / NOT QUALIFIED by this pass.
- Contour A: NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED.
- Contour B: GATED.

## Next bounded action

Review the exact runner bootstrap/service configuration and Git configuration source paths using read-only metadata only, without reading secret values or invoking the worker. Then propose a small testable worker contract that strips ambient publisher credentials and exports only an allowlisted environment; do not ship it until contracts and CI tests demonstrate that model execution still functions without write authority.
