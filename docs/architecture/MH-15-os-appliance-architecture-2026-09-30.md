# MH-15 — OS & Appliance Architecture

Status: ETALON BASELINE / RECONCILED / READY_FOR_AUTONOMOUS_QUALIFICATION
Qualification: QUEUED / NOT YET EXECUTED
Production: NOT AUTHORIZED

## Canonical invariant
MediaHub Appliance is not a specific computer or OS. It is a qualified system profile implementing one MediaHub contract on a concrete hardware/platform substrate.

## System model
Hardware → Firmware → Boot/Verified Boot → Platform Substrate → Kernel/Platform APIs → HAL/Capabilities → Hardware Qualification → OS Qualification → Runtime Substrate → MediaHub Services → Security/Policy/State Authority → Capability Profile → Admission → Production.

OS, kernel, HAL, drivers, containers and health telemetry are not canonical State Authority. Platform implementations may differ; contract, authority, security, lifecycle and capability semantics remain unified.

## Hardware independence
Detection is: Detect → Identify → Capability Detection → Driver Binding → Trust Evaluation → Qualification → Hardware Profile → Policy Admission.
Supported profiles: Full MediaHub Node, Compact Node, Smart Home Node, Media Node, Compute Node, Storage Node, iPad Core. A device name does not define a profile.

## Platform boundary
Linux-based MediaHub OS is the clean-install baseline for qualified x86/ARM appliance hardware where appropriate. macOS/iPadOS use platform adaptation rather than Linux emulation. Raspberry Pi uses a qualified ARM substrate. iPad Core is a specialized local Core profile constrained by Apple security/lifecycle rules; iPhone/Android are Remote Access surfaces without independent Core Authority; Wall Panel is a context-limited UI surface.

## Boot, firmware and integrity
Firmware → Secure/Verified Boot → Bootloader → OS Integrity → Critical Runtime Integrity → Service Admission. Use signed artifacts, measured/verified boot, rollback protection and hardware-backed trust where available. Missing assurance is represented explicitly as reduced assurance; it is never silently treated as equivalent.

Firmware qualification covers identity, provenance, signature, compatibility, vulnerability state, update and recovery. OS integrity covers immutable/verified components where useful, package provenance, signed artifacts, filesystem/configuration/service integrity.

## Kernel / HAL / drivers / devices
Kernel is platform substrate. HAL exposes capability-oriented CPU/GPU/NPU/storage/network/camera/audio/display/GPIO/USB/Thunderbolt/sensor interfaces and has no authority. Critical drivers require provenance, version, platform/hardware compatibility, security, functional/performance qualification and recovery behavior. Device admission is Detect → Identify → Capability → Driver → Trust → Qualification → Admission. Unknown critical devices may be DENIED or QUARANTINED. DMA-capable external devices are elevated-risk boundaries.

## Runtime and isolation
Host responsibilities: boot, hardware, network/storage/security substrate, recovery and orchestration substrate. Workload responsibilities: domain services, plugins, AI, media and integrations. Isolation may use native processes, sandboxes, containers, VMs or WASM according to risk and capability. Containerization is not a security guarantee by itself.

Services are identity-bound, capability-scoped, supervised, observable, restartable, updateable and recoverable. Each service has owner, authority scope, dependencies, resource limits, network/storage permissions and lifecycle.

## Storage and filesystem
Logical system areas: boot, system, runtime, persistent state, user data, media, documents, recovery, update artifacts, logs/telemetry. Physical partitioning and filesystem vary by platform. Required properties: durability, integrity, encryption, permissions, quotas, snapshots where useful and recovery. Storage authority remains MH-14.

## Resource / memory / network
OS provides enforcement substrate for Section 24 — Resource Management Architecture: CPU/GPU/NPU/RAM/storage I/O/network/accelerator/thermal/power. Scheduler semantics remain centralized in Resource Management. Memory distinguishes local RAM, compression, swap, remote memory, pressure and reservations; remote memory is not assumed coherent without hardware support. Network substrate includes Ethernet, Wi-Fi, Bluetooth, USB/TB/USB4 networking and VPN interfaces; network authority remains in the Network Architecture.

High-speed fabric supports qualified Thunderbolt/USB4/high-speed IP/direct links and topology discovery; physical transport is not cluster authority.

## Identity and lifecycle
Each node has cryptographic identity, lifecycle, qualification state and revocation state, with attestation where available. Hostname/IP are not identity. Lifecycle: FACTORY → PROVISIONING → QUALIFICATION → STAGING → PRODUCTION → MAINTENANCE/QUARANTINE/RECOVERY → DECOMMISSIONED. Operational modes: FULL, REDUCED, MAINTENANCE, RECOVERY, QUARANTINE, OFFLINE.

Bootstrap: establish identity → verify software → detect hardware → determine capabilities → secure management → obtain policy → qualify. Bootstrap does not automatically obtain user data.

Production admission: Hardware Identity → Hardware Qualification → Firmware Qualification → OS Qualification → Driver Qualification → Runtime Qualification → Security Qualification → Capability Profile → Policy Admission → Production.

## Cluster and failure
Cluster join: Discovery → Identity → Trust → Capability → Qualification → Policy → User/System Admission → Synchronization. Sensitive state is not synchronized before trust/admission. Leave revokes identity/leases/credentials and updates topology according to policy. Failure handling: Detect → Isolate → Preserve Authority → Reschedule/Failover → Recover → Requalify → Reintegrate. OS does not independently make distributed authority decisions.

## Recovery, reset and update
Recovery is a minimal trusted base for boot, identity, storage, required network, verification, backup/restore, update and diagnostics; it does not automatically receive production authority. Reset levels: configuration, application, user data, full secure erase, recovery reinstall; authorization, confirmation, backup option and audit apply by risk. Update substrate supports signed artifacts, staged rollout, A/B or equivalent recovery, rollback, compatibility, migration hooks and verification; detailed lifecycle is handed to MH-16.

## Artifact, configuration and secrets
Production artifacts require ID, version, source, provenance, signature, SBOM, license, compatibility, qualification and rollback information. Configuration is schema-defined, versioned, policy-checked, auditable and recoverable. Secrets use Secret Management, short-lived credentials, hardware-backed protection where available, rotation and revocation; secrets are not ordinary configuration/logs/images/arbitrary environment variables.

## Observability and security boundary
OS exposes boot/service/kernel/driver/CPU/GPU/NPU/memory/storage/network/thermal/power/security diagnostics. MH-11 owns unified observability semantics. Logs are classified, redacted, retained with integrity and buffered locally. Crash artifacts are minimized, sanitized and export-controlled. OS must not bypass Identity, Policy, State Authority, HA, Persistence or Privacy. Administrative access is identity-aware, capability-scoped, auditable and revocable. Support is request → authentication → authorization → policy → limited session → audit → close/revoke; no permanent support tunnel.

## Development / production / cloning / migration
Development, qualification, staging, production and recovery are distinct trust states. Development mode does not automatically expose production user data. Cloning creates new identity/keys/qualification/admission. Hardware migration is Detect New Hardware → Qualify → Establish Identity → Validate Software → Restore Data/State → Validate Policy → Resume.

## Appliance roles and degraded operation
Roles may include Gateway, Router, Firewall, DHCP, DNS, VPN, AP, Controller, Media Server and Smart Home Node, subject to capability and policy. A node may have multiple roles. Network failure preserves safe local operation, persistence, Smart Home, local AI and diagnostics. Resource/storage pressure protects critical state before throttling, rescheduling, degradation and recovery. Power recovery validates integrity/filesystem/State Authority/dependencies before cluster rejoin and requalification. Thermal risk throttles/migrates/stops noncritical workloads while preserving critical functions.

## External devices and supply chain
USB/Thunderbolt/USB4/external storage/network/accelerator/capture/DMA-capable devices require identification, capability, trust, policy and qualification. Production OS components require provenance, license, SBOM, vulnerability assessment, reproducibility where required, qualification and rollback. Unknown packages are not admitted to production.

## Qualification matrix
Hardware; Firmware; OS; Drivers; Runtime; Network; Storage; Security; Resource; Recovery; Update are independently evidenced against an exact revision/environment. Architecture text is not implementation evidence.

## Cross-MH boundaries
MH-2 defines system boundaries; MH-3 Runtime Foundation; MH-4 Security; MH-6 Core Runtime Services; MH-7 Configuration/Policy; MH-11 Observability; MH-12 Security Analysis; MH-13 Privacy; MH-14 Persistence. Section 24 owns Resource Management semantics. MH-16 owns installation/recovery/update lifecycle. MH-17 devices/protocols; MH-20 audit/governance evidence; MH-21 hybrid cloud; MH-22 production/qualification; MH-23 migration. MH-15 provides the OS/appliance substrate and does not duplicate those authorities.

## Residual gaps for qualification
G-01 exact implementation evidence for supported hardware matrix.
G-02 platform-specific secure/measured boot and attestation evidence.
G-03 critical driver qualification inventory and recovery evidence.
G-04 exact filesystem/storage implementation matrix and persistence evidence.
G-05 resource enforcement evidence against Section 24.
G-06 Apple/iPadOS capability and sandbox qualification evidence.
G-07 external DMA-capable device admission evidence.
G-08 node bootstrap/identity/revocation implementation evidence.
G-09 recovery/reset/update implementation evidence handed to MH-16.
G-10 supply-chain/SBOM/package qualification evidence.
G-11 production admission end-to-end evidence.
G-12 independent cross-MH contradiction and dependency verification.

## Closure
Architecture state: RECONCILED / ETALON BASELINE.
Qualification state: QUEUED / NOT YET EXECUTED.
Production state: NOT AUTHORIZED.

Required closure artifact: MH-15 OS & Appliance Architecture Closure with per-wave evidence, exact revision/environment, gaps, contradictions, residual UNKNOWNs and independent disposition.

Final invariant: Hardware-Independent · Capability-Based · Qualification-Driven · Secure-Boot-Aware · Identity-Centric · Policy-Controlled · Local-First · Resource-Aware · Failure-Tolerant · Recoverable · Updateable · Observable · Privacy-Preserving · Supply-Chain-Verified · Production-Qualified.
