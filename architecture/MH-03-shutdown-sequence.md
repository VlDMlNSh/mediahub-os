# MH-03 Shutdown Sequence

**Status:** PROPOSED

1. Enter STOPPING; advertise non-readiness.
2. Stop accepting new work.
3. Drain or cancel in-flight operations according to their contracts.
4. Emit required lifecycle/diagnostic observations.
5. Stop integration/consumer activity.
6. Stop dependent runtime services in reverse dependency order.
7. Stop supervision/event dispatch where safe.
8. Close runtime resources.
9. Terminate runtime and enter STOPPED.

Shutdown must not introduce a new mutation path and must not make persistence authoritative.
