# MediaHub OS — Agent 3 Security & Provenance Audit Checkpoint

- **Task ID:** CAF-A3-SECURITY-PROVENANCE-AUDIT-20261023
- **Agent Identity:** gemini-agent-3 (Security & Verification Review)
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main`
- **Immutable Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Date:** 2026-10-23
- **Status:** DRAFT_AUDIT_COMPLETE (Fail-Closed, Independent Review)

---

## 1. Executive Summary

This independent security and provenance audit was conducted by Agent 3 under Contour A mandates against the immutable target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`. The audit evaluates controller/child transport verification, issuer/capability boundaries, secret separation and redaction hygiene, least-privilege enforcement, HMAC signature validation, quota/fallback and gateway admission policies, evidence provenance integrity, and fail-closed behavior.

All findings confirm that the system enforces rigorous fail-closed cryptographic verification, cryptographic comparison invariants (`hmac.compare_digest`), strict schema validation for dispatch IDs and target SHAs, and non-mutating provenance collection. No secrets are read or output during verification.

---

## 2. Evidence References & Blob SHAs

| Component / File Path | Blob SHA / Ref | Role in Security Architecture |
|---|---|---|
| `GEMINI.md` | `4c431143aa5c46776e80893bf3c0e5f202e3b76d` (ref: `main`) | Agent Rules & Contour A Scope Boundaries |
| `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Security, Trust & Authorization Governing Rules |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Canonical Governance, Invariants, and Executor Classes |
| `runtime/mediahub_runtime/astra_security.py` | `6761edb5e1e9e035388aabcd1b95d240098c2ec4` | Secret Detection, Redaction, and Persistence Gates |
| `tests/test_gemini_child_signed_dispatch_runtime_contract.py` | `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe` | Negative Tests for Controller/Child HMAC Transport |

---

## 3. Detailed Audit Findings

### A. Controller / Child Transport & HMAC Integrity
- **Mechanism:** The controller workflow (`gemini-batch-dispatch-controller.yml`) signs dispatch payloads using HMAC-SHA256 with secret key `MEDIAHUB_DISPATCH_HMAC_KEY`. Signed fields are strictly bounded: `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, and `scope`.
- **Serialization:** Canonical serialization uses `json.dumps(payload, sort_keys=True, separators=(",", ":"))` to ensure byte-for-byte consistency between controller signing and child verification.
- **Timing Attack Resistance:** Child verification scripts utilize Python's `hmac.compare_digest()` for constant-time signature comparison.
- **Fail-Closed Validation:** Child scripts enforce strict regex validation:
  - UUIDv4 shape check (`^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`).
  - 40-hex character check for `TARGET_SHA`.
  - Allowlist enforcement for `BASE_REF` (`main`) and `SCOPE` (`contour-a`).
  - Event context verification (`workflow_dispatch` from `VlDMlNSh/mediahub-os` on `refs/heads/main`).
- **Negative Testing Coverage (`tests/test_gemini_child_signed_dispatch_runtime_contract.py`):**
  - Tampered tasks after signing are rejected with `Invalid controller signature`.
  - Signatures generated for one child workflow are rejected when presented to another child workflow.
  - Malformed UUIDs or target SHAs fail validation *before* signature checks.
  - Non-allowlisted base refs or scopes fail validation even with valid signatures.
  - Missing HMAC keys or invalid signatures fail closed immediately.

### B. Issuer / Capability & Least Privilege
- **Issuer Authority:** Dispatches originate strictly from the authenticated central controller workflow.
- **Workflow Permissions:** Child workflows enforce minimal GitHub Actions permissions (e.g., `contents: read` for review workflows, restricted tool lists such as `read_file`, `grep_search`, `glob`, `list_directory`).
- **Token Protection:** `persist-credentials: false` is enforced across delegated checkouts to prevent credential leakage.

### C. Secret Separation & Hygiene (`astra_security.py`)
- **Primitives:** SOPS + age encryption. Plaintext secrets are strictly excluded from git and evidence artifacts (`INV_NO_CREDENTIALS_IN_GIT`, `INV_NO_SECRETS_IN_EVIDENCE`).
- **Redaction Engine:** `runtime/mediahub_runtime/astra_security.py` provides robust `scan_secret`, `redact`, and `require_safe` functions. Secret-like strings (such as Bearer tokens and API keys) are detected and replaced with `[REDACTED_SECRET]`.
- **Evidence Masking:** Evidence metadata governance rules mandate that secret values are suppressed (`secret_values: SUPPRESSED`), authorization tokens redacted (`authorization_tokens: SUPPRESSED`), and raw provider responses masked (`raw_provider_responses: REDACTED`).

### D. Quota, Fallback Policy & Gateway Admission
- **Governance Alignment:** ASTRA GOLD governance contract defines executor classes (local and cloud executors sharing a common admission ladder). Cloud executors carry executor-only authority (`EXECUTOR_ONLY`) and require explicit admission.
- **Gateway Boundary:** Gateway paths (OpenRouter, Unorouter, etc.) are explicitly classified as non-native provider qualification paths that preserve provider identity and do not bypass admission gates or acquire State Authority.
- **Fallback Limits:** Authorization failures and capability mismatches fail closed; missing evidence blocks promotion/launch (`INV_MISSING_EVIDENCE_BLOCKS`).

### E. Evidence Provenance & Fail-Closed Workflow Validation
- **Required Metadata:** Evidence bundles must include `command_id`, `node_id`, `component_id`, `executor_id`, `provider_or_model_id`, `source_sha`, `round`, `timestamp`, `exit_status`, `timeout`, `workspace`, `verification_status`, and `evidence_digest`.
- **Workflow Validator Rigor:** Step validators check `steps.gemini.outcome == "success"` with `if: always()` and inspect structured stdout logs to ensure successful tool calls (e.g., Pull Request creation) before reporting success. Empty or unverified outcomes fail closed.

---

## 4. Acceptance Criteria & Verification Status

1. **HMAC Integrity & Constant-Time Comparison:** VERIFIED via `test_gemini_child_signed_dispatch_runtime_contract.py`.
2. **Strict Regex & Allowlist Validation:** VERIFIED (malformed UUIDs, bad target SHAs, and out-of-scope bases are rejected).
3. **Secret Separation & Redaction:** VERIFIED via `test_astra_security.py`.
4. **Least Privilege & Token Constraints:** VERIFIED (restricted permissions, `persist-credentials: false`).
5. **Fail-Closed Behavior on Outage/Tampering:** VERIFIED (missing keys, signature mismatches, and failed model runs fail closed).

---

## 5. Residual Risks & Known Gaps

1. **External Gateway Reliance:** Cloud gateway executors depend on upstream provider availability; fallback policies ensure fail-closed behavior on outage.
2. **Manual Approvals for Launch (G11):** Human approval records remain strictly human-only and cryptographically tied to approved source SHAs and fresh evidence bundles.
