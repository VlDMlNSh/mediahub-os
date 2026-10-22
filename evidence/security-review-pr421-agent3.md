# Independent Security Review: MediaHub OS PR #421

- **Reviewer:** Gemini Agent 3 (Security & Verification Review)
- **Authorized Contour:** Contour A (Developer Fabric)
- **Target PR:** #421
- **PR Head Ref:** `contour-a/workflow-call-controller-governance-wave243`
- **Reviewed Commit SHA:** `185f55b63121b1aece7e60f6c087ecfceab2721e`
- **Date:** October 21, 2026

---

## 1. Executive Summary & Scope

This independent security review evaluates MediaHub OS PR #421 (`contour-a/workflow-call-controller-governance-wave243` at exact commit `185f55b63121b1aece7e60f6c087ecfceab2721e`). The changes establish strict reusable workflow governance, controller caller-context verification, secret isolation, full-SHA immutability pinning for actions and container images, and fail-closed batch dispatch.

### Reviewed Files at PR Head:
1. `.github/workflows/gemini-batch-dispatch-controller.yml`
2. `.github/workflows/gemini-autonomous-engineering.yml`
3. `.github/workflows/gemini-agent-2.yml`
4. `.github/workflows/gemini-agent-3.yml`
5. `.github/workflows/gemini-controller-context-probe-wave284.yml`
6. `.github/workflows/gemini-reusable-context-probe-wave284.yml`
7. `.github/workflows/gemini-workflow-contract-validation-wave284.yml`
8. `tests/test_gemini_controller_context_probe_wave284_contract.py`
9. `tests/test_gemini_controller_positive_context_probe_wave292_contract.py`
10. `tests/test_gemini_reusable_workflow_contract.py`
11. `tests/test_gemini_transport_controller_contract.py`

---

## 2. Detailed Technical Evaluation

### A. Caller Context Semantics & Trusted Guards
- **Mechanism:** Reusable child workflows (`gemini-autonomous-engineering.yml`, `gemini-agent-2.yml`, `gemini-agent-3.yml`) capture `github.event_name` and `github.workflow_ref` in the `caller_context` job.
- **Trusted Ref Pin:** The expected controller ref is explicitly pinned to:
  `VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/heads/main`
- **Guard Validation:** Contract tests (`test_gemini_reusable_workflow_contract.py`) statically assert that loose string matching (`contains`, `startsWith`) is strictly prohibited, and that exact equality matching is enforced.

### B. Spoofing and Bypass Protection
- **Direct Dispatch Prevention:** Child workflows declare `workflow_call` triggers exclusively; they do not expose `workflow_dispatch` directly, preventing external direct manual triggers.
- **Fail-Closed Rejection:** The `reject_untrusted_caller` job evaluates `trusted_controller == 'true'`. If invoked from any other workflow, event, or branch, it exits with an error (`::error::Reusable workflow called from an untrusted workflow context.`).
- **Job Gating:** The `engineer` job conditions explicitly require:
  - `inputs.probe_only != true`
  - `needs.caller_context.outputs.trusted_controller == 'true'`
  - `github.event_name == 'workflow_dispatch'`
  - `github.workflow_ref == 'VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/heads/main'`

### C. Permissions Ceilings & Secret Isolation
- **Controller Permissions:** The controller workflow defines `permissions: {}` (zero default token permissions).
- **Job-Level Least Privilege:** Model execution jobs (`engineer`) have explicit minimum permissions:
  - `contents: write`
  - `pull-requests: write`
  - `issues: read`
- **Secret Hygiene:** `secrets: inherit` is explicitly banned across workflows and verified by contract tests. Provider secrets (`GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`) are explicitly mapped per-job. No transport PAT (`MEDIAHUB_GITHUB_TOKEN`) is used or leaked.

### D. Immutability Pinning (Actions & Containers)
- **GitHub Actions:** All external actions (e.g., `actions/checkout`, `google-github-actions/run-gemini-cli`) are pinned to immutable 40-character commit SHAs.
- **GitHub MCP Server Container:** Pinned to immutable SHA256 digest:
  `ghcr.io/github/github-mcp-server@sha256:cbca61d547beec9b819b26bbfe6ac66ba6b373f1d6b64e8291e346bf524633e2`
- Mutable tags (e.g. `:v0.27.0`) are actively caught and rejected by negative fixtures in `test_gemini_reusable_workflow_contract.py`.

### E. Probe-Only Default Mode & Input Validation
- **Default Safety:** `workflow_dispatch` inputs define `mode` with default `"probe"` and `confirm` with default `"no"` (options: `["no", "yes"]`).
- **Agents Mode Gate:** Agent dispatch jobs (`agent1`, `agent2`, `agent3`) and aggregate `summarize` require `inputs.mode == 'agents'` and `inputs.confirm == 'yes'`.
- **Non-Launching Probe:** The `probe` and `assert_probe_context` jobs validate caller context under both `pull_request` (untrusted) and `workflow_dispatch` (trusted) triggers without provisioning model secrets or write tokens.

### F. Test Coverage & Static Contract Verification
- Four dedicated test suites (`test_gemini_controller_context_probe_wave284_contract.py`, `test_gemini_controller_positive_context_probe_wave292_contract.py`, `test_gemini_reusable_workflow_contract.py`, `test_gemini_transport_controller_contract.py`) contain extensive negative test fixtures ensuring that regression vectors (mutable refs, loose matching, secret inheritance, direct invocation) fail validation.
- **Organization / Repository Settings:** Effective org-level branch protection and rulesets are **NOT VERIFIED** (out of token scope; state: NOT VERIFIED).

---

## 3. Findings Summary Table

| ID | Category | Severity | Description | Preconditions | Remediation / Status |
|---|---|---|---|---|---|
| F-01 | Workflow Governance | Info (Low) | Zero default permissions and strict ref pinning implemented. | None | Remediated in PR #421 (Verified). |
| F-02 | Secret Exposure | Info (Low) | `secrets: inherit` banned; explicit per-job key mapping. | None | Remediated in PR #421 (Verified). |
| F-03 | Supply Chain Pinning | Info (Low) | Actions and MCP server container pinned by exact SHAs. | None | Remediated in PR #421 (Verified). |

---

## 4. Final Verdict

**Verdict:** **APPROVE**

### Rationale:
PR #421 implements robust defense-in-depth across workflow caller verification, fail-closed access control, strict input validation, zero-trust permissions ceilings, and comprehensive static contract testing. No security vulnerabilities or policy bypasses were identified in the reviewed changes at commit `185f55b63121b1aece7e60f6c087ecfceab2721e`.
