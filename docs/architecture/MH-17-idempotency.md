# MH-17 — Idempotency

**Status:** CANDIDATE

Each command category must be classified `IDEMPOTENT`, `CONDITIONALLY_IDEMPOTENT`, `NON_IDEMPOTENT`, or `IRREVERSIBLE`.

Retries require a stable command/idempotency key and adapter-specific evidence that the protocol/device will not duplicate a physical action. For non-idempotent or irreversible operations, ambiguous outcomes become `UNKNOWN` and require explicit recovery policy rather than blind retry.

Critical classes (locks, gates, power, heating, security and destructive operations) require stronger authorization, timeout and confirmation policy. Transport retry is never a substitute for command semantics.