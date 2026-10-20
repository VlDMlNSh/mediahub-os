# MediaHub OS Contour A — worker trust-boundary source audit (Wave 218)

- Date: 2026-10-20
- Status: **SOURCE AUDIT / NOT QUALIFICATION / NOT ACCEPTANCE**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Working documentation PR: https://github.com/VlDMlNSh/mediahub-os/pull/396
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Functional baseline: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md

## 1. Exact source observations

### PR #388 — schema validation
- Candidate head queried: `4a131acf6484f6e370625b0ebc454ee7b4b5116c`.
- `tools/validate_contracts.py` blob SHA: `45739d931a146f5639f790272bcef58a84075f22`.
- Source imports `Draft202012Validator` and `FormatChecker`; `build_validator` calls `Draft202012Validator.check_schema(schema)`, checks declared format names, and returns a validator with a format checker.
- Exact-head runs observed: Astra Verify run `39323095151` SUCCESS; Astra Cloud Runtime Validation run `39323095228` SUCCESS.
- Independent report PR #395 calls out that a separate YAML launch-gate evaluator is not itself proof of JSON Schema Draft 2020-12 validation, and semantic cross-schema reference resolution remains unproven. This does not contradict the validator source; it limits the scope of what can be claimed.
- PR #389 is a separate documentation review candidate. GitHub review submissions on PR #388 itself: none returned by the review API. Review artifact existence is not the same as a submitted GitHub approval.

### PR #392 — child-process environment and publication boundary
- Candidate head queried: `b76a88aa7da9f8ad211d9377ac3458f7ed561a90`.
- `ops/qualification/run_distributed_local_worker.py` blob SHA: `d1f6591c7732888b2d4d918374b8a892674ff3c5`.
- The file defines `CHILD_ENV_ALLOWLIST` and `child_environment`, and uses the helper for FCC, Codex, Claude, and test subprocess paths.
- The generic `run(argv, timeout, cwd=ROOT, env=None)` still passes `env=None` directly to `subprocess.run`; Python therefore inherits the ambient parent environment for call sites that omit `env`. Source call sites include Ollama discovery, git status/rev-parse/switch, and git publication commands.
- Worker-side publication still executes `git add -A`, `git commit`, and `git push` in the worker process (around lines 673–678 at this source revision). This means the child-env allowlist alone does not establish a separate artifact-only trusted-publisher boundary.
- Exact-head runs observed: Astra Cloud Runtime Validation run `39325464506` SUCCESS; Astra Verify run `39325464533` SUCCESS.
- Independent report PR #393 calls the change CONDITIONAL PASS and explicitly recommends future git credential isolation. GitHub review submissions on PR #392 itself: none returned by the review API.

## 2. Decision

**Do not merge either candidate solely on green CI.** PR #388 has useful formal schema self-validation, but full runtime payload reference resolution and the distinction between JSON schemas and YAML gate configuration must remain explicit. PR #392 narrows environment inheritance only on selected model/test subprocess paths; the generic helper and direct worker git publication are still open trust-boundary gaps.

A seemingly simple change to make every `run()` invocation inherit the allowlist by default is unsafe without a call-site design: Git and SSH publication may rely on ambient credential/configuration variables, and the current architecture still places publication authority inside the worker. Do not silently sanitize the generic helper in a way that breaks authentication or masks the actual authorization problem.

## 3. Smallest safe next implementation slice

Design and test the artifact-only publication boundary before changing the generic command helper:
1. Worker can write only to an isolated task workspace and emit a bounded artifact manifest (task ID, immutable target SHA, allowed paths, hashes, result metadata).
2. Worker has no write-capable repository token or inherited Git/SSH publication credentials.
3. A separate trusted publisher validates issuer/capability, task lease and cancellation state, immutable base SHA, path allowlist, artifact digests, size limits, and evidence manifest before publishing a dedicated branch/PR.
4. Negative tests prove rejection of path traversal, unexpected files, mismatched target SHA, stale lease, duplicate/replayed task ID, missing digest, and worker-supplied publication instructions.
5. Exact-head CI and independent security review must pass; keep candidate Draft and do not deploy.

## 4. Execution and evidence boundary

- This pass was a source-level audit via GitHub file/blob and workflow-run APIs. It did not run tests locally or alter production code.
- Exact-head CI results above are tied to the recorded candidate SHAs only.
- The generated current truth at main blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` reports G0–G11 BLOCKED, overall NOT_PROVEN / BLOCKED, and G11 HUMAN_ONLY.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED.
- No merge, deployment, credential change, branch-protection change, or production action was performed.

## 5. Next concrete action

Open a dedicated, bounded Draft PR for the worker artifact envelope/publisher separation design and negative-test contract, after locating existing stable publication components and the authoritative A0 issuer/capability contract. First inspect current main and candidate workflow permissions at exact SHAs; do not start a code change until publisher authority and permitted write surfaces are explicit.
