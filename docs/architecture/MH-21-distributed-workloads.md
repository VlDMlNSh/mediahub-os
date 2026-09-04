# MH-21 Distributed Workloads

Status: PROPOSED.

Distributed workers may compute bounded jobs and return results. They must not create distributed canonical state. Canonical flow is Distributed Compute → Result → Local Validation → Local Authority. Single-node/no-HA remains baseline; Docker replicas are not physical nodes or HA.