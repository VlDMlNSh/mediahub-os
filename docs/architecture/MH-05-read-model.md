# MH-5 — Read Model

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

Canonical reads follow:

```text
Consumer → authorized read → immutable value representation
```

A read MUST NOT expose mutable references, internal object identity, transaction internals, State Authority objects, private runtime structures, secrets, or hidden capability material.

Reads are snapshot/value based. The consumer receives one bounded, internally consistent representation for the selected read operation. Read authorization is distinct from mutation authorization.

Snapshot freshness and consistency are operation-specific. Stale data may be reported as stale where required, but a read must never silently acquire write authority. Large representations require bounded retrieval and, where later justified, pagination/chunking under an explicit contract.
