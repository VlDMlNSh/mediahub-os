# Media Mesh / Compute Fabric qualification checkpoint

Date: 2026-09-29

## Scope

This checkpoint extends the MediaHub network-plane separation already recorded in:
- 6cef62ff0d5ceed32d1c5a919c41da378b22da16

It does not deploy or modify the canonical Astra node and does not alter GOLD #176.

## Architectural separation

1. Control Plane
   - GitHub / GitHub Actions / Astra / GitHub Secrets.
2. Development Mesh
   - VPN bridge, node discovery, ACL, remote development workers and artifact transport.
3. Media Mesh
   - high-throughput media data plane.
4. Compute Fabric
   - distributed CPU/GPU scheduling and execution.
5. Storage Fabric
   - distributed media storage.
6. AI Gateway
   - OmniRoute first; alternatives remain candidates.

The Development Mesh is not the Media Mesh and is not the storage or compute substrate.

## Compute Fabric candidates investigated

### OpenFabric

OpenFabric is a promising experimental candidate for the personal/distributed compute layer. Its public project describes decentralized P2P discovery, resource-aware scheduling, pooled resource visibility, shared file synchronization and self-healing task rescheduling across macOS, Linux, Windows and Raspberry Pi.

Important limitation: OpenFabric does not pool VRAM across GPUs; an inference job is routed to one GPU node. Therefore it should be treated as a candidate compute scheduler/orchestrator, not as transparent multi-GPU memory aggregation.

Qualification status: CANDIDATE / NOT QUALIFIED.

### Ray

Ray is a mature distributed compute framework for Python and AI workloads. It provides tasks, actors, resource management, GPU-aware scheduling, distributed data processing and cluster execution.

Ray is a stronger candidate than OpenFabric for a production-oriented Compute Fabric where workloads can be expressed as distributed tasks/actors.

Qualification status: CANDIDATE / NOT QUALIFIED.

### Nomad

Nomad provides general workload scheduling, resource placement, device plugins and GPU scheduling, including an NVIDIA device plugin. It is more infrastructure-oriented than Ray.

It is a candidate if MediaHub needs general heterogeneous workload orchestration rather than primarily Python/AI execution.

Qualification status: CANDIDATE / NOT QUALIFIED.

### Dask

Dask provides a distributed task scheduler and explicit resource constraints, including user-defined GPU resources. It is useful for Python/data workloads but requires stronger environment consistency across scheduler and workers than a simple heterogeneous node pool implies.

Qualification status: CANDIDATE / NOT QUALIFIED.

## Preliminary architecture decision

Do not install Kubernetes, Nomad, Ray, Dask or OpenFabric on mh-dev-01 during this research phase.

The preferred qualification sequence is:

1. OpenFabric — rapid feasibility benchmark.
2. Ray — distributed AI/compute benchmark.
3. Nomad — heterogeneous infrastructure scheduling benchmark.
4. Dask — Python/data workload benchmark.

The winner is not selected by feature count. Each candidate must pass measurable tests for:
- node discovery;
- heterogeneous CPU/GPU capability reporting;
- task scheduling;
- node failure and task recovery;
- network overhead;
- data locality;
- throughput;
- resource isolation;
- security/identity;
- compatibility with the separate Development Mesh;
- ability to operate without storing MediaHub AI credentials on worker nodes.

## Storage integration target

Compute Fabric must not own canonical media persistence.

Storage remains a separate layer, with SeaweedFS and JuiceFS currently retained as storage candidates.

## Transport integration target

The Media Mesh transport remains a separate concern. QUIC/iroh is a candidate data-plane transport and is not being treated as a VPN replacement.

## Security invariant

All provider/API secrets remain exclusively in GitHub Secrets. Compute nodes must receive only ephemeral runtime material when an actual qualified workflow requires it; no persistent provider credentials are to be stored on nodes, in repositories, images, logs or artifacts.

## Immutable constraints

- GOLD #176 remains untouched.
- Canonical Astra worker remains untouched.
- R4 baseline 471f709f5633feab7aeb62dd3ea52effad6d2bc584 remains immutable.
- Desktop Commander remains prohibited.
- No VPN/mesh component is to be used as a mechanism to circumvent provider regional restrictions.

## Next qualification pass

Build an isolated, non-canonical benchmark plan for Compute Fabric candidates and Storage Fabric candidates. Do not deploy to mh-dev-01 until explicit deployment authorization is given and the benchmark design has been reviewed.
