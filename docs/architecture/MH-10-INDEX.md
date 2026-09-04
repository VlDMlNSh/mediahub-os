# MH-10 — AI / INTELLIGENCE ARCHITECTURE

Status: PROPOSED / ARCHITECTURE DRAFT
Authority: MH-10 Architecture Authority
Date: 2026-09-04

## Scope
AI, intelligence, inference, recommendations, proposals, agents, RAG, knowledge, local/cloud AI, model lifecycle, resource governance, safety, privacy, security, observability and AI interaction boundaries.

## Canonical rule
**AI is intelligence, not authority.**

Canonical mutation path:
`AI → Recommendation/Proposal → Policy Evaluation → Authorization → Command → Consumer Boundary → State Authority → Canonical Runtime State`

Read path:
`Authorized Read Model → AI → Analysis/Recommendation`

## Frozen dependencies
P0-03 State Authority, P0-04 In-Memory State Authority, P0-05 Consumer/Integration Boundary and P0-06 Core Runtime Services are protected baselines. P0-07 remains in-progress and production mutation publication is blocked pending its governance/API gap.

## Evidence
Repository already contains AI contracts under `contracts/ai` and mirrored schemas under `schemas/ai`, plus AI tests. These are implementation evidence only; they do not grant AI authority or make MH-10 accepted/frozen.

## Known cross-chat issue
MH-21 contains a substantial distributed/hybrid AI architecture set. MH-10 must not silently replace or duplicate it. The relationship is recorded as a contradiction/coordination item pending governance resolution.

## Required companion records
- authority boundary
- intelligence levels
- AI modes/autonomy
- safety/security/privacy
- RAG/knowledge
- local/cloud/hybrid/routing
- agents/tools/orchestration
- model lifecycle/provenance/supply chain/qualification
- resource/failure/degradation
- interaction boundaries
- evidence/decision/contradiction/unknowns
- acceptance criteria
- Master Prompt / Reverse Master Prompt
