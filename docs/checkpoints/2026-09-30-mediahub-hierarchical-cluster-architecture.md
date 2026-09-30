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

Developer servers should be treated as interchangeable cluster capacity rather than requiring one permanent "master compute server". Astra and the scheduler are logical cluster services and should be able to continue on any admitted developer node or redundant service set. A developer cluster may therefore start with one available server and expand horizontally as additional developer servers appear.

## Compute contribution boundary

Compute contribution is distinct from user-data federation.

A contributing MediaHub node exposes only an explicitly schedulable compute capability. It does not automatically expose:

- the user's media library;
- personal files or personal data;
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

## Developer privacy boundary

The MediaHub developer/company environment must not provide developers or developer personnel with access to personal user data.

This is a hard architectural invariant, not merely a default preference.

Developer compute may receive an executable workload or privacy-bounded input only when the job contract explicitly permits it. The developer environment must not expose raw personal data to developers, administrative operators, or unrelated development services.

For user-originated cloud escalation:

- the local MediaHub remains the preferred place for processing personal data;
- only the minimum information necessary for the admitted computation may cross the boundary;
- where feasible, computation should use transformed, redacted, encrypted, aggregated, or otherwise privacy-preserving inputs rather than raw personal data;
- job execution identity is not permission to inspect the user's source data;
- logs, metrics, traces and evidence must not contain personal payloads;
- results must be bounded to the requested output;
- access to user-originated execution material expires with the job lease;
- developer personnel do not receive persistent access to the user's data as a consequence of cloud execution.

If a requested computation intrinsically requires raw personal data and the architecture cannot process it without exposing that data to the developer environment, the workload must remain local or be denied/escalated only after an explicit product-level privacy policy is defined. It must never silently become developer-accessible data.

This separation means:

Compute Contribution
  !=
User Data Access
  !=
Developer Personnel Access

A MediaHub node may contribute CPU/GPU/NPU capacity while the developer environment remains unable to inspect the user's personal data.

## Data locality

Compute may travel to data, or bounded transformed data may travel to compute, depending on workload policy.

For user-owned data, local execution remains preferred.

For developer workloads, source code, build artifacts, model shards, datasets and other engineering inputs may be distributed to admitted compute contributors when the workload contract permits it.

For user-originated workloads, personal data must remain local whenever feasible. If bounded input must cross the boundary, it must satisfy the Developer Privacy Boundary above.

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

Local media remains local unless policy explicitly requires transfer and the privacy boundary permits it.

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

### Privacy Boundary
Independent authorization/data-minimization boundary ensuring developer compute and developer personnel do not gain access to personal user data.

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

Developer compute authorization does not imply developer personnel authorization to view user data.

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
- privacy/data-class requirements;
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
- Compute contribution does not imply access to personal user data.
- Developer personnel do not receive access to personal user data.
- Every contributed compute job has explicit identity, scope and lease.
- A contributor can revoke/lose execution authority when the lease expires.
- A developer workload cannot enumerate arbitrary user-local resources.
- User-originated logs/evidence contain no personal payloads.
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
6. privacy/data-boundary PoC;
7. Development Mesh PoC;
8. Media Transport direct/relay benchmark;
9. Storage Fabric benchmark;
10. Compute Fabric benchmark;
11. local MediaHub compute-contributor PoC;
12. Cloud Development Cluster PoC;
13. distributed developer compute PoC;
14. federation/sync PoC;
15. end-to-end MediaHub distributed-development qualification.

## Scope and safety

This checkpoint records architecture and qualification direction only.

It does not authorize deployment to mh-dev-01.

GOLD #176 remains untouched.

Immutable R4 baseline remains untouched.

No production credentials are introduced or moved.
