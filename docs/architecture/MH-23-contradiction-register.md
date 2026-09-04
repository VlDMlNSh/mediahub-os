# MH-23 Contradiction Register

| ID | Source | Conflict | Impact | Authority | Decision | Status |
|---|---|---|---|---|---|---|
| CONTRADICTION-001 | requested P0-03 baseline vs current main | baseline declared ACCEPTED/FROZEN but exact canonical file is absent from main evidence | HIGH | P0-03 governance | do not alter frozen claim; reconcile lineage | REQUIRES VERIFICATION |
| CONTRADICTION-002 | migration workflow vs current lineage | smoke workflow pins an older P0-06 SHA rather than current main | HIGH | lifecycle evidence | treat as historical evidence until revalidated | REQUIRES VERIFICATION |
| CONTRADICTION-003 | P0-07 PR/governance vs acceptance state | implementation exists as draft PR and lacks production qualification | HIGH | P0-07 governance | keep NOT ACCEPTED/NOT FROZEN | VERIFIED |
| CONTRADICTION-004 | multiple integration branches vs canonicality | several P0-08 integration/reconciliation candidates coexist | HIGH | repository governance | branch existence never implies canonical status | VERIFIED |

No contradiction is silently resolved.