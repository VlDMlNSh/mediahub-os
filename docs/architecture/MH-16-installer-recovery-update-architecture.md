# MH-16 — Installer / Recovery / Update Architecture

**Status:** PROPOSED / GOVERNANCE ACCEPTANCE PENDING / NOT FROZEN / IMPLEMENTATION NOT AUTHORIZED
**Scope:** MediaHub OS 11.x LTS / MediaHub iOS
**Canonical source:** MH-16 architecture chat + this repository artifact
**Rule:** this document is architecture/governance only; implementation work belongs in the dedicated development chat/branch.

## 1. Purpose

Define the normative architecture for Installer, Provisioning, Bootstrapping, Enrollment, Boot/Trust Chain, Update, Migration, Rollback, Recovery, Backup/Restore, Factory Reset, Secure Wipe and Disaster Recovery without creating an alternate canonical mutation authority.

## 2. Governing invariant

Installer, Update Coordinator, Migration Engine, Recovery Manager, Backup/Restore and Factory Reset mechanisms are lifecycle authorities only. They MUST NOT become or emulate the MediaHub State Authority.

Canonical MediaHub state mutation remains inside the accepted P0-03 State Authority Contract v1.0. Lifecycle mechanisms may request approved State Authority operations but MUST NOT mutate canonical state directly.

## 3. Canonical lifecycle

Build → Package → Sign → Install → Initialize → Enroll → Configure → Start → Health Gate → Operate → Update → Health Gate → Rollback / Recovery

Recovery:

Detect → Classify → Authorize → Preserve Evidence → Recover → Validate → Health Gate → Resume

Every lifecycle operation requires: initiator, identity, authorization, scope, target, preconditions, expected result, failure semantics, evidence/audit, and rollback/recovery semantics.

## 4. Installer / Provisioning

Installer boundary:

External Request → Identity/Context → Authorization → Installer Plane → Approved Contracts → State Authority / OS Runtime → Health Gate

Installer state:

REQUESTED → AUTHORIZED → DISCOVERING → COMPATIBILITY_CHECK → ARTIFACT_VERIFICATION → STORAGE_PREPARATION → INSTALLING → INITIALIZING → PROVISIONING → ENROLLMENT → FIRST_BOOT → HEALTH_GATE → COMPLETE

Terminal states include FAILED, ABORTED, BLOCKED and RECOVERY_REQUIRED.

Provisioning state:

UNINITIALIZED → INITIALIZED → ENROLLED → CONFIGURED → OPERATIONAL

Enrollment is not operational trust. Configuration is not health. Boot success is not readiness.

Existing installations MUST be detected and classified before destructive action. Silent data destruction is forbidden.

## 5. Secure bootstrapping / trust chain

Canonical conceptual chain:

Hardware → Firmware → Bootloader → OS → Host Services → MediaHub Runtime → State Authority

The concrete boot/security technology is not fixed by this document. Secure Boot, TPM, EFI/UEFI, measured boot, hardware-backed keys, specific bootloaders and recovery mechanisms require platform evidence and ADR before selection.

Trust Chain != Authorization
Trust Chain != State Authority
Trust Chain != Administrator
Trust Chain != Recovery Authority

## 6. Artifact trust

Production artifact identity SHOULD contain at minimum:

- artifact_id
- artifact_type
- version
- build_id
- digest
- signature
- signer_id
- provenance
- compatibility
- architecture
- channel
- security metadata
- dependencies
- rollback constraints

Verification sequence:

identity → format → digest → signature → signer trust → provenance → compatibility → security policy → rollback policy → deployment authorization

Signature verification is necessary but does not by itself establish complete trust or deployment authorization.

Supply-chain model:

Source → Build → Dependency Resolution → Artifact → SBOM → Sign → Publish → Verify → Deploy

Specific SBOM format/tool is CANDIDATE pending ADR.

## 7. Update planes

Four independent planes:

1. Host Update — firmware, boot components, kernel, OS, host services and hardware enablement.
2. Application Update — MediaHub runtime, services, plugins, application packages and containers where proven.
3. Data Migration — schema, indexes, metadata, state representation and compatibility versions.
4. Security Update — revocations, certificates, trust roots, vulnerable components and emergency security changes.

Host, application, data and security versions MUST NOT be collapsed into one generic version concept.

## 8. Update transaction

REQUESTED → IDENTIFIED → AUTHORIZED → DISCOVERING → DOWNLOADING → VERIFYING → COMPATIBILITY_CHECK → STAGING → PREPARED → ACTIVATING → REBOOT_REQUIRED → BOOTING_NEW_VERSION → HEALTH_GATE → COMMITTED

Failure states include BLOCKED, FAILED, ABORTED, ROLLBACK_REQUIRED, RECOVERY_REQUIRED and UNKNOWN_STATE.

UNKNOWN_STATE MUST NOT be reported as success.

Atomicity technology is not fixed. A/B, dual-root, immutable image, transactional filesystem, package transactions, snapshots and container replacement are candidates subject to requirements, compatibility, security review, ADR and evidence.

## 9. Rollback

Rollback is independently classified for host, application, configuration, policy, data, security state, trust roots, firmware and credentials. Not all rollback operations are safely reversible.

A security floor / minimum allowed version MUST constrain rollback. The system MUST NOT automatically downgrade below a prohibited security floor.

## 10. Migration

Migration is explicit and versioned. A migration contract includes migration_id, source_version, target_version, preconditions, authorization, steps, expected result, validation, failure semantics, recovery strategy, compatibility and rollback capability.

Migration MUST NOT directly manipulate canonical state outside approved State Authority/Persistence contracts.

Migration must distinguish recoverable, non-rollbackable and unknown states.

## 11. Health Gate

Health Gate is required after installation, first boot, update, migration, rollback, recovery and restore.

Minimum dimensions:

boot, OS, runtime, State Authority, persistence, security, policy, configuration, critical services, storage, network, observability, device integrations and integrity.

Process alive != healthy. Host alive != MediaHub ready. Boot successful != operational.

## 12. Recovery

Recovery is a separate lifecycle trust domain with distinct Recovery Identity. Recovery privilege != runtime privilege.

Recovery MUST preserve evidence before destructive remediation where feasible and MUST validate the resulting system through Health Gate.

Offline recovery MUST NOT require Internet, cloud or external APIs. Offline artifacts remain subject to identity, integrity, signature, provenance, compatibility, security-floor and authorization checks.

## 13. Backup / Restore

Backup != HA. Backup != replica. Backup != State Authority.

Restore path:

Backup → Verify → Authorize → Stage → State Authority.restore() → Validate → Health Gate

Direct replacement of canonical state files by recovery/update code is forbidden unless explicitly represented by an accepted contract that preserves State Authority semantics.

A backup is not considered proven recoverable merely because the backup file exists. Evidence requires actual restore and validation.

## 14. Factory reset / secure wipe

Factory reset MUST be scoped. Candidate scopes:

RESET_CONFIGURATION, RESET_POLICY, RESET_APPLICATION, RESET_DATA, RESET_CREDENTIALS, RESET_ENROLLMENT, SECURE_WIPE, COMPLETE_APPLIANCE_RESET

Every destructive operation requires identity, authorization, explicit scope, preconditions, confirmation policy, audit/evidence, expected result and failure/recovery semantics.

Secure-wipe guarantees are platform/storage dependent and therefore require hardware/storage verification.

## 15. Disaster recovery / compromised artifacts

Disaster classes include boot corruption, OS/runtime corruption, State Authority or persistence corruption, failed update/migration, storage failure, power loss, credential/host compromise, signing-key compromise, malicious artifact and accidental deletion.

Compromised artifact response:

DETECT → QUARANTINE → STOP PROMOTION → REVOKE TRUST → BLOCK DEPLOYMENT → PRESERVE EVIDENCE → IDENTIFY KNOWN-GOOD → RECOVER → HEALTH GATE

Security revocation overrides convenience and cannot be bypassed by AI, plugins, UI or ordinary lifecycle code.

## 16. AI / Plugin / UI boundaries

AI may observe, classify, recommend and prepare proposals but MUST NOT self-authorize production update/rollback, modify trust roots, disable Health Gate, lower security floor or access signing keys.

Plugins MUST NOT change boot trust, trust roots, installer authorization or lifecycle security boundaries and MUST NOT perform hidden self-update.

UI is a request initiator only and is never lifecycle or state authority.

## 17. Required evidence before acceptance

Evidence is required for installer/provisioning, enrollment, first boot, artifact identity/signing/provenance/SBOM, trust roots, boot chain, rollback floor, update transaction, health gates, migration, power-loss handling, recovery, offline recovery, backup/restore, factory reset, secure wipe capability, compromised-artifact response, revocation, State Authority integration, security/privacy/observability reviews, AI/plugin/UI boundaries, hardware compatibility and traceability.

## 18. Current repository evidence

The repository currently demonstrates a contract-oriented foundation with top-level .github, contracts, docs, schemas, tests and tools. The root README identifies the repository as the MediaHub OS foundation repository.

Current repository search performed for MH-16 did not produce implementation evidence for installer, provisioning, bootloader/Secure Boot/EFI/TPM, firmware, artifact verifier/signing/provenance/SBOM, update coordinator, migration engine or recovery manager. These areas therefore remain UNKNOWN rather than being declared absent.

## 19. Governance status

Architecture: PROPOSED.

Contracts/ADRs: CANDIDATE / NOT ACCEPTED.

Security review: REQUIRED.

Hardware/platform qualification: REQUIRED.

Implementation authorization: NOT GRANTED.

Production qualification: NOT GRANTED.

Freeze: NOT FROZEN.

## 20. Architectural gate

ADR → Security Review → Hardware Capability Verification → Trust/Artifact Evidence → State Authority/Persistence Integration Verification → Failure/Power-Loss/Migration/Recovery Testing → Governance Acceptance → Freeze → Implementation Authorization

## 21. Development-chat boundary

MH-16 architecture chats are canonical architecture/governance records. They are not implementation workspaces. Code implementation, experiments, long debugging sessions and implementation-specific discussion belong in the dedicated development chat/branch.

The development workspace may consume MH-16 through the Master Prompt and return implementation/evidence status through the Reverse Master Prompt. Changes to canonical architecture require an explicit architecture/governance update, not silent implementation drift.
