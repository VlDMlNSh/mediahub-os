# Contour A — PR #375 divergence and tests (Wave 221)

- Date: 2026-10-20
- Status: TARGETED TEST PASS; INTEGRATION BLOCKED BY BRANCH DRIFT; NOT APPROVAL
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Candidate PR: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/396

## Exact refs and divergence

Authenticated GitHub CLI and Git on the SentinelX host returned:
- PR #375 head: `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.
- PR base SHA: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Current `origin/main`: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- `git rev-list --left-right --count origin/main...origin/pr-375-wave220`: `6 12` (main has 6 commits absent from PR; PR has 12 commits absent from main).
- Merge base remains the old base SHA.
- PR remains OPEN / Draft / mergeState CLEAN / no review decision. Both named CI checks SUCCESS on exact PR head.
- Diff against merge base has 3 paths: worker workflow, Astra Verify workflow, and `ops/qualification/test_worker_workflow_credential_policy.py`.
- `git diff --check origin/main...origin/pr-375-wave220` passed with no output.

Decision: do not merge/rebase PR #375 directly. Reconcile its twelve commits and six missing main commits, including the current-main security-gate restoration, before making a fresh narrow candidate.

## Targeted tests

Created disposable venv `/tmp/mediahub-contour-a-wave220-venv` and installed only `requirements-dev.txt` dependencies into it. No shared environment or tracked product files were changed.

At exact PR head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`, ran:
`/tmp/mediahub-contour-a-wave220-venv/bin/pytest /tmp/mediahub-pr375-wave220/ops/qualification/test_worker_workflow_credential_policy.py -q`

Result: **11 passed in 0.10s**.

At separate local checkout SHA `4a131acf6484f6e370625b0ebc454ee7b4b5116c`, ran:
`pytest tests/test_validate_contracts.py tests/test_worker_security_gate.py tests/test_distributed_workflow_contract.py -q`

Result: **28 passed in 0.49s** after installing declared dev dependencies in the disposable venv. This is not a test result for PR #375 or current main.

## Limits and next action

PR #375 reduces workflow permissions and disables persisted checkout credentials, but does not remove worker-side Git publication or prove issuer/capability and artifact provenance enforcement. Those remain separate gates.

No rebase, merge, push, workflow dispatch, deployment, or credential change was performed. Immediate automation run was requested, but no completion receipt is available; the eight-hour background run remains unconfirmed. Contour A remains NOT_PROVEN / BLOCKED; G0–G11 BLOCKED; G11 HUMAN_ONLY.

Next: inspect current-main changes since the old base, especially worker workflow, verification workflow, security gate and tests. Build a fresh minimal candidate on current main only after confirming no behavior is lost; rerun targeted tests and require independent review.

Canonical checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md