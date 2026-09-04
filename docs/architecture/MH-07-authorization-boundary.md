# MH-7 — Authorization Boundary

Status: CANDIDATE / BLOCKED FOR PUBLICATION

Policy admissibility and principal authorization are separate gates. Authorization answers whether a principal may perform a concrete operation; policy answers whether that operation is admissible under policy.

The effective authorization condition is conjunctive with the independently required P0-05/P0-04 authorization.

P0-07 capabilities cannot self-grant authority and are never silently translated into lower-layer capabilities.

## Publication blocker
Current P0-07 mutation publication is BLOCKED by the P0-07→P0-05 governance/API composition gap. Approved resolution classes are:
1. existing-context model;
2. explicit governance-approved authorization bridge;
3. revised P0-05 contract.

P0-03…P0-06 must not be changed merely to bypass this blocker.
