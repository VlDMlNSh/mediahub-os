# MH-17 — Safety Testing

**Status:** PROPOSED / CANDIDATE

Safety tests MUST verify the precedence `Hard Safety > Manual Emergency > Explicit Admin Policy > Local Automation > Optimization > Recommendation`.

Coverage includes unsafe capability exposure, invalid targets, stale state, command timeout/ambiguity, retries of non-idempotent operations, device disconnects, malformed values, concurrent commands, degraded/quarantined devices, and recovery from partial execution.

Safety test success requires observable evidence; simulation alone cannot establish physical safety.
