# ASTRA GOLD — Unified Autonomous Development System

Status: CANONICAL / QUALIFICATION-READY DESIGN
Version: 1.0
Date: 2026-10-02
Scope: MediaHub OS / MediaHub iOS

## 1. Definition

**ASTRA GOLD is the complete distributed autonomous development system.**

It is not a name for Astra coordinator alone. ASTRA GOLD is the integrated control, execution, verification, transport, provider, evidence, recovery, queue, security and observability fabric used to develop MediaHub autonomously.

Qualification is therefore performed against the **whole system**, not against isolated components.

## 2. System topology

```
                         HUMAN AUTHORITY
                               |
                     architecture / release
                               |
                         ASTRA GOLD
                               |
        +----------------------+----------------------+
        |                      |                      |
   A0 ASTRA              Governance Plane       Evidence Plane
 coordination             policies/contracts     immutable-ish records
        |
   +----+----------------------+----------------+
   |                           |                |
 A1 Architect              A2 Builder       A3 Verifier
   |                           |                |
   +------------- task-scoped workers ---------+
                               |
                     AUTONOMOUS CONTROLLER
                               |
             +-----------------+-----------------+
             |                                   |
       Command / Claim Plane                Queue / State
             |                                   |
      +------+-------------------+---------------+
      |                          |
 Execution Fabric            GitHub Transport
      |
 +----+-------------------+------------------+
 |                        |                  |
Codex                  Claude Code        auxiliary
 |                        |               ECC/support
 +----------- transports / adapters -------+
              |                 |
             FCC            OmniRoute
              |                 |
        local execution nodes / isolated workspaces
              |
       tests / build / runtime
              |
       A3 independent verification
              |
        integration / reconciliation
              |
        canonical GitHub state
              |
       continuous controller loop
              |
        recovery / heartbeat / soak
```

## 3. Authority model

1. Human remains final authority for global architecture, production deployment, destructive changes, security-sensitive decisions and permanent governance changes.
2. A0 Astra is the single coordination authority.
3. A1 Architect owns architecture proposals, contracts and decision records within assigned scope.
4. A2 Builder performs bounded implementation.
5. A3 Verifier independently verifies integrated results.
6. Executor clients (Codex, Claude Code) have executor authority only.
7. FCC and OmniRoute are transport/routing mechanisms, not architecture or state authorities.
8. ECC is auxiliary support only; it has no provider-selection, credential-creation or state authority.
9. GitHub is the transport/evidence substrate, not MediaHub domain State Authority.
10. AI providers and cloud services never become MediaHub State Authority.

## 4. Component classes

### 4.1 Coordination
- A0 Astra
- mission decomposition
- scheduling
- claims
- conflict detection
- integration
- architecture reconciliation
- retry/recovery policy

### 4.2 Persistent role fabric
- A1 Architect
- A2 Builder
- A3 Verifier
- dynamic task-scoped instances
- bounded adaptive parallelism

### 4.3 Autonomous controller
- command ingestion
- command identity
- target SHA binding
- worker liveness
- claim leases
- queue advancement
- result publication
- restart/re-execution
- duplicate suppression
- failure classification
- recovery
- heartbeat

### 4.4 Execution fabric
Qualified executor identities:
- Codex
- Claude Code

Qualified execution paths:
- Codex via FCC
- Claude Code via FCC
- Codex via OmniRoute
- Claude Code via OmniRoute

Direct native launchers may be qualified as additional execution paths, but their qualification is separate from transport qualification and cannot be inferred from FCC/OmniRoute evidence.

### 4.5 Auxiliary intelligence
ECC is auxiliary local assistant support. It can assist with analysis where explicitly allowed, but it cannot:
- select providers;
- create credentials;
- mutate State Authority;
- bypass A3 verification;
- bypass qualification;
- redefine architecture.

### 4.6 Transport and persistence
- GitHub repository and branches
- command contracts
- claim/evidence records
- result records
- workflow execution
- artifact storage
- canonical branch reconciliation

### 4.7 Verification
- focused tests
- regression suite
- contract tests
- architecture conformance
- security boundary checks
- concurrency checks
- timeout/failure checks
- recovery checks
- independent A3 verification
- exact-SHA evidence

### 4.8 Observability and recovery
- structured logs
- health/heartbeat
- worker identity
- duplicate detection
- queue state
- evidence freshness
- timeout/retry state
- restart/recovery
- 24h soak
- failure injection

## 5. Core lifecycle

Every autonomous mission follows:

```
DISCOVER
  -> DECOMPOSE
  -> CLAIM
  -> EXECUTE
  -> VERIFY
  -> CONFLICT ANALYSIS
  -> INTEGRATE
  -> SYSTEM VERIFY
  -> ARCHITECTURE RECONCILIATION
  -> EVIDENCE COMMIT
  -> CLOSE
```

A mission is not complete because an executor reports success. Completion requires fresh observable evidence.

## 6. Unified ASTRA GOLD state machine

```
DESIGNED
  -> PREFLIGHT
  -> ADMITTED
  -> QUALIFICATION
  -> EXECUTION
  -> VERIFICATION
  -> INTEGRATION
  -> RECONCILIATION
  -> SOAK
  -> GOLD_ACTIVE

Any failed mandatory gate
  -> BLOCKED
  -> DIAGNOSE
  -> REPAIR
  -> PREFLIGHT
```

No state may transition to GOLD_ACTIVE using historical evidence.

## 7. Qualification model

Qualification is a system qualification.

### Gate G0 — identity
- canonical node identity
- runner identity
- repository identity
- exact source SHA
- clean worktree

### Gate G1 — control plane
- Astra coordinator
- command contract
- claim lease
- queue
- duplicate suppression
- result publication

### Gate G2 — executor fabric
For each Codex/Claude path:
- executable identity
- provider identity
- exact source SHA
- isolated workspace
- marker probe
- timeout
- malformed-result rejection
- nonzero exit handling

### Gate G3 — 23-wave qualification
Minimum 23 fresh rounds for every mandatory execution path.

Required paths:
1. Codex/FCC
2. Claude Code/FCC
3. Codex/OmniRoute
4. Claude Code/OmniRoute

A missing launcher is BLOCKED, not PASS.

### Gate G4 — concurrency
- maximum two concurrent autonomous claims by default
- disjoint write boundaries required
- shared surfaces serialized
- collision detection
- independent evidence

### Gate G5 — recovery
- executor timeout
- executor failure
- transport interruption
- stale claim
- worker restart
- duplicate controller
- replay/idempotency
- result publication after recovery

### Gate G6 — integrated verification
A3 verifies the complete integrated result independently of A0/A2 assertions.

### Gate G7 — pre-soak
All required evidence bundles must be fresh and PASS.

### Gate G8 — 24h GOLD soak
- canonical controller remains alive
- queue remains serviceable
- heartbeat remains fresh
- executor admission remains fail-closed
- recovery path remains functional
- no unauthorized authority transfer
- evidence remains publishable

### Gate G9 — GOLD_ACTIVE
Only after all mandatory gates have fresh evidence.

## 8. Evidence contract

Every qualification result must contain:
- schema version
- mission/command ID
- node ID
- controller identity
- executor identity
- provider identity
- exact source SHA
- start/end timestamps
- round number
- exit status
- timeout status
- marker status
- workspace identity
- mutation result
- verification result
- failure classification
- evidence references
- credential status = SUPPRESSED

Historical evidence cannot satisfy a fresh gate.

## 9. Fail-closed rules

The system MUST block when:
- launcher is missing;
- executable identity is ambiguous;
- provider identity is ambiguous;
- source SHA cannot be proven;
- workspace isolation cannot be proven;
- marker probe is absent;
- timeout cannot be enforced;
- malformed result is accepted;
- A3 evidence is missing;
- evidence is stale;
- transport state is uncertain;
- claim ownership is ambiguous;
- duplicate controller ownership exists.

## 10. Controller 24/7 contract

The autonomous controller is a continuously supervised state machine, not a single shell process.

Required properties:
- one canonical coordination owner;
- bounded worker concurrency;
- durable command identity;
- idempotent claim handling;
- heartbeat;
- liveness detection;
- restart/re-exec;
- stale-claim recovery;
- duplicate-worker prevention;
- queue advancement;
- evidence publication;
- fail-closed degradation;
- periodic integrated verification.

A scheduled GitHub workflow alone is not sufficient proof of a 24/7 controller. The controller itself must remain alive and produce fresh heartbeat/evidence records throughout the soak.

## 11. Security boundaries

- credentials never committed;
- credentials never emitted in evidence;
- executor cannot become architecture authority;
- transport cannot become state authority;
- cloud provider cannot bypass admission;
- ECC cannot create credentials;
- A2 cannot self-verify;
- A0 cannot self-certify a disputed implementation;
- A3 must remain independently verifiable;
- destructive/production actions require explicit human authorization.

## 12. Qualification result semantics

Only these top-level states are valid:

- PASS — every mandatory gate has fresh evidence.
- BLOCKED — required capability/evidence is unavailable.
- FAILED — a required test executed and failed.
- RECONCILIATION_REQUIRED — system state is uncertain.
- NOT_APPLICABLE — explicitly excluded by architecture contract.

There is no implicit PASS.

## 13. Canonical implementation boundary

ASTRA GOLD owns the autonomous development fabric.

MediaHub product domains remain separate:
- Media domain
- Document domain
- Digital Twin domain
- Smart Home domain
- Engineering domain
- Asset metadata
- UI/API
- persistence
- recovery
- update/release

ASTRA GOLD may develop and verify these domains but must never silently become their domain State Authority.

## 14. Target repository layout

```
.github/agent-system/       governance
.github/agents/             role profiles
.github/workflows/          controller and qualification automation
architecture/               canonical architecture
control/commands/           command contracts
control/claims/             claims
control/results/            execution results
control/qualification/      qualification contracts/evidence
ops/agent-fabric/           executor routing
ops/qualification/         qualification executors
runtime/                    autonomous runtime
evidence/                   fresh qualification evidence
tests/                      verification
```

## 15. Definition of ready

ASTRA GOLD is **qualification-ready** when:
1. the unified contract is committed;
2. all mandatory components have one canonical owner;
3. all executor paths are explicitly classified;
4. qualification gates are machine-readable;
5. the controller can ingest and publish commands/results;
6. 23-wave evidence can be generated fresh;
7. recovery tests are defined;
8. 24h soak is explicitly gated;
9. no component can silently acquire authority outside its role.

ASTRA GOLD is **GOLD_ACTIVE** only after actual execution proves those properties.

## 16. Current truth

As of 2026-10-02 the architecture is being normalized to this unified ASTRA GOLD definition.

The repository already contains substantial pieces: Astra coordination, A1/A2/A3 role contracts, autonomous queue, provider routing, qualification workflows, pre-soak/GOLD workflows, evidence contracts and recovery mechanisms.

The current runtime qualification is not yet PASS because the canonical GitHub Actions execution has been observed pending with no executing job, and fresh 23-wave executor evidence has not been produced.

This document therefore defines the target qualification surface; it does not convert unverified runtime behavior into PASS.
