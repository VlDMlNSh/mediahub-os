# MediaHub Master Architecture Reconstruction

Date: 2026-09-05
Status: DRAFT — NOT ACCEPTED

## 1. Architectural proposition

MediaHub is one system with one user-facing model. Internal implementation is capability-centric and contract-driven. Domain services may be distributed across processes, nodes or variants, but this distribution is never allowed to redefine the product model.

## 2. Control plane

### State Authority
Owns canonical state semantics and state transitions. It does not imply trust or authorization.

### Security / Identity / Trust
Identity, authentication, authorization and trust are separate concerns. Every privileged operation is authenticated and authorized. Discovery, physical connection, presence, health or readiness cannot grant rights.

### Consumer Boundary
Separates ordinary user surfaces from engineering/installer/operator and Cloud Development privileges.

## 3. Runtime capability planes

- Smart Home & Device Plane: Home Assistant internally, vendor/protocol adapters, unified device/function model.
- Automation & Scheduling Plane: triggers, conditions, scenes, schedules, execution history.
- Surveillance Plane: discovery, live, direct recording, archive, playback, events, authorized export.
- Media Plane: ingestion, Personal Media Library, playback, streaming, live media, transcoding, HDMI, audio and mobile endpoints.
- Energy & Engineering Plane: energy infrastructure plus Professional Engineering/Digital Twin/project lifecycle.
- Network Plane: Ethernet/Wi-Fi/VPN, Keenetic/Ubiquiti integration and supported network extension.
- Cluster Plane: local node membership, workload scheduling, distributed processing/storage/media and degraded operation.
- Assistant & Knowledge Plane: Local Assistant, search, metadata, Knowledge Graph and controlled cloud escalation.
- Lifecycle Plane: diagnostics, telemetry, health/readiness, update, recovery, backup/restore and migration.

## 4. Storage architecture

Logical domains are mandatory:
1. System Storage
2. Surveillance Recording Storage
3. Personal Media Library Storage

Physical disks/pools may vary by product variant, but logical isolation, retention, authorization, recovery and capacity semantics remain distinct.

## 5. Local/cloud architecture

Local MediaHub Runtime is primary. Local Assistant first attempts local execution. Cloud Development is a separate privileged environment. Cloud escalation is controlled by contract and never grants ordinary-user access to Cloud Development.

## 6. Cluster architecture

Local MediaHub Cluster is a single coordinated MediaHub system. Nodes can share compute, AI, media processing, transcoding, storage, streaming, automation and redundancy/failover where supported. User intent targets capabilities/results, not nodes.

Cloud Development Cluster is separate in trust, identity, authorization and governance.

## 7. User surfaces

- Ordinary MediaHub UI
- Advanced/Engineering UI
- Installer UI
- Professional Engineering Edition
- User mobile client
- Privileged Developer/Operator tools

Home Assistant UI and internal service UIs are not ordinary user surfaces.

## 8. Variant architecture

Full Mac mini and Full mini PC expose the full product capability envelope subject to hardware. Simplified Raspberry Pi excludes local hard-disk surveillance recording and local Personal Media Library storage. iOS/iPadOS object variant excludes those local hard-disk capabilities and is constrained by platform execution/storage/network rules. Professional Engineering is a separate role/product contour.

## 9. Integration architecture

Vendor/protocol integration is an internal adapter concern. Canonical capability identity remains MediaHub-owned. First-class evidence includes KINCONY/KCS, Dahua, Hikvision, Ajax, KNX, DALI, RS-485, Centrsvet, Arlight, Maytoni, Keenetic, Ubiquiti, Loxone, HomeKit and Yandex Alice.

## 10. Safety/security architecture

Defense-in-depth spans devices, users, network, remote access, data, automation, cluster, integrations, updates, recovery and privileged development infrastructure. Unknown/untrusted equipment is isolated until trusted/enrolled according to policy. Security is not a deferred feature even where exact cryptographic/protocol choices are deferred.

## 11. Architecture status

This is the reconstructed master architecture draft derived from the accepted functional baseline and currently accessible historical evidence. It is implementation-ready in boundary intent but NOT implementation authorization and NOT user-accepted architecture.

Open reconciliation remains mandatory for exhaustive MH-01…MH-23 historical corpus coverage and exact technical contracts.
