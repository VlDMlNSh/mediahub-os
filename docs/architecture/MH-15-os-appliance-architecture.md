# MH-15 — OS / Appliance Architecture

**Status:** ARCHITECTURE WORK IN PROGRESS  
**Acceptance:** NOT AUTHORIZED  
**Freeze:** NOT AUTHORIZED  
**Implementation authorization:** NONE

## 1. Prime invariant

> The host provides execution; MediaHub defines authority.

Host resources include CPU, RAM, storage, network, process isolation, filesystem, device access, timers, power, and thermal facilities. None is canonical MediaHub State Authority.

## 2. Layer model

Hardware -> Firmware/Boot -> Kernel -> Host OS -> Host Services/Supervisor -> MediaHub Runtime -> MediaHub Services -> Consumers/UI/AI/Plugins/Integrations.

## 3. Authority boundary

OS process started != MediaHub service READY. Disk mounted != storage subsystem usable. Network interface UP != authenticated/authorized integration. Filesystem mutation != canonical state mutation. Container alive != MediaHub READY.

## 4. Hardware baseline

Candidate platform: Apple Mac mini Server 2011. Exact model, CPU, RAM, GPU, storage, NIC, firmware/EFI, sensors, thermal/power behavior, storage health and Linux compatibility remain UNKNOWN until forensic evidence exists.

Qualification sequence: Discovery -> read-only inspection -> evidence capture -> compatibility analysis -> security review -> qualification decision. Destructive operations require separate authorization.

## 5. Boot and lifecycle

Host boot, MediaHub initialization, and MediaHub READY are separate states. Proposed order: Hardware -> OS -> Security Foundation -> Runtime Foundation -> State Authority -> Core Services -> Policy/Configuration -> Integrations -> UI/AI/Plugins -> health gates. Exact dependency order requires implementation evidence.

Graceful shutdown: stop ingress -> stop new operations -> drain allowed work -> finalize authorized state operations -> persist only according to an authorized persistence contract -> stop services -> close resources -> host shutdown.

## 6. Process and service model

Service identities are separate where justified. Define UID/GID, capabilities, filesystem, network, devices, IPC, secrets, dependencies, lifecycle, restart policy, resource limits, health and observability. Process separation alone is not complete security isolation.

Root is exceptional, not normal application privilege.

## 7. systemd and containers

systemd is candidate host lifecycle/supervision infrastructure, not domain authority. Container runtime is candidate deployment/isolation infrastructure, not State Authority or physical HA. Exact choices require ADR and compatibility/security evidence.

If containers are adopted, evaluate rootless/rootful mode, namespaces, cgroups, capabilities, seccomp, MAC, mounts, network, devices, secrets, provenance, signatures, digests and limits. Privileged containers require explicit justification.

## 8. Filesystem and devices

Separate OS, binaries, configuration, runtime temporary data, logs, telemetry, media, future persistence, backups, recovery artifacts and secrets. Filesystem is a storage mechanism, not authority. Device output is input/data, not authority; device commands require authorized adapters and policy boundaries.

## 9. Network and hardening

Separate management, MediaHub control/API, device network, cloud, update and recovery planes where required. Deny unnecessary ingress, control egress, isolate management/recovery and expose only required services. Firewall does not replace application authorization. Hardening must follow compatibility assessment.

## 10. Security and privileged operations

Host administrator, runtime users, recovery identity, update identity and diagnostic identity are conceptually distinct. Shell is not the canonical MediaHub command path. Arbitrary shell from AI/plugin/untrusted paths is FORBIDDEN. Privileged operations require identity, authorization, policy, bounded execution and audit.

Secrets are isolated, permission-restricted, non-source-controlled, non-logged, non-exported and rotatable.

## 11. Resources, power and time

Protect State Authority and core runtime from CPU, RAM, disk, network, process/thread, FD, IPC, temporary-storage, telemetry, plugin and AI exhaustion. Thermal/power properties require hardware evidence. Use monotonic time for durations/timeouts; wall-clock semantics must be explicit. Host time is not automatically trusted security evidence.

## 12. Observability and failures

Host observations feed MH-11. Observability is observer, not authority. Security enforcement remains MH-12. Optional service failure must not automatically compromise core authority. Self-healing follows Observation -> Policy -> Authorization -> Command -> Consumer Boundary -> State Authority.

## 13. Recovery and updates

Recovery is a separate trust boundary. Host update, MediaHub application update, data migration and security update are separate planes. No update may silently expand application privilege. Installer/update/recovery are not State Authority and are detailed by MH-16.

## 14. Appliance model

Target properties: deterministic baseline, minimal mutable surface, controlled configuration, controlled updates, predictable recovery, least privilege, observable health and reproducible build. Appliance does not mean immutable by definition.

## 15. Development vs production

Development and production are separate trust/configuration domains. Development privileges and tools must not silently enter production.

## 16. Acceptance

MH-15 remains WORK IN PROGRESS until evidence exists for host boundary, hardware baseline/qualification, lifecycle, process/service model, least privilege, filesystem/storage, devices, network/firewall, hardening, CI/build/supply chain, updates, recovery, resources, thermal/power, time, observability, failure domains, privileged operations, shell/secrets/sandboxing, OS lifecycle, appliance qualification, testing, evidence/contradiction/unknown registers and traceability to MH-1…MH-14 and P0-03…P0-07.

## 17. Implementation gate

Architecture -> ADR -> Governance Authorization -> Implementation -> Verification -> Evidence -> Acceptance. MH-15 alone authorizes no installation, formatting, bootloader/kernel/firmware modification, container deployment, firewall/hardening deployment, storage change or persistence implementation.

## 18. Final answer

A safe appliance execution environment is achieved by treating host mechanisms as bounded infrastructure and preserving canonical domain authority inside MediaHub State Authority. The architectural model is defined; production qualification and hardware/host evidence are not yet established.
