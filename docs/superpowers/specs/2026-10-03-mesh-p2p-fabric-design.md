# MediaHub Mesh / P2P Fabric Design

Date: 2026-10-03
Status: Approved design
Scope: MediaHub control mesh, executor admission, and content-addressed artifact distribution on mh-dev-01/mh-dev-02 and future nodes.

## Goal
Define a fail-closed Mesh control plane and P2P artifact plane without making BitTorrent/IPFS an authority layer and without coupling Mesh admission to Astra Gold qualification execution.

## Architecture
The system has four cooperating layers:
1. GitHub Transport — authenticated project/control transport.
2. Mesh Control Plane — node registry, capabilities, heartbeat, health and admission state.
3. Executor Fabric — Codex, Claude Code, FCC, Ollama, OmniRoute and other explicitly registered execution providers.
4. Artifact Fabric — content-addressed artifacts transported through BitTorrent and an IPFS/CID adapter.
GitHub Transport is not the artifact transport. BitTorrent/IPFS are not the control authority. Mesh state does not grant Astra Gold qualification.

## Node Registry
Every node record MUST contain: stable node_id; role; schema version; declared capabilities; executor inventory; artifact transport capabilities; resource profile; last heartbeat timestamp; current health/state; evidence references where applicable.
A node MUST NOT elevate its own authority by changing its local record.
Unknown or malformed node records are rejected.

## Capabilities
Capabilities are explicit declarations, not inferred from package installation.
A capability record identifies: capability name; provider/executable identity; version; execution path where applicable; immutable identity information when available; declared resource requirements; policy state.
Installation alone MUST NOT imply qualification or admission.
OpenFlux and ECC, once provenance is established, are auxiliary execution capabilities unless a later approved governance change explicitly grants another authority.

## Heartbeat
Heartbeat records MUST be authenticated by the existing control transport and contain: node_id; issued_at; sequence or monotonic marker; runtime state; capability summary; resource summary.
Stale, malformed or unverifiable heartbeats result in RECONCILIATION_REQUIRED or BLOCKED; they MUST NOT silently preserve active admission.

## Executor Admission
Admission follows: node identity -> role -> capability -> executable/provider identity -> policy -> current health.
Missing launcher, missing provider identity, authentication denial, policy denial or stale state results in fail-closed behavior.
Mesh admission does not bypass Astra Gold qualification gates.

## Artifact Registry
Every artifact MUST have a content identity independent of its transport.
Minimum fields: artifact_id; SHA-256; size; media/type classification; manifest metadata; origin; transport references; replica state; verification state.
The registry accepts an artifact only after hash and metadata validation.
Transport URLs, peers or CIDs are locators, not authorities.

## P2P Fabric
### BitTorrent
The existing Transmission tooling is the first transport adapter.
Required lifecycle: publish -> discover -> transfer -> hash verify -> registry admission -> replica state update.
An artifact failing verification MUST NOT become an admitted replica.

### IPFS
IPFS is an optional content-addressed transport adapter.
The implementation MUST treat CID resolution as transport/discovery and independently verify the artifact against the registry's cryptographic identity.
IPFS installation is not a prerequisite for Mesh Control Plane operation.

## Replication and Recovery
Replica state is explicit: DECLARED, TRANSFERRING, VERIFIED, AVAILABLE, STALE, FAILED, RECOVERY_REQUIRED.
Recovery MUST preserve the original artifact identity. A replacement replica must pass the same verification procedure.

## Failure Model
The system is fail-closed for: unknown nodes; stale or invalid heartbeat; missing capability identity; missing executable; authentication/policy denial; artifact hash mismatch; malformed manifests; unverifiable transport state.
Network loss MUST NOT create new authority.

## Security Boundaries
Secrets MUST remain outside committed evidence and manifests.
No component in this Mesh design may create credentials, self-promote qualification, modify Astra Gold gate results, convert installation state into qualification state, or treat historical evidence as fresh evidence.

## Resource Constraints
mh-dev-02 currently has a 16 GiB physical RAM profile. Mesh services MUST remain bounded and must not require multiple simultaneously loaded LLMs.
The artifact plane may use disk aggressively within the available disk budget, but downloads must remain bounded and observable.

## Qualification Boundary
This design does NOT launch G4, G4/115, or any autonomous qualification workflow.
Qualification remains governed by the existing Astra Gold launch schema and requires fresh evidence.

## Implementation Sequence
1. Canonical schemas for node, capability, heartbeat and artifact registry.
2. Pure validators and fail-closed state transitions.
3. Mesh registry integration with GitHub Transport.
4. Artifact registry and SHA-256 verification.
5. BitTorrent adapter.
6. IPFS adapter.
7. Replication/recovery state machine.
8. mh-dev-02 runtime integration.
9. Independent verification.
10. Only after all of the above, consider qualification integration as a separate task.

## Non-Goals
This design does not install arbitrary OpenFlux/ECC packages without provenance, replace GitHub Transport, make P2P the Mesh control plane, start Astra Gold qualification, or introduce a second authority database that conflicts with canonical project governance.
