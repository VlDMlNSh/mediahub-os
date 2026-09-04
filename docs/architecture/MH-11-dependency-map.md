# MH-11 Dependency Map

Status: PROPOSED

| Authority / architecture | MH-11 relationship |
|---|---|
| MH-1 | governance, product/system charter |
| MH-2 | system boundaries and authority separation |
| MH-3 | runtime foundation observation hooks |
| MH-4 | security, trust, authorization, audit and privacy constraints |
| MH-5 | consumer/integration access boundary |
| MH-6 | runtime services and canonical lifecycle semantics |
| MH-7 | configuration/policy observation; no independent mutation authority |
| MH-8 | plugin capability boundary |
| MH-9 | diagnostic UI read-first and authorization-aware presentation |
| MH-10 | AI analysis/recommendation provenance and authority boundary |
| P0-03 | canonical State Authority; immutable authority dependency |
| P0-04 | in-memory State Authority implementation; no diagnostic persistence backdoor |
| P0-05 | consumer/integration boundary |
| P0-06 | core runtime services and lifecycle |
| P0-07 | configuration/policy; currently not production-qualified |

Conflict with frozen P0-03…P0-06 is a STOP condition.
