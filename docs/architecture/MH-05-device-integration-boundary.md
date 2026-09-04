# MH-5 — Device / Protocol Integration Boundary

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

```text
Protocol Adapter
 → normalization
 → capability model
 → command/event model
 → authorization
 → Consumer Boundary
 → State Authority
```

Adapters normalize external protocols and device facts. They are not State Authority, cannot directly publish canonical state, cannot self-authorize, and do not receive unrestricted filesystem/network/subprocess primitives.

Unknown devices remain untrusted. Discovery is not authentication; enrollment is not unrestricted authority. Device commands are explicit operations subject to capability and authorization. Device observations become bounded events/data and cannot mutate canonical state merely by arriving.
