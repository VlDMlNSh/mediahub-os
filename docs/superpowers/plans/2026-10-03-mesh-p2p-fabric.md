# MediaHub Mesh / P2P Fabric Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved fail-closed MediaHub Mesh control plane and content-addressed P2P artifact plane without changing Astra Gold qualification authority.

**Architecture:** Add focused Mesh schemas and pure validators under `architecture/mesh` and `ops/mesh`, integrate them with the existing GitHub Transport and agent registry, then add an artifact registry with BitTorrent and optional IPFS adapters. Keep transport separate from authority and keep OpenFlux/ECC qualification-gated.

**Tech Stack:** Python 3, JSON/YAML schemas, pytest/unittest patterns already used by the repository, SHA-256, existing GitHub Transport, Transmission 4.x, optional IPFS CLI/API adapter.

**Spec:** `docs/superpowers/specs/2026-10-03-mesh-p2p-fabric-design.md`

## Global Constraints

- Fail closed on unknown nodes, stale/invalid heartbeat, missing executable/provider identity, authentication/policy denial, malformed manifests, hash mismatch, and unverifiable transport state.
- Installation MUST NOT imply qualification or admission.
- BitTorrent/IPFS are transport/discovery layers, never authority.
- OpenFlux and ECC remain authority=`none`, provider selection=false, credential creation=false, state authority=false.
- Secrets MUST NOT enter manifests or committed evidence.
- Mesh admission MUST NOT bypass Astra Gold qualification gates.
- mh-dev-02 is bounded to its 16 GiB physical RAM profile and one simultaneously loaded LLM.
- G4/G4/115 and autonomous qualification are out of scope for this plan.

## Review Focus

- Schema drift between node/capability/heartbeat/artifact records — contract tests must reject incompatible versions.
- Replay/stale heartbeat — sequence and timestamp tests must force STALE/RECONCILIATION_REQUIRED.
- Transport substitution — artifact admission tests must verify SHA-256 independently of torrent/CID.
- Authority escalation — admission tests must reject self-promoted nodes/providers and OpenFlux/ECC authority changes.
- Partial recovery — replica tests must preserve artifact identity and reject unverified replacement data.

---

### Task 1: Canonical Mesh schemas

**Files:**
- Create: `architecture/mesh/node.schema.json`
- Create: `architecture/mesh/capability.schema.json`
- Create: `architecture/mesh/heartbeat.schema.json`
- Create: `architecture/mesh/artifact.schema.json`
- Test: `tests/schemas/test_mesh_schemas.py`

**Interfaces:**
- Produces versioned JSON Schemas consumed by Tasks 2–8.
- Schema identifiers must use the `mediahub.mesh.*.v1` family.

- [ ] Step 1: Write failing schema tests covering required fields, enums, and rejection of malformed records.
- [ ] Step 2: Run `pytest tests/schemas/test_mesh_schemas.py -v`; expected FAIL because the new schemas do not exist.
- [ ] Step 3: Implement the four schemas with exact states from the approved spec: node states `DISCOVERED, ACTIVE, STALE, BLOCKED, QUARANTINED, RETIRED`; replica states `DECLARED, TRANSFERRING, VERIFIED, AVAILABLE, STALE, FAILED, RECOVERY_REQUIRED`.
- [ ] Step 4: Run the focused test and the existing schema test suite; expected PASS.
- [ ] Step 5: Commit as `feat: add canonical mediahub mesh schemas`.

### Task 2: Pure validation and state transitions

**Files:**
- Create: `ops/mesh/__init__.py`
- Create: `ops/mesh/validators.py`
- Create: `ops/mesh/state.py`
- Test: `tests/test_mesh_validation.py`

**Interfaces:**
- `validate_node(record: dict) -> ValidationResult`
- `validate_capability(record: dict) -> ValidationResult`
- `validate_heartbeat(record: dict, now: datetime) -> ValidationResult`
- `transition_node_state(current: str, event: str) -> str`
- `transition_replica_state(current: str, event: str) -> str`

- [ ] Step 1: Write failing tests for unknown node, malformed capability, stale heartbeat, invalid state transition, and hash-verification prerequisite.
- [ ] Step 2: Run `pytest tests/test_mesh_validation.py -v`; expected FAIL.
- [ ] Step 3: Implement pure validation/state logic with no network or filesystem side effects.
- [ ] Step 4: Run focused tests; expected PASS.
- [ ] Step 5: Commit as `feat: add fail-closed mesh validation`.

### Task 3: Mesh registry and GitHub Transport integration

**Files:**
- Create: `ops/mesh/registry.py`
- Create: `ops/mesh/admission.py`
- Modify: `profiles/agent-registry.json` only where required to reference Mesh capability metadata.
- Test: `tests/test_mesh_registry.py`
- Test: `tests/test_mesh_admission.py`

**Interfaces:**
- `register_node(record: dict) -> RegistryResult`
- `record_heartbeat(record: dict, now: datetime) -> RegistryResult`
- `admit_executor(node: dict, capability: dict, policy: dict) -> AdmissionResult`

- [ ] Step 1: Write failing tests for duplicate node identity, self-promotion, missing executable, stale heartbeat, and valid admission.
- [ ] Step 2: Run the focused tests; expected FAIL.
- [ ] Step 3: Integrate with existing GitHub Transport conventions without creating a second authority database.
- [ ] Step 4: Add regression tests proving Mesh admission does not alter Astra Gold qualification state.
- [ ] Step 5: Run focused tests plus existing agent-fabric and qualification governance tests; expected PASS.
- [ ] Step 6: Commit as `feat: add mesh registry and admission`.

### Task 4: Artifact registry and cryptographic verification

**Files:**
- Create: `ops/mesh/artifacts.py`
- Test: `tests/test_mesh_artifacts.py`

**Interfaces:**
- `compute_sha256(path: Path) -> str`
- `validate_artifact_manifest(manifest: dict) -> ValidationResult`
- `verify_artifact(path: Path, expected_sha256: str) -> VerificationResult`
- `admit_verified_artifact(manifest: dict, verification: VerificationResult) -> RegistryResult`

- [ ] Step 1: Write failing tests for valid artifact, wrong hash, size mismatch, malformed manifest, and transport-only locator.
- [ ] Step 2: Run focused tests; expected FAIL.
- [ ] Step 3: Implement SHA-256 verification and admission only after verification.
- [ ] Step 4: Run focused tests; expected PASS.
- [ ] Step 5: Commit as `feat: add verified artifact registry`.

### Task 5: BitTorrent adapter

**Files:**
- Create: `ops/p2p/__init__.py`
- Create: `ops/p2p/torrent.py`
- Test: `tests/test_p2p_torrent.py`

**Interfaces:**
- `publish_torrent(artifact_path: Path, output_path: Path) -> TorrentMetadata`
- `inspect_torrent(torrent_path: Path) -> TorrentMetadata`
- `verify_download(path: Path, expected_sha256: str) -> VerificationResult`

- [ ] Step 1: Write failing tests using the existing deterministic qualification artifact pattern.
- [ ] Step 2: Run focused tests; expected FAIL.
- [ ] Step 3: Wrap the existing Transmission tooling without enabling the currently disabled daemon as a side effect.
- [ ] Step 4: Verify that a corrupted download never reaches `AVAILABLE`.
- [ ] Step 5: Run focused tests; expected PASS.
- [ ] Step 6: Commit as `feat: add bittorrent artifact adapter`.

### Task 6: IPFS adapter contract

**Files:**
- Create: `ops/p2p/ipfs.py`
- Test: `tests/test_p2p_ipfs.py`

**Interfaces:**
- `resolve_cid(cid: str) -> TransportReference`
- `fetch_cid(cid: str, destination: Path) -> Path`
- `verify_cid_artifact(path: Path, expected_sha256: str) -> VerificationResult`

- [ ] Step 1: Write tests using a fake transport provider; no live IPFS daemon required.
- [ ] Step 2: Run focused tests; expected FAIL.
- [ ] Step 3: Implement an adapter boundary that treats CID as a locator and always performs independent SHA-256 verification.
- [ ] Step 4: Add an explicit `ipfs_available()` capability probe returning unavailable when the binary/service is absent.
- [ ] Step 5: Run focused tests; expected PASS.
- [ ] Step 6: Commit as `feat: add ipfs artifact adapter contract`.

### Task 7: Replication and recovery state machine

**Files:**
- Create: `ops/p2p/replication.py`
- Test: `tests/test_p2p_replication.py`

**Interfaces:**
- `plan_replication(artifact: dict, replicas: list[dict]) -> ReplicationPlan`
- `mark_replica_event(artifact: dict, replica_id: str, event: str) -> dict`
- `plan_recovery(artifact: dict, replicas: list[dict]) -> RecoveryPlan`

- [ ] Step 1: Write failing tests for first replica, lost replica, corrupt replacement, network loss, and no-source recovery.
- [ ] Step 2: Run focused tests; expected FAIL.
- [ ] Step 3: Implement deterministic transitions preserving the original artifact SHA-256.
- [ ] Step 4: Run focused tests; expected PASS.
- [ ] Step 5: Commit as `feat: add artifact replication recovery state machine`.

### Task 8: Node 02 runtime integration

**Files:**
- Create: `ops/systemd/mediahub-mesh.service` only after runtime behavior is implemented and tested.
- Create: `ops/systemd/mediahub-mesh.env.example`
- Create: `ops/node/mh-dev-02-mesh-check.sh`
- Test: `tests/test_mesh_runtime_contract.py`

**Interfaces:**
- Runtime must read `/etc/mediahub/node-profile.env`.
- Runtime must remain non-authoritative and fail closed.

- [ ] Step 1: Add offline runtime-contract tests; no installation is assumed.
- [ ] Step 2: Prepare a terminal installation/verification packet for mh-dev-02.
- [ ] Step 3: On mh-dev-02, install only provenance-approved dependencies; do not install OpenFlux/ECC until their identity is verified.
- [ ] Step 4: Verify Ollama, OmniRoute, Codex, Claude Code, FCC, bwrap, llama.cpp and local execution paths without starting Astra Gold qualification.
- [ ] Step 5: Install IPFS only if the adapter is ready and disk/resource policy permits it.
- [ ] Step 6: Enable Mesh service only after offline contract tests pass and runtime smoke evidence is collected.
- [ ] Step 7: Commit runtime integration separately from host installation evidence.

### Task 9: OpenFlux/ECC provenance gate

**Files:**
- Modify: `profiles/agent-registry.json` only with verified source/version/identity fields.
- Test: `tests/test_openflux_registry.py`
- Test: add `tests/test_ecc_registry.py`

- [ ] Step 1: Verify upstream repository, release/commit, package identity and installation method for OpenFlux and ECC.
- [ ] Step 2: If provenance cannot be independently established, keep both uninstalled and mark them `NOT_PROVEN`.
- [ ] Step 3: If provenance is established, add immutable identity fields without granting authority.
- [ ] Step 4: Install on mh-dev-02 only after explicit runtime provenance evidence.
- [ ] Step 5: Run registry and authority-boundary tests; expected PASS with authority still `none`.

### Task 10: Independent verification and handoff

**Files:**
- Create: `ops/mesh/verify_mesh.py`
- Create: `tests/test_mesh_verification.py`
- Create: `docs/superpowers/verification/2026-10-03-mesh-p2p-fabric.md`

- [ ] Step 1: Write verification tests for all five Review Focus failure classes.
- [ ] Step 2: Run the full focused Mesh/P2P suite.
- [ ] Step 3: Run the existing repository governance, schema, agent-fabric and qualification tests affected by the changes.
- [ ] Step 4: Verify that no qualification workflow was started.
- [ ] Step 5: Record only fresh evidence; do not reuse historical PASS claims.
- [ ] Step 6: Commit verification artifacts separately.

## Self-Review

Coverage check:
- Node schema/state: Task 1 and Task 2.
- Capability identity/admission: Tasks 1–3 and Task 9.
- Authenticated/stale heartbeat: Tasks 1–3.
- Artifact SHA-256 admission: Task 4.
- BitTorrent: Task 5.
- IPFS/CID adapter: Task 6.
- Replication/recovery: Task 7.
- mh-dev-02 integration/resource boundary: Task 8.
- OpenFlux/ECC provenance and authority boundary: Task 9.
- Independent verification and Astra Gold boundary: Task 10.

Type/interface check:
- Validators consume Task 1 schemas.
- Registry consumes validators.
- Artifact adapters consume artifact verification.
- Replication consumes artifact/transport state.
- Runtime consumes all prior contracts but does not create authority.
- Verification consumes all public contracts without changing state.

Review-focus coverage:
- Schema drift → Task 1 tests.
- Replay/stale heartbeat → Tasks 2–3.
- Transport substitution → Tasks 4–6.
- Authority escalation → Tasks 3 and 9.
- Partial recovery → Task 7.

No task launches Astra Gold qualification.

## Execution Handoff

The repository design is approved. Implementation itself is intentionally not started by this plan document. Execution requires a chosen implementation mode and fresh repository checkout state before code changes.
