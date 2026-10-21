# MediaHub OS — Wave 232 A3 Independent Security & Verification Review

- **Task ID:** Wave 232 A3
- **Agent Identity:** `gemini-agent-3`
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref / Dispatch SHA:** `main` (`25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`)
- **Target Review Scope:** PR 400 exact head (`6049f07325998257d8c12296887e0027c04e7d4d`), `ops/control/sign_command.py`, `tests/test_astra_command_auth.py`, `ops/mesh/admission.py`, `tests/test_mesh_admission_boundary.py`, `astra_github_agent.py` (`read_command`, `execute`, `publish`), and direct Git push paths.

---

## 1. Executive Summary

This independent security and verification review (Wave 232 A3) evaluates the Astra control-command signing subsystem, mesh admission boundary, worker task execution (`read_command`), and direct Git push publication path (`publish`). 

Contour A maintains strict isolation from Contour B product implementation. Product State Authority alone owns canonical MediaHub product-state mutation; AI agents, cloud queues, and adapters do not acquire product-state mutation authority.

---

## 2. Threat Model & Trust Boundary Analysis

### A. Trust-Boundary Gaps
1. **Symmetric HMAC vs. Asymmetric Trust:** Control commands are signed using node-specific symmetric HMAC keys (`ASTRA_NODE_HMAC_KEY_*`). While sufficient for localized worker dispatch, symmetric keys require secret distribution to both the signer (`sign_command.py`) and worker runtime (`astra_github_agent.py`), increasing exposure surface if environment segregation is compromised.
2. **Product State Authority Separation:** The worker executes code review, qualification, and telemetry publishing, but must never mutate canonical product state. The boundary is enforced by constraining worker push operations to isolated per-node branches (`astra-node/{NODE_ID}`) rather than `main`.

### B. Replay, Revocation, Issuer, & Capability Omissions
1. **Replay Protection:** Replay mitigation relies on execution marker files (`EXECUTED_COMMANDS/{command_id}.done`) and timestamp freshness (`MAX_AGE_SECONDS`, default 900s). However, there is no cluster-wide cryptographic nonce revocation store or distributed lease coordination outside local state directories.
2. **Issuer & Key Management:** Node IDs (`mh-dev-01`, `mh-dev-02`, etc.) map to static environment variable secret names. Key rotation requires out-of-band secret updates without built-in key rollover grace periods or issuer attestation chains.
3. **Capability Omissions:** Mesh admission (`ops/mesh/admission.py`) rigorously verifies capability authorities (`EXECUTION` vs `CONTROL`) and disables provider selection/credential creation for auxiliary capabilities (`openflux`, `ecc`). However, command operations permitted by `astra_github_agent.py` span a wide privileges list (`OPERATIONS`), requiring strict operation whitelist enforcement per node role.

### C. Path & Target Binding Risks
1. **Owned Paths Sanitization:** `read_command()` verifies that `owned_paths` contain no absolute paths or traversal sequences (`..`). However, worker checkout state and target SHA drift must be strictly synchronized (`_current_head().lower() == cmd["target_sha"].lower()`).
2. **Direct Git Push & Branch Separation:** The publish function executes:
   ```python
   git_network(["git","push","origin",f"HEAD:astra-node/{NODE_ID}"],120).check_returncode()
   ```
   This pushes worker results directly to remote result branches. The safeguard relies on branch isolation (`astra-node/{NODE_ID}`) rather than direct pushes to `main`. Concurrency and stale publisher race conditions are mitigated by failing closed if remote fetch/detach fails.

---

## 3. Test Coverage & Gap Analysis

- **Existing Tests:**
  - `tests/test_astra_command_auth.py`: Validates signature verification, expiration windows (`COMMAND_HMAC_MAX_AGE_SECONDS`), path safety (`_safe_id`), SHA shaping (`_valid_target_sha`), required command fields, and idempotent execution markers.
  - `tests/test_mesh_admission_boundary.py`: Validates node activation state, role requirements, execution authority checks, and auxiliary capability restriction.
- **Identified Test Gaps:**
  - Lack of negative fuzzing tests for malformed JSON payload structures exceeding memory bounds or containing nested dictionary injection.
  - Absence of concurrency race integration tests simulating simultaneous conflicting signed command dispatches across multiple nodes.

---

## 4. Safest Artifact-Only Publisher Separation

To maintain architectural integrity in Contour A:
1. **Artifact Isolation:** Workers publish strictly to isolated evidence/result branches (`astra-node/{NODE_ID}`) and never issue direct commits or merges to `main`.
2. **Secret Suppression:** All published telemetry and result payloads automatically scrub credentials (`"secret_values": "SUPPRESSED"`).
3. **Fail-Closed Execution:** Any network failure during fetch, checkout, or push aborts execution without modifying workspace state or compromising base branches.

---

## 5. Verification Status & Acceptance Criteria

- **Evidence Status:** Independent review completed against dispatch commit (`25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`).
- **Runtime Execution:** Unmodified (per agent mandate: do not modify runtime execution paths, invoke workers, use secrets, merge, or deploy).
- **Acceptance Criteria Met:** Threat-model analysis documented, trust-boundary gaps identified, publisher separation validated as artifact-only.
