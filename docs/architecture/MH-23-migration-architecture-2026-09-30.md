# MH-23 — Migration Architecture — Etalon Baseline

Status: RECONCILED / ETALON ARCHITECTURE CANDIDATE
Qualification: QUEUED FOR INDEPENDENT AUTONOMOUS QUALIFICATION
Production: NOT AUTHORIZED
Repository: VlDMlNSh/mediahub-os
Target branch: engineering/mh21-sandbox-lifecycle-20260910
Immutable R4 baseline: 471f709f5633feab7aeb62dd3ea52effad6d2bc4

## 1. Purpose and boundary

Migration is a system control-plane capability that moves or transforms MediaHub system state between qualified source and target states.

Migration is NOT:
- State Authority
- Identity Provider
- Policy Authority
- Smart Home Authority
- AI Authority
- Data Authority
- Cloud Authority
- Security bypass
- qualification authority
- production/release authority

Migration coordinates domain authorities through versioned contracts. It never becomes the canonical writer for another domain.

Core invariant:

No Verified Target -> No Destructive Source Cleanup.

## 2. Canonical lifecycle

SOURCE_STATE
-> PREFLIGHT
-> MIGRATION_PLAN
-> COMPATIBILITY_VALIDATION
-> CHECKPOINT
-> TRANSFER_TRANSFORM
-> TARGET_VALIDATION
-> TARGET_QUALIFICATION
-> READY_FOR_CUTOVER
-> CUTOVER
-> POST_CUTOVER_VERIFICATION
-> ACCEPTANCE
-> SOURCE_RETIREMENT

Terminal/interruption states:
BLOCKED, PAUSED, FAILED, ABORTED, ROLLBACK_REQUIRED, ROLLING_BACK,
RECOVERY_REQUIRED, QUARANTINED, REQUIRES_REQUALIFICATION, COMPLETED.

Transitions are deterministic, authorized, journaled, idempotent and observable.

## 3. Migration Manifest

Every migration has a versioned, integrity-protected Manifest containing:
- migration ID;
- source/target identity and versions;
- source/target capability profiles;
- platform and topology;
- data classes, volumes and object sets;
- dependencies and contract versions;
- adapters;
- resource requirements;
- security/privacy/residency/egress constraints;
- backup and recovery point;
- checkpoint strategy;
- rollback strategy;
- cutover preconditions;
- qualification criteria;
- acceptance criteria;
- provenance;
- actor/automation identity;
- timestamps.

Manifest is a plan/evidence object, not authorization.

## 4. Orchestrator and workers

Migration Orchestrator owns:
plan construction, dependency graph, sequencing, checkpoints, retries,
pause/resume, evidence aggregation and report generation.

It does not own domain truth.

Workers are capability-scoped, identity-bound, least-privileged, resumable,
idempotent and auditable:
State, Storage, DB, Identity, Device, Smart Home, Media, Document,
Knowledge, Twin, Engineering, Network, AI/Model, Cluster, Cloud.

Workers mutate domain state only through canonical domain APIs/contracts.

## 5. Dependency graph

Minimum safe order:

Identity/Trust
-> Target Hardware
-> Platform
-> Storage
-> State Authority
-> Core Services
-> Configuration/Policy
-> Network/Devices
-> Smart Home
-> Documents/Media/Knowledge/Twin/Engineering
-> AI/Models
-> UI/Remote Access
-> Final Qualification
-> Cutover.

Optimization is allowed only if authority, dependency and safety invariants remain proven.

## 6. Mandatory preflight

Preflight must verify:
identity, trust, authorization, target identity;
hardware/software/API/event compatibility;
storage/network/HIGH_SPEED/resource capacity;
thermal/power constraints;
backup/restore;
State Authority topology and consistency;
cluster semantics;
Smart Home ownership;
database/storage integrity;
AI/model/plugin/protocol compatibility;
policy;
security;
privacy/residency/egress;
rollback and recovery paths.

Critical failure => BLOCKED. No automatic continuation.

## 7. State Authority migration

State Authority migration uses a dedicated protocol.

Required:
authority epoch;
source/target identity;
journal/sequence/version continuity;
checkpoint;
replication consistency;
quorum/leadership semantics;
split-brain prevention;
cutover fencing;
rollback/recovery evidence.

Before cutover, target is not an independent canonical writer.
After cutover, source authority is fenced and target authority becomes canonical
through the existing State Authority protocol.

No last-write-wins for critical canonical state.
Copying a database is not completion.

## 8. Identity and trust

User, node, service, workload, device, cryptographic and cluster identities
remain distinct.

Copying key material is not identity migration.

Each identity is classified as:
transferable, re-enrollable, rotatable, revocable, hardware-bound or
platform-bound.

Hardware-bound identity migration:
re-enrollment -> new attestation -> trust re-establishment -> policy admission.

Ordinary migration artifacts contain no long-lived secrets.

## 9. Data and storage semantics

For each data class explicitly select:
COPY, TRANSFORM, REBUILD, REINDEX, RECALCULATE or REQUALIFY.

State Authority:
transactional state, journal, history, provenance, replication metadata.

Documents:
files, metadata, full-text/semantic indexes, provenance.

Media:
assets, metadata, artwork, indexes, playback state, rights metadata,
thumbnails and transcode cache.

Knowledge Graph:
entities, relationships, provenance, temporal validity, confidence and references.

Digital Twin:
geometry, coordinates, units, object identity, topology and engineering relations.

Engineering:
projects, models, calculations, drawings, configurations and metadata.

Configuration/Policy:
version, provenance, effective time and state.

Derived data should normally be rebuilt rather than transferred when safe.

## 10. Database/schema migration

Schema changes require:
versioning;
compatibility windows;
expand/contract where applicable;
transactional boundaries;
resumable checkpoints;
integrity validation;
index migration/rebuild;
rollback/recovery point.

No destructive schema transformation without a verified recovery point.

## 11. API and event contracts

Migration preserves:
API versions;
event schemas;
compatibility windows;
deprecation rules;
adapters;
replay semantics;
idempotency;
correlation IDs;
schema transforms.

Rolling migration uses old/new contracts through a compatibility layer.
Old contracts are retired only after dependent consumers are removed or migrated.

## 12. Smart Home and device/protocol migration

Canonical device identity, ownership, HA ownership, mappings,
automations, scenes, schedules, desired/observed state and safety policies
must be preserved.

Target HA takeover:
discovery -> identity correlation -> capability validation ->
qualification -> policy admission -> ownership cutover.

Duplicate ownership, stale state and partitioned source/target conditions
are explicit failure states.

Protocol migration requires identity correlation, adapter qualification,
capability validation and policy re-evaluation. Vendor/model equality alone
does not prove compatibility.

## 13. Media, documents, knowledge, twin and engineering

Media migration preserves library/filesystem semantics, metadata, indexes,
codec capability, playback state and rights constraints.

Documents preserve file identity, metadata, extracted/derived indexes and provenance.

Knowledge Graph preserves entity IDs, relationship provenance, temporal validity,
confidence and authority references. Similar names never imply automatic merge.

Digital Twin and Engineering migration preserves coordinate systems, units,
geometry, topology, object identity, equipment references and version/project state.

Twin reference is not physical device identity.

## 14. AI and models

Migration may transfer:
model registry references, metadata, provenance, runtime configuration,
tokenizer/runtime compatibility, quantization, accelerator requirements,
benchmarks, safety/policy metadata and qualification evidence.

Required sequence:
integrity -> runtime compatibility -> benchmark -> security ->
qualification -> canary -> admission.

AI gains no new authority through migration.

## 15. Network and HIGH_SPEED fabric

Migration covers gateway/router/firewall/DHCP/DNS/VPN/VLAN/routing/QoS,
remote access and management paths.

Before critical cutover, preserve:
management path;
State Authority path;
recovery path;
observability path.

HIGH_SPEED/Thunderbolt migration preserves topology, interface identity,
link capability, bandwidth/latency, redundancy, storage/compute paths,
resource leases and scheduler topology.

Do not assume coherent shared memory merely from Thunderbolt/USB4.
Distributed-memory semantics remain unless separately qualified.

## 16. Resource management

Migration itself is a governed workload.

Target Resource Profile is recomputed from target CPU/GPU/NPU/RAM/NVMe/HDD,
network, HIGH_SPEED, accelerator, thermal, power, bandwidth and latency.

Section 24 Resource Management remains canonical.

Use reservations, leases, throttling, priority, bandwidth limits and
checkpointing. Migration must not silently evict critical workloads.

## 17. Backup, checkpoint and recovery

Before destructive or hard-to-reverse stages:
verified recovery point -> integrity check -> provenance -> key availability ->
restore path -> restore test by criticality -> checkpoint.

An unrestorable backup is insufficient.

Large transfers are checkpointed and resumable.
Committed operations are idempotent.

Rollback is qualified in advance.

Post-cutover rollback is not a blind restore of old state over changed canonical
state; it uses journal/version/recovery-point/reverse-migration semantics and
requires revalidation.

## 18. Dual-run and cutover

Permitted techniques:
dual-read, shadow execution, parallel validation, replicated target,
comparison and canary.

Forbidden:
two canonical State Authority writers.

Cutover requires:
verified backup;
healthy source/target;
target qualification;
contract compatibility;
valid identities/policies;
storage integrity;
authority consistency;
recovery path.

Cutover is explicit, timestamped, fenced, audited and observable.

## 19. Security and privacy

Security boundary:
Identity -> Capability -> Policy -> Scope -> Resource -> Action -> Audit.

Use least privilege, JIT authorization, short-lived credentials,
encrypted transport/artifacts, protected key storage, replay protection,
integrity and provenance.

Worker privileges expire with their lease.

Privacy boundary:
classification -> destination -> egress policy -> authorization ->
encryption -> audit.

Developer Cloud / Developer Compute Fabric must not receive MediaHub user data
and is not migration staging, backup, debug mirror or qualification sink.

Qualification uses synthetic, sanitized or otherwise explicitly approved
non-user fixtures.

Cloud remains external/supporting and never becomes canonical authority.

## 20. Observability and audit

Migration emits versioned events:
migration.created
migration.preflight.started
migration.preflight.failed
migration.backup.verified
migration.checkpoint.created
migration.transfer.started
migration.transfer.completed
migration.validation.started
migration.validation.failed
migration.qualification.started
migration.qualification.failed
migration.cutover.started
migration.cutover.completed
migration.rollback.started
migration.rollback.completed
migration.recovery.started
migration.completed
migration.source.retired

Every event carries migration ID, correlation ID, actor, source, target,
timestamp, state and provenance.

Audit records initiator, identities, source/target, versions, data classes,
policies, checkpoints, transformations, failures, approvals, cutover,
authority epoch, result and source-retirement evidence.

## 21. Qualification

Migration qualification uses MH-22 levels:
L0 Unqualified
L1 Structural
L2 Functional
L3 Integration
L4 Failure/Recovery
L5 Production Candidate
L6 Production Qualified

Migration qualification evidence is part of the Qualification Report.

Qualification is distinct from authorization.

Production gate:
Identity -> Hardware -> Platform -> Software -> Security -> Privacy ->
Capability -> Integration -> Failure -> Recovery -> Migration Qualification ->
Policy Admission -> Cutover.

## 22. Failure injection minimum

Verify detection, containment, pause/abort, recovery, resume/rollback and
requalification for:
node failure, network loss, storage failure, power loss, process crash,
partial transfer, corruption, insufficient capacity, capability mismatch,
API/event incompatibility, identity failure, credential expiry, policy denial,
State Authority partition/split brain, HA ownership conflict, protocol drift,
AI runtime incompatibility and backup-restore failure.

## 23. Compatibility matrix

Compatibility is multidimensional:
source/target version;
OS/platform;
hardware/capability profile;
State Authority;
DB schema;
API/event contracts;
Smart Home/devices/protocols;
AI/runtime/models;
Media/Documents/KG/Twin/Engineering;
Storage/Network/HIGH_SPEED;
Resource Profile;
backup/recovery.

Version equality alone never proves compatibility.

## 24. Idempotency and transformation rules

Every migration has stable:
migration ID, object IDs, operation IDs, idempotency keys, checkpoints
and commit markers.

Allowed transformation classes:
Copy, Move, Transform, Normalize, Rebuild, Reindex, Recalculate,
Reconcile, Requalify.

No transformation without a versioned schema/rule, deterministic semantics,
validation and provenance.

Irreversible transformation requires a verified recovery point.

## 25. Source retirement

Only after:
target accepted;
post-cutover verification passed;
stability window passed;
recovery point confirmed;
retention/policy conditions satisfied.

Cleanup is a separate controlled, audited action and is reversible where possible.

## 26. UX contract

The UI exposes:
what is migrating;
why;
current state/stage;
progress;
impact;
limitations/degradation;
completion;
problems;
next actions.

Explicit user confirmation is required when ownership, security boundary,
data destination, destructive action, critical operational state,
irreversible policy or major capability loss changes.

## 27. Legacy and scale

Legacy adapters are temporary compatibility boundaries with explicit sunset,
security scope and requalification requirements.

No permanent security/policy bypass through legacy.

Architecture supports single-node through large-cluster migration without a
fixed artificial maximum. Actual limits are topology, resources, bandwidth,
storage, latency, policy and safety constraints.

## 28. Required qualification blueprint

W0 exact branch/commit/tree/R4 ancestry
W1 architecture and authority reconciliation MH-01..MH-22
W2 manifest/schema/state-machine verification
W3 identity/trust/security
W4 privacy/data classification/Developer Cloud isolation
W5 State Authority/HA/split-brain/cutover
W6 storage/DB/schema/API/event compatibility
W7 device/protocol/Smart Home/media/documents/KG/twin/engineering
W8 AI/model/runtime qualification
W9 network/HIGH_SPEED/resource management
W10 backup/checkpoint/recovery/rollback
W11 failure injection and negative forbidden-path verification
W12 observability/audit/provenance
W13 performance/scale/minimal-downtime behavior
W14 source-retirement safety
W15 independent cross-MH contradiction scan
W16 final evidence reconciliation and disposition

Hard rule:
Architecture text is not implementation evidence.
Every result binds to exact revision and environment.
UNKNOWN remains UNKNOWN.
Missing or contradictory evidence blocks QUALIFIED.

## 29. Acceptance criteria

Architecture is eligible for independent qualification when:
- no migration authority conflict exists;
- all required domain boundaries are explicit;
- State Authority remains sole canonical mutation authority;
- no two canonical writers are permitted;
- Developer Cloud user-data path is denied by architecture;
- identity and trust migration semantics are explicit;
- data-class transformation semantics are explicit;
- backup/checkpoint/rollback semantics are explicit;
- cutover and source-retirement gates are explicit;
- API/event compatibility is explicit;
- Smart Home/device/protocol/AI/media/KG/twin boundaries are explicit;
- resource management is canonical and migration is a governed workload;
- observability/audit/provenance are explicit;
- qualification and production authorization are separate;
- no destructive Git history operation is required.

## 30. Governance disposition

This document is the canonical MH-23 architecture artifact for the current
qualification target.

It does not authorize implementation, merge, release or production.

Qualification transition:
RECONCILED -> VERIFIED -> QUALIFIED.

No historical R4 object is modified.
Erroneous/stale GitHub records are neutralized by explicit supersession/closure,
never by history rewrite.

