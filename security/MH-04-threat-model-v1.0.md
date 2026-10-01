# MH-04 State Authority Threat Model v1.0

Status: PROPOSED / VERIFICATION REQUIRED

## Assets
- canonical state
- authorization context
- command identity/correlation
- transaction state
- checkpoint authority binding
- emitted state-change events
- evidence records

## Trust boundaries
1. external/remote consumer → Consumer Boundary
2. Consumer Boundary → Authorization/Policy
3. Authorization/Policy → State Authority
4. State Authority → canonical state/event stream
5. observers → read-only observation/evidence

## Threats and controls
| Threat | Required control |
|---|---|
| unauthorized mutation | authenticated context + explicit authorization + deny-by-default |
| command replay | command identity/idempotency semantics |
| stale writer | generation/state-version validation |
| forged checkpoint | authority-bound checkpoint token + compatibility validation |
| shadow authority | single State Authority invariant + negative tests |
| event bypass | events are facts; mutation re-enters governed command path |
| remote escalation | remote access never increases authorization |
| read-side mutation | immutable/read-isolated snapshots |
| integrity failure | fail closed; no canonical publication |
| evidence spoofing | exact SHA/environment/command identity and reproducible evidence |
| secret leakage | no secrets in source, logs or evidence artifacts |

## Security acceptance
No threat is considered closed from source inspection alone. Runtime execution and independent security testing are required.
