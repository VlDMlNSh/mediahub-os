# MediaHub OS Contour A — worker child-environment isolation (Wave 227)

Date: 2026-10-20. Status: implementation candidate with focused local tests; not qualified, deployed, or accepted.

## Navigation and baseline

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing objective: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Related prior design: [Wave 207 credential chain](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-CREDENTIAL-CHAIN-AND-PUBLISHER-BOUNDARY-WAVE-207-2026-10-19.md), [Wave 210 worker artifact/publisher boundary](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-WORKER-ARTIFACT-PUBLISHER-BOUNDARY-WAVE-210-2026-10-19.md), and [Wave 179 negative-test matrix](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-TRUSTED-PUBLISHER-CONTRACT-NEGATIVE-TEST-MATRIX-WAVE-179-2026-10-19.md).
- Implementation base: `main` / `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- Work branch: `work/contour-a-wave227-model-child-env-isolation-20261020`.

## Findings and change

The distributed worker previously built the Codex child environment from `os.environ.copy()`, built the FCC server/client environment by copying the runner environment and overlaying the full FCC env file, and separately built test environments from the full runner environment. The latter code also copied the environment twice, discarding the first controlled `PYTHONPATH` assignment. This creates unnecessary propagation of ambient runner credentials/configuration into model-controlled processes and tests.

Changes in this candidate:

1. Add `build_model_child_env()` to remove known authority-bearing prefixes, credential-like variable names, Git credential/config overrides, cloud-provider credentials, and inherited Python import-path overrides. Set `PYTHONPATH` only to this checkout's `runtime` and root paths.
2. Add `build_fcc_child_env()` to admit only the explicit local FCC configuration keys from the dedicated FCC env file; unrelated runner/FCC keys such as publisher credentials are not copied.
3. Use the sanitized environment for Codex, Claude/FCC, the FCC server process, and worker-launched test subprocesses.
4. Add synthetic negative tests for inherited GitHub/GH/ACTIONS/Astra/MediaHub/cloud/API credentials, Git credential helpers, arbitrary `PYTHONPATH`, and FCC env-file fields outside the allowlist.
5. Correct two stale assertions in `tests/test_distributed_local_worker.py`: the 23-wave workflow is read-only, not workspace-write; the permanent executor pool currently binds all three nodes to Claude and permits one claim per node. Tests now assert the checked-in contract rather than the previous Codex/mixed-executor assumption.

No real secret values were read or written. The only inspection of the local FCC env file was a listing of variable names; no values were printed. No worker was dispatched and no repository publication credential was used by this pass.

## Verification evidence

On the exact `main` base worktree, after the change:

- `PYTHONPATH=runtime uv run --with pytest --with PyYAML pytest -q tests/test_distributed_local_worker.py tests/test_worker_security_gate.py tests/test_astra_command_auth.py tests/test_astra_github_agent_contract.py tests/control/test_sign_command.py` — **46 passed**.
- `python3 -m py_compile ops/qualification/run_distributed_local_worker.py tests/test_distributed_local_worker.py` — passed.
- `git diff --check` — passed.
- `uv` used an ephemeral test environment; no project dependency manifest or lockfile was changed.

These tests verify the new pure environment-building helpers and adjacent command/security contracts. They do not prove host-level process isolation, network isolation, safe publication, or end-to-end issuer/capability enforcement.

## Remaining blockers and disposition

- The worker still has a direct Git branch commit/push path. This wave does not implement the separately trusted artifact publisher described by Waves 177/179/207/210.
- The distributed workflow's end-to-end signed-command/issuer/capability verification remains unproven at its admission boundary.
- The environment scrub is a defense-in-depth boundary, not an OS sandbox: a process with filesystem/network access may still access resources outside its environment. Runner/workspace/network isolation gates remain open.
- PR #397 remains Draft/unmerged; its credential minimization must be reconciled with the worker's existing push path before merge.
- The requested third host is not available to this pass: Desktop Commander reports `mh-dev-01` offline, and SentinelX reports that host disabled by the user. No attempt was made to re-enable it or dispatch a worker elsewhere.
- No merge, deployment, qualification promotion, or acceptance is claimed. Overall Contour A remains **NOT_PROVEN / BLOCKED**; G0–G11 remain blocked and G11 remains human-only unless a later evidence-backed status update says otherwise.

## Next bounded step

Review the exact-head CI and independently inspect the final diff. Then add a worker contract test proving no direct publication is possible from the model/test subprocess boundary, and separately implement the already-proposed artifact-only handoff only after the issuer/capability governance gate permits it. Keep publisher credential acquisition out of the model worker.
