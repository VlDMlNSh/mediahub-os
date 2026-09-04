# MH-11 Contradiction Register

Status: OPEN / REQUIRES VERIFICATION

| ID | Potential contradiction | Authority involved | Status | Required action |
|---|---|---|---|---|
| C-01 | Observability mutation could bypass P0-03 | P0-03 | REQUIRES VERIFICATION | inspect implementation/contracts |
| C-02 | Diagnostic storage could become hidden persistence | P0-04 | REQUIRES VERIFICATION | persistence/capability scan |
| C-03 | Health could become second lifecycle authority | MH-6 | REQUIRES VERIFICATION | compare frozen lifecycle contract |
| C-04 | Audit and diagnostic events conflated | MH-4 / MH-11 | REQUIRES VERIFICATION | contract separation |
| C-05 | AI diagnostic recommendation treated as authority/evidence | MH-10 | REQUIRES VERIFICATION | provenance + authority review |
| C-06 | Plugin diagnostics exceed capability grant | MH-8 | REQUIRES VERIFICATION | capability review |
| C-07 | Cloud telemetry treated as trusted authority | MH-4 | REQUIRES VERIFICATION | trust-boundary review |
| C-08 | Debug facilities bypass authorization | MH-4 | REQUIRES VERIFICATION | security test |
| C-09 | P0-07 diagnostic UI exposes mutation before publication authority | P0-07 | REQUIRES VERIFICATION | contract/API review |
| C-10 | Monitoring/self-healing creates hidden mutation | MH-6/MH-7 | REQUIRES VERIFICATION | policy/authorization path review |

Rule: if a real conflict with frozen P0-03…P0-06 is discovered, STOP implementation and request governance decision.
