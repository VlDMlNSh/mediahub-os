# MH-01 — Product / Governance / System Charter

**MediaHub OS 11.x LTS / MediaHub iOS**  
Status: **PROPOSED / REQUIRES VERIFICATION**  
Repository: `VlDMlNSh/mediahub-os`  
Canonical branch: `recovery/full-functional-spec`

## 1. Role

MH-01 is the normative root of the MH-01…MH-23 Master Reference Architecture. It defines product identity, mission, scope, authority, safety, governance, lifecycle and change-control constraints. It does not implement domain architecture.

## 2. Product identity

MediaHub OS is a local-first operating/runtime platform for management, integration, observation, automation and intelligent interaction with physical and digital media/device environments under explicit authority, authorization, safety and governance.

This formulation is **PROPOSED** until historical reconciliation is complete.

## 3. Frozen foundation

P0-03 State Authority Contract v1.0 — ACCEPTED / FROZEN.  
P0-04 In-Memory State Authority v1.0 — ACCEPTED / FROZEN.  
P0-05 Consumer / Integration Boundary — ACCEPTED / FROZEN.  
P0-06 Core Runtime Services — ACCEPTED / FROZEN.  
P0-07 Configuration / Policy — IMPLEMENTATION IN PROGRESS; production qualification not granted.

MH-01 cannot modify P0-03…P0-06. Any such change is a separate governance change.

## 4. Authority

State Authority is the sole canonical runtime mutation authority. UI, AI/LLM, agents, plugins, RAG, Knowledge Graph, Digital Twin, persistence, cache, cloud, external devices and monitoring are not canonical mutation authorities.

Canonical path:

`External Input → Integration Boundary → Consumer Contract → Capability/Command → Authorization/Policy → State Authority → Canonical Runtime State → Event → Observers/Diagnostics/UI/AI`

No alternative canonical mutation path is permitted.

## 5. Safety

`Hard Safety > Manual Emergency > Explicit Admin Policy > Local Automation > Optimization > Recommendation`.

AI confidence cannot override critical safety or authorization controls.

## 6. Local/cloud

Core functionality is local-first and offline-capable. Cloud is optional, external, policy-controlled and untrusted by default. Hybrid Local Cluster + external GPU/cloud is CANDIDATE, not frozen. Cloud cannot receive direct State Authority access.

## 7. Privacy/security

Default data posture is Local/Private. External transfer must be explicit, bounded, authorized, observable and auditable. Security baseline: least privilege, deny-by-default, explicit trust, identity-before-authorization, human/service separation, secrets never in source, audited critical actions, defense in depth, signed releases, verified recovery, isolated recovery privilege, secure failure.

## 8. Reliability

Current baseline: SINGLE NODE / NO HA. Backup or storage mirroring does not constitute HA. RTO/RPO and final HA model are UNKNOWN/TBD.

## 9. Trust

`Discovered → Untrusted → Verified → Enrolled → Configured → Active`.
Presence ≠ trust; trust ≠ authorization; authorization ≠ State Authority.

## 10. Data invariants

Command ≠ Event; Desired State ≠ Runtime State; Audit ≠ Domain Event; Knowledge ≠ Authority; Prediction ≠ Observation; Simulation ≠ Execution; Persistence ≠ State Authority; Cache ≠ Canonical State; AI Recommendation ≠ Authorization.

## 11. System boundary

Inside: runtime, state, policy, authorization, integrations, automation, UI, diagnostics, AI/knowledge, security, recovery and lifecycle. Outside: external devices, third-party platforms, external AI, cloud/Internet, external identity, storage and services. External systems do not become canonical by integration alone.

## 12. Lifecycle

Provisioning, initializing, self-test, ready, degraded, safe, recovery, maintenance, update and emergency are normative concepts. Exact semantics remain delegated to P0-04/P0-06 and downstream lifecycle architecture.

## 13. Governance

Evidence → Canonical State → Decision → Architecture → Implementation → Verification → Governance Acceptance → Freeze.

Documentation is not acceptance. Implementation is not qualification. Verification is not governance approval.

## 14. Architecture series

MH-01 is the normative root for MH-02…MH-23. The series is one architecture divided into domains, not 23 independent systems. Historical mapping remains PROPOSED where evidence is insufficient.

## 15. Development/chat separation

Architecture chats MH-01…MH-23 are canonical architecture custodians. They are not development workspaces. Production implementation, deployment and prolonged engineering discussion belong to separate development chats. Development chats may consume architecture through the current MH Master Prompt and may return findings through a Reverse Master Prompt/evidence package. Architecture changes must return through governance; development cannot silently rewrite architecture.

## 16. Status

MH-01 remains PROPOSED / REQUIRES VERIFICATION until its acceptance gate is satisfied and governance explicitly records ACCEPTED, followed by a separate FREEZE action.