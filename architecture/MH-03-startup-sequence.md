# MH-03 Startup Sequence

**Status:** PROPOSED

1. OS launches runtime.
2. Bootstrap establishes minimal execution context.
3. Configuration is loaded and validated.
4. Trust/security context is initialized.
5. In-memory State Authority is initialized.
6. Core Runtime Services are initialized.
7. Dependency graph is resolved.
8. Consumer / Integration Boundary is initialized.
9. Command execution and event propagation boundaries are initialized.
10. Health/observability is initialized.
11. Readiness checks execute.
12. Runtime enters READY or controlled DEGRADED/NOT READY state.

No startup step may create a second canonical mutation authority.
