# MH-22 — Production Gates

| Gate | Transition | Required evidence |
|---|---|---|
| G1 | DESIGN → IMPLEMENTED | implementation identity |
| G2 | IMPLEMENTED → TESTED | reproducible test execution |
| G3 | TESTED → VERIFIED | evidence review against requirements |
| G4 | VERIFIED → QUALIFICATION CANDIDATE | complete release identity |
| G5 | CANDIDATE → QUALIFIED | qualification matrix PASS |
| G6 | QUALIFIED → RELEASED | governance release decision |
| G7 | RELEASED → DEPLOYED | authorized deployment evidence |
| G8 | DEPLOYED → OBSERVED | operational observation evidence |
| G9 | OBSERVED → PRODUCTION ACCEPTED | governance acceptance |

No implicit gate transitions are allowed. Failed or unknown gates stop promotion.
