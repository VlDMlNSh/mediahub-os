# MH-06 — Resource Governance

Status: PROPOSED; numeric limits UNKNOWN.

Resource classes: CPU, memory, storage, file descriptors, network, IPC, task concurrency, queue depth.

For each class define admission, bound, exhaustion response, degradation and recovery. Concrete limits require host/hardware evidence and later governance. Resource exhaustion must not cause privilege escalation or hidden persistence.
