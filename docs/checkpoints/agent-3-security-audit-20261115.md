# Agent 3 Security and Provenance Audit Report

- **Agent Identity:** `gemini-agent-3`
- **Credential Reference:** `GEMINI_API_KEY_3`
- **Immutable Target SHA:** `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main`
- **Branch:** `agent-3-security-audit-ffa3ac73-696f-4ddb-a51e-94db7b79dbc1`
- **Date:** 2026-11-15
- **Status:** Independent Audit Complete (Draft / Read-Only Pass)

---

## 1. Executive Summary
This independent security and provenance audit was conducted by Agent 3 under MediaHub OS Contour A constraints against immutable target SHA `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`. The evaluation covers controller/child transport protocols, cryptographic HMAC verification, capability and scope enforcement, secret separation, least privilege boundaries, fail-closed error semantics, and execution provenance.

No secrets were accessed, emitted, or exposed. All negative test vectors and validation harnesses were verified against local test modules (`tests/test_gemini_child_signed_dispatch_runtime_contract.py`, `tests/test_astra_security.py`, `tests/test_astra_command_auth.py`).

---

## 2. Controller & Child Transport Security
- **Architecture:** Controller workflows (`.github/workflows/gemini-batch-dispatch-controller.yml`) sign dispatch payloads using HMAC-SHA256 (`HMAC_KEY`). Child workflows (`.github/workflows/gemini-autonomous-engineering.yml`, `gemini-agent-2.yml`, `gemini-agent-3.yml`, `gemini-fcc-independent-review-wave409.yml`) independently verify the signature before executing any payload steps.
- **Payload Binding:** Signed fields strictly include `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, and `scope`. Serialized via `json.dumps(..., sort_keys=True, separators=(",", ":"))`.
- **Blob SHAs & References:**
  - `runtime/mediahub_runtime/astra_security.py` (Blob SHA: `ff4ba9b581cf30e0f2d6bbed70c5290d93bfa27d`)
  - `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (Blob SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`)
  - `tests/test_astra_command_auth.py` (Blob SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`)
  - `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` (Blob SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`)

---

## 3. Cryptographic HMAC & Integrity Verification
- **Validation Mechanics:** Child pre-flight authorization scripts use constant-time comparison (`hmac.compare_digest`) against computed HMAC-SHA256 digests.
- **Type and Shape Validation:**
  - `target_sha` must conform strictly to 40- or 64-character hex strings (`_valid_target_sha`).
  - `dispatch_id` must conform to UUIDv4 regex format (`r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"`).
- **Negative Tests Verified:**
  - Task tampering post-signing (rejected with "Invalid controller signature").
  - Cross-workflow signature replay (signing for workflow A, running in workflow B — rejected).
  - Malformed UUIDv4 or non-hex target SHA (rejected prior to signature evaluation with "Malformed target SHA or dispatch ID").
  - Unauthorized base ref or scope (rejected with "Input outside allowlist").
  - Wrong event type, repository, or ref name (rejected with "Child must run from trusted main workflow_dispatch").
  - Missing HMAC key or invalid signature (fail-closed).

---

## 4. Issuer, Capability, & Least Privilege
- **Contour Separation:** Contour A (Developer Fabric) remains strictly gated from Contour B (Product Implementation).
- **Permissions & Least Privilege:** Review and execution child workflows maintain granular GitHub token permissions (e.g., `contents: read` for review tasks) and explicitly set `persist-credentials: false`.
- **Tool Allowlist:** Tool use within bounded agent execution is restricted to authorized primitives (e.g. `read_file`, `grep_search`, `glob`, `list_directory`, and permitted PR creation tools where applicable). Unauthenticated or arbitrary command execution outside the sandbox is prohibited.

---

## 5. Secret Separation & Defense in Depth
- **Secret Scanning & Redaction (`astra_security.py`):**
  - Patterns detect API keys, GitHub tokens (`ghp_`, `github_pat_`), Bearer tokens, `sk-` keys, and key-value assignments.
  - `require_safe` and `redact` enforce pre-persistence checks and context-export sanitization.
- **Isolation:** Secrets are sourced exclusively from repository secrets (`secrets.MEDIAHUB_DISPATCH_HMAC_KEY`, `secrets.GEMINI_API_KEY_*`) and never logged, emitted to unrestricted telemetry, or exposed across unauthorized execution boundaries.

---

## 6. Quota, Fallback, & Fail-Closed Behavior
- **Fail-Closed Semantics:** Ambiguous policy results, missing secrets, invalid signatures, or failed execution steps default to immediate failure (`fail closed`).
- **Workflow Error Handling:** Child execution steps do not use unsafe `continue-on-error` bypasses; output validators (`Validate non-empty structured review output`, etc.) execute with `if: always()` and abort if model output is missing, malformed, or lacks verified tool execution success.

---

## 7. Evidence Provenance & Residual Risks
- **Acceptance Criteria Verification:** All security acceptance criteria specified in `SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` and test suites are backed by automated unit tests in `tests/`.
- **Residual Risks:**
  - Reliance on GitHub Actions runner environment isolation for secrets management.
  - Strict dependence on HMAC secret key entropy and rotation policies.
- **Conclusion:** The architecture demonstrates robust defense-in-depth, fail-closed handling, cryptographic binding of controller-to-child dispatches, and rigorous sanitization of sensitive content.
