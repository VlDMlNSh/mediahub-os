# MediaHub A0 credential-boundary source revalidation — Wave 175

- Date: 2026-10-19
- Status: SOURCE REVIEW ONLY; no remediation implemented or qualified.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Prior matrix: [Wave 173 credential-boundary remediation and negative-test matrix](MEDIAHUB-A0-CREDENTIAL-BOUNDARY-REMEDIATION-AND-NEGATIVE-TEST-MATRIX-WAVE-173-2026-10-19.md)

## Exact source evidence re-read on main

| Source | Blob SHA | Verified observation |
|---|---|---|
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | In `exec_claude`, `env = os.environ.copy()`, then FCC env-file values are merged; the same FCC auth token is set as both `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` for the Claude subprocess. The non-structured branch permits `Bash(git *)` and `Bash(python *)`. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Workflow grants `contents: write`; each inspected checkout sets `persist-credentials: true`; worker executes from that checkout. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | `github_auth_env()` copies the process environment and may add the result of `gh auth token` as `GH_TOKEN` before dispatch. This dispatcher environment must not be reused for model execution. |

These are source-level exposure paths, not proof that a credential was read, used outside its intended endpoint, or exfiltrated. This pass did not access credential values, run the worker, invoke a provider, dispatch a workflow, or execute tests.

## Implementation boundary

The Wave 173 design already defines a negative-test matrix. The next implementation candidate should be a separate branch based on a verified current source SHA, with no edits to canonical `main` and no worker dispatch. First implement static policy checks and unit tests with synthetic sentinel values; then isolate runtime credential handling only after the FCC client/authentication contract is established. Do not simply remove the FCC token without verifying how the local transport authenticates, and do not claim OS/network isolation from prompt restrictions.

Minimum tests before any controlled execution:
- model child environment excludes synthetic `GH_TOKEN`, `GITHUB_TOKEN`, unrelated provider/cloud/SSH credentials and dispatcher-only variables;
- FCC authentication material is not copied into model-controlled environment unless an approved broker contract explicitly requires it;
- workflow policy rejects `contents: write` and `persist-credentials: true` for the model worker;
- synthetic secret sentinels are absent from prompts, logs, artifacts and result metadata;
- negative tests assert rejection, without printing sentinel values.

## Governance and next step

WB-05 issuer/verifier decisions, GOV-CAP-01…07, R-06 authority/privacy, accepted runner/workspace/network manifest, lease/cancel/recovery, independent review, and setuptools bootstrap publisher provenance remain open. No issuer/token lifecycle is selected by this report.

Next: create a separate minimal remediation candidate with static workflow-policy tests and synthetic-secret environment tests, inspect the diff, and run only isolated tests. Keep real secrets and workflow dispatch out of scope. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**; Contour B remains gated.
