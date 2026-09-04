# MH-19 — Knowledge Graph / Digital Twin Architecture

Status: PROPOSED / NOT ACCEPTED / NOT FROZEN
Date: 2026-09-04

## Core invariant
Knowledge Graph and Digital Twin are semantic/read/projection layers. They are never State Authority, Policy Engine, Authorization Engine, Capability Authority, or Device Control Authority.

## Authority flow
User / Service / Device / AI / Plugin -> Consumer Boundary -> Policy -> Authorization -> State Authority -> Canonical State -> Knowledge Projection.

Physical control: Observation -> Representation -> Analyze -> Propose -> Policy -> Authorization -> Consumer Boundary -> State Authority -> Device Adapter -> Device -> Observation.

## Evidence baseline
Existing repository evidence confirms canonical Device, Identity, Relationship and Event contracts and AI inference contracts. A production Knowledge Graph, Digital Twin, vector database, RAG runtime, graph persistence or graph-driven automation is not currently verified.

## Architecture layers
1. Canonical domain/state sources.
2. Observation and evidence normalization.
3. Knowledge assertion/provenance layer.
4. Derived/inferred knowledge.
5. Graph/read model.
6. Search/vector projections.
7. Digital Twin projections.
8. UI/AI consumers.

Derived/inferred/cached projections must be rebuildable where practical and must not be required to preserve canonical state.

## Governance
No graph database, vector database, private-data ingestion, cloud synchronization, autonomous inference, ontology migration or graph-driven device control is authorized by MH-19 alone. Such changes require Security Review, Privacy Review, evidence, ADR and Governance Authorization.
