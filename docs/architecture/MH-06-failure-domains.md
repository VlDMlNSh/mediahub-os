# MH-06 — Failure Domains

Status: PROPOSED

Domains: individual task, service, dependency group, runtime, host, storage, network, external service.

Each domain requires a defined blast radius and containment behavior. A consumer/service failure must not silently corrupt canonical state. Supervisor, scheduler, health or recovery failure must not automatically imply State Authority corruption or authority escalation.

Single-node / no-HA remains the reliability baseline. Clustering, consensus and distributed State Authority are out of scope without ADR.
