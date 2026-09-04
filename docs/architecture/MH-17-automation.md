# MH-17 — Automation Interaction

**Status:** PROPOSED / CANDIDATE

Automation produces intents, not unrestricted device commands. Every automated action is evaluated against current identity, trust, capability, scope, policy, authorization, safety class, and State Authority rules.

Automation MUST handle stale/unknown state, conflicts, retries, offline queues, device replacement, quarantine, and cancellation explicitly. A rule trigger or group membership does not itself authorize an operation.

Safety policy takes precedence over optimization and recommendation.
