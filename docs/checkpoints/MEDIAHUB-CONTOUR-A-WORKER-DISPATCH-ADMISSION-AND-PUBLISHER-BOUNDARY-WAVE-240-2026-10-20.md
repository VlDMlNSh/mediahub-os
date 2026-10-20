# MediaHub OS — Wave 240: worker dispatch admission and publication boundary

- Date: 2026-10-20
- Status: **SOURCE AUDIT COMPLETE; DISPATCH NOT AUTHORIZED BY CURRENT EVIDENCE; CONTOUR A NOT_PROVEN / BLOCKED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #405: https://github.com/VlDMlNSh/mediahub-os/pull/405
- Previous pass: [Wave 239 — Gemini dispatch and large-document I/O](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-GEMINI-DISPATCH-AND-LARGE-DOCUMENT-IO-WAVE-239-2026-10-20.md)

## Live refs and evidence

- `main` observed through compare API at `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- PR #405 remains OPEN / Draft / mergeable; head `59951fb247a6251b1693d5f0bc807c96480f7424`; base `main`; compare result: 2 commits ahead, 0 behind, merge base equals base SHA.
- PR #405 workflow blob: `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`.
- PR #405 worker blob: `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`.
- Regression test blob: `12f25f684f0b37cf6d34d5c905394f9e0664fbf2`.
- Exact-head workflow runs `39377730257` (Astra Verify) and `39377730292` (Astra Cloud Runtime Validation) report SUCCESS. The combined-status endpoint returned no individual statuses. CI success does not establish signed-task admission or runtime credential boundaries.
- Issue #301 remains OPEN.
- Bootstrap blob `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`; checkpoint blob `b9978ca997f966c1d3fc0c9baa2520a0c5366826`; Master Roadmap blob `beef785c787702dc174cf9a5515bac8c9f4b292f` (317,131 characters returned by connected reader).
- Canonical map blob `2187b4ca50792fe073f0979442c0f73432a2f6f9`; connected Contents read again returned empty content. Treat as a reader limitation, not an empty file.

## Source-bound findings

### 1. Workflow input reaches self-hosted execution

The workflow `.github/workflows/astra-distributed-local-worker.yml` exposes `workflow_dispatch` inputs including `command_id`, `target_sha`, `task_id`, `node_id`, `executor`, and full `task_json`. The JSON input is assigned to `ASTRA_MICRO_TASK_JSON` in the self-hosted job environment. The workflow pins checkout to the supplied target SHA and uses `persist-credentials: false` with `permissions: contents: read`, which is a useful least-privilege reduction.

### 2. Worker validates shape and target SHA, but this is not issuer/capability admission

At worker blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`, `load_task()` parses JSON and checks required field names. `main()` checks that `ASTRA_TARGET_SHA` is a 40-character lowercase hexadecimal SHA and equals the checked-out HEAD. These checks establish payload shape and target consistency only; they do not by themselves establish a trusted issuer, signature, capability, expiry, revocation, replay protection, or binding of the command to the authorized task/node/executor.

The signed-command verifier discussed in earlier project evidence is not proven integrated into this worker path. No claim is made that another external gate cannot exist; none was evidenced in this source audit.

### 3. Worker still publishes directly to Git

At worker source lines 663–680, changed work is staged with `git add -A`, committed, and pushed using `git push origin HEAD:refs/heads/{branch}`; then `git ls-remote` is used to verify the branch SHA. The worker therefore still requires publication authority and is not artifact-only. Workflow-level read-only permissions do not prove that self-hosted ambient credentials cannot authorize this push.

### 4. Dispatch decision

Do not dispatch this worker with arbitrary task JSON or use `PAT_DISPATCH` to compensate for the current boundary. The secret value was not read, printed, logged, or passed to any process. This pass did not dispatch a workflow, launch Gemini agents, run a worker, access hosts/provider credentials, merge, deploy, or qualify Contour A.

## Required next engineering slice

1. Implement and independently test a fail-closed issuer/capability admission path bound to immutable command ID, task digest, target SHA, node, executor, expiry and policy. Define replay, revocation, cancellation and recovery behavior from accepted contracts rather than inventing a token protocol.
2. Replace worker-side branch creation/commit/push with an artifact-only result (patch or declared output files plus manifest and SHA-256 digest). Keep ref updates in a separate publisher that independently validates issuer/capability and artifact provenance.
3. Add negative tests for missing/invalid signature, wrong target SHA, task/node/executor mismatch, expired/revoked/replayed command, forbidden path, artifact digest mismatch, cancellation, and attempted worker ref mutation.
4. Only after source review and required tests, consider a controlled workflow dispatch. Keep all Gemini task briefs from Wave 239 prepared but not dispatched until a suitable authorized dispatch path exists.

## Verification limits

This was a read-only source audit and report write. No code or workflow was changed. No large-file write test was performed; Wave 239's large-read evidence remains separate from write verification. No agent dispatch, runtime execution, qualification, release, deployment, or acceptance is claimed.

## Next step

Implement the artifact-only worker/publisher boundary and negative admission tests on a dedicated branch; then verify the exact diff and CI before any controlled dispatch. Keep Contour B gated until Contour A is deployed and independently accepted.
