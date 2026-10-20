# MediaHub OS — Wave 232 A1: Trusted Authorization Architecture Checkpoint

## Metadata
- **Contour:** Contour A (Developer Fabric)
- **Task ID / Wave:** Wave 232 A1 — Trusted Authorization Architecture
- **Base Ref:** `main`
- **Target Branch:** `contour-a/wave-232-a1-trusted-authorization-architecture`
- **Date:** October 20, 2026
- **Status:** Architecture Checkpoint / Draft PR

---

## Executive Summary
Wave 232 A1 defines the trusted authorization architecture for MediaHub OS Contour A. This checkpoint synthesizes empirical inspection of existing security contracts (`architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`), signed-command verification mechanisms (`astra_github_agent.py`), mesh admission boundaries (`ops/mesh/admission.py`, `tests/test_mesh_admission_boundary.py`), and distributed worker execution models (`tests/test_distributed_local_worker.py`). It establishes the formal architectural chain from authenticated issuer/workload identity through capability and policy evaluation to command binding, freshness, revocation, replay protection, and separately authorized publishing.

---

## 1. Inspected Artifacts & Current Facts
1. **Security / Trust / Authorization Contract (`architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md`)**:
   - **Status:** Proposed Architectural Baseline (SHA `8d831c2...`).
   - **Core Rule:** Security is a prerequisite to command execution, not an observer after mutation. No UI, AI, plugin, device, cloud service or integration may mutate canonical state without passing the same identity, trust, authorization and State Authority path.
   - **Trust Chain:** Boot/Runtime Trust Context -> authenticated principal -> device/workload identity -> capability and policy evaluation -> authorized command -> Consumer Contract -> State Authority.
   - **Invariants:** Default deny, least privilege, explicit capability/scope, pre-mutation resource/operation checks, revocation rejection, unknown device quarantine, fail-closed on ambiguity, audit production without secondary mutation authority.

2. **Signed-Command Verifier / Agent Transport (`astra_github_agent.py`)**:
   - **Status:** Implemented Transport & Verification Layer (SHA `dd2f373...`).
   - **Verification Mechanisms:**
     - HMAC-SHA256 signature verification over canonical JSON command payload (`_command_auth_valid`).
     - Freshness check (`COMMAND_HMAC_MAX_AGE_SECONDS`, default 900s).
     - Node identity binding (`NODE_ID` matching command `node_id`).
     - Command ID path safety (`_safe_id` regex validation preventing path traversal).
     - Target Git SHA strict validation (`_valid_target_sha`, 40-64 hex chars matching current head).
     - Idempotency via execution marker files (`EXECUTED_COMMANDS`).
     - State separation: consumed commands restored/cleaned to prevent dirty worktree side effects before branch publishing.

3. **Mesh Admission Boundary (`ops/mesh/admission.py` & `tests/test_mesh_admission_boundary.py`)**:
   - **Status:** Implemented Admission Engine (SHA `46e92d3...`).
   - **Rules:**
     - Nodes must have `ACTIVE` status and valid ID/role.
     - Capabilities must pass capability schema validation (`validate_capability`).
     - Executor admission strictly requires `EXECUTION` authority (Control authority rejected).
     - Auxiliary capabilities (`openflux`, `ecc`) cannot select providers, create credentials, or receive execution authority.
     - Qualification state must be `QUALIFIED` or `PASS`.

4. **Distributed Worker Model (`tests/test_distributed_local_worker.py`, `ops/qualification/run_distributed_local_worker.py`)**:
   - **Status:** Validated Execution Lanes (SHA `5fd79a6...`).
   - **Guarantees:**
     - Claude-only executor constraint in GitHub Actions workflow (`astra-distributed-local-worker.yml`).
     - Isolated config directories (`CLAUDE_CONFIG_DIR`, temporary home isolation).
     - Disabled reasoning effort for non-thinking local models (`REASONING_POLICY = "off"`, `CLAUDE_CODE_DISABLE_THINKING = "1"`, `MAX_THINKING_TOKENS = "0"`).
     - Strict path bounding and forbidden path checks (`scope_paths`).

---

## 2. Architectural Gap Analysis & Proposed Chain (Wave 232 A1)
To achieve a clean, reproducible Contour A system independent of legacy/current servers, the complete authorization chain from issuer to publisher is formally defined as follows:

```text
[1. Authenticated Issuer / Workload Identity]
    │ (mTLS / OIDC / Cryptographic Token / Node HMAC)
    ▼
[2. Cryptographic Command Binding & Enveloping]
    │ (Schema Version, Command ID, Target Git SHA, Owned Paths, Issued Timestamp)
    ▼
[3. Mesh Admission & Capability Evaluation]
    │ (Node Active Status, Role Check, Capability Registry, Qualification State, Least Privilege)
    ▼
[4. Policy Evaluation & Freshness / Replay Protection]
    │ (Default Deny, Max Age Expiration, Idempotency Marker / Executed Store, Path Safety)
    ▼
[5. Execution Isolation & Scope Enforcement]
    │ (Dedicated Worktree, Sandbox Mode, Bounded Owned Paths, Secret Suppression)
    ▼
[6. Separately Authorized Publisher]
    │ (Branch-Isolated Result Push: astra-node/<node_id>, Result JSON Payload, No State Mutation Authority)
```

### Key Distinctions (Existing Facts vs. Proposals)
- **Existing Facts:** HMAC signature validation, node identity binding, max age freshness, executed command idempotency markers, mesh admission constraints (`admit_executor`), and bounded worktree publish workflows are fully implemented and tested.
- **Proposals (Future Clean Contour A):** Transition from static node HMAC keys to dynamic, workload-scoped mTLS / cryptographic attestation tokens; decentralized capability issuance backed by cryptographic manifests; automated capability revocation lists distributed via the mesh transport.

---

## 3. Acceptance Criteria & Verification Status
1. **Authenticated Issuer / Workload Identity:** Verified via node binding and HMAC verification. (Status: Implemented & Tested)
2. **Capability & Policy Evaluation:** Verified via `admit_executor` and capability validation schemas. (Status: Implemented & Tested)
3. **Command Binding & Freshness:** Verified via target SHA matching and timestamp max age checks. (Status: Implemented & Tested)
4. **Replay Protection & Idempotency:** Verified via `.done` execution marker files. (Status: Implemented & Tested)
5. **Separately Authorized Publisher:** Verified via branch-isolated `astra-node/<node_id>` push without State Authority mutation privileges. (Status: Implemented & Tested)

---
- **Contour B Gate:** Maintained (Contour B product features remain strictly gated).
- **Verification Status:** Documentation and architecture checkpoint verified against repository state on `main`. No runtime code modified, no secrets used, no tests executed.
