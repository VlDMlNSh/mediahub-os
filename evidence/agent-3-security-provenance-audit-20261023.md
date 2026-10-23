# MediaHub OS — Contour A Agent 3 Security and Provenance Audit

## Audit Metadata
- **Agent Identity:** `gemini-agent-3`
- **Credential Reference:** `GEMINI_API_KEY_3`
- **Immutable Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main`
- **Audit Date:** October 23, 2026
- **Status:** Draft Independent Audit Report (No Merge, No Deployment)

---

## 1. Executive Summary
This independent security and provenance audit evaluates MediaHub OS Contour A against the immutable target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`. The assessment verifies that controller-to-child dispatch mechanisms, cryptographic authentication (HMAC-SHA256), capability scoping, secret separation, least privilege access controls, and fail-closed error handling operate strictly in accordance with the Security, Trust, and Authorization Contract (`architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`) and Baseline 2.0 specifications.

---

## 2. Controller / Child Transport & HMAC Integrity
- **Mechanism:** Controller-to-child workflow dispatches enforce cryptographic signing using HMAC-SHA256 (`tests/test_gemini_child_signed_dispatch_runtime_contract.py`).
- **Canonical Payload Serialization:** Payloads are serialized deterministically via `json.dumps(payload, sort_keys=True, separators=(",", ":"))` before hashing.
- **Verification Logic:** Child workflows execute an inline verification step (`authorize_dispatch`) using `hmac.compare_digest` to prevent timing attacks.
- **Signed Fields:** `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`.
- **Negative Test Coverage:**
  - Tampering with `TASK` after signing fails validation ("Invalid controller signature").
  - Reusing a signature across different child workflow files fails validation.
  - Non-allowlisted `base_ref` or `scope` values (e.g., `feature/unsafe`, `contour-b`) are strictly rejected even with a valid signature ("Input outside allowlist").
  - Mismatched event name, repository, or ref name is rejected ("Child must run from trusted main workflow_dispatch").
  - Missing secret key or invalid signature results in immediate fail-closed termination.

---

## 3. Issuer / Capability & Shape Enforcement
- **Dispatch ID Shape:** Enforces strict UUIDv4 regex validation (`r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"`). Malformed UUIDs are rejected ("Malformed target SHA or dispatch ID").
- **Target SHA Shape:** Requires exactly 40 hex characters (`_valid_target_sha`). Arbitrary strings or path traversal attempts (e.g., `../main`) fail instantly.
- **Command Authority (`astra_github_agent.py`):** Requires schema version, command ID, node ID, operation, target SHA, workflow only, owned paths, title, description, exclusive actions, and issued timestamp. Idempotent marker tracking ensures commands cannot be replayed (`_command_already_executed`).

---

## 4. Secret Separation & Least Privilege
- **Secret Isolation:** HMAC keys (`HMAC_KEY`, `MEDIAHUB_DISPATCH_HMAC_KEY`) are stored exclusively as GitHub repository secrets and passed via environment variables. Secret values are strictly suppressed in provider models (`evidence/provider-model.json`, `evidence/execution-backends.json`). No plaintext secrets or API keys are committed or logged.
- **Least Privilege Access Control:** Read-only review workflows (`gemini-fcc-independent-review-wave409.yml`) drop write permissions (`permissions: contents: read`), exclude pull-request write capabilities, restrict allowed tool sets to bounded inspection primitives (`read_file`, `grep_search`, `glob`, `list_directory`), and disable persistence (`persist-credentials: false`).

---

## 5. Quota / Fallback Policy & Fail-Closed Behavior
- **Provider Reliability:** Provider catalog integration (`evidence/provider-model.json`) models explicit failure classes (`BLOCKED_BILLING`, `BLOCKED_RATE_LIMIT`, `FAIL`, `BLOCKED_AUTH`, `credential_missing`).
- **Fail-Closed Principle:** Any ambiguity, validation failure, missing secret, or unauthorized input results in a fail-closed exit code (`exit 1`), preventing silent degradation or unauthorized state mutation. Product State Authority remains solely owned by canonical MediaHub state mechanisms; AI agents and cloud workflows hold zero state-mutation authority.

---

## 6. Evidence Provenance & Artifacts
- **Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Repository:** `VlDMlNSh/mediahub-os`
- **Key Files Audited:**
  - `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` (SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`)
  - `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`)
  - `tests/test_astra_command_auth.py` (SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`)
  - `evidence/provider-model.json` (SHA: `3112dc235c5f2e8aefcc2d9ee68ae331a6079944`)
  - `evidence/execution-backends.json` (SHA: `30d2c64acd169caf10dd96137c4ca24beb13c623`)

---

## 7. Residual Risks & Recommendations
1. **Token Permissions:** GitHub Actions restricted permissions (`403` on PR creation when run under automated service tokens) require manual PR creation or elevated workflow token privileges if autonomous PR creation is desired.
2. **Provider Quotas:** Commercial AI providers exhibit rate-limit or billing blocks (`BLOCKED_RATE_LIMIT`, `BLOCKED_BILLING`), requiring robust fallback and local inference handling.
3. **Status:** Audit completed successfully in draft mode. No merge, deployment, qualification, or state mutation performed.
