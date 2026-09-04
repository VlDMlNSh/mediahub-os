# MH-20 Architecture Status

## Status

**ARCHITECTURE WORK AUTHORIZED / NOT YET ACCEPTED / NOT FROZEN**

Date: 2026-09-04

## Governance boundary

MH-20 is an architecture guardian, not a development workspace. Implementation, debugging and feature development belong to the development workspace. Material architecture decisions are synchronized to GitHub.

## Execution model

MH-20 passes are evaluated as:

Evidence → Canonical State → Decision → Architecture → Implementation → Verification → Governance Acceptance → Freeze

Absence of evidence is **UNKNOWN / REQUIRES VERIFICATION**. Proposed decisions are **PROPOSED**. Accepted but unimplemented decisions are **ACCEPTED / NOT IMPLEMENTED**. Implemented but incompletely verified work is **IMPLEMENTED / NOT VERIFIED**.

## MH-20.1–12 consolidated assessment

### MH-20.1 Current State / Evidence Audit
**UNKNOWN / REQUIRES VERIFICATION** for repository implementation state. The repository currently contains MH-20 governance/master/reverse-master artifacts, but document presence is not implementation evidence. No evidence was established here for a production automation engine, scheduler, energy controller or self-healing implementation.

### MH-20.2 Automation Authority Boundary
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Automation is orchestration, never authority. Every mutation path must be Policy → Authorization → Consumer Boundary → State Authority. No second State Authority is permitted.

### MH-20.3 Rule / Trigger / Condition Contract
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Trigger, condition, rule, action, proposal, command and execution remain distinct. Conditions are side-effect-free and bounded. Trigger ≠ authorization; proposal ≠ command.

### MH-20.4 Scheduler / Time / Idempotency
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Scheduler plans but cannot authorize or mutate state. Wall-clock and monotonic-clock semantics must remain distinct; DST, reboot, crash, power loss and clock correction require explicit contracts. Duplicate triggers require deduplication/idempotency semantics.

### MH-20.5 Safety / Manual Override / Critical Actions
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Safety hierarchy is Hard Safety → Manual Emergency → Explicit Admin Policy → Local Automation → Optimization → Recommendation. Critical/destructive actions require explicit gates. Manual emergency control does not bypass security.

### MH-20.6 Energy Architecture
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Measurement/forecast/optimization never grants control authority. Energy control follows Measure → Validate → Normalize → Observe → Analyze → Forecast/Optimize → Policy → Authorization → Command → Device → Observe → Verify.

### MH-20.7 Self-Healing / Remediation
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Self-healing is bounded remediation. Evidence, diagnosis, authorization, bounds, observability and verification are mandatory. Destructive remediation is operator/explicit-gate territory.

### MH-20.8 AI / Device / Media / KG / Plugin Integration
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. AI, Knowledge Graph, plugins and device/media integrations are consumers/providers of context or proposals, not authority. Plugin composition cannot increase authority. Cloud remains external/untrusted by default.

### MH-20.9 Security / Privacy / Observability
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Threats include injection, replay, privilege escalation, automation loops, capability abuse, malicious plugins/rules and AI proposal abuse. Automation context is subject to privacy minimization and explicit external-transfer rules. Observability is passive.

### MH-20.10 Resource / Failure / Offline-First
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Automation must be bounded by execution, queue, concurrency, command-rate and resource budgets. Failure states must distinguish sent/applied/observed/verified. Critical local control must not depend on cloud availability. SINGLE NODE / NO HA remains canonical.

### MH-20.11 Testing / Threat Model / Qualification
**ARCHITECTURAL DECISION — ACCEPTED / NOT IMPLEMENTED**. Required verification spans unit, contract, integration, security, safety, reliability, stress and controlled chaos testing. Test existence is not PASS evidence.

### MH-20.12 Acceptance / Freeze Review
**BLOCKED / NOT ACCEPTED / NOT FROZEN**. Required evidence for implementation, verification and governance acceptance is not established. Therefore MH-20 cannot be promoted to ACCEPTED/FROZEN.

## Canonical invariants

1. State Authority remains the sole canonical mutation authority.
2. Automation, Scheduler, Rule Engine, Energy Engine, Self-Healing Engine and AI are not authority.
3. Trigger, observation and prediction are not authorization.
4. Proposal is not command; command is not execution; execution is not verified state.
5. Critical actions require explicit authorization and safety gates.
6. Unknown execution result is never success.
7. Retry respects idempotency and safety.
8. Automation is bounded; recursive/cascading loops must be detected and controlled.
9. Self-healing is bounded remediation; destructive remediation requires an explicit gate.
10. Energy measurement does not grant control authority.
11. Automation cannot bypass Consumer Boundary or directly mutate Persistence.
12. AI cannot self-authorize or bypass policy.
13. Cloud is external/untrusted by default; local critical control is offline-first.
14. SINGLE NODE / NO HA remains canonical.
15. No hidden retry/rebase/merge/LWW semantics or privilege escalation.
16. Failure must fail safely and observably.

## Evidence limitations

No repository-wide implementation verification is claimed by this document. Exact branch/HEAD, clean-dirty status, test/CI/security-scan results and actual mutation paths remain verification items for the development workspace/repository audit.

## Governance outcome

**MH-20 remains ARCHITECTURE WORK AUTHORIZED / NOT YET ACCEPTED / NOT FROZEN.**
