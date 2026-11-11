# Agent 3 — Independent Security and Provenance Audit

- **Agent Identity**: `gemini-agent-3`
- **Credential Reference**: `GEMINI_API_KEY_3`
- **Authorized Contour**: `contour-a`
- **Target SHA (Immutable)**: `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Date**: 2026-10-23
- **Status**: DRAFT_AUDIT_COMPLETED (No merge, deployment, qualification, or nested dispatch)

---

## 1. Executive Summary

This independent security and provenance audit evaluates the MediaHub OS Contour A codebase at the immutable target SHA `fbbdc9a06ef344cd57aae13b230a042af76bbc60`. The review covers controller/child transport isolation, issuer/capability models, secret separation & hygiene, HMAC command authentication, quota/fallback policies, evidence provenance integrity, and fail-closed behaviors.

All findings indicate strict adherence to the ASTRA-GOLD governance contract and security invariants, with zero plaintext secrets exposed or committed.

---

## 2. Examined Source Artifacts & Blob SHAs

| Component / File Path | Blob / File SHA | Purpose & Security Relevance |
|---|---|---|
| `GEMINI.md` | `4c431143aa5c46776e80893bf3c0e5f202e3b76d` | Agent operating rules & authority scope (Contour A separation) |
| `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Security, trust, and authorization invariants |
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Gate registry, runtime thresholds, invariant registry & executor classes |
| `runtime/mediahub_runtime/astra_security.py` | `ff4ba9b581cf30e0f2d6bbed70c5290d93bfa27d` | Secret scanning, redaction, and persistence safety gates |
| `tests/test_astra_security.py` | `6761edb5e1e9e035388aabcd1b95d240098c2ec4` | Secret detection and persistence gate tests |
| `tests/test_astra_command_auth.py` | `8df49fc55e660c13ad54aca9b9dc78132c335dd1` | HMAC verification, stale rejection, path safety, and SHA shaping tests |
| `tests/test_astra_github_agent_contract.py` | `7dc0b70c9b5c3e0ef664749d5527b71740cb1656` | Transport routing, environment isolation, and sign-off contracts |

---

## 3. Detailed Security Findings

### A. Controller / Child Transport & Isolation
- **Isolation**: Child transport utilizes isolated environment copies (`fcc_env = base_env.copy()`, `direct_claude_env`) without inheriting ambient unauthorized credentials.
- **Routing**: Model reasoning controls and OmniRoute proxy bindings (`base_url = "http://127.0.0.1:20128/v1"`, `wire_api = "responses"`) ensure traffic remains within bounded local gateways.
- **Evidence Consumption**: Controllers consume pre-signed/downloaded node evidence (`ASTRA_PROVIDER_EVIDENCE_PATH`, `distributed-verification-result.json`) rather than executing arbitrary unverified local scripts.

### B. Issuer / Capability & Least Privilege
- **Role Hierarchy**: Strict four-tier role separation (`A0`, `A1`, `A2`, `A3`).
- **Product State Authority**: AI agents, cloud workflows, queues, and adapters do not possess State Authority mutation privileges. Canonical product-state changes remain strictly separated from automation fabric.
- **Exclusive Actions**: Command envelopes explicitly declare required authority fields (`schema_version`, `command_id`, `node_id`, `operation`, `target_sha`, `workflow_only`, `owned_paths`, `exclusive_actions`).

### C. Secret Separation & Hygiene
- **Detection & Redaction**: `astra_security.py` enforces regex patterns for API keys (`sk-`, `ghp_`, `github_pat_`, Bearer tokens, etc.) with automatic `[REDACTED_SECRET]` substitution (`scan_secret`, `redact`).
- **Persistence Gate**: `require_safe()` blocks any data containing secret-like structures from entering durable storage or evidence logs (`INV_NO_CREDENTIALS_IN_GIT`, `INV_NO_SECRETS_IN_EVIDENCE`).
- **Suppression**: Published results explicitly enforce `secret_values: SUPPRESSED`.

### D. HMAC Command Authentication & Replay Protection
- **Node-Specific Keys**: Commands require cryptographic signatures verified using node-specific environment keys (e.g., `ASTRA_NODE_HMAC_KEY_MH_DEV_01`), preventing cross-node privilege escalation.
- **Replay/Staleness Window**: `COMMAND_HMAC_MAX_AGE_SECONDS` (900s default) rejects expired commands.
- **Idempotency**: Executed command markers prevent duplicate execution of processed command IDs.

### E. Quota / Fallback Policy & Fail-Closed Behavior
- **Fail-Closed**: Ambiguous policy results, invalid signatures, unknown principal identities, or mismatched SHA targets result in immediate rejection (`fail-closed`).
- **Retry Bounds**: Git network operations employ bounded retries with exponential backoff (`git_network`) before terminating cleanly.

### F. Evidence Provenance & Verification Integrity
- **Exact Target Enforcement**: Autonomous missions enforce exact SHA matching against current HEAD (`target_sha_not_exact_current_head` / `target_sha_changed_during_retry`).
- **No Self-Promotion**: Candidates cannot self-qualify or self-promote; independent A3 review is mandatory (`INV_NO_CANDIDATE_SELF_QUALIFICATION`, `INV_NO_LAUNCH_WITHOUT_INDEPENDENT_A3`).

---

## 4. Negative Tests & Test Coverage

Verified unit and contract tests covering failure modes:
1. `test_signature_is_required_and_verified`: Rejects altered operations or missing/invalid signatures.
2. `test_stale_command_is_rejected`: Rejects commands issued older than max age threshold.
3. `test_command_id_path_safety_is_enforced`: Rejects path traversal (`../`) in command IDs.
4. `test_target_sha_is_strictly_git_sha_shaped`: Rejects non-SHA target references.
5. `test_secret_like_values_are_detected_and_redacted`: Verifies detection and redaction of tokens/keys.
6. `test_persistence_gate_rejects_secret_like_content`: Enforces `ValueError` on attempted persistence of secret-like payloads.
7. `test_signer_requires_node_specific_key`: Prevents fallback to global wildcard secrets.

---

## 5. Residual Risks & Governance Gaps

1. **Candidate Cloud Executors**: Several direct provider paths (Gemini, Perplexity, Kimi, Deepseek, OpenAI, Anthropic, GigaChat) are currently marked `NOT_PROVEN` in the governance contract, pending complete 23-round qualification passes.
2. **Gateway vs Native**: Gateway executors (OpenRouter, etc.) do not substitute for native provider qualification.

---

## 6. Verification Status & Acceptance Criteria

- **Audit Status**: Complete.
- **Scope Compliance**: Contour A developer fabric only. No modifications to Contour B product logic.
- **Action Status**: Draft audit checkpoint created. No merge, deployment, qualification, or nested dispatch performed.
