# MH-20 — Automation / Energy / Self-Healing Architecture

Status: ARCHITECTURE WORK AUTHORIZED / NOT YET ACCEPTED / NOT FROZEN

## Governance
MH-20 is an architecture guardian record, not a development workspace. Implementation, debugging and feature work belong to the development chat. Material architecture decisions are synchronized to GitHub.

Canonical workflow: Evidence → Canonical State → Decision → Architecture → Implementation → Verification → Governance Acceptance → Freeze.

## Authority invariant
Automation, Scheduler, Rule Engine, Energy Engine, Self-Healing Engine, AI, Plugin, Knowledge Graph, Device, UI and Persistence are not State Authority. State Authority remains the sole canonical mutation authority.

Every mutation path must be traceable as:
Policy → Authorization → Consumer Boundary → State Authority → Canonical State → Device/Service → Observation → Verification.

## Core domains
MH-20 defines contracts for automation/rules/triggers/conditions/actions/commands, scheduling/time/idempotency/retry/rate limiting/debounce/hysteresis, conflict/manual override/safety/critical actions, energy measurement/control/safety, self-healing/remediation/circuit breaker/loop detection/quarantine, AI/device/media/KG/plugin/UI integration, security/privacy/observability/resource governance/offline-first/recovery/persistence/failure/testing.

## Safety
Unknown is not permission. Sent is not applied. Applied is not verified. Timeout is not success. Critical or destructive actions require explicit authorization and dedicated safety gates; AI-only critical execution is prohibited.

## Energy
Measurement, observation, prediction and optimization never grant control authority. Energy control follows Measure → Validate → Normalize → Observe → Analyze → Forecast/Optimize → Policy → Authorization → Command → Device → Observe → Verify.

## Self-healing
Self-healing is controlled remediation. It requires sufficient evidence, bounded pre-authorized remediation, authorization, rollback/failure semantics, observability and verification. Destructive remediation is operator-only unless separately gated by explicit architecture.

## Offline-first / topology
SINGLE NODE / NO HA remains canonical. Local critical control must not depend on cloud availability. Cloud and remote AI are external/untrusted by default and are not authority.

## Technology policy
Home Assistant, Node-RED, openHAB, Temporal, Airflow, Celery, APScheduler, cron, systemd timers, MQTT, Kafka, Redis, PostgreSQL, InfluxDB, Grafana, Prometheus, OpenTelemetry, ML/optimization frameworks and similar technologies remain CANDIDATE until requirements, compatibility, security, resource, operational, licensing and evidence review plus ADR.

## Required registers
Evidence Register, Decision Log, Contradiction Register, Unknown Register, Acceptance Criteria and dependency/traceability records are mandatory.

## Required passes
MH-20.1 Current State / Evidence Audit; MH-20.2 Authority Boundary; MH-20.3 Rule/Trigger/Condition; MH-20.4 Scheduler/Time/Idempotency; MH-20.5 Safety/Override/Critical Actions; MH-20.6 Energy; MH-20.7 Self-Healing; MH-20.8 Integrations; MH-20.9 Security/Privacy/Observability; MH-20.10 Resource/Failure/Offline; MH-20.11 Testing/Qualification; MH-20.12 Acceptance/Freeze.

## Current evidence position
Repository `VlDMlNSh/mediahub-os` is the durable source-of-record. Current GitHub evidence shows recent architecture-governance work through commit `176ab9fca332248c4a4071903a9b8760fddce98f` on 2026-09-04. The repository is private, default branch `main`. No claim about MH-20 implementation is inferred from file existence or commit messages alone.

## Freeze rule
MH-20 cannot be marked ACCEPTED/FROZEN until all required contracts, evidence, verification, contradiction/unknown registers, traceability and governance gates are satisfied.