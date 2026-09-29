# Storage Fabric and Media Transport qualification checkpoint

Date: 2026-09-29

## Storage Fabric

### SeaweedFS

Current leading storage candidate for the MediaHub Media Fabric.

Evidence from the upstream project:
- one weed binary can expose S3 object storage, POSIX filesystem and lakehouse interfaces;
- storage capacity scales by adding volume servers;
- master servers track volume locations and are not in the normal read path after lookup;
- filer and S3 gateways are stateless and can scale horizontally;
- replication can be rack/data-center aware;
- active-active and active-passive cross-cluster replication are supported;
- TLS/mTLS and encryption-at-rest capabilities are available.

Architecture fit:
- strong fit for local-disk-first distributed media storage;
- strong fit for heterogeneous machines contributing storage;
- S3 compatibility gives MediaHub an application-facing object interface;
- requires benchmark validation of WAN behavior, recovery, replication cost and metadata behavior.

Status: PRIMARY STORAGE CANDIDATE / NOT QUALIFIED.

### JuiceFS

JuiceFS is a distributed POSIX filesystem separating file data from metadata. File data is stored in object storage while metadata is handled by a dedicated metadata engine. The client communicates with both.

Important MediaHub implication:
- JuiceFS is especially attractive if MediaHub wants an object-storage-backed POSIX filesystem;
- it introduces a dependency on both object storage and a metadata engine;
- the architecture is not equivalent to simply pooling local disks directly.

JuiceFS also exposes a Python SDK/fsspec integration that can integrate with frameworks such as Ray.

Status: SECONDARY STORAGE CANDIDATE / NOT QUALIFIED.

## Preliminary storage direction

SeaweedFS should receive the first isolated benchmark because MediaHub's target is a distributed media data plane composed of participating machines and their local disks.

JuiceFS remains the alternative where object-storage-backed POSIX semantics become more important.

No production deployment is authorized by this checkpoint.

## Media Transport

QUIC/iroh remains the transport candidate for a future high-throughput P2P Media Data Plane.

Transport qualification must measure:
- direct connection establishment;
- relay fallback;
- throughput;
- latency;
- packet loss recovery;
- concurrent streams;
- large-file transfer;
- node churn;
- NAT traversal;
- CPU overhead.

Transport must remain independent from Development Mesh management.

## Target layering

Development Mesh
  -> secure management connectivity / identity / ACL

Media Transport
  -> direct-first high-throughput P2P data movement

Storage Fabric
  -> SeaweedFS first; JuiceFS alternative

Compute Fabric
  -> Ray first; Nomad/OpenFabric/Dask alternatives

Control Plane
  -> GitHub / Astra / GitHub Secrets

AI Gateway
  -> OmniRoute

## Constraints

- Do not deploy candidates to canonical mh-dev-01 during research.
- GOLD #176 remains untouched.
- R4 baseline remains immutable.
- Provider/API credentials remain exclusively in GitHub Secrets.
- No transport or mesh mechanism is to be used to circumvent provider regional restrictions.

## Next step

Create a non-canonical benchmark specification for SeaweedFS, JuiceFS and the selected P2P transport. The benchmark should use synthetic/non-sensitive test data and report reproducible throughput, latency, recovery and resource-overhead measurements.
