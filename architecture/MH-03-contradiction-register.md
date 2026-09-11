# MH-03 Contradiction Register

**Status:** PROPOSED

The current pass identified one governance-level contradiction requiring explicit classification.

| ID | Risk | Resolution | Status |
|---|---|---|---|
| C03-01 | Runtime mistaken for State Authority | explicit boundary | RESOLVED BY BOUNDARY |
| C03-02 | Runtime cache becomes shadow state | prohibited | RESOLVED |
| C03-03 | Event-driven reaction bypasses command path | re-enter governed command path | RESOLVED |
| C03-04 | Supervisor gains excessive authority | bounded lifecycle authority | OPEN FOR REVIEW |
| C03-05 | Persistence becomes hidden authority | prohibited/deferred | RESOLVED |
| C03-06 | Cloud fallback becomes authority | prohibited | RESOLVED |
| C03-07 | AI bypasses authorization | proposal only | RESOLVED |
| C03-08 | Proposed PostgreSQL/etcd/NATS HA path conflicts with frozen P0-04 single-node/in-memory foundation | reclassify as future governance-gated extension; no current activation | GOVERNANCE REVIEW REQUIRED |

C03-08 is not an implementation defect. It is an architectural change request against the frozen foundation and therefore cannot be silently activated.

Any future conflict with a parent frozen decision requires: CONTRADICTION / GOVERNANCE CHANGE REQUIRED.
