# MediaHub OS — Wave 431: reuse reviewed path-containment patterns in the local executor

- Date: 2026-10-23
- Status: **IMPLEMENTED ON WORKING BRANCH / EXACT-HEAD CI PENDING / NOT ACCEPTED**
- Base/main SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Working branch: `contour-a/worker-path-containment-wave431-20261023`
- Related architecture research: [Issue #568 — Ruflo architecture evaluation](https://github.com/VlDMlNSh/mediahub-os/issues/568)
- Parent Contour A: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## Scope clarification

The owner confirmed the objective is **not to install Ruflo or introduce a second orchestrator**. Mature projects are inspected as upstream sources for proven, license-compatible patterns, and relevant ideas/code are adapted directly into MediaHub with tests and evidence. This pass adds no third-party runtime dependency and performs no Ruflo installation, provider call, model inference, or local executor task.

## Upstream pattern review

- Ruflo upstream main was observed at commit `88349655ebc2de8f9bf702aaf31d6be768e1ea11`.
- Root package blob `00adf9205546dd88762d96ea2a264b45a567a11c` reports `claude-flow@3.59.17`; license blob `5c4718198a4156beacc780980077043a98b0dd6a` is MIT.
- Current [hooks-tools.ts](https://github.com/ruvnet/ruflo/blob/88349655ebc2de8f9bf702aaf31d6be768e1ea11/v3/@claude-flow/cli/src/mcp-tools/hooks-tools.ts) blob `7c7e219a5eba4d699ee6d89cc931d3a8097bfc65` still uses lexical-only `abs.startsWith(cwd + sep)` in `resolveTargets` (observed source line 5442); it did not contain the described `realCanonical()` hardening in this snapshot.
- Decision: **do not copy the current Ruflo containment implementation**. Reuse only the general reviewed design of canonical path resolution and explicit workspace containment, implemented with Python's standard-library `pathlib.Path.resolve()`/relative-path checks and stricter symlink-component rejection. License review found no need to copy source code or add a dependency.

## MediaHub code change

- `ops/qualification/run_distributed_local_worker.py` — new helper `_resolve_workspace_path` denies absolute declared boundaries, traversal components, symlink components and resolved paths outside the repository root. The bounded Claude `Write`/`Edit` materializer now requires a repository-relative declared boundary, a contained canonical target, and exact target-to-boundary equality before writing.
- Source blob SHA: `3479450a585496e557f0b2dc6272eb9111950840`.
- `tests/test_distributed_local_worker.py` — five regressions:
  1. legitimate exact-boundary write remains available;
  2. absolute declared boundary is rejected;
  3. traversal boundary is rejected;
  4. symlinked parent escaping the workspace is rejected;
  5. symlinked boundary target escaping the workspace is rejected.
- Test blob SHA: `9996d42cec8ae586029b575b11c0b22d379ca54b`.
- No new runtime dependency. The tests use the existing Python test surface and temporary filesystem fixtures.

## Security limits and verification state

This is a narrow path-confinement improvement, not a claim of race-free filesystem isolation. Path validation is still followed by a separate path-based write; a concurrent same-user process able to swap filesystem entries between check and write presents a residual TOCTOU concern. A descriptor-based/open-once implementation would need a separate portable design and adversarial race tests before claiming race-free containment.

- Source and test files were read back from the working branch; blob SHAs above match the returned source.
- Local execution of the repository test file: **NOT RUN** in this pass.
- Exact-head GitHub CI: **PENDING**.
- Independent security review: **PENDING**.
- Merge/deployment/runtime qualification: **NOT RUN**.

## Next step

Open a draft PR and verify exact-head CI, including the five new tests. Obtain an independent security review of path resolution and residual TOCTOU behavior. Do not merge if any relevant check or review is unavailable; missing evidence is NOT VERIFIED, not PASS.
