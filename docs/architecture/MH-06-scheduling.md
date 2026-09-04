# MH-06 — Scheduling

Status: PROPOSED / TECHNOLOGY UNKNOWN

Scheduler responsibilities: admission, priority, deadlines, fairness, concurrency limits, resource constraints and cancellation.

Priority order: Hard Safety > Manual Emergency > Explicit Admin Policy > Local Automation > Optimization > Recommendation.

Scheduler has no State Authority capability and cannot elevate authorization. AI recommendation priority cannot turn a proposal into a critical command.

Technology candidates such as cron, systemd timers, queues, brokers or custom loops remain non-canonical until ADR + evidence + security review + governance approval.
