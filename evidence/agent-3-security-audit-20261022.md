# MediaHub OS — Agent 3 Security & Provenance Audit

- **Agent ID:** `gemini-agent-3`
- **Authorized Contour:** `contour-a`
- **Immutable Target SHA:** `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- **Base Ref:** `main`
- **Audit Date:** 2026-10-22
- **Status:** DRAFT AUDIT / CHECKPOINT PASS

---

## 1. Verified Artifacts & Blob SHAs
- `GEMINI.md`: SHA `4c431143aa5c46776e80893bf3c0e5f202e3b76d`
- `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`: SHA `8d831c2a8fa333977dd86524099568bae2a8db0e`
- `tests/test_astra_security.py`: SHA `6761edb5e1e9e035388aabcd1b95d240098c2ec4`
- `tests/test_gemini_child_signed_dispatch_runtime_contract.py`: SHA `efb573f36861508e440e2e4f5da4d5a76b54005b`

---

## 2. Audit Findings

### A. Controller / Child Transport & HMAC
- **Mechanism:** HMAC-SHA256 signature verification over serialized payload dictionaries (`workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`).
- **Canonicalization:** Strict sorted keys and minimal separators (`json.dumps(payload, sort_keys=True, separators=(",",":"))`) ensure deterministic signature generation between controller and child workflows.
- **Constant-Time Comparison:** Uses `hmac.compare_digest` to prevent timing attacks.
- **Validation:** `tests/test_gemini_child_signed_dispatch_runtime_contract.py` exhaustively tests valid canonical signatures, tampered task bodies, cross-child signature reuse, and missing secrets.

### B. Issuer / Capability & Least Privilege
- **Default Deny:** All workflow dispatches and command executions enforce default-deny.
- **Allowlist Enforcement:** Base references (`main`) and scopes (`contour-a`) are strictly validated against allowlists; attempts to use unauthorized scopes (e.g. `contour-b`) or branches are rejected even when signed.
- **Identity & Shape Validation:** Strict regex matching enforces UUIDv4 structure for dispatch IDs and 40-character hexadecimal strings for target SHAs.

### C. Secret Separation & Protection
- **Storage:** Secrets such as `HMAC_KEY` and API credentials reside exclusively in repository secrets / environment configurations and are never logged or committed.
- **Redaction Primitives:** `runtime.mediahub_runtime.astra_security` provides robust scanning (`scan_secret`, `redact`, `require_safe`) to intercept and reject secret-like values in persistence gates.
- **Zero Secret Leakage:** No secret values are read or emitted in test suites or audit reports.

### D. Quota / Fallback & Fail-Closed Behavior
- **Fail-Closed Semantics:** Missing keys, invalid signatures, malformed payload shapes, or unexpected event triggers (e.g. `pull_request` instead of `workflow_dispatch`) immediately cause the authorizer to abort with non-zero exit codes.
- **State Authority Boundary:** AI agents and child dispatch runners operate entirely within Contour A developer fabric and possess zero authority to mutate canonical MediaHub product state without passing through validated Product State Authority paths.

---

## 3. Negative Test Coverage
- Task tampering after signing -> Rejected (`Invalid controller signature`)
- Cross-workflow signature reuse -> Rejected (`Invalid controller signature`)
- Malformed UUIDv4 dispatch IDs -> Rejected (`Malformed target SHA or dispatch ID`)
- Malformed target SHAs -> Rejected (`Malformed target SHA or dispatch ID`)
- Unauthorized scope (`contour-b`) -> Rejected (`Input outside allowlist`)
- Unauthorized event (`pull_request`) -> Rejected (`Child must run from trusted main workflow_dispatch`)
- Missing HMAC secret -> Rejected (`Dispatch HMAC secret missing`)

---

## 4. Residual Risks & Known Gaps
- **Runtime Enclosure:** Active distributed node attestation relies on operational telemetry state; offline CI evaluation provides static policy enforcement and contract validation.
- **External Dependencies:** Sovereign adapters rely on strict sandbox boundaries; unverified external inputs are treated as untrusted data.

---
*Certified by Gemini Agent 3 (Security & Verification Review).*
