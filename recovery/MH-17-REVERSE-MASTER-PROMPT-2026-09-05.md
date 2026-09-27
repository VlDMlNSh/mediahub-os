# MH-17 REVERSE MASTER PROMPT

Date: 2026-09-05
Repository: VlDMlNSh/mediahub-os
Branch: recovery/full-functional-spec
Status: RECONCILED / PROPOSED / NOT ACCEPTED / NOT FROZEN

## 1. MH identifier
MH-17 — Device / Protocol / Integration Architecture.

## 2. Historical scope
Device model; device identity; discovery; enrollment; trust; lifecycle; capability model; commands and command lifecycle; idempotency; events; telemetry; normalization; protocol adapters and protocol selection; network/security boundary; quarantine; device failure and safety; automation/AI/plugin/cloud interaction; configuration; firmware; replacement; groups/scopes; privacy; observability; persistence boundary; threat/resource governance; backpressure/error model; offline-first; simulator; testing/security/safety/compatibility; technology evaluation; dependency/evidence/decision/contradiction/unknown/acceptance artifacts.

## 3. Source evidence / provenance
Primary canonical evidence:
- recovery/forensic-control-point-2026-09-05.md
- recovery/MH01-23-REDISTRIBUTION-ARCHITECTURE-CHAT-HANDOFF-MASTER-PROMPT-2026-09-05.md
- recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml
- specification/capability-registry.yaml
- specification/contract-registry.yaml
- specification/invariant-registry.yaml
- specification/decision-registry.yaml
- specification/dependency-graph.yaml
- development/implementation-map.yaml
- current MH-17 architecture-chat historical evidence and previously recorded repository audit.

Repository evidence on the historical MH-17 contour includes canonical Device/Identity/Capability/State/Desired State/Trust/Binding/Event schemas and architecture contracts. Dedicated production protocol/discovery/enrollment/PKI/simulator implementations were not established by the recorded search surface; those items remain UNKNOWN rather than LOST.

## 4. CAP mapping

Direct / primary MH-17 mappings:
- CAP-002 unified_device_function_model
- CAP-003 home_assistant_internal_integration_automation
- CAP-004 kincony_kcs_usb_firmware_network_onboarding
- CAP-005 automation_scenes_triggers_conditions_actions
- CAP-007 unified_energy_ups_solar_wind_generator_battery_consumers
- CAP-008 direct_camera_recording_live_archive_playback_events_export (device/integration boundary only; recording ownership remains surveillance_core)
- CAP-019 homekit_yandex_loxone_projection (integration boundary only)
- CAP-023 ethernet_wifi_keenetic_ubiquiti_network_extension
- CAP-029 discovery_identification_configuration_lifecycle
- CAP-030 authenticated_authorized_device_commands
- CAP-031 unified_telemetry
- CAP-032 health_observation_and_operation_scoped_readiness
- CAP-034 self_recovery_checkpoints_filesystem_integrity (device/recovery interaction only)
- CAP-035 local_operation_without_internet_where_possible
- CAP-039 privacy_data_governance (cross-cutting)
- CAP-040 defense_in_depth_trust_authentication_authorization_secure_remote_access
- CAP-044 user_initiated_update_firmware_lifecycle
- CAP-049 vendor_protocol_ecosystem_extensibility
- CAP-050 simulation_verification_acceptance
- CAP-052 device_onboarding_operation_update_retirement
- CAP-054 actionable_contextual_installation_configuration_guidance
- CAP-056 authorized_device_automation_media_surveillance_engineering_export
- CAP-058 security_safety_system_invariant

Cross-domain preservation audit additionally checks all CAP-001…CAP-058; no capability is removed or retired by MH-17.

## 5. Requirement mapping

R-17-01 external devices/protocols are non-authoritative sources and execution endpoints.
R-17-02 discovery must not establish trust or authorization.
R-17-03 identity must distinguish MediaHub logical identity, physical/manufacturer/protocol/cryptographic identity and endpoint evidence.
R-17-04 enrollment requires proof/evidence, collision checks, trust decision, authorization scope, capability validation, configuration binding and audit.
R-17-05 device-reported, observed, desired, policy-allowed, commanded, committed, applied, confirmed and predicted states remain distinct.
R-17-06 commands require identity, authorization, policy, capability, safety, audit, timeout/deadline and idempotency semantics.
R-17-07 acknowledgements/events must not silently become canonical state.
R-17-08 protocol adapters translate and execute only already-authorized operations.
R-17-09 external input is validated/normalized/bounded at the integration boundary.
R-17-10 untrusted/revoked/malformed/mismatched devices may be quarantined and denied ordinary control.
R-17-11 firmware is a lifecycle plane, not an ordinary device command.
R-17-12 automation/AI/plugins/cloud cannot bypass authorization or State Authority.
R-17-13 local/offline operation remains preferred where technically possible.
R-17-14 protocol technology remains candidate until evidence/alternatives/constraints/ADR/verification/acceptance.
R-17-15 device lifecycle, replacement, groups/scopes and failure semantics preserve identity, authorization and audit boundaries.

## 6. Contract mapping

Primary:
- CTR-003 identity-authentication-authorization
- CTR-004 trust
- CTR-005 discovery-onboarding
- CTR-006 device-command
- CTR-007 event
- CTR-009 automation
- CTR-016 network
- CTR-020 health
- CTR-021 readiness
- CTR-022 diagnostics
- CTR-024 update-lifecycle
- CTR-026 privacy
- CTR-029 ecosystem-projection
- CTR-031 guidance
- CTR-033 telemetry
- CTR-035 resource-governance
- CTR-036 verification-acceptance

Cross-boundary:
- CTR-001 state-authority
- CTR-002 consumer-boundary
- CTR-017 cluster
- CTR-023 recovery
- CTR-025 migration
- CTR-030 variant-capability
- CTR-032 export

The contract registry currently leaves exact protocol/device matrix, HA boundary/version, camera modes, mobile protocols, cluster semantics, threat model and AI qualification open; MH-17 does not close those items by assumption.

## 7. Invariant mapping

Primary MH-17 invariants:
INV-001, INV-002, INV-003, INV-004, INV-005, INV-006, INV-008, INV-009, INV-012, INV-014, INV-015, INV-016, INV-018, INV-020, INV-021, INV-022, INV-023, INV-024, INV-026, INV-027, INV-029, INV-030.

Additional operational invariants established by MH-17 architecture:
- Device/Protocol Adapter is never State Authority.
- Sent != Applied; Applied != Confirmed.
- Timeout != physical failure.
- Capability declaration != permission.
- Group membership != authorization.
- VPN/TLS/network reachability != application authorization.

These are projections/candidate invariants and require central governance before registry promotion.

## 8. Decision mapping

Accepted decisions applicable to MH-17:
DEC-001 functional baseline primary truth; DEC-002 HA internal; DEC-005 local/offline-first; DEC-008 health/readiness distinction; DEC-009 system-level security; DEC-010 variant differences; DEC-011 P0-P8 historical decomposition; DEC-012 deferred detail is not rejection.

Draft architecture decisions relevant to MH-17:
DEC-A-001 capability-centric master architecture; DEC-A-002 explicit authority/security boundaries; DEC-A-003 separate local/cloud trust/control planes; DEC-A-004 logical storage domains.

MH-17-specific proposed decisions remain OPEN pending central evidence/ADR:
- canonical integration-boundary contract;
- protocol adapter lifecycle and qualification model;
- device trust lifecycle extension;
- command outcome/confirmation semantics;
- quarantine authority and recovery semantics;
- protocol/device compatibility matrix;
- firmware/device lifecycle integration.

## 9. Architecture / boundary mapping

Canonical observation path:
Device / External World → Protocol Adapter → Integration Boundary → Normalization → Runtime/Event Boundary → State Authority / Consumers.

Canonical control path:
User / Automation / AI / Plugin / External Service → Intent → Policy → Authorization → Consumer Boundary → State Authority → Authorized Command → Protocol Adapter → Device.

Forbidden direct paths:
Device → DB; Device → State Authority bypass; AI → Device direct; Plugin → Device unrestricted; Cloud → Device direct.

Device trust lifecycle candidate:
Discovered → Untrusted → Identified → Verified → Enrolled → Authorized → Configured → Active → Degraded → Quarantined → Revoked / Removed.

## 10. Historical classification

RETAIN:
- Device/Identity/Capability/State/Desired State/Trust/Binding/Event contract concepts.
- separation of observation from authority;
- protocol neutrality;
- explicit device lifecycle, command lifecycle, idempotency and safety;
- offline-first, telemetry, diagnostics and simulator/testing requirements;
- security/quarantine and external integration boundaries.

REMAP:
- protocol/device implementation responsibilities → integration_core/device_onboarding/device_management/command_system;
- device health/readiness → observability, not trust;
- automation/device execution → automation_core + command_system + State Authority boundary;
- HA integration → smart_home_core, not user-facing UI;
- firmware → lifecycle_core with device_onboarding/device_management integration;
- storage/persistence → owning canonical domain and State Authority, not device adapter.

RECONCILE:
- repository lifecycle enum versus required richer trust/device lifecycle;
- Device protocol_ids/hardware_ids shape mismatch with separate identity schema;
- permissive nested Device objects as external-input contracts;
- State Authority/P0-05/P0-06 boundary interaction;
- precise command confirmation semantics;
- exact protocol and device compatibility matrix.

REPLACE:
- any interpretation that lets a device, adapter, plugin, AI or cloud become canonical state authority is replaced by the central State Authority model.
- any interpretation that treats discovery/presence/health/readiness as trust or authorization is replaced by the canonical security semantics.

RETIRE:
- none proposed from historical MH-17 evidence.

UNKNOWN:
- concrete production adapters;
- discovery/enrollment runtime;
- certificate/PKI provisioning and rotation;
- simulator implementation;
- exact supported protocol versions and device families;
- exact firmware transport/update mechanisms;
- exact production command executor;
- hardware-specific security capabilities.

## 11. Contradictions

C-001: canonical handoff requires richer device trust/lifecycle states than current repository lifecycle schema. Requires ADR/contract evolution; no silent reinterpretation.

C-002: Device protocol_ids/hardware_ids are arrays while identity schema represents related identifiers as objects. Requires contract reconciliation.

C-003: critical nested Device structures are permissive objects; insufficient by themselves as hostile external-input security boundary. Requires hardened validation contract.

C-004: previously recorded repository test surface contained a duplicate declaration of an event immutability test. Status: OBSERVED / REQUIRES VERIFICATION.

C-005: State Authority remains sole canonical mutation authority; P0-05 consumer authorization and P0-06 State Authority boundaries must not be collapsed into device integration. Requires central cross-MH consistency verification.

## 12. Missing evidence

No qualifying evidence was established for concrete production protocol adapters, discovery/enrollment engines, device PKI/certificate provisioning, simulator, production command executor, quarantine runtime, telemetry ingestion runtime or protocol-specific compatibility guarantees.

No protocol selection is therefore closed.

## 13. Dangling references

- richer lifecycle states are referenced by architecture but not represented equivalently in the current Device lifecycle schema;
- protocol-specific capabilities may reference adapters/protocols for which no production implementation evidence exists;
- confirmation/applied semantics require runtime evidence before acceptance;
- exact firmware workflow references require concrete lifecycle evidence.

## 14. Stale references

- any direct dependence on the historical P0 decomposition as canonical ownership is stale under DEC-011;
- any adapter-specific implementation claim without current evidence is stale/UNVERIFIED;
- any assumption that network presence implies trust/authorization is stale.

## 15. Proposed technical decisions

TD-17-01: define a canonical Integration Boundary contract separating transport/protocol parsing from normalized MediaHub semantics.
TD-17-02: define device trust lifecycle as a security lifecycle independent from availability/health.
TD-17-03: define command outcome as multi-stage evidence, never as acknowledgement-only state.
TD-17-04: define compatibility as a versioned evidence-backed matrix of device family, protocol, firmware and capability.
TD-17-05: define firmware update as lifecycle operation with independent authorization, rollback and safety semantics.

All five remain OPEN / EVIDENCE-BLOCKED until evidence + alternatives + constraints + ADR + verification + acceptance authority exist.

## 16. Contract impacts

Potential impact: CTR-004, CTR-005, CTR-006, CTR-016, CTR-020, CTR-021, CTR-024, CTR-033, CTR-036; and cross-boundary CTR-001/002/023/030.

No canonical contract registry was changed by MH-17.

## 17. Invariant impacts

Potential strengthening of INV-003/005/020/024/026/027 and security invariant set; candidate additions above require central approval. No invariant was removed or weakened.

## 18. Dependency impacts

Primary dependency path:
smart_home_core → device_onboarding → device_management → command_system.

Cross-cutting dependencies:
integration_core → smart_home_core; network_core; security_core; observability; lifecycle_core; automation_core; event_core; recovery_core; resource_governance.

Dependency graph endpoints are already represented in the canonical graph; exact runtime ordering and ownership remain subject to central reconciliation.

## 19. Verification requirements

Required evidence:
- schema/contract validation of external device input;
- identity collision and enrollment tests;
- authentication/authorization/revocation/quarantine tests;
- command idempotency and ambiguous-outcome tests;
- adapter protocol conformance tests;
- event causality/order/deduplication tests;
- telemetry provenance/freshness/privacy tests;
- firmware interruption/rollback/security-floor tests;
- offline/degraded/backpressure tests;
- simulator parity and fault-injection tests;
- compatibility matrix tests across supported protocol/device/firmware combinations;
- safety and negative authorization tests;
- State Authority boundary tests proving no bypass path.

## 20. Acceptance evidence / authority

Acceptance evidence must be reproducible, timestamped and tied to contract/version/hardware/firmware context where applicable.

Acceptance authority is central governance / explicit human acceptance of the Master Architecture, not MH-17.

## 21. OPEN items

MH-17 remains OPEN on all implementation-specific protocol, hardware, PKI, simulator, compatibility and production command questions. No OPEN item is treated as loss.

## 22. Anti-loss confirmation

ANTI-LOSS RESULT: PASS at preservation/accounting level.

CAP-001…CAP-058 were checked as a canonical preservation baseline; MH-17 introduces no deletion, retirement or replacement of any canonical capability. Primary ownership remains centralized in the capability registry. Historical gaps remain UNKNOWN/EVIDENCE_GAP.

## 23. Proposed canonical registry changes

P-17-01: add/normalize Integration Boundary semantics in contract registry after ADR.
P-17-02: reconcile Device lifecycle schema with trust lifecycle without conflating health/readiness.
P-17-03: reconcile Device identity identifier shapes.
P-17-04: add evidence-backed compatibility-matrix contract requirements.
P-17-05: strengthen external-input schema validation requirements.

For each proposal: reason = ambiguity/contract gap; evidence = MH-17 repository audit + canonical registries; affected CAP = 002/004/023/029/030/040/044/049/050/052/058; affected CTR = 003/004/005/006/016/020/021/024/033/036; affected INV = 003/005/020/021/024/026/027; affected DEC = DEC-001/005/008/009/011/012 and draft DEC-A-002; dependency impact = device_onboarding/device_management/integration_core/command_system/security_core/observability/lifecycle_core; verification impact = identity/enrollment/command/adapter/compatibility/security/safety/offline tests; acceptance authority = central reconciliation + explicit human acceptance.

## 24. Unilateral-authority statement

MH-17 has NO unilateral authority to apply any proposed canonical registry change, alter capability ownership, retire a capability, accept the Master Architecture, or authorize production implementation.

## 25. Final state

MH-17 RECONCILED as a historical architecture projection.
Canonical truth remains controlled centrally.
Master Architecture remains DRAFT / NOT ACCEPTED.
Production implementation remains BLOCKED.
