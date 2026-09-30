# MediaHub Hierarchical Cluster Architecture

Date: 2026-09-30

## Architectural correction

MediaHub is a hierarchical/federated distributed-compute system, not one flat global VPN network.

The architecture has two primary deployment domains:

1. Local MediaHub Cluster
   - assembled inside the user's local network;
   - optimized for local media, storage and compute;
   - uses direct LAN/P2P data paths;
   - does not require VPN for normal media traffic;
   - may contribute otherwise free/idle compute capacity to the MediaHub developer compute fabric through the external federation path.

2. Cloud Development Cluster
   - permanently available in an external/cloud network;
   - provides development, CI, remote compute, shared engineering storage and distributed development infrastructure;
   - uses a managed encrypted Development Mesh for management connectivity;
   - direct P2P is preferred, with relay/fallback only when required;
   - acts as the coordinating development-side compute domain for contributed MediaHub capacity.

## Distributed development compute fabric

A core architectural property is that MediaHub devices can contribute available, otherwise unused compute capacity to the developer-side distributed compute fabric.

The intended topology is:

MediaHub devices
  -> local MediaHub clusters
  -> external federation/compute contribution path
  -> Cloud Development Cluster
  -> developer scheduler / distributed execution fabric

The result is a heterogeneous distributed development computer assembled from:

- developer servers;
- MediaHub nodes;
- available CPU/GPU/NPU capacity on participating MediaHub devices;
- other explicitly admitted development compute resources.

This fabric is intended to provide a substantially larger aggregate development compute capacity than the permanently provisioned developer servers alone.

The contribution of compute capacity does not mean that a MediaHub device becomes a permanent member of the Cloud Development Cluster. The device remains part of its local MediaHub Cluster and contributes bounded compute resources through a separately controlled execution relationship.

## Compute contribution boundary

Compute contribution is distinct from user-data federation.

A contributing MediaHub node exposes only an explicitly schedulable compute capability. It does not automatically expose:

- the user's media library;
- local storage;
- local credentials;
- local network services;
- arbitrary local processes;
- unrestricted inbound access.

The scheduler must treat compute capacity as a leased, capability-scoped resource.

A compute contribution request therefore requires:

1. node identity;
2. trust verification;
3. advertised compute capabilities;
4. resource availability;
5. workload classification;
6. explicit job admission;
7. bounded resource lease;
8. execution isolation;
9. result/evidence reporting;
10. lease termination and resource release.

## Data locality

Compute may travel to data, or bounded data may travel to compute, depending on workload policy.

For user-owned data, local execution remains preferred.

For developer workloads, source code, build artifacts, model shards, datasets and other engineering inputs may be distributed to admitted compute contributors when the workload contract permits it.

A compute contributor must not receive more data than the admitted job requires.

## Federation

Local clusters and the Cloud Development Cluster are connected by a separate Federation/Sync Layer.

The local cluster should not become a permanently full-tunnel VPN extension of the cloud cluster.

Cross-domain traffic is selective and policy-controlled:

- compute-job admission;
- bounded workload transfer;
- execution metadata;
- bounded results;
- synchronization;
- backup;
- explicitly selected media objects;
- remote processing inputs/outputs;
- development artifacts.

Local media remains local unless policy explicitly requires transfer.

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
Distributed scheduling and execution across admitted developer servers and contributed MediaHub compute resources.

### API Egress
Separate policy-controlled path for approved external API destinations.

### Compute Contribution Plane
Request-scoped control and workload transport used to contribute available MediaHub compute to the developer-side compute fabric.

The Compute Contribution Plane must not become a general-purpose bridge into the user's local network.

## Local cluster networking

Preferred path:
LAN Ethernet/Wi-Fi direct.

VPN is not required for ordinary local media/storage/compute traffic.

When a MediaHub node contributes compute externally, only the required federation/compute-control and workload paths are opened for the admitted job.

## Cloud cluster networking

Preferred path:
direct P2P between authorized nodes.

Fallback:
relay only when direct connectivity is unavailable.

The cloud development network coordinates the aggregate compute fabric but does not acquire unrestricted access to contributing local networks.

## Cross-domain rule

Local-to-cloud connectivity must be explicit and selective.

The external compute contribution mechanism must not replace the local data plane with a global VPN.

Compute contribution and user-data federation are separate authorization domains.

## Scheduler implication

Scheduling is cluster-aware and resource-aware.

A job should declare:

- workload class;
- originating domain;
- locality requirements;
- CPU/GPU/NPU requirements;
- memory/storage requirements;
- maximum execution lease;
- network requirements;
- data-transfer limits;
- result limits;
- whether contributed MediaHub compute is eligible.

The scheduler should prefer:

1. local execution when required or efficient;
2. developer-server execution for company workloads;
3. admitted contributed MediaHub compute when additional capacity is useful;
4. distributed execution across multiple contributors when the workload supports partitioning.

Large local datasets should preferably be processed where the data resides, avoiding unnecessary WAN transfer.

## Security invariants

- Provider credentials remain exclusively in GitHub Secrets.
- Credentials are never included in node capability metadata.
- Development Mesh does not imply access to Media Data Plane.
- Compute contribution does not imply storage or network access.
- Every contributed compute job has explicit identity, scope and lease.
- A contributor can revoke/lose execution authority when the lease expires.
- A developer workload cannot enumerate arbitrary user-local resources.
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

1. cluster identity and trust PoC;
2. workload classification and admission PoC;
3. compute capability advertisement PoC;
4. compute contribution lease PoC;
5. developer scheduler simulation;
6. Development Mesh PoC;
7. Media Transport direct/relay benchmark;
8. Storage Fabric benchmark;
9. Compute Fabric benchmark;
10. local MediaHub compute-contributor PoC;
11. Cloud Development Cluster PoC;
12. distributed developer compute PoC;
13. federation/sync PoC;
14. end-to-end MediaHub distributed-development qualification.

## Scope and safety

This checkpoint records architecture and qualification direction only.

It does not authorize deployment to mh-dev-01.

GOLD #176 remains untouched.

Immutable R4 baseline remains untouched.

No production credentials are introduced or moved.
