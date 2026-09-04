# MH-17 — Device Privacy

**Status:** PROPOSED / CANDIDATE

Device telemetry, identifiers, topology, occupancy-like signals, logs, and command history are treated according to data classification and least-privilege rules. Collection MUST be purpose-bound and minimized.

Persistent identifiers SHOULD be separated from transient locators where practical. Sensitive telemetry MUST NOT be exposed to plugins, AI, UI, cloud, or observability consumers beyond their authorized contract.

Privacy requirements do not weaken safety, security, audit, or State Authority invariants. Retention and deletion policies remain subject to MH-13 and Persistence governance.
