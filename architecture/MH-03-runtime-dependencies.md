# MH-03 Runtime Dependencies

**Status:** PROPOSED

Dependency principles:
- State Authority is a critical dependency for canonical mutation.
- Core Runtime Services depend on the lifecycle foundation.
- Consumer/Integration Boundary is initialized only after required runtime foundations are ready.
- Optional cloud, AI, RAG and external knowledge services must not be hard dependencies of deterministic core operation.
- Dependency readiness is not authorization.
- Dependency failure is isolated where safe; critical failure blocks readiness or causes controlled degraded operation.

Technology-specific dependency choices remain CANDIDATE.
