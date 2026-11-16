# Agent 3 — Independent Security and Provenance Audit

- **Agent ID**: `gemini-agent-3`
- **Contour**: Contour A (Developer Fabric)
- **Immutable Target SHA**: `1694cde38c7b7d69baf9676b4908c1bb6e197fbe`
- **Date**: 2026-11-16
- **Status**: Audit Completed — Draft PR

## Scope & Verified Artifacts
- `GEMINI.md` (SHA: `4c431143aa5c46776e80893bf3c0e5f202e3b76d`)
- `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` (SHA: `8d831c2a8fa333977dd86524099568bae2a8db0e`)
- `astra_github_agent.py` (SHA: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`)
- `tests/test_astra_security.py` (SHA: `6761edb5e1e9e035388aabcd1b95d240098c2ec4`)
- `tests/test_astra_command_auth.py` (SHA: `8df49fc55e660c13ad54aca9b9dc78132c335dd1`)

## Audit Findings & Invariants

### 1. Controller / Child Transport & HMAC Authentication
- **Mechanism**: Commands issued via `control/commands/{node_id}.json` require HMAC-SHA256 signatures over canonicalized JSON bodies (`_canonical_command_body`).
- **Validation**: `_command_auth_valid` enforces:
  - Non-empty signature and string-typed `issued_at`.
  - Max age check (`COMMAND_HMAC_MAX_AGE_SECONDS`, default 900s) preventing replay attacks.
  - Constant-time comparison via `hmac.compare_digest`.
  - Node-specific HMAC environment variable mapping (`COMMAND_HMAC_ENV`).
- **Negative Tests**: Verified in `test_astra_command_auth.py` (`test_signature_is_required_and_verified`, `test_stale_command_is_rejected`). Stale timestamps (> max age) and modified operations are correctly rejected.

### 2. Secret Separation & Least Privilege
- **Secret Handling**: Zero tolerance for plaintext secret leakage. `astra_security.py` provides `scan_secret` and `require_safe` primitives that redact sensitive tokens (e.g. `[REDACTED_SECRET]`).
- **Result Suppression**: `publish()` enforces `publish_result.setdefault("secret_values", "SUPPRESSED")`.
- **Least Privilege**: Commands restrict state modification through explicit ownership paths (`owned_paths`), workflow-only constraints (`workflow_only`), and strict command schema validation (`REQUIRED_COMMAND_FIELDS`).

### 3. Quota / Fallback Policy & Fail-Closed Behavior
- **Network Failures**: `git_network` implements bounded exponential backoff with retries and fails closed upon exhaustion.
- **Result Branch Safety**: Remote node branch pushing (`git push origin HEAD:astra-node/{NODE_ID}`) fails closed on divergence without remote branch rewriting.
- **Claim Leasing**: Agent claims use lease expiry (`claim_lease_seconds`) with explicit verification status transitions (`ACTIVE`, `VERIFIED`, `REJECTED`).

### 4. Evidence Provenance
- Results include source revisions, execution heads, claim records, durations, and artifact digests.
- No direct product state mutation occurs via agent transport without passing State Authority gates.

## Residual Risks & Recommendations
1. **Secret Key Provisioning**: Relies on external environment variables (`ASTRA_NODE_HMAC_KEY_*`). Proper out-of-band secret rotation and SOPS/age integration must be maintained.
2. **Clock Drift**: HMAC max age verification depends on synchronized system clocks (NTP). Significant clock skew could lead to false-positive rejections.
