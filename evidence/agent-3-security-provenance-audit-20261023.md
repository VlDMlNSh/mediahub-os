# MediaHub OS — Independent Security & Provenance Audit (Agent 3)

- **Audit ID:** `AGENT-3-SECURITY-PROVENANCE-AUDIT-20261023`
- **Agent Identity:** `gemini-agent-3`
- **Authorized Contour:** `Contour A` (Developer Fabric)
- **Immutable Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Status:** DRAFT AUDIT RECORD (No merge, deployment, qualification, or nested dispatch)

---

## 1. Executive Summary

This independent security and provenance audit conducted by Gemini Agent 3 reviews the cryptographic transport verification, secret separation, least privilege access controls, quota/fallback mechanisms, and fail-closed behaviors across MediaHub OS Contour A components. 

All evaluations reference the immutable target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60` and verify that cryptographic signing, identity isolation, and strict input validation gates adhere to the canonical security contracts (`architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` and `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`).

---

## 2. Evidence Provenance & Canonical Blobs

| Component / Contract | Path | Blob SHA |
|---|---|---|
| Gemini Agent Rules | `GEMINI.md` | `4c431143aa5c46776e80893bf3c0e5f202e3b76d` |
| Security Trust Authorization Contract | `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` |
| Astra Gold Governance Contract | `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` |
| Astra Security Tests | `tests/test_astra_security.py` | `6761edb5e1e9e035388aabcd1b95d240098c2ec4` |
| Astra Command Auth Tests | `tests/test_astra_command_auth.py` | `8df49fc55e660c13ad54aca9b9dc78132c335dd1` |
| Gemini Child Signed Dispatch Runtime Contract Tests | `tests/test_gemini_child_signed_dispatch_runtime_contract.py` | `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe` |

---

## 3. Detailed Audit Findings

### 3.1 Controller / Child Transport & HMAC Integrity
- **Mechanism:** Controller-to-child dispatches are cryptographically secured using HMAC-SHA256 signatures computed over canonically serialized JSON payloads (`sort_keys=True, separators=(",", ":")`).
- **Timing Attacks Defense:** Verification enforces constant-time comparison via `hmac.compare_digest`.
- **Field Binding:** Signed fields include `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, and `scope`.
- **Validation Gates:** Strict regex validation ensures `dispatch_id` matches RFC-4122 v4 UUID format and `target_sha` conforms to valid 40/64 character Git SHA shapes.

### 3.2 Issuer & Capability Isolation
- **Separation of Concerns:** Review and audit agents operate under read-only permissions (`contents: read`), lacking pull request creation or write capabilities where restricted.
- **Workflow Permissions:** Explicit job-level permissions prevent privilege escalation.
- **State Authority Boundary:** Product State Authority alone owns canonical MediaHub product-state mutation. AI agents and cloud workflows do not acquire state mutation authority.

### 3.3 Secret Separation & Credential Hygiene
- **SOPS + Age Primitives:** Managed secrets adhere to SOPS and age encryption standards.
- **Suppression:** Secret values, API keys, and authorization tokens are strictly suppressed or redacted in logs and evidence (`scan_secret`, `redact`, `require_safe` in `tests/test_astra_security.py`).
- **No Credentials in Git:** Enforced via repository hygiene gates (`INV_NO_CREDENTIALS_IN_GIT`).
- **Runtime Injection:** Secrets are securely passed via GitHub Actions secrets (`secrets.MEDIAHUB_DISPATCH_HMAC_KEY`, `secrets.GEMINI_API_KEY_3`, etc.) without plain-text leakage.

### 3.4 Least Privilege & Tool Boundaries
- Tool access is bounded per agent role. Independent review and audit agents operate with minimal necessary tools (e.g. `read_file`, `grep_search`, `glob`, `list_directory`).
- No unauthorized tool invocation or cross-agent privilege bleeding exists.

### 3.5 Quota, Fallback & Fail-Closed Behavior
- **Fail-Closed Semantics:** 
  - Missing HMAC secret results in immediate rejection ("Dispatch HMAC secret missing").
  - Invalid signatures or tampered task payloads are rejected ("Invalid controller signature").
  - Malformed dispatch IDs or target SHAs fail closed before signature verification.
  - Non-allowlisted base refs or scopes (e.g. `contour-b`) trigger immediate rejection ("Input outside allowlist").
  - Missing or incomplete evidence blocks downstream transitions (`INV_MISSING_EVIDENCE_BLOCKS`).

---

## 4. Negative Test Coverage

Negative test validation is explicitly codified in `tests/test_gemini_child_signed_dispatch_runtime_contract.py` and `tests/test_astra_command_auth.py`, ensuring robust coverage of invalid states:
1. **Task Tampering:** Modifying task descriptions post-signing is detected and rejected.
2. **Cross-Workflow Signature Replay:** Reusing a signature generated for one workflow file on another child workflow is rejected.
3. **Malformed UUID / SHA Shapes:** Invalid UUIDv4 formats or non-SHA shapes fail validation.
4. **Out-of-Scope / Unauthorized Base Ref:** Attempts to target non-allowlisted base branches or scopes fail validation.
5. **Event / Repository Mismatch:** Dispatches originating from non-`workflow_dispatch` events (e.g. `pull_request`) or unauthorized repositories are rejected.
6. **Missing Key / Invalid Signature:** Zeroed-out or empty HMAC keys/signatures fail closed.

---

## 5. Residual Risks & Recommendations

1. **Operator Key Rotation:** Ensure periodic rotation of `MEDIAHUB_DISPATCH_HMAC_KEY` across GitHub repository secrets.
2. **Provider Rate Limits:** Monitor external model API quotas to ensure resilience during high-frequency validation passes.
3. **Strict Environment Boundary:** Maintain strict isolation between Contour A (developer fabric) and Contour B (product release gate).

---

## 6. Verification Status

- **Audit Status:** COMPLETED (Draft Audit)
- **Target SHA Verified:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Author:** Gemini Agent 3 (Security & Verification Review)
- **Action:** Pull Request opened against `main`. No merge or deployment executed.
