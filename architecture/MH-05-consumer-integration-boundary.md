# MH-05 — Consumer Integration Boundary

## Canonical architectural baseline

Status: RECONCILED — READY FOR INDEPENDENT AUTONOMOUS QUALIFICATION  
Product decisions Q1–Q12: D

This record fixes the MH-05 Consumer Integration Boundary as a continuation of MH-01..MH-04. It does not replace or create a competing State Authority.

## Product decisions

- Q1 External consumer integrations: D — official first-class integrations plus isolated, capability-controlled custom integrations.
- Q2 Plugins/adapters: D — official/qualified path plus sandboxed user integrations without critical authority.
- Q3 Cloud: D — Local First; cloud is an additional capability source and every transfer is classified, authorized and governed by egress policy.
- Q4 External ecosystem authority: D — Home Assistant Core remains Smart Home operational authority; external ecosystems are integration/interface boundaries, with exceptions only through separate qualification and policy.
- Q5 Custom API integrations: D — safe Integration SDK with qualification, policy and capability restrictions.
- Q6 Unknown device: D — automatic DENY/QUARANTINE with safe limited qualification and no critical rights.
- Q7 External media services: D — official integrations first, approved adapters where qualified; DRM bypass is prohibited.
- Q8 Consumer data sharing: D — Local First, data classification, egress controls and explicit consent where required; absent permission is DENY.
- Q9 External automation: D — capability-scoped read/write; critical operations require full authorization, policy evaluation and fresh-state validation.
- Q10 Integration SDK: D — public/partner SDK with versioned contracts, sandboxing, capability controls, qualification and security controls.
- Q11 Main user principle: D — balance compatibility, security, Local First and simplicity while preserving strict trust and authority boundaries.
- Q12 Openness: D — Controlled Open Platform with broad compatibility through contracts, adapters and plugins without violating authority, security, data or trust boundaries.

## Canonical integration chain

Discovery -> Identity -> Capability Detection -> Trust Assessment -> Qualification -> Contract/Adapter -> Policy -> Admission -> Integration -> Runtime Operation -> Monitoring -> Lifecycle/Revocation

Discovery never implies trust. Technical compatibility never implies authorization.

## Authority invariants

1. MediaHub State Authority remains the single logical canonical platform authority.
2. Home Assistant Core remains Smart Home operational authority.
3. External ecosystems never become implicit internal authorities.
4. Adapters, plugins, events, caches and replicas cannot bypass State Authority.
5. AI remains non-authoritative and uses only approved contract paths.
6. Developer Cloud has no access to User Data.
7. User Network and Developer Compute Fabric remain separate trust/data planes.
8. Unknown devices are denied or quarantined until qualified and admitted.
9. Ambiguous critical state fails closed.
10. Critical operations require fresh authorization and policy evaluation.

## Integration SDK and adapter boundary

Adapters are compatibility layers, not authorities. Each qualified integration is identity-bound, capability-scoped, lifecycle-managed, versioned, provenance-tracked, auditable and revocable.

Plugins and custom integrations execute through sandboxed, capability-scoped contracts with resource, network and data limits. They cannot obtain unrestricted filesystem, network, secrets or User Data access and cannot bypass MH-04 security, MediaHub API, Home Assistant authority or canonical state mutation controls.

## Cloud and data boundary

Cloud is an external trust domain and optional capability source. Supported states include LOCAL, CLOUD_ASSISTED, CLOUD_REQUIRED, DEGRADED and UNAVAILABLE. External transfer follows:

Need -> Capability -> Data Classification -> Destination Verification -> Authorization -> Consent where required -> Egress Policy -> Contract Validation -> Transfer -> Audit

User Data, Integration Data and Developer Data remain separate. Integration Data is minimized to the contract-required scope.

## State and event model

Desired, observed, reported, cached, historical and canonical state remain distinct. Cache or external copy is never canonical authority.

External events follow:

Receive -> Authenticate -> Validate -> Classify -> Authorize -> Normalize -> Contract -> Process -> Audit

An event is not permission to mutate canonical state.

## Lifecycle and recovery

Integration lifecycle:

Discovered -> Identified -> Qualified -> Admitted -> Active -> Degraded -> Quarantined -> Revoked -> Removed

After recovery:

Reconnect -> Identity Verification -> Capability Revalidation -> Trust Reassessment -> State Reconciliation -> Policy -> Reintegration

Recovery does not automatically restore trust.

## Qualification contract

The independent qualification target is this exact Git revision, not historical MH-05 implementation branches or prior R4 evidence. Qualification must independently verify:

1. Contract completeness and internal consistency.
2. Preservation of MH-01..MH-04 authority, trust, runtime and security boundaries.
3. Adapter/plugin non-authority and capability scoping.
4. Unknown-device DENY/QUARANTINE behavior.
5. Cloud/data classification and egress-deny semantics.
6. Event authentication/validation and the event != mutation-permission invariant.
7. State synchronization conflict handling and fail-closed critical behavior.
8. Lifecycle, revocation and recovery re-admission rules.
9. OSS/provenance/qualification requirements.
10. Explicit forbidden-path inventory: State Authority bypass, UI/API bypass, AI authority, cloud authority, Developer Cloud -> User Data, unrestricted plugin/API passthrough, Smart Home bypass, CPRG bypass, cache-as-authority.

Architecture text is not implementation evidence. Historical R4 qualification evidence is not transferable to this architecture revision.

## Final MH-05 architectural position

MediaHub is a Controlled Open Platform. Broad interoperability is permitted through versioned contracts, qualified adapters, sandboxed integrations and capability-scoped SDKs while preserving Local First data sovereignty, State Authority, MH-02 boundaries, MH-03 runtime contracts, MH-04 security architecture and Home Assistant operational authority.

Qualification is a separate state transition:

RECONCILED -> VERIFIED -> QUALIFIED

Qualification does not imply release or production authorization.

No MH-06 work is implied by this record.
