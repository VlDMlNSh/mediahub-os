# MediaHub OS — Agent 3 Independent Security & Provenance Audit

- **Audit Agent:** `gemini-agent-3`
- **Authorized Contour:** `contour-a` (Developer Fabric)
- **Immutable Target SHA:** `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`
- **Audit Date:** 2026-11-16
- **Status:** Draft Independent Audit Report (No Merge / No Deployment / No Qualification / No Nested Dispatch)

---

## 1. Executive Summary

This independent security and provenance audit evaluates the cryptographic transport security, authorization boundaries, secret separation, least privilege enforcement, HMAC validation, fail-closed mechanics, and evidence provenance across MediaHub OS Contour A components at immutable target SHA `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`.

All findings confirm that the system adheres strictly to defense-in-depth principles, requiring signed controller-to-child dispatches, strict UUIDv4 / Git SHA format checks, explicit permission boundaries, and fail-closed error handling without insecure fallbacks or secret leakage.

---

## 2. Scope & Verified Source References

| Domain / Component | Source Path | Blob SHA / Ref Reference | Key Security Property |
|---|---|---|---|
| **Security Contract** | `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `6761edb5e1e9e035388aabcd1b95d240098c2ec4` | Default deny, least privilege, fail-closed policy, audit evidence separation from State Authority |
| **Child Transport & HMAC Authorizer Tests** | `tests/test_gemini_child_signed_dispatch_runtime_contract.py` | `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe` | Validates HMAC-SHA256 signature verification, strict UUIDv4 & Git SHA shapes, event/repo/ref checks, fail-closed handling |
| **Command Auth & ID Safety** | `tests/test_astra_command_auth.py` | `8df49fc55e660c13ad54aca9b9dc78132c335dd1` | HMAC max age rejection, path traversal prevention (`_safe_id`), idempotent execution markers |
| **Secret Scanning & Redaction** | `runtime/mediahub_runtime/astra_security.py` | (Loaded via test suite) | Secret-like pattern detection, redaction (`[REDACTED_SECRET]`), persistence gate enforcement |
| **Evidence Contracts & Verifiers** | `tests/test_astra_gold_evidence_contracts.py` | `2387273506a72ef92483a36d5cf0cd79497b7bba` | G4 115-round contract verification, transport identity mismatch blocking |

---

## 3. Detailed Audit Findings

### A. Controller / Child Transport & HMAC Security
- **Mechanism:** Controller generates a signed payload (`workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`) signed with HMAC-SHA256 (`HMAC_KEY`).
- **Validation:** Children run an inline authorization snippet validating:
  1. Presence and non-emptiness of secret key (`HMAC_KEY`).
  2. Cryptographic signature match using `hmac.compare_digest`.
  3. Exact match of signed workflow file name against environment `WORKFLOW_FILE`.
  4. Strict UUIDv4 pattern regex matching for `DISPATCH_ID` (`^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`).
  5. Strict 40-character Git SHA shape for `TARGET_SHA`.
  6. Event name (`workflow_dispatch`), repository (`VlDMlNSh/mediahub-os`), and ref name (`refs/heads/main`) constraints.
- **Fail-Closed Behavior:** Any tampering (task modification, workflow identity swap, invalid UUID version, malformed target SHA, missing secret, or mismatched signature) results in immediate non-zero exit code failure and rejection, preventing unauthorized execution.

### B. Issuer / Capability & Least Privilege
- **Permissions:** Review and engineering workflows declare explicit minimum permissions (e.g., `contents: read` for review jobs).
- **Credential Hygiene:** `persist-credentials: false` is enforced across untrusted execution steps.
- **Scope Restriction:** Scope is strictly bound to `contour-a` (Developer Fabric) and `main` base ref. Contour B product mutations and unauthorized branches/scopes are rejected at authorization.

### C. Secret Separation & Redaction
- **Storage:** Secrets reside solely in GitHub repository secrets (`MEDIAHUB_DISPATCH_HMAC_KEY`, `GEMINI_API_KEY_3`, etc.).
- **Handling:** Plaintext secrets are never committed to git, embedded in code, or emitted into telemetry logs.
- **Redaction:** `astra_security.py` provides automated pattern scanning and redaction (`scan_secret`, `redact`, `require_safe`) ensuring any accidental secret-like text in logs or outputs is neutralized with `[REDACTED_SECRET]`.

### D. Quota & Fallback Policy
- **No Insecure Fallback:** If authentication, signatures, or security dependencies fail or are unavailable, the system fails closed (denies mutation/execution) rather than falling back to permissive defaults.

### E. Evidence Provenance & Audit Integrity
- **Evidence Bundles:** Dispatches and test runs generate cryptographically hashed and schema-validated evidence records (e.g., G4 evidence contracts).
- **Separation:** Audit and evidence records are strictly non-mutating observability artifacts; they do not possess Product State Authority.

---

## 4. Negative Testing & Verification Status

Negative test coverage in `test_gemini_child_signed_dispatch_runtime_contract.py` and `test_astra_command_auth.py` successfully verifies:
1. **Tampered task payload** -> Rejected ("Invalid controller signature").
2. **Cross-workflow signature reuse** -> Rejected ("Invalid controller signature").
3. **Malformed UUID / UUIDv1/v3/v5/v8 shapes** -> Rejected ("Malformed target SHA or dispatch ID").
4. **Short or invalid target SHA** -> Rejected ("Malformed target SHA or dispatch ID").
5. **Unauthorized base ref (`feature/unsafe`) or scope (`contour-b`)** -> Rejected ("Input outside allowlist").
6. **Incorrect event type (`pull_request`), repository, or ref** -> Rejected ("Child must run from trusted main workflow_dispatch").
7. **Missing HMAC secret** -> Rejected ("Dispatch HMAC secret missing").

---

## 5. Residual Risks & Recommendations

- **Risk:** Exposure of `MEDIAHUB_DISPATCH_HMAC_KEY` secret in GitHub Actions secrets.
  - *Mitigation:* Strict least-privilege secret access policies and automated secret rotation schedules.
- **Risk:** Upstream dependency vulnerabilities in third-party tooling.
  - *Mitigation:* Continuous SBOM, Cosign signature verification, and Trivy vulnerability scans feeding into release gates.

---

## 6. Acceptance Criteria & Conclusion

- [x] Immutable target SHA locked (`1694cde38c7b7d69baf9676b4908c1bb6e197fbe`).
- [x] Controller/child HMAC transport & schema constraints audited.
- [x] Least privilege, secret separation, and redaction verified.
- [x] Fail-closed behavior on negative test vectors confirmed.
- [x] No secrets read, emitted, or compromised.
- [x] Draft audit report created; no merge, deployment, or qualification performed.
