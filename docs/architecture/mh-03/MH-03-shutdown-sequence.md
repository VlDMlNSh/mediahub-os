# MH-03 Shutdown Sequence

1. Enter STOPPING and reject new work admission.
2. Mark readiness false.
3. Complete or cancel bounded in-flight operations according to their contracts.
4. Preserve canonical state semantics; no shutdown shortcut may mutate outside State Authority.
5. Emit required lifecycle facts and bounded diagnostics.
6. Stop dependent services in reverse dependency order.
7. Stop remaining Core Runtime Services.
8. Terminate Runtime cleanly and enter STOPPED.

If a service fails during shutdown, continue controlled shutdown where safe; do not invent a fallback authority.
