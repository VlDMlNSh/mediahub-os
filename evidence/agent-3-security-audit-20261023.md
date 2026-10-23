# MediaHub OS — Independent Security and Provenance Audit (Agent 3)

## Audit Metadata

- **Agent Identity:** `gemini-agent-3`
- **Authorized Contour:** `contour-a` (Developer Fabric)
- **Immutable Target SHA:** `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- **Base Ref:** `main`
- **Audit Date:** 2026-10-23
- **Status:** DRAFT INDEPENDENT AUDIT (No merge, deployment, qualification, or nested dispatch executed)

---

## 1. Controller / Child Transport Security

- **Primary Artifacts:**
  - `astra_github_agent.py` (Blob SHA: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`)
  - `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` (Blob SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`)
- **Transport Architecture:**
  - The worker synchronizes via bounded git operations with exponential backoff (`git_network`).
  - Worktree state is checked out deterministically (`git checkout --detach origin/main` or remote result branches).
  - Consumed commands are restored and cleaned locally without disturbing unrelated user worktree modifications (`git restore` / `git clean`).
  - Self-re-execution (`maybe_reexec_updated_agent`) ensures running agent code matches the synchronized repository revision via SHA verification (`RUNNING_AGENT_SHA`).

---

## 2. Issuer / Capability & Least Privilege

- **Command Envelope Enforcement:**
  - Strict validation of required fields: `schema_version`, `command_id`, `node_id`, `operation`, `target_sha`, `workflow_only`, `owned_paths`, `title`, `description`, `exclusive_actions`, `issued_at`.
  - Allowed operations are restricted to an explicit whitelist (`OPERATIONS`).
- **Path and Scope Validation:**
  - `owned_paths` are validated to ensure they are relative paths and prohibit directory traversal (`..`).
  - Command IDs and node IDs are validated against strict regex (`SAFE_ID_RE`, `SHA_RE`).
- **State Authority Boundary:**
  - In accordance with `GEMINI.md` and the security contract, AI agents, cloud workflows, and transport workers do not possess Product State Authority. State mutation paths remain strictly governed by the canonical Product State Authority.

---

## 3. HMAC & Credential Separation

- **HMAC-SHA256 Authentication:**
  - Command envelopes require valid cryptographic signatures computed over the canonicalized JSON body (`_canonical_command_body`, sorted keys, compact separators).
  - Node-specific environment secrets (`ASTRA_NODE_HMAC_KEY_MH_DEV_01`, `ASTRA_NODE_HMAC_KEY_MH_DEV_02`, `ASTRA_NODE_HMAC_KEY_VOKTORS_MAC`) are retrieved from secure environment variables.
  - Maximum age check (`COMMAND_HMAC_MAX_AGE_SECONDS`, default 900s) prevents replay attacks.
  - Constant-time comparison (`hmac.compare_digest`) prevents timing attacks.
- **Secret Separation & Suppression:**
  - Production plaintext secrets are never committed or logged.
  - Published execution results and diagnostic payloads explicitly suppress secret values (`"secret_values": "SUPPRESSED"`).

---

## 4. Quota / Fallback & Fail-Closed Behavior

- **Fail-Closed Invariants:**
  - Unknown node identities, invalid or missing signatures, expired command timestamps, target SHA mismatches, or invalid distributed verification evidence result in immediate rejection (`BLOCKED` status).
  - There are no insecure fallbacks when authentication, signature verification, or security dependencies fail.
- **Retry & Bounded Execution:**
  - Autonomous missions use bounded retry cycles (`ASTRA_AUTONOMOUS_MAX_CYCLES`) tied immutably to the target SHA without unauthorized drift to `origin/main` mid-retry.

---

## 5. Evidence Provenance & Negative Testing

- **Verified Test Suite Evidence:**
  - `tests/test_astra_command_auth.py` (Blob SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`)
  - `tests/test_astra_security.py` (Blob SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`)
- **Negative Test Coverage:**
  - *Invalid/Altered Signatures & Operations:* Verified that unauthorized operation overrides or altered payloads fail `_command_auth_valid`.
  - *Stale Commands:* Verified that commands issued outside `COMMAND_HMAC_MAX_AGE_SECONDS` are rejected.
  - *Path Traversal:* Verified that `../` in command IDs or owned paths is blocked by `_safe_id` / `owned_paths` validators.
  - *Target SHA Mismatch:* Verified that execution halts if current HEAD does not match the signed `target_sha`.

---

## 6. Residual Risks & Recommendations

1. **Secret Key Management:** Ensure environment key rotation schedules are enforced outside the repository scope.
2. **Distributed Evidence Freshness:** Maintain strict validation of evidence timestamps (`ASTRA_DISTRIBUTED_MAX_AGE_SECONDS`) across multi-node workers.
3. **Draft Scope Limitation:** This audit is delivered as a read-only architectural and provenance verification report; no merge, deployment, or qualification execution was performed.
