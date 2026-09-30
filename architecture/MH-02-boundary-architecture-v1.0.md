# MH-02 — Архитектура границ системы

**Status:** QUALIFIED FOR ARCHITECTURAL CHECKPOINT  
**Scope:** logical system boundaries and cross-boundary authority/contracts  
**Product:** MediaHub OS / MediaHub iOS  
**Branch:** `architecture/mh02-boundaries-20260930`  
**Provenance base:** Section 4 checkpoint commit `863e61783272e0107ce74ab1620212285946aca8`  
**R4:** `471f709f5633feab7aeb62dd3ea52effad6d2bc4` (confirmed as an ancestor by GitHub comparison)

## 1. Canonical boundary model

MediaHub is one logical platform architecture over heterogeneous qualified hardware.

```
USER DOMAIN
  State Authority
  Security / Identity / Trust
  Policy / Configuration
  Runtime / Core Services
  Smart Home / HA
  Media / Documents / Knowledge
  AI / Digital Twin / Engineering
  Network / Devices / Storage / Observability
        |
        | governed contracts + authorization + policy
        v
BOUNDARY / EGRESS CONTROL
        |
        +--> Developer Domain
        |      Developer Fabric / CI / corporate data / cloud development
        |
        +--> External Systems
        |      adapters / validation / qualification / admission
        |
        +--> Internet / Cloud
               controlled, non-authoritative
```

A logical domain is not a deployment unit. A domain may span processes/nodes; multiple domains may share a node. Placement is determined by qualification, resource, criticality, security, topology, latency, reliability, policy and lifecycle.

## 2. Authority model

| Boundary/domain | Canonical authority | Allowed mutation | Forbidden authority |
|---|---|---|---|
| Platform | MediaHub State Authority | governed canonical platform state | any second platform authority |
| Smart Home | Home Assistant Core | operational Smart Home state and automation | MediaHub/AI/cloud direct device mutation |
| Security | Security/Identity/Trust control plane | identity/trust/authz decisions within its contract | replacing State Authority |
| Policy | Policy/Configuration authority | policy/configuration publication | direct execution authority |
| AI | none | proposals/requests through governed path | direct State Authority/HA mutation |
| UI/Mobile Remote | none | requests via Public API | direct internal service mutation |
| Media/Documents/Knowledge/Engineering | domain authority | domain-owned state/data | platform-wide canonical authority |
| Observability | none | telemetry/evidence only | canonical mutation |
| Storage/Persistence | none by storage alone | domain persistence | becoming canonical merely by holding a copy |
| Developer Fabric | none over User Domain | developer-domain workloads | User Data / State Authority access |
| Cloud Development | none over User Domain | approved corporate development workloads | user-data or platform-state authority |
| External systems | external authority only inside their own system | adapter-mediated integration | unrestricted admission into MediaHub |

## 3. Canonical mutation path

For platform state:

`Input → Identity → Authorization → Policy → Contract Validation → State Authority → Canonical State → Event → Observation → Evidence`

For Smart Home:

`Input/AI/Workflow → Identity → Authorization/Policy → Smart Home Contract → HA Core → Device → Observation`

AI, cloud, UI, telemetry, recovery, plugins and external adapters are never alternate mutation authorities.

## 4. Trust boundaries

1. **User Trust Domain** — authenticated users and explicitly authorized operators.
2. **System Trust Domain** — qualified MediaHub runtime and State Authority.
3. **Device Trust Domain** — discovered devices remain untrusted until identity, qualification, capability and policy admission.
4. **Developer Trust Domain** — corporate engineering infrastructure, isolated from User Domain.
5. **Cloud Development Trust Domain** — controlled external compute; non-authoritative.
6. **External Trust Domain** — third-party systems accessed only through adapters/contracts.
7. **Unknown/Quarantine Domain** — default state for unknown or ambiguous components.

Discovery, network visibility, physical connection, health or readiness never establish authorization.

## 5. Data boundaries

| Data class | Default residency | Cross-boundary rule |
|---|---|---|
| User Data | User Domain | explicit classification + authorization + policy + residency + egress + audit |
| System State | State Authority | never exported as an uncontrolled canonical copy |
| Domain Data | owning domain | contract-scoped access |
| Security Data | Security boundary | least privilege; no developer/cloud leakage |
| Developer Data | Developer Domain | may enter approved cloud development paths |
| Cloud Development Data | Cloud Development Domain | corporate/approved engineering data only |
| Telemetry | Observability Domain | observational; policy-controlled export; never canonical by itself |

Developer Cloud receives no user documents, photos, video, Smart Home data, cameras, user logs, personal data, secrets, State Authority, user storage or user AI memory.

## 6. Deployment boundary model

`Logical Domain → Service → Process → Node → Cluster → Cloud Environment → Mobile Application`

These are separate architectural dimensions.

Supported profiles are implementations of one architecture:

`Unified Architecture → Unified Contracts → Hardware Qualification → Capability Profile → Platform Execution`

Mac mini, mini-PC, Raspberry Pi and iPad are not separate architectures.

iPad can be a qualified local MediaHub node. iPhone/Android Remote Access are remote applications and are not MediaHub Core nodes.

## 7. Network and compute boundaries

User Network and Developer/Compute Fabric are distinct trust/data planes.

Thunderbolt/USB4/high-speed IP are transport mechanisms. They do not imply hardware-coherent shared RAM. A distributed memory abstraction is allowed only where the qualified platform supports the required semantics.

Internet ingress is a cluster resource, not permanent ownership of one node. Primary Development Node is a dynamic role selected by workload and qualified capacity; it is not a permanent authority or SPOF.

CPRG is registration-only:

`Request → Authentication → Policy → Lease → Protected Registration → Verification → Close`

CPRG is not a general proxy, NAT, compute node, storage node or data-plane tunnel.

## 8. Mobile and UI boundaries

MediaHub iOS/iPadOS Core and MediaHub Remote Access remain separate applications.

- iPad Core: local qualified MediaHub node.
- iPhone/Android Remote: remote access only.
- Remote clients use Public MediaHub API + versioned contracts + authorization/policy.
- UI never calls internal domain services directly.

Canonical UI path:

`UI → Public API → Domain Contract → Authorization/Policy → Authority`

## 9. AI boundary

AI is proposal-generating and advisory/non-authoritative.

`User/Event → AI → Proposal/Request → Identity → Authorization → Policy → Contract → Authority → Execution → Observation`

For Smart Home, HA Core remains the final Smart Home execution authority.

Cloud Development AI follows:

`User MediaHub Domain → Security/Egress Gateway → AI Gateway → Cloud Development Domain`

The path is fail-closed and data-minimized. Cloud never becomes platform authority.

## 10. External integration boundary

Every external integration follows:

`External System → Contract → Adapter → Validation → Qualification → Policy Admission`

No unknown OSS, protocol, API, vendor system or device receives unrestricted internal access.

Unknown device state is **DENY/QUARANTINE** until:

`Discovery → Identity → Qualification → Capability → Policy → Admission`

## 11. Failure and recovery boundaries

Every boundary defines:

- normal path;
- degraded path;
- failure detection;
- containment;
- fallback;
- recovery;
- reconciliation;
- audit.

Optional-domain failure must not collapse the entire platform.

Local-first means qualified local operation does not depend on Internet or Cloud. Cloud loss must not transfer authority to an unqualified fallback. Recovery sources are verified durable State Authority state plus qualified journal/provenance and domain recovery state; cache, AI, UI or cloud copies cannot silently become authority.

## 12. Forbidden cross-boundary paths

- AI → direct State Authority mutation.
- AI → direct Smart Home device bypassing HA Core.
- Cloud → direct State Authority mutation.
- Developer Domain → User Data.
- Developer Domain → User State Authority.
- Cloud Development → User Data.
- UI → internal domain-service mutation.
- Remote Mobile → direct internal service access.
- Unknown Device → production admission.
- Discovery → implicit trust.
- Physical connectivity → implicit authorization.
- Telemetry → canonical mutation.
- Cache/database/backup copy → canonical authority.
- External integration → unrestricted internal access.
- CPRG → general data-plane access.
- Developer Fabric → User Network trust equivalence.
- Thunderbolt/USB4 → assumed shared RAM semantics.
- Internet → permanent node ownership.
- Secondary cluster node → independent competing State Authority.

## 13. Criticality boundary

Critical functions retain qualified operation through Internet loss, Cloud loss, one-node failure, partial local-network failure, primary-AI failure and one-storage-component failure, subject to the dedicated qualification architecture.

Criticality hierarchy is preserved:

Security / Access Control / Surveillance > Climate / Energy > other non-critical domains,

with final SLO/topology qualification delegated to the relevant MH domains.

## 14. Reconciled historical decisions

### Historical Compute Contribution
**Historical:** Section 1 described Compute Contribution as intended for every MediaHub deployment.

**Current explicit decision:** user Compute Contribution into the Developer Fabric is not accepted in the current architecture.

**Reconciliation:** the historical capability remains provenance but is not a current enabled boundary. No user compute enters Developer Fabric unless a future explicit architecture decision re-admits it.

### Historical cluster authority
**Historical:** one logical distributed State Authority with a designated active authority node for the current epoch.

**Current:** preserved and strengthened: distribution/replication/failover are mechanisms of one logical authority; no node becomes an independent authority.

### Historical Smart Home authority
**Historical/current:** HA Core is the sole Smart Home operational authority; MediaHub State Authority remains platform authority. Cross-domain orchestration may sequence work but cannot replace HA Core.

### Historical mobile model
**Historical/current:** iPad Core is a local MediaHub node; iPhone/Android Remote is a separate remote-access application.

## 15. Remaining product decision

**Q-MH2-01 — HA Core unavailable while a physical safety-critical device remains reachable.**

The current architecture forbids a general HA bypass, but does not yet specify whether a narrowly qualified emergency/safety path may exist outside HA Core under a separate safety authority/contract. This must be resolved in the relevant safety/security architecture before implementation of such a path.

No other user decision is required to define the MH-2 logical boundary model.

## 16. Handoffs

- MH-3: runtime/process/service boundary mechanics and lifecycle.
- MH-4: State Authority implementation, consistency, quorum and failover qualification.
- MH-5: consumer and external integration ingress.
- MH-6: internal service boundaries.
- MH-7: policy publication/enforcement.
- MH-8: extension/plugin isolation.
- MH-9: UI/API implementation.
- MH-10: AI proposal/admission boundary.
- MH-11: observability and evidence plane.
- MH-12: security/threat/negative verification.
- MH-13: privacy/data classification and egress governance.
- MH-14: persistence, journal and recovery storage.
- MH-15: OS/appliance/platform qualification.
- MH-16: update/recovery lifecycle.
- MH-17: device/protocol trust and admission.
- MH-18: media domain boundary.
- MH-19: knowledge/digital-twin boundary.
- MH-20: independent boundary audit.
- MH-21: hybrid-cloud/developer boundary.
- MH-22: production/qualification evidence.
- MH-23: migration/version compatibility.

## 17. Qualification conclusion

MH-2 defines the system boundary architecture without replacing downstream domain architectures. The architecture has one logical platform authority, one Smart Home operational authority, explicit trust/data/deployment boundaries, Local First operation, Developer/User isolation, contract-mediated integration and no hidden authority paths.

This checkpoint does not authorize production release, production deployment, credential provisioning, or architecture freeze.
