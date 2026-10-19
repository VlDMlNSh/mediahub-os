# MediaHub OS Contour A — explicit child-environment allowlist (Wave 227)

Date: 2026-10-20. Status: implementation candidate in existing Draft PR #392; not qualified, deployed, or accepted.

## Navigation and source-of-truth refs

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Existing implementation PR: https://github.com/VlDMlNSh/mediahub-os/pull/392
- Independent prior review PR: https://github.com/VlDMlNSh/mediahub-os/pull/393
- Prior architecture reports: Wave 179 trusted-publisher negative-test matrix; Wave 207 credential chain; Wave 210 artifact/publisher boundary.
- Base `main` SHA: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.

## New source-bound finding

The existing PR #392 uses a strict parent-environment allowlist, but `child_environment(explicit)` previously copied every key supplied by its caller. Both FCC startup and the Claude client passed the entire parsed FCC env file as `explicit`. Therefore the parent environment was constrained, but an unapproved field accidentally added to the FCC env file could still be propagated to the model/FCC child. The existing positive test also demonstrated arbitrary explicit-key propagation rather than an allowlisted FCC configuration contract.

## Changes in this wave

1. Added `FCC_ENV_ALLOWLIST` for the exact runtime fields used by the current FCC configuration: model binding, host/port, Ollama URL, bounded provider/proxy settings, reasoning policy, and the local proxy auth token.
2. Changed `child_environment()` so explicit values are copied only when their keys appear in a caller-provided `explicit_allowlist`; the default permits no explicit additions.
3. Bound the Codex `CODEX_HOME` override explicitly; bound FCC server/client environment updates to `FCC_ENV_ALLOWLIST`.
4. Added a regression test proving that injected `GH_TOKEN`, `ASTRA_PUBLISHER_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY`, arbitrary MediaHub fields and `PYTHONPATH` do not propagate from the FCC env map while required local FCC fields do.
5. Corrected two stale worker tests: the checked-in 23-wave workflow is `read-only`, not `workspace-write`; the permanent executor pool binds the three nodes to Claude and permits at most one claim per node.

No worker was dispatched. No real secret values were read or written. The local FCC file was not read in this wave; tests use synthetic values only.

## Verification

- TDD red phase: new tests failed before implementation because `child_environment()` did not accept an explicit-key allowlist and `FCC_ENV_ALLOWLIST` did not exist.
- Focused pytest command: `PYTHONPATH=runtime uv run --with pytest --with PyYAML pytest -q tests/test_distributed_local_worker.py tests/test_worker_security_gate.py tests/test_astra_command_auth.py tests/test_astra_github_agent_contract.py tests/control/test_sign_command.py` — **46 passed**.
- Full unittest discovery in an ephemeral environment: `PYTHONPATH=runtime uv run --with pytest --with PyYAML python -m unittest discover -s tests -p 'test_*.py' -v` — **428 tests passed**, 0 failures/errors.
- `python3 -m py_compile ops/qualification/run_distributed_local_worker.py tests/test_worker_security_gate.py tests/test_distributed_local_worker.py` — passed.
- `git diff --check` — passed.
- A plain system-Python full discovery initially failed to import eight YAML-dependent test modules because PyYAML was absent; rerunning with the ephemeral `uv` environment passed. No project dependency manifest or lockfile was modified.

## Current limits / disposition

- Exact-head CI for the updated PR commit is pending at report creation; check PR #392 before calling the CI gate green.
- The worker still commits/pushes its own branch. This change does not implement the separate trusted publisher from Waves 177/179/207/210.
- The existing independent review of PR #392 is conditional on the host Git publication credential path; this wave does not close that finding.
- A strict environment allowlist is defense-in-depth, not an OS/filesystem/network sandbox. Runner/workspace/network isolation and issuer/capability verification remain unproven.
- The separate PR #398 created during this pass duplicates the existing PR #392 direction and will be closed in favor of this reviewed branch, preserving the implementation work here.
- No merge, deployment, qualification promotion or acceptance is claimed. Contour A remains **NOT_PROVEN / BLOCKED**; G0–G11 remain blocked and G11 remains human-only unless later evidence explicitly changes those states.

## Next bounded step

Read back the exact PR #392 head and its CI/job steps; obtain independent review of the new FCC explicit-key allowlist and confirm the current conditional Git-publication finding remains clearly open. Do not merge or dispatch a worker until the publication/authority gates are resolved.
