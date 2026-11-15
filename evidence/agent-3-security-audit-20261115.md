# MediaHub OS — Independent Security & Provenance Audit (Agent 3)

- **Audit Date:** 2026-11-15
- **Auditor Agent:** `gemini-agent-3` (Credential Ref: `GEMINI_API_KEY_3`)
- **Authorized Contour:** Contour A (Developer Fabric)
- **Immutable Target SHA:** `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`
- **Branch:** `agent-3-security-audit-bc4fa9a4-cec6-4ccc-89ab-e811754917b8`
- **Task / Queue Ref:** A3-SECURITY-PROVENANCE-AUDIT-20261115

---

## 1. Executive Summary

This independent security and provenance audit evaluates the MediaHub OS Contour A runtime, controller/child transport protocols, command authorization mechanisms, secret separation boundaries, least privilege invariants, and fail-closed error handling against immutable target SHA `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`. 

All findings confirm that the architecture maintains rigorous cryptographic verification, strict secret-redaction boundaries, and a fail-closed posture. No secrets are logged, emitted, or committed to git.

---

## 2. Core Security Domains & Evidence

### A. Controller / Child Transport & HMAC Authentication
- **Verified Files:** `astra_github_agent.py`, `tests/test_astra_command_auth.py` (Blob SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`)
- **Mechanism:** Command messages require HMAC-SHA256 signatures derived from a pre-shared key (`COMMAND_HMAC_KEY`) and bounded by a maximum age window (`COMMAND_HMAC_MAX_AGE_SECONDS`, e.g., 900s).
- **Controls & Negative Tests:**
  - Unauthorized/tampered command payloads fail signature verification (`test_signature_is_required_and_verified`).
  - Stale commands older than the maximum age threshold are rejected (`test_stale_command_is_rejected`).
  - Command ID path safety (`_safe_id`) rejects path traversal (`../escape`, `cmd/escape`, empty strings).
  - Target SHA validation (`_valid_target_sha`) enforces strict 40/64 hex-character git SHA formatting.
  - Idempotent execution markers prevent replay attacks.

### B. Issuer / Capability & Least Privilege
- **Verified Files:** `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` (Blob SHA: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`), `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` (Blob SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`)
- **Invariants:**
  - Default deny across all operations.
  - Product State Authority alone owns canonical MediaHub product-state mutation; AI agents, cloud workflows, and transport adapters possess zero state authority (`INV_NO_PROVIDER_STATE_AUTHORITY`, `INV_NO_TRANSPORT_STATE_AUTHORITY`).
  - Emergency/recovery operations use explicitly defined capabilities with no wildcard authority.
  - Independent A3 review and human approval (`G11`) are strictly enforced prior to launch.

### C. Secret Separation & Persistence Gate
- **Verified Files:** `runtime/mediahub_runtime/astra_security.py` (Blob SHA: `ff4ba9b581cf30e0f2d6bbed70c5290d93bfa27d`), `tests/test_astra_security.py` (Blob SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`)
- **Mechanisms:**
  - Strict pattern matching (`_SECRET_PATTERNS`) detects API keys, GitHub tokens (`ghp_`, `github_pat_`), Bearer tokens, passwords, and authorization headers.
  - Persistence gates (`require_safe`) intercept secret-like content before writing to durable memory or persistence stores, raising `ValueError`.
  - Context-export boundaries apply `redact()` as defense in depth (`[REDACTED_SECRET]`).
- **Negative Tests:** `test_secret_like_values_are_detected_and_redacted`, `test_persistence_gate_rejects_secret_like_content`.

### D. Quota / Fallback Policy & Fail-Closed Behavior
- **Governance Thresholds:** Heartbeat TTL (120s), lease TTL (600s), executor timeout (900s), evidence freshness (86400s).
- **Fail-Closed Invariants:**
  - Ambiguous policy results fail closed.
  - Authorization service unavailability denies mutation unless a bounded local policy is explicitly authorized.
  - Missing evidence blocks execution (`INV_MISSING_EVIDENCE_BLOCKS`).
  - Gateway paths (`OPENROUTER_GATEWAY`, etc.) do not substitute for native provider qualification.

### E. Evidence Provenance & Integrity
- **Metadata Requirements:** Every evidence record must contain `command_id`, `node_id`, `component_id`, `executor_id`, `provider_or_model_id`, `source_sha`, `round`, `timestamp`, `exit_status`, `timeout`, `workspace`, `verification_status`, and `evidence_digest`.
- **Secret & Token Suppression:** Secret values are suppressed, authorization tokens suppressed, raw provider responses redacted.

---

## 3. Acceptance Criteria & Verification Status

| Acceptance Criterion | Status | Verification Reference |
|---|---|---|
| Valid principal + authorized command | PASS | `tests/test_astra_command_auth.py` |
| Invalid signature / tampered command | PASS | `tests/test_astra_command_auth.py` |
| Stale command rejection | PASS | `tests/test_astra_command_auth.py` |
| Path safety & SHA validation | PASS | `tests/test_astra_command_auth.py` |
| Secret detection & persistence gate | PASS | `tests/test_astra_security.py` |
| Least privilege & state authority isolation | PASS | `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` |
| Fail-closed on ambiguity/outage | PASS | `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` |

---

## 4. Known Gaps & Residual Risks

1. **Candidate Cloud Executors:** Multiple cloud executors (Gemini, Perplexity, Kimi, Deepseek, OpenAI, Anthropic, GigaChat, OpenRouter) currently hold `NOT_PROVEN` status under `ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`. Until 23 rounds of independent qualification and A3 verification are completed, their authority remains zero.
2. **Runtime Telemetry Exposure:** Continuous monitoring must ensure telemetry sinks do not inadvertently ingest environment variables containing provider API keys. `astra_security.py` redaction provides defense in depth.

---

## 5. Conclusion

Agent 3 security and provenance audit is complete. The system exhibits robust cryptographic authentication, strict secret separation, fail-closed design, and absolute separation of execution from canonical state authority. Draft audit concluded; no merge, deployment, qualification, or nested dispatch executed.
