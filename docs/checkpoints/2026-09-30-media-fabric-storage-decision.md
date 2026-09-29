# Media Fabric Storage Direction

Date: 2026-09-30

## Decision status

This is a qualification checkpoint, not a production deployment decision.

### SeaweedFS

Current primary candidate for the MediaHub Storage Fabric.

Reasons:
- a single distributed system exposes S3, POSIX and lakehouse interfaces over the same underlying data;
- capacity scales by adding volume servers;
- S3/filer gateways are stateless and can scale horizontally;
- the project supports cross-cluster active-active and active-passive replication;
- Linux, macOS and Windows access paths are available;
- TLS/mTLS and encryption-at-rest capabilities exist.

The architecture is a strong match for a MediaHub fabric in which participating machines contribute local storage.

Remaining qualification gates:
- WAN throughput;
- failure/rebuild behavior;
- replication bandwidth;
- small-file behavior;
- large sequential media transfer;
- disk heterogeneity;
- node churn;
- resource overhead;
- security and credential handling.

Status: PRIMARY CANDIDATE / NOT QUALIFIED.

### JuiceFS

Secondary candidate.

JuiceFS separates metadata from file data. File data is stored in object storage while metadata is maintained by a supported metadata engine. The client communicates with both. Community Edition supports metadata engines including Redis, MySQL, PostgreSQL, TiKV and SQLite.

The architecture is attractive when MediaHub wants:
- POSIX semantics over object storage;
- independent scaling of data and metadata;
- Python/fsspec integration for data/AI workloads.

It is less directly aligned with the initial requirement of pooling arbitrary participating machines' local disks into one storage fabric, because an object-storage layer and metadata engine become architectural dependencies.

Status: SECONDARY CANDIDATE / NOT QUALIFIED.

## Revised storage hypothesis

Initial MediaHub Storage Fabric hypothesis:

Participating node local disks
        -> Storage Fabric
        -> distributed placement/replication
        -> S3/POSIX access
        -> Compute Fabric data locality

SeaweedFS is the first implementation to benchmark for this hypothesis.

JuiceFS remains the alternative if the benchmark shows that object-storage-backed POSIX semantics are more valuable than direct local-disk federation.

## Transport boundary

Storage Fabric must not be responsible for Development Mesh connectivity.

Media Transport remains an independent layer. The transport benchmark must measure direct path, relay fallback, throughput, latency, loss recovery and node churn.

## No deployment

No storage or transport candidate is authorized for installation on canonical mh-dev-01 by this checkpoint.

GOLD #176, canonical Astra worker and immutable R4 baseline remain untouched.
