# MediaHub Hierarchical Cluster Architecture

Date: 2026-09-30

## Architectural correction

MediaHub is a hierarchical/federated cluster system, not one flat global VPN network.

The architecture has two primary deployment domains:

1. Local MediaHub Cluster
   - assembled inside the user's local network;
   - optimized for local media, storage and compute;
   - uses direct LAN/P2P data paths;
   - does not require VPN for normal media traffic.

2. Cloud Development Cluster
   - permanently available in an external/cloud network;
   - provides development, CI, remote compute, shared storage and distributed development infrastructure;
   - uses a managed encrypted Development Mesh for management connectivity;
   - direct P2P is preferred, with relay/fallback only when required.

## Federation

Local clusters and the Cloud Development Cluster are connected by a separate Federation/Sync Layer.

The local cluster should not become a permanently full-tunnel VPN extension of the cloud cluster.

Cross-domain traffic is selective and policy-controlled:
- synchronization;
- backup;
- explicitly selected media objects;
- remote processing inputs/outputs;
- metadata;
- development artifacts.

Local media remains local unless policy requires transfer.

## Plane separation

Each domain keeps separate logical planes:

### Control Plane
GitHub/Astra and cluster control metadata.

### Development Mesh
Encrypted management/discovery connectivity.

### Media Data Plane
Direct/high-speed data transfer preferred.

### Storage Fabric
Distributed storage inside the relevant cluster.

### Compute Fabric
Resource scheduling and execution inside the relevant cluster.

### API Egress
Separate policy-controlled path for approved external API destinations.

## Local cluster networking

Preferred path:
LAN Ethernet/Wi-Fi direct.

VPN is not required for ordinary local media/storage/compute traffic.

## Cloud cluster networking

Preferred path:
direct P2P between authorized nodes.

Fallback:
relay only when direct connectivity is unavailable.

## Cross-domain rule

Local-to-cloud connectivity must be explicit and selective. It must not replace the local data plane with a global VPN.

## Future federation model

Conceptually:

MediaHub Federation
  -> Local Cluster A
  -> Local Cluster B
  -> Cloud Development Cluster
  -> optional additional cloud/edge clusters

Each cluster maintains local resource and data-plane autonomy.

## Scheduler implication

Scheduling is cluster-aware.

A job should declare whether it is:
- local-cluster eligible;
- cloud-cluster eligible;
- federation eligible.

Large local datasets should preferably be processed in the cluster where the data resides, avoiding unnecessary WAN transfer.

## Security invariants

- Provider credentials remain exclusively in GitHub Secrets.
- Credentials are never included in node capability metadata.
- Development Mesh does not imply access to Media Data Plane.
- External API routing must respect provider access restrictions.
- No VPN mechanism is to be used to bypass regional/provider restrictions.

## Current component mapping

Local/Cloud Network:
- Development Mesh: Netmaker candidate;
- direct Media Transport: separate qualification required.

Compute:
- Ray primary PoC candidate;
- Nomad secondary infrastructure scheduler;
- OpenFabric feasibility candidate.

Storage:
- SeaweedFS primary local-disk-oriented candidate;
- JuiceFS secondary object-storage-oriented candidate.

AI Gateway:
- OmniRoute candidate/installed local component.

Control:
- GitHub + Astra.

## Qualification sequence

1. non-canonical schema/scheduler simulator;
2. Development Mesh PoC;
3. Media Transport direct/relay benchmark;
4. Storage Fabric benchmark;
5. Compute Fabric benchmark;
6. Local cluster PoC;
7. Cloud Development Cluster PoC;
8. federation/sync PoC;
9. end-to-end MediaHub cluster qualification.

## Scope and safety

This checkpoint records architecture only.

It does not authorize deployment to mh-dev-01.

GOLD #176 remains untouched.

Immutable R4 baseline remains untouched.

No production credentials are introduced or moved.
