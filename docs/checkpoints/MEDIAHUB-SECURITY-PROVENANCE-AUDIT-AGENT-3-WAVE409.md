# MediaHub OS — Contour A Security and Provenance Audit (Agent 3)

- **Agent Identity:** `gemini-agent-3`
- **Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Base Ref:** `main`
- **Audit Date:** 2026-10-23
- **Scope:** Contour A (Developer Fabric) Security, Transport, HMAC, Least Privilege, Secret Separation, and Fail-Closed Behavior.

---

## 1. Executive Summary & Audit Scope
This audit report evaluates the security posture, trust boundaries, cryptographic signing mechanics, least privilege enforcement, and fail-closed failure modes of MediaHub OS Contour A as of target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`. All evaluations are based on static analysis of canonical contracts, GitHub Actions dispatch workflows, and rigorous negative-test suites. No plaintext secrets or sensitive tokens are read, logged, or emitted.

---

## 2. Controller & Child Transport Security
- **Controller Workflow:** `.github/workflows/gemini-batch-dispatch-controller.yml` (Blob SHA: `0a1246f6755020faf8b7e48d07bfff790bbaece3`)
- **Child Workflow (Agent 3):** `.github/workflows/gemini-agent-3.yml` (Blob SHA: `781df56e8aa7c75ba453c08378611857862b2e44`)
- **Transport Security Evaluation:**
  - Dispatches are strictly triggered via `workflow_dispatch` with explicit inputs (`dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`, `dispatch_signature`).
  - Event and repository origin checks (`github.event_name == 'workflow_dispatch'`, repository `VlDMlNSh/mediahub-os`, branch `refs/heads/main`) enforce strict origin validation before any execution or secret access.
  - Non-launching caller-context probes (`gemini-reusable-context-probe-wave284.yml`) independently verify unprivileged caller context without mapping provider secrets.

---

## 3. Cryptographic HMAC & Signature Verification
- **Signing Mechanism:** SHA-256 HMAC utilizing canonical JSON serialization (`json.dumps(payload, sort_keys=True, separators=(",", ":"))`).
- **Signed Fields:** `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`.
- **Verification Logic:** Child workflows execute strict pre-flight authorization scripts (`authorize_dispatch` job) verifying HMAC signature using `hmac.compare_digest` against `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`.
- **Negative Tests & Fail-Closed Behavior (Covered in `tests/test_gemini_child_signed_dispatch_runtime_contract.py`, Blob SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`):**
  - *Task Tampering:* Post-signing task modification is rejected with `"Invalid controller signature"`.
  - *Cross-Child Signature Replay:* Signatures generated for one child workflow file are rejected when presented to another child workflow.
  - *Malformed Shapes:* Invalid UUID4 shapes or non-40-hex target SHAs trigger immediate rejection (`"Malformed target SHA or dispatch ID"`).
  - *Missing Key / Invalid Signature:* Missing HMAC secrets or mismatched signatures fail closed (`"Dispatch HMAC secret missing"` / `"Invalid controller signature"`).

---

## 4. Issuer, Capability, & Least Privilege Enforcement
- **Permission Boundaries:**
  - Controller permissions: `{}` (least privilege).
  - Child workflows: `contents: read` (or `write` / `pull-requests: write` strictly scoped to the engineer job with `persist-credentials: false` in checkout).
  - Read-only review workflows (e.g., Wave 409 independent review) have explicit `contents: read` permissions, restricted tool allowlists (`read_file`, `grep_search`, `glob`, `list_directory`), and lack PR creation capabilities (`create_pull_request` absent).
- **Product State Authority:** AI agents, cloud workflows, and automation adapters operate exclusively within Contour A Developer Fabric. Canonical product-state mutation authority remains strictly separated from agent execution and is never bypassed.

---

## 5. Secret Separation & Egress Boundaries
- **Secret Protection:** SOPS + age primitives govern production configuration. GitHub Actions secrets (`MEDIAHUB_DISPATCH_HMAC_KEY`, `GEMINI_API_KEY_3`, `MEDIAHUB_GITHUB_TOKEN`) are isolated to authorized jobs.
- **Redaction & Scanning:** Runtime security scanners (`runtime.mediahub_runtime.astra_security`, tested in `tests/test_astra_security.py`, Blob SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`) actively detect and redact secret-like patterns (`[REDACTED_SECRET]`), preventing secret leakage in telemetry, logs, or workspace persistence gates (`require_safe`).

---

## 6. Quota, Fallback, & Error Semantics
- **Quota & Error Handling:** Controller dispatch logic validates HTTP status codes and handles ambiguous vs. definite HTTP 4xx rejections.
- **Fail-Closed Semantics:** Ambiguous upstream errors, missing authorization secrets, validation failures, or unmet artifact preconditions fail closed with exit code 1 or 2, preventing unverified state mutations or partial runs.

---

## 7. Evidence Provenance & Acceptance Criteria
- **Exact References:**
  - Target Commit SHA: `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
  - Controller Workflow SHA: `0a1246f6755020faf8b7e48d07bfff790bbaece3`
  - Agent 3 Workflow SHA: `781df56e8aa7c75ba453c08378611857862b2e44`
  - Security Contract SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`
  - Security Test SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`
  - Dispatch Runtime Contract Test SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`
- **Acceptance Status:** All Contour A transport, HMAC verification, least privilege, and fail-closed negative test cases pass. Audit completed as a draft PR with zero live deployments or merges.
