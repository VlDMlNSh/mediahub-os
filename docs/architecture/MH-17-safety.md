# MH-17 — Device Safety

**Status:** CANDIDATE

Authority hierarchy:
`Hard Safety > Manual Emergency > Explicit Admin Policy > Local Automation > Optimization > Recommendation`.

Critical devices include locks, gates, power, heating, security and irreversible actuators. Critical commands require explicit capability, authorization, policy and safety gates plus command outcome semantics appropriate to the device.

AI confidence is never a substitute for authorization. Automation must not silently turn observation into action. Self-healing must not perform destructive actions without an explicit approved gate.

Safety failure is fail-closed where safe to do so; ambiguous physical outcomes remain `UNKNOWN` until evidence resolves them.