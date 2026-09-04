# MH-03 Startup Sequence

1. OS launches runtime bootstrap.
2. Load minimal runtime configuration.
3. Validate configuration; malformed configuration blocks readiness.
4. Establish trust/security context.
5. Initialize the in-memory State Authority according to P0-04.
6. Initialize Core Runtime Services under P0-06.
7. Resolve dependency graph and initialize critical dependencies.
8. Initialize governed consumer/integration interaction.
9. Initialize command execution and event propagation.
10. Initialize bounded health/observability.
11. Execute readiness checks.
12. Enter READY or controlled DEGRADED state.

No startup step creates a second state store or bypasses P0-05.
