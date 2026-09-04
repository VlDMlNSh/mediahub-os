# MH-02 — Reference Architecture
Status: PROPOSED / RECONCILIATION IN PROGRESS
Parent: MH-01

## Canonical principle
MediaHub OS is one system, one reference architecture, one canonical mutation authority, and 23 coherent architectural domains.

## Frozen foundation
- P0-03 State Authority Contract v1.0 — ACCEPTED/FROZEN
- P0-04 In-Memory State Authority v1.0 — ACCEPTED/FROZEN
- P0-05 Consumer/Integration Boundary — ACCEPTED/FROZEN
- P0-06 Core Runtime Services — ACCEPTED/FROZEN
- P0-07 Configuration/Policy — IMPLEMENTATION IN PROGRESS

## Logical layers
Presentation → AI/Intelligence → API/Capability/Command → Policy/Authorization/Security → Consumer/Integration → State Authority → Core Runtime/Lifecycle → OS/Hardware.

State Authority is the only canonical mutation authority. UI, AI, plugins, cloud, persistence, observability and external systems cannot create a second mutation path.

## Planes
Control, Data, Management, Intelligence and Integration planes are logically separated.

## Reliability
Current state: SINGLE NODE / NO HA. No active-active, consensus or multi-primary assumption.

## Local-first
Core operation must not require Internet, cloud, external AI, external RAG or paid APIs.

## Cloud
Cloud is an external compute plane, never canonical control/state authority.

## AI
AI produces proposal/recommendation; mutation requires Policy → Authorization → Command → Consumer Boundary → State Authority.

## Status
This document is not ACCEPTED/FROZEN until the MH-2 acceptance gate is passed.