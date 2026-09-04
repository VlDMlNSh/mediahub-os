# MH-15 — Index

Status: ARCHITECTURE WORK IN PROGRESS

## Canonical artifacts

- `MH-15-ARCHITECTURE-CHAT-CHARTER.md` — scope and governance
- `MH-15-CHAT-MASTER-PROMPT.md` — request to consult MH-15
- `MH-15-REVERSE-MASTER-PROMPT.md` — evidence return contract
- `MH-15-os-appliance-architecture.md` — canonical architecture baseline
- `MH-15-acceptance-criteria.md` — acceptance gate
- `MH-15-evidence-register.md` — evidence status
- `MH-15-unknowns.md` — unresolved properties
- `MH-15-contradiction-register.md` — cross-architecture conflicts
- `MH-15-decision-log.md` — architecture decisions
- `MH-15-dependency-map.md` — upstream/downstream dependencies and traceability rules
- `MH-15-technology-evaluation.md` — candidate host technologies and selection gates
- `MH-15-architecture-audit.md` — completed multi-pass architecture audit

## Topic families

Host boundary; hardware qualification; boot/startup/shutdown; process/service identity; least privilege; systemd; containerization/security; filesystem/storage/temp; device access/security; network/firewall; hardening; CI/build/supply chain; OS/application updates; recovery; kernel; resource governance; thermal/power; time; observability/security events; runtime boundary; failure domains; criticality/self-healing; privileged operations; host admin/shell/secrets; sandboxing; legacy hardware; OS selection/lifecycle; appliance model; development/production; security and hardware testing; technology evaluation; dependency mapping.

## Rule

Topic artifacts are subordinate to the canonical MH-15 baseline and must not contradict frozen MH-1…MH-14 or P0-03…P0-07 without explicit governance.

## Current gate

The architecture baseline is synchronized, internally reconciled and audited, but MH-15 remains NOT ACCEPTED / NOT FROZEN / IMPLEMENTATION NOT AUTHORIZED until the evidence and acceptance criteria are satisfied.
