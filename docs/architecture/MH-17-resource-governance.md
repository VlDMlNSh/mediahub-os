# MH-17 — Resource Governance

**Status:** PROPOSED / CANDIDATE

Integration components MUST have bounded CPU, memory, queue, connection, socket, retry, timeout, payload, subscription, and concurrency budgets. External device input is untrusted for resource accounting.

Budgets are enforced before unbounded work. Per-device, per-adapter, and global limits may coexist. Resource exhaustion MUST degrade or quarantine the affected integration path rather than compromise State Authority or unrelated devices.

No specific numeric limits are frozen until target hardware and protocol evidence exist.
