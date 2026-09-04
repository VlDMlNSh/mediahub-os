# MH-18 — Storage
Status: PROPOSED / NOT ACCEPTED

Separate canonical metadata/state, content bytes, derived artifacts and cache. Media filesystem/object store is never domain authority. Candidate backends: local filesystem, removable media, NAS/network storage, object storage and cloud object storage. Selection requires requirements, security, reliability, performance and ADR.