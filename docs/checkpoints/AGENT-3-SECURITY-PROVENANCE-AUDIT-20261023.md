# MediaHub OS — Contour A Agent 3 Security & Provenance Audit

- **Date:** October 23, 2026
- **Agent Identity:** `gemini-agent-3`
- **Authorized Contour:** `contour-a`
- **Immutable Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Base Ref:** `main`

---

## 1. Executive Summary & Scope

This independent security and provenance audit was conducted by Agent 3 under MediaHub OS Contour A guidelines. The audit examines the cryptographic trust chain, authorization invariants, secret separation, transport mechanisms, least privilege enforcement, HMAC verification, quota/fallback policies, and evidence provenance across the controller and child agent workflows.

No plaintext secrets were read, logged, or emitted. All evaluations were performed statically against immutable contracts and test suites at target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`.

---

## 2. Exact References & Source Blob SHAs

| Artifact / Module | Path | Ref / SHA |
|---|---|---|
| Repository Base | `VlDMlNSh/mediahub-os` | `fbbdc9a06ef344cd57aae13b230a042af76bbc60` |
| Agent Rules | `GEMINI.md` | `4c431143aa5c46776e80893bf3c0e5f202e3b76d` |
| Security Contract | `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` |
| Security Unit Tests | `tests/test_astra_security.py` | `6761edb5e1e9e035388aabcd1b95d240098c2ec4` |
| Command Auth Tests | `tests/test_astra_command_auth.py` | `8df49fc55e660c13ad54aca9b9dc78132c335dd1` |
| Child Signed Dispatch Tests | `tests/test_gemini_child_signed_dispatch_runtime_contract.py` | `e92e1c3f4e52fb2005845e520d1bbe10dcdacfbe` |
| Transport Controller Tests | `tests/test_gemini_transport_controller_contract.py` | `5ae0e8db9465ce36bd4020df69b552c659cd6187` |

---

## 3. Detailed Security Findings & Architectural Invariants

### 3.1 Controller / Child Transport & HMAC Integrity
- **Mechanism:** The batch dispatch controller (`.github/workflows/gemini-batch-dispatch-controller.yml`) issues signed dispatches using HMAC-SHA256 (`MEDIAHUB_DISPATCH_HMAC_KEY`).
- **Signed Payload:** The payload strictly includes `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, and `scope`, serialized using sorted keys (`sort_keys=True`) and compact separators (`separators=(",", ":")`).
- **Verification:** Child workflows (`gemini-autonomous-engineering.yml`, `gemini-agent-2.yml`, `gemini-agent-3.yml`, `gemini-fcc-independent-review-wave409.yml`) independently re-compute the HMAC and verify it using constant-time comparison (`hmac.compare_digest`).

### 3.2 Issuer & Capability Controls
- **Allowlist Enforcements:** Child workflows strictly validate that `BASE_REF == "main"`, `SCOPE == "contour-a"`, `EVENT_NAME == "workflow_dispatch"`, and `REPOSITORY == "VlDMlNSh/mediahub-os"`.
- **Format Validation:** UUIDv4 dispatch IDs and 40-character Git target SHAs are validated against strict regular expression patterns before signature evaluation.
- **Fail-Closed Behavior:** Any tampering with task descriptions, workflow file targets, scopes, or missing/invalid HMAC keys results in immediate, non-zero exit and fail-closed rejection.

### 3.3 Secret Separation & Least Privilege
- **Provider Isolation:** Each agent job uses dedicated, separate provider secrets (`GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`) alongside `MEDIAHUB_DISPATCH_HMAC_KEY`.
- **No Inheritance:** `secrets: inherit` is explicitly prohibited across all controller and child workflows.
- **Token Scope:** `MEDIAHUB_GITHUB_TOKEN` is confined to the controller for dispatch API calls and is never exposed to child execution environments.

### 3.4 Quota, Fallback, & Readiness Gates
- **Readiness Gate:** Batch execution is gated by `MEDIAHUB_GEMINI_BATCH_ENABLED`, defaulting to disabled (closed).
- **Reconciliation:** Pending or unknown dispatch statuses are systematically tracked and reconciled without abandoning fail-closed semantics or bypassing safety boundaries.

### 3.5 Evidence Provenance & Output Validation
- **Structured Validation:** Child outputs are subjected to strict post-execution parsing to verify non-empty responses, structured statistics (`stats.tools.byName`), successful tool execution counts, and mandatory Pull Request creation evidence.

---

## 4. Negative Testing & Failure Scenarios
The automated test suite (`tests/test_gemini_child_signed_dispatch_runtime_contract.py`) covers:
1. Valid canonical signatures succeeding across all authorized children.
2. Task tampering after signing being rejected (`Invalid controller signature`).
3. Cross-workflow signature replay attacks being rejected.
4. Malformed UUIDv4 formats and non-v4 identifiers being rejected.
5. Malformed target SHAs being rejected prior to signature verification.
6. Non-allowlisted base refs (`feature/unsafe`) and scopes (`contour-b`) being rejected.
7. Incorrect event types, repositories, or refs being rejected.
8. Missing HMAC secrets or invalid signature hashes failing closed.

---

## 5. Residual Risks & Recommendations
- **Runner Security:** Relies entirely upon GitHub Actions runner isolation and secure secret storage.
- **Recommendation:** Maintain strict access control on GitHub repository secrets (`MEDIAHUB_DISPATCH_HMAC_KEY` and model API keys) and utilize SOPS + age for any auxiliary repository-stored configuration.

---

## 6. Verification Status
- **Status:** PASSED (Static & Contract Verification)
- **Deployment / Merge:** NONE (Draft audit report only; no merge, deployment, qualification, or nested dispatch performed).
