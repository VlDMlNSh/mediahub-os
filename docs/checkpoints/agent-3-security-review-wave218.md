# MediaHub OS — Wave 218 / GitHub Actions Transport Security Review

## Metadata

- **Task ID:** Wave 218 / Agent-3 Independent Controller Security Review
- **Agent identity:** `gemini-agent-3`
- **Contour:** Contour A (Developer Fabric)
- **Reviewed base:** `main`, commit `80be45a70732b1d568164571d4273a6397792c3b` at review time
- **Status:** **PARTIAL REVIEW COMPLETE — RESIDUAL RISKS OPEN / NOT ACCEPTED**
- **Review date:** 2026-10-20

## Scope correction

The initial draft of this PR reviewed the local `astra_github_agent.py`, bootstrap script, systemd unit and orchestrator. Those files are outside the assigned task and do not establish the security of the GitHub Actions transport controller. The source-bound findings below replace that out-of-scope assessment.

## Exact GitHub Actions sources inspected

| File | Ref | Blob SHA | Relevant area |
|---|---|---|---|
| `.github/workflows/gemini-batch-dispatch-controller.yml` | `main` | `99e5a87825aeb239568f96ecef004a102ff3e53b` | confirmation input, token binding, dispatch, run correlation and fail-closed monitor |
| `.github/workflows/gemini-autonomous-engineering.yml` | `main` | `09523d809530ae5b7bf528eab5fa53bc5deaf92d` | A1 provider secret, job permissions, MCP allowlist and output validation |
| `.github/workflows/gemini-agent-2.yml` | `main` | `259c8c82b8d90a39e1c90e65390e469b241b5581` | A2 provider secret, job permissions, MCP allowlist and output validation |
| `.github/workflows/gemini-agent-3.yml` | `main` | `91b5397001e088dfae2f450ee77c9c23118b5601` | A3 provider secret, job permissions, MCP allowlist and output validation |
| `tests/test_gemini_transport_controller_contract.py` | `main` | `00fcbdb4416031ef6f736661823a7c8b6d93f344` | automated controller contract assertions |

## Findings

### 1. Credential route and observed authorization

- The controller binds `GH_TOKEN` to `secrets.MEDIAHUB_GITHUB_TOKEN` in both the dispatch and monitor steps.
- The controller declares `permissions: {}`, so its built-in `GITHUB_TOKEN` has no repository permissions. REST API operations use the repository secret explicitly.
- Runtime evidence: controller run [39396854829](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396854829) completed SUCCESS. Its dispatch step successfully launched A1/A2/A3 and its monitor step correlated all three child runs; this demonstrates that the configured secret had sufficient access for these API operations at that time.
- Secret value and actual token scope were not inspected. Runtime success does **not** prove the token is least-privilege. Verify repository settings keep it restricted to the necessary repository and Actions read/dispatch capabilities; rotate it if its exposure or scope is uncertain.

### 2. Confirmation input

- The controller exposes a required `choice` with string options `"no"` and `"yes"`, default `"no"`, and job condition `inputs.confirm == 'yes'`.
- The initial unquoted values were rejected by GitHub with HTTP 422. PR #412 quoted them; the corrected workflow dispatched successfully.
- Regression test in `tests/test_gemini_transport_controller_contract.py` checks the exact options/default and condition. Post-merge Astra Verify run [39398784963](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39398784963) passed 431 tests.

### 3. Child workflow permissions and secret boundaries

- Each child workflow checks out `inputs.base_ref` with `persist-credentials: false`.
- Each job grants `contents: write`, `pull-requests: write`, and `issues: read` so the bounded agent can create an isolated branch and PR. The configured GitHub MCP tool allowlist contains only file read, branch create, file create/update, and PR create tools.
- Each workflow uses its own provider secret: `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, or `GEMINI_API_KEY_3`. No provider or GitHub secret value was read or emitted during this review.
- The child validator rejects missing/empty/non-JSON output, zero successful tool calls, or a missing successful PR-creation tool call. Artifact inspection for runs 39397165125/39397167382/39397169704 found non-empty response JSON and one successful PR-creation tool call per run.

### 4. Correlation and fail-closed behavior

- The controller snapshots the latest run ID for each child workflow, sends fixed tasks to the three known workflow files, then filters candidates by `workflow_dispatch`, branch `main`, creation time at/after batch start, and run ID above the recorded baseline.
- It fails closed if more than one candidate matches and fails the controller if any child is missing or does not conclude SUCCESS.
- Runtime controller run 39396854829 SUCCESS confirms the monitor correlated A1/A2/A3 to the expected IDs: 39397165125, 39397167382 and 39397169704.
- **Residual risk:** correlation uses time/baseline filtering, not a unique batch nonce echoed in child run metadata. An unrelated run created after a baseline could be the sole visible candidate before the controller's own run appears. Current ambiguity detection mitigates multiple candidates but cannot prove a unique token match. A future hardening change should pass a unique batch ID into each child workflow and bind it into `run-name` or a structured run output, then require exact equality before accepting the run.

### 5. Supply-chain pinning

- The child workflows reference `actions/checkout@v4`, `google-github-actions/run-gemini-cli@v0`, and the GitHub MCP container tag `ghcr.io/github/github-mcp-server:v0.27.0`.
- These are version tags, not full commit-SHA action pins or a container digest. This is a provenance-hardening gap, not evidence of compromise. Pin and review exact upstream revisions before treating the supply chain as fully hardened.

## Remaining negative tests

- Invalid or missing `MEDIAHUB_GITHUB_TOKEN` must fail without logging the value.
- Insufficient token permissions must fail closed and avoid partial/untracked batches.
- Two concurrent manual child runs during controller correlation must produce an ambiguity failure, not accidental acceptance.
- Delayed child run visibility must not permit correlation to an unrelated run; a unique batch nonce is the recommended fix.
- Child provider quota exhaustion, malformed output, missing artifact and missing PR must leave the controller failed with run IDs and safe diagnostics.
- Unpinned action/image drift remains a supply-chain control gap.

## Disposition

This is a bounded static/runtime evidence review, not independent qualification. Controller dispatch and correlation passed for the observed batch; the current run-correlation scheme still has a residual uniqueness risk, and secret scope/supply-chain pinning remain unverified. The three generated agent PRs remain proposals. No deployment or Contour A acceptance is claimed.
