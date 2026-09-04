# MH-06 — Startup / Shutdown

Status: PROPOSED / REQUIRES VERIFICATION

Conceptual startup: Boot -> Runtime Initialization -> Security Initialization -> State Authority availability -> Core Services -> Dependent Services -> Consumers.

Critical failures fail closed. Partially initialized services are not published as healthy. Destructive recovery is never implicit. Deterministic ordering is required only where dependencies prove it necessary.

Controlled shutdown: stop admission -> reject new work -> handle/cancel in-flight work -> complete or abort transactions according to their contracts -> flush permitted events -> stop observers -> terminate services.

No guarantee of operation completion is made without evidence. Crash/reboot requires fresh initialization, re-authentication and re-establishment of external trust.
