# MediaHub OS — Contour A Pre-Deployment Readiness Work Breakdown, Draft 01

- Date: 2026-10-15
- Status: **PLANNING BASELINE / SOURCE-ONLY / NOT NORMATIVE / NOT AN ACCEPTANCE OR DEPLOYMENT AUTHORIZATION**
- Scope: break the next request into small, independently verifiable work packages and begin package 1.
- Immediate target: greenfield Contour A — Jarvis + ASTRA/Astra Gold + autonomous controllers + hybrid distributed development fabric. Contour B product development remains gated on Contour A deployment and independent acceptance.
- Ref state at pass start: `main` HEAD `608d7463011798ca75e36bfce4b749a9caf4f9a0`; docs branch `docs/mediahub-chat-tree-map-20261012` DIVERGED, 1360 ahead / 3 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No integration performed.

## 1. Work breakdown

Each package is a separate bounded `/next` pass. Dependencies must be rechecked against live sources before starting each package.

| ID | Work package | Required output / done condition | Current status / dependency |
|---|---|---|---|
| WB-01 | Target hardware/OS/topology evidence audit | Separate owner-confirmed target facts from assumptions; exact inventory fields and unresolved decisions recorded | **CURRENT PASS — source audit complete; owner-input blockers remain** |
| WB-02 | Contract and authority conflict register | Exact conflicting clauses, source refs/SHAs, approved decision and controlled disposition for each | Partially documented; refresh only where live evidence indicates gaps |
| WB-03 | Jarvis → ASTRA A0 ingress contract gap closure | Accepted protocol/version, identity, authentication, request/ack/error and replay semantics or explicit owner decision packet | BLOCKED: no accepted ingress edge |
| WB-04 | Capability issuer/delegation/revocation lifecycle | Issuer/verifier, audience, scope, expiry, attenuation, rotation, revocation and audit contract | BLOCKED: issuer lifecycle not accepted |
| WB-05 | Mission/task/DAG/result/evidence schema governance | Existing-ID crosswalk, producer/consumer closure, version/compatibility policy, approved wire schema | Draft only; not normative |
| WB-06 | Claim fencing, cancellation, idempotency and result publication | Accepted authoritative storage/fencing semantics, stale-worker rejection, race tables and publication contract | BLOCKED: wire/storage contract not accepted |
| WB-07 | Component admission and dependency/provenance gates | Candidate-by-candidate immutable source/artifact pins, license/SBOM/advisory, isolation, egress and interface fit | Ongoing source-only review; no install/runtime evaluation |
| WB-08 | Target deployment topology and placement plan | Service-to-node allocation, trust zones, network flows, resource envelope, recovery and rollback | Depends on WB-01 and owner decisions |
| WB-09 | Requirements-to-evidence and acceptance matrix | Each requirement linked to source contract, verification evidence, owner and gate | Partial artifacts exist; reconcile before claiming completeness |
| WB-10 | Architecture readiness review / deploy decision packet | Critical blockers, exact preconditions, risk/rollback and explicit go/no-go decision | Depends on WB-02…WB-09; no deployment authorization implied |

### Sequencing rules

1. WB-01 can proceed from repository documents without inspecting hosts or runtime.
2. Do not select authentication, token, issuer, hardware, or service placement technologies by inference.
3. WB-03/WB-04/WB-06 are hard blockers for safe autonomous mission dispatch and authoritative result handling.
4. Candidate admission does not imply selection, installation, runtime readiness or qualification.
5. Keep source design, implementation, testing, verification, qualification, release, deployment and independent acceptance as distinct states.
6. If a package requires owner-only input, record the precise question and continue independent source-only work rather than inventing an answer.

## 2. WB-01 — Target hardware/OS/topology evidence audit

### Sources re-read on the documentation branch

| Source | Blob SHA | Relevant source-backed finding |
|---|---|---|
| `docs/architecture/MEDIAHUB-GREENFIELD-LEGACY-ARTIFACT-LEDGER-WAVE-01-2026-10-15.md` | `f97d44567328633602cdc2ca52bcd0b20138e082` | §2 explicitly records the new hardware/OS/topology inventory as OPEN INPUT; no authoritative exact model, OS version, RAM/storage/network/GPU/accelerator or role-to-machine allocation. |
| `docs/checkpoints/MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md` | `59107fd6d7b8a73d671098adcf2824c310642907` | §§3–6 distinguish accepted target roles from unknown capabilities and unqualified placements. Mac Pro, legacy Mac mini Server 2011 and future GPU/video server have separate open evidence/decision gates. |
| `docs/architecture/MEDIAHUB-JARVIS-ASTRA-DISTRIBUTED-AI-CORPORATION-TARGET-ARCHITECTURE-WAVE-01-2026-10-15.md` | `c9f1716de8419d66f181fc0a9c465c65a81c7d5b` | §3 is a logical topology only; endpoints, protocols, actual capacity and runtime compatibility are not established. |
| `docs/checkpoints/MEDIAHUB-LOCAL-COMPONENT-INVENTORY-WAVE-01-2026-10-14.md` | `a89c31423e1af185261340b432cc770f4300e469` | Existing local inventory is explicitly bounded and does not establish a complete target hardware/runtime profile. |
| `docs/checkpoints/MEDIAHUB-UNIFIED-LOCAL-INVENTORY-AND-VERIFIABLE-COMPONENT-MATRIX-WAVE-02-2026-10-14.md` | `4d239780af2367fdecd00e7156521934ef2f8114` | Prior local inventory excludes hardware/thermal data and is not a full host/runtime inventory; it must not be promoted into a greenfield target profile. |

### Findings

- Confirmed target direction: design a new system for Mac Pro, Mac mini/server and a remote video server; do not reuse old-server installation attempts as target runtime evidence.
- The node/service placement register identifies historical names such as Mac Pro 2013 and Mac mini Server 2011 as target/legacy roles, but does not establish that they are the exact final assets for the newly confirmed target. Treat them as unresolved until owner confirmation.
- The future owned GPU/video server is optional and not selected; no exact model, GPU/VRAM, OS or runtime is recorded.
- The logical topology does not establish IPs, ports, endpoints, protocols, actual model performance, video capacity, or deployment readiness.
- No authoritative source reviewed here provides the complete exact hardware/OS/topology inventory. This is a documented input gap, not evidence that the hardware does not exist.

### Owner-input register (no answers inferred)

| ID | Required confirmation | Why it blocks | Current status |
|---|---|---|---|
| HW-01 | Exact Mac Pro model/year/chip, RAM, storage, network and OS/build | Capacity, compatibility and supported runtime cannot be inferred from “Mac Pro” | OPEN |
| HW-02 | Exact Mac mini/server model, architecture, RAM/storage, intended OS/build and support lifecycle | Must decide whether it is an optional low-risk worker or a critical dependency | OPEN |
| HW-03 | Remote video server ownership, exact hardware/GPU/VRAM, OS/runtime and intended workloads | Must not assume local/remote memory pooling or video-model capability | OPEN |
| HW-04 | Confirm node identities and role-to-machine allocation for Jarvis, A0/Astra Gold, controllers, executors, routing and evidence services | Needed for trust boundaries and placement; names alone are not a topology | OPEN |
| HW-05 | Confirm whether the future product/production Mac Pro is the same asset as the developer Mac Pro or a separate asset (DEC-DEV-03) | Prevents accidental identity/data/credential and trust-domain reuse | OPEN |
| HW-06 | Confirm whether Mac mini Server 2011 is still part of the new target or only a historical/optional worker (DEC-DEV-04) | Existing documents call it a low-resource/legacy candidate, not a proven modern build/model host | OPEN |
| HW-07 | Workload envelope for the optional GPU/video server before hardware selection (DEC-DEV-07) | Hardware selection should follow workload, privacy, capacity and isolation requirements | OPEN |

### WB-01 disposition

**Source audit complete; hardware-specific deployment planning remains BLOCKED on owner-confirmed facts.** Do not inspect hosts, collect runtime data, change infrastructure, choose hardware, or start installation under this pass. This work package does not change any accepted target decision.

## 3. Next bounded package

Proceed to **WB-02: contract and authority conflict register**, using live primary source clauses and owner-approved DEC-DEV-02 Option C. Record exact conflicts and current branch-specific SHAs; do not modify normative `main` sources or run tests. Keep WB-03, WB-04 and WB-06 as explicit hard blockers until accepted contracts and any required owner decisions exist.

## 4. Verification boundary

This pass used GitHub branch comparison and read-only source fetches. It did not inspect hosts/runtime, download artifacts, install packages, resolve dependencies, execute code/tests/scans, invoke models/providers, use credentials, qualify components, change infrastructure, deploy, merge, rebase or cherry-pick. This document is a planning aid, not an accepted normative architecture or deployment authorization.
