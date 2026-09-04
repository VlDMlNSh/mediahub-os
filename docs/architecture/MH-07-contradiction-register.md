# MH-7 Contradiction Register

Status: ACTIVE

| ID | Potential contradiction | Finding | Status |
|---|---|---|---|
| C-01 | Configuration vs Runtime State | Domain objects are separate; direct mutation prohibited | RESOLVED ARCHITECTURALLY |
| C-02 | Policy vs Authorization | P0-07 policy gate and exact capability grant are separate; P0-04 auth remains independent | RESOLVED ARCHITECTURALLY |
| C-03 | P0-07 vs P0-05 authorization | No approved composition mechanism exists | BLOCKED |
| C-04 | P0-07 vs P0-04 authority | Direct P0-04 access prohibited | RESOLVED ARCHITECTURALLY |
| C-05 | Defaults vs fail-safe | Undocumented security defaults prohibited | OPEN FOR DOMAIN-SPECIFIC REVIEW |
| C-06 | Published vs Applied | Publication does not imply runtime application | UNKNOWN / REQUIRES VERIFICATION |
| C-07 | Reset vs Delete | Must remain distinct operations | CANDIDATE |
| C-08 | Partial application vs atomic publication | P0-04 commit is atomic, but runtime application rollback semantics are not established | UNKNOWN |
| C-09 | Restart recovery vs transient model | No persistence authorized | DEFERRED |
