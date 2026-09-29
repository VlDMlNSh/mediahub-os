# Compute Fabric qualification matrix

Date: 2026-09-29

## Evidence-driven assessment

### Ray
Ray is explicitly designed to scale Python and AI applications from a laptop to clusters. It provides tasks, actors, resource management and AI-oriented libraries. Ray documents node/task/actor fault tolerance and heterogeneous CPU/GPU data workloads.

Assessment: PRIMARY COMPUTE-FABRIC CANDIDATE for MediaHub AI/data workloads.

Required PoC gates:
- heterogeneous CPU/GPU scheduling;
- task retry after worker failure;
- data locality;
- resource isolation;
- network overhead;
- operation across the planned Development Mesh;
- no persistent provider credentials on workers.

### Nomad
Nomad is a general distributed scheduler for services and batch workloads. Its device-plugin model exposes hardware such as GPUs to the scheduler and supports device constraints/affinity including vendor, model and memory attributes. Nomad also provides multi-region federation and failure handling.

Assessment: PRIMARY INFRASTRUCTURE-SCHEDULER CANDIDATE if MediaHub needs heterogeneous general-purpose workloads in addition to AI.

### OpenFabric
OpenFabric is a lightweight decentralized compute mesh using libp2p/mDNS and supports local heterogeneous nodes. Its current project explicitly states that VRAM is not pooled transparently across GPUs; inference jobs are routed to a single suitable GPU node.

Assessment: RAPID-FEASIBILITY CANDIDATE, not a transparent multi-GPU fabric.

### Dask
Dask remains a candidate for Python/data workloads and explicit distributed task execution, but is not currently the leading general infrastructure scheduler for the MediaHub architecture.

Assessment: SECONDARY DATA/COMPUTE CANDIDATE.

## Architecture consequence

Do not force one scheduler to solve every layer.

Provisional target:

Development Mesh
  -> node connectivity / identity / ACL

Compute Fabric
  -> Ray for AI/data workloads
  -> Nomad only if general infrastructure scheduling is required

Storage Fabric
  -> SeaweedFS or JuiceFS

Media Transport
  -> QUIC/iroh PoC

Control Plane
  -> GitHub/Astra

AI Gateway
  -> OmniRoute

The final stack must be selected by benchmark evidence rather than feature count.

## Safety and isolation constraints

- Do not deploy these candidates to canonical mh-dev-01 during research.
- GOLD #176 remains untouched.
- R4 baseline remains immutable.
- GitHub Secrets remains the canonical credential store.
- No provider credential may become persistent on compute nodes.
- Media Mesh is not a VPN workaround for provider regional restrictions.
