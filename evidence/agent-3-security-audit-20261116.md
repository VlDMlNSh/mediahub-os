# MediaHub OS — Agent 3 Independent Security and Provenance Audit

- **Agent Identity:** `gemini-agent-3`
- **Credential Reference:** `GEMINI_API_KEY_3`
- **Authorized Contour:** `contour-a` (Developer Fabric)
- **Base Ref:** `main`
- **Immutable Target SHA:** `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`
- **Audit Date:** 2026-11-16
- **Status:** DRAFT INDEPENDENT SECURITY REVIEW (No merge, deployment, or qualification)

---

## 1. Executive Summary & Scope

This independent security and provenance audit was conducted by Gemini Agent 3 under MediaHub OS Contour A governance rules. The scope covers:
1. Controller-to-child transport and signed dispatch verification (`.github/workflows/gemini-batch-dispatch-controller.yml` and child workflow authorizers).
2. Issuer/capability and least privilege enforcement (read-only review workflows vs. engineering dispatch workflows).
3. Secret separation, detection, and redaction primitives (`runtime/mediahub_runtime/astra_security.py` and `tests/test_astra_security.py`).
4. Cryptographic integrity via HMAC-SHA256, payload sorting (`sort_keys=True`, compact separators), and strict shape validation (UUIDv4 format, valid git SHAs).
5. Fail-closed behavior on missing keys, mismatched signatures, tampering, malformed inputs, and unauthorized base/scope overrides.
6. Evidence provenance and audit verification without secret leakage.

---

## 2. Controller / Child Transport & HMAC Integrity

### Architecture & Verification
- **Signing mechanism:** The batch dispatch controller computes an HMAC-SHA256 signature over a canonical JSON payload (`workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`) serialized with `sort_keys=True` and separators `(',', ':')`.
- **Child verification:** Child workflows execute an inline bash authorizer that re-serializes the received environment variables into the identical payload structure and compares signatures using `hmac.compare_digest` to prevent timing attacks.
- **Fail-Closed Guarantees:**
  - Missing `HMAC_KEY` results in immediate rejection (`Dispatch HMAC secret missing`).
  - Tampering with any signed field (e.g. `TASK`, `TARGET_SHA`, `BASE_REF`) invalidates the signature (`Invalid controller signature`).
  - Cross-workflow signature replay (using a signature generated for workflow A on workflow B) is rejected.

---

## 3. Input Validation & Strict Shape Checks

### Bounded Invariants
- **Dispatch ID:** Must strictly conform to RFC 4122 UUID version 4 regex (`^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`). Malformed UUIDs or non-v4 UUIDs are rejected before signature execution.
- **Target SHA:** Must be a valid 40-character or 64-character hex string representing a git commit SHA. Relative paths (e.g. `../main`) or short non-hex identifiers are rejected.
- **Base Ref & Scope:** Explicitly checked against allowlists (`main` for base ref; `contour-a` for scope). Any attempt to pass `contour-b` or arbitrary branch references is rejected with `Input outside allowlist`.
- **Event Context:** Requires explicit `workflow_dispatch` trigger from the repository owner on `refs/heads/main`. Pull request events or external repositories are rejected.

---

## 4. Secret Separation & Redaction Defense

### Implementation Review (`runtime/mediahub_runtime/astra_security.py`)
- **Pattern Coverage:** Robust regex patterns detect OpenAI API keys (`sk-...`), GitHub tokens (`ghp_...`, `github_pat_...`), generic authorization headers/bearer tokens, and assignment patterns (`api_key=...`, `secret=...`, `x-api-key:...`).
- **Defense in Depth:**
  - `require_safe()` acts as a persistence gate, raising `ValueError` if secret-like patterns are detected in state inputs.
  - `redact()` masks detected secrets with `[REDACTED_SECRET]` without outputting plaintext values.
- **Zero Secret Leakage:** All unit tests (`tests/test_astra_security.py`, `tests/test_astra_command_auth.py`, `tests/test_gemini_child_signed_dispatch_runtime_contract.py`) operate entirely on synthetic test keys (e.g., `unit-test-key`, `unit-test-only-not-a-secret`) and mock payloads. No repository secrets or live provider tokens were accessed or emitted.

---

## 5. Least Privilege & Role Separation

- **Review Workflows:** Workflows such as `gemini-fcc-independent-review-wave409.yml` operate under strict read-only permissions (`contents: read`), restricting tool access to read operations (`read_file`, `grep_search`, `glob`, `list_directory`). They lack pull request creation capabilities (`create_pull_request`), preventing privilege escalation during independent audits.
- **Product State Authority:** AI agents, cloud workflows, and dispatch queues do not hold canonical product-state mutation authority; state changes remain gated behind verified contracts and human approval checkpoints.

---

## 6. Negative Tests & Failure Handling

Empirical test evidence from `tests/test_gemini_child_signed_dispatch_runtime_contract.py` confirms the following fail-closed behaviors:
1. **Task Tampering:** Detected and rejected (`Invalid controller signature`).
2. **Signature Replay Across Children:** Rejected.
3. **Malformed UUID / SHA:** Rejected (`Malformed target SHA or dispatch ID`).
4. **Scope/Base Escape:** Rejected (`Input outside allowlist`).
5. **Event Context Mismatch:** Rejected (`Child must run from trusted main workflow_dispatch`).
6. **Missing HMAC Secret:** Rejected (`Dispatch HMAC secret missing`).
7. **Gemini Execution Failure:** Child validators (`Validate non-empty structured review output`) verify that non-success outcomes (`failure`, `cancelled`, `skipped`) fail the job step and upload artifacts.

---

## 7. Residual Risks & Recommendations

1. **Secret Rotation Cadence:** Ensure HMAC dispatch keys stored in GitHub Actions secrets are rotated according to compliance policy.
2. **Dependency Monitoring:** Keep Python and GitHub Actions action versions pinned to immutable SHAs where feasible.
3. **Contour Separation:** Strict separation between Contour A (Developer Fabric) and Contour B (Product Implementation) must be maintained in future workflow dispatches.
