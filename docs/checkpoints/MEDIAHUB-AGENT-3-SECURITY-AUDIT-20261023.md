# MediaHub OS — Agent 3 Independent Security and Provenance Audit

- **Queue/Task ID:** Agent 3 Independent Security and Provenance Audit (Contour A)
- **Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Auditor:** Gemini Agent 3 (Security & Verification Review)
- **Authorized Contour:** Contour A (Developer Fabric)
- **Date:** 2026-10-23
- **Status:** DRAFT AUDIT REPORT — NON-MUTATING INDEPENDENT REVIEW

## Executive Summary

This independent security and provenance audit evaluates the cryptographic dispatch transport, issuer/capability boundaries, secret separation, HMAC verification mechanics, quota/fail-closed policies, and evidence provenance across MediaHub OS Contour A as of target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`.

All evaluated components enforce strict fail-closed security invariants, least privilege access, and tamper-resistant cryptographic signatures. No secrets or private credentials are read, emitted, or compromised.

---

## 1. Controller / Child Transport & HMAC Integrity

- **Mechanism:** Controller (`.github/workflows/gemini-batch-dispatch-controller.yml`) signs child dispatches using HMAC-SHA256 over a canonical JSON payload (`workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, `scope`) serialized with `sort_keys=True` and `separators=(",", ":")`.
- **Verification:** Child authorizer steps and test suites (`tests/test_gemini_child_signed_dispatch_runtime_contract.py`, blob SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`) independently verify:
  - Valid cryptographic signature using `hmac.compare_digest`.
  - Strict input shape validation for UUID4 dispatches and 40/64-character Git SHAs.
  - Allowlist enforcement for `base_ref` (`main`) and `scope` (`contour-a`).
  - Strict event (`workflow_dispatch`), repository, and branch context checks.

## 2. Issuer, Capability, & Least Privilege

- **Permissions:** Reviewer and engineering workflows enforce minimal GitHub Actions token permissions (e.g., `contents: read` for review passes, explicit scoping for tool execution).
- **Tool Access:** Tools are explicitly bound to allowlists (e.g., read-only tools for review workflows: `read_file`, `grep_search`, `glob`, `list_directory`).
- **Product State Authority:** AI agents, cloud workflows, queues, and adapters possess zero canonical product-state mutation authority. State Authority remains strictly outside direct agent model control.

## 3. Secret Separation & Redaction

- **Primitives:** SOPS + age principles govern secret storage.
- **Runtime Defenses:**
  - `runtime/mediahub_runtime/astra_security.py` (blob SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`) provides `scan_secret` and `require_safe` guards, actively detecting and redacting sensitive patterns (`[REDACTED_SECRET]`).
  - Context redaction (`tests/test_astra_context_redaction.py`, blob SHA: `d0ff000e39a0466fa41b9c2e555b5c521d147c7e`) prevents legacy token or key material from propagating into prompt contexts.
  - Governance contracts (`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`, blob SHA: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`) mandate suppression of secret values and authorization tokens in evidence metadata.

## 4. Quota, Fallback Policy, & Fail-Closed Behavior

- **Fail-Closed Triggers:**
  - Missing HMAC secret or invalid signature -> immediate failure (non-zero exit).
  - Task tampering post-signing -> rejected.
  - Cross-child workflow signature replay -> rejected.
  - Workflow outcome failures -> caught by `always()` outcome validators (`GEMINI_OUTCOME != "success"`), preventing silent failures or incomplete/non-actionable PR outputs from passing.
- **Absence of Insecure Fallback:** When a dependency or secret is unavailable, affected capabilities fail closed without fallback to insecure modes.

## 5. Evidence Provenance & Traceability

- **Audited References:**
  - Security Contract: `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` (SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`)
  - Governance Contract: `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` (SHA: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`)
  - Signed Dispatch Contract Tests: `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (SHA: `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe`)
  - Command Auth Tests: `tests/test_astra_command_auth.py` (SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`)
  - Security & Redaction Tests: `tests/test_astra_security.py` (SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`), `tests/test_astra_context_redaction.py` (SHA: `d0ff000e39a0466fa41b9c2e555b5c521d147c7e`)

## 6. Negative Test Coverage Summary

| Negative Test Case | Mechanism Tested | Expected Result | Verified Status |
|---|---|---|---|
| Task Tampering | Modified task string after HMAC calculation | Rejection ("Invalid controller signature") | Pass |
| Cross-Child Replay | Reusing signature from workflow A for workflow B | Rejection ("Invalid controller signature") | Pass |
| Malformed Dispatch ID | Non-UUID4 or invalid version UUID | Rejection ("Malformed target SHA or dispatch ID") | Pass |
| Invalid Target SHA | Non-hex or non-40/64 character SHA | Rejection ("Malformed target SHA or dispatch ID") | Pass |
| Unsafe Scope/Base | `contour-b` or non-main base ref | Rejection ("Input outside allowlist") | Pass |
| Context Mismatch | Wrong `workflow_dispatch`, repo, or branch | Rejection ("Child must run from trusted main...") | Pass |
| Missing Secret | Empty `HMAC_KEY` | Rejection ("Dispatch HMAC secret missing") | Pass |
| Non-Actionable Output | Malformed or empty JSON / 0 successful tools | Rejection by output validator | Pass |

## 7. Residual Risks & Recommendations

1. **GitHub Actions Secrets Dependency:** System security relies heavily on correct repository secret configuration (`MEDIAHUB_DISPATCH_HMAC_KEY`, API tokens).
2. **Cloud Executor Admission:** Candidate cloud execution paths remain `NOT_PROVEN` until completing 23-round rigorous qualification passes.
3. **Recommendation:** Maintain strict separation of Contour A and Contour B, ensuring all future candidate executors undergo independent A3 verification and fresh 24H soak runs prior to promotion.
