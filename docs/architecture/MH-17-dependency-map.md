# MH-17 — Dependency Map

**Status:** PROPOSED / CANDIDATE

Core dependency direction:

`Device/External World → Protocol Adapter → Integration Boundary → Normalization → Capability Model → Authorization/Policy → Command Boundary → State Authority → Canonical Runtime State`

Consumers such as UI, Automation, AI, Plugins, Cloud, and Observability interact through their approved contracts and do not bypass authorization or State Authority.

Dependencies on MH-01…MH-16 and P0-03…P0-07 are architectural constraints, not evidence of implementation. Concrete framework/library dependencies require separate technology evaluation and ADR.
