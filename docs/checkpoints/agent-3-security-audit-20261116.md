# MediaHub OS — Agent 3 Independent Security and Provenance Audit

- **Agent Identity**: `gemini-agent-3`
- **Credential Reference**: `GEMINI_API_KEY_3`
- **Authorized Contour**: Contour A (Developer Fabric)
- **Immutable Target SHA**: `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`
- **Date**: 2026-11-16
- **Status**: DRAFT AUDIT REPORT — NO MERGE / DEPLOYMENT AUTHORIZED

---

## 1. Executive Summary

This independent security and provenance audit evaluates the transport security, issuer/capability models, secret separation, least privilege enforcements, HMAC integrity checks, quota/fallback policies, and evidence provenance across MediaHub OS Contour A against the immutable target SHA `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`.

All findings confirm rigorous adherence to fail-closed design principles, cryptographic dispatch verification, strict redaction boundaries, and the governance invariants codified in Baseline 2.0.

---

## 2. Controller & Child Transport Security (HMAC & Signatures)

- **Mechanisms**: 
  - Controller and child workflows implement HMAC-SHA256 signature verification over canonical JSON payloads (`workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`).
  - Strict key comparison via `hmac.compare_digest` prevents timing attacks.
  - Strict validation of UUIDv4 shape for `DISPATCH_ID` and 40/64 hex character shape for `TARGET_SHA`.
  - Event provenance validation requires `workflow_dispatch` events originating exclusively from trusted repository ref `refs/heads/main`.
- **Blob SHAs & References**:
  - `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`)
  - `tests/test_astra_command_auth.py` (SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`)

---

## 3. Issuer, Capability & Least Privilege

- **Invariants**:
  - Default deny and least privilege are enforced across all principal classes (human, device, workload, automation/agent, external integration).
  - Review workflows operate with read-only content permissions (`permissions: contents: read`) and lack token escalation or PR creation privileges.
  - Product State Authority alone owns canonical MediaHub product-state mutation. AI agents, cloud workflows, and adapters do not acquire mutation authority.
- **Blob SHAs & References**:
  - `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` (SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`)
  - `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` (SHA: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`)

---

## 4. Secret Separation & Hygiene

- **Mechanisms**:
  - Regular-expression based pattern detection (`_SECRET_PATTERNS`) covers API keys, GitHub tokens (`ghp_`, `github_pat_`), Bearer tokens, and secret assignments.
  - Persistence gate (`require_safe`) actively rejects secret-like content before persistence.
  - Redaction (`redact`) substitutes sensitive values with `[REDACTED_SECRET]`.
  - Evidence metadata explicitly suppresses secret values and authorization tokens (`secret_values: SUPPRESSED`, `authorization_tokens: SUPPRESSED`).
- **Blob SHAs & References**:
  - `runtime/mediahub_runtime/astra_security.py` (SHA: `ff4ba9b581cf30e0f2d6bbed70c5290d93bfa27d`)
  - `tests/test_astra_security.py` (SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`)

---

## 5. Quota, Fallback Policy & Fail-Closed Behavior

- **Behavior**:
  - Missing HMAC keys, invalid signatures, malformed payload fields, or unauthorized base/scope parameters result in immediate non-zero exit and fail-closed termination.
  - Executor classes (local vs cloud) share an admission ladder requiring credential presence, non-mutating probes, and independent A3 verification.
  - Ambiguous policy results or missing evidence blocks execution (`INV_MISSING_EVIDENCE_BLOCKS`).

---

## 6. Negative Tests & Coverage Verification

- **Verified Negative Test Scenarios**:
  1. Task tampering after signing (`test_task_tampering_after_signing_is_rejected`).
  2. Cross-child workflow signature reuse (`test_signature_from_another_child_workflow_is_rejected`).
  3. Malformed UUIDv4 and non-hex target SHAs (`test_invalid_uuid_shapes_are_rejected_even_with_valid_signature`, `test_invalid_target_sha_is_rejected_before_signature_check`).
  4. Non-allowlisted base or scope parameters (`test_non_allowlisted_base_and_scope_are_rejected_even_when_signed`).
  5. Wrong event triggers, repositories, or refs (`test_wrong_event_repository_or_ref_is_rejected`).
  6. Missing HMAC secret and invalid signature (`test_missing_key_and_invalid_signature_fail_closed`).

---

## 7. Residual Risks & Recommendations

- **Residual Risks**:
  - Security posture relies on the integrity of GitHub Actions secret storage for `HMAC_KEY` and API keys.
  - Periodic rotation of HMAC secrets and least-privilege credential scopes must be maintained.
- **Conclusion**:
  - No security regressions or unverified token escalations were identified. The implementation satisfies the security and provenance requirements for Contour A dispatch tasks.
