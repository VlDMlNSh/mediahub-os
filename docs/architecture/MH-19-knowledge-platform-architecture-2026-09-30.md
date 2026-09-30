# MH-19 — Knowledge Platform / Graph of Knowledge Architecture

Date: 2026-09-30
Status: ETALON BASELINE / RECONCILED — QUALIFICATION QUEUED
Scope: Knowledge Platform, Knowledge Graph, semantic context, provenance, temporal knowledge, authorized retrieval.

## 1. Authority boundary

**Knowledge Graph ≠ Authority.**

The Knowledge Platform is a semantic/read/context layer. It does not replace MediaHub State Authority, Smart Home/HA Core, domain authorities, Security, Policy, Persistence, Workflow, Media, Documents, Network, Engineering or Digital Twin authorities.

Forbidden:
- canonical-state mutation through the graph;
- direct physical actions;
- authorization issuance;
- policy execution;
- direct Smart Home control;
- graph-to-tool authorization;
- AI self-authorized knowledge promotion.

Physical command path remains:
MediaHub → Policy → Authority/HA Core → Device.

## 2. Canonical pipeline

Source Domains → Extraction → Identity Correlation → Validation → Provenance → Knowledge Graph → Full-Text/Semantic Indexes → Authorized Retrieval → UI/AI/Engineering/Search

Domain authorities own canonical facts. The graph stores semantic references, relationships and qualified derived knowledge.

## 3. Knowledge layers

1. Canonical References
2. Semantic Graph
3. Documents
4. Structured Facts
5. Derived Knowledge
6. AI Inferences / Hypotheses
7. Historical Knowledge
8. Provenance

Derived/indexed/vector knowledge is rebuildable where possible and never becomes canonical merely by materialization.

## 4. Entity contract

Every entity has:
- stable MediaHub-compatible identifier/reference;
- entity type;
- source;
- authority reference;
- provenance;
- lifecycle;
- classification.

Core classes include User, Household, Building, Site, Floor, Room, Zone, Device, Equipment, Sensor, Actuator, Camera, NetworkNode, MediaObject, Document, Project, EngineeringObject, TwinObject, Service, Protocol, CredentialReference, Event, Task, Automation, Scene, PolicyReference, AIModel and AIOutput.

The graph correlates HA/vendor/protocol/Twin/document identifiers but does not equate identities without evidence.

## 5. Relationships

Every relationship has:
- source entity;
- relation type;
- target entity;
- provenance;
- timestamp;
- validity;
- confidence where probabilistic;
- authority/reference;
- classification.

Minimum vocabulary:
contains, located_in, connected_to, controls, controlled_by, measures, measures_for, powers, powered_by, belongs_to, uses, depends_on, provides, consumes, streams_to, stored_on, derived_from, documented_by, configured_by, modeled_by, installed_in, part_of, member_of, related_to.

Relationship state is temporal: current, historical, planned, effective-from/effective-until.

Engineering semantics distinguish designed, planned, purchased, installed, configured, desired, observed, actual and removed.

## 6. Identity, merge and split

Identity correlation requires evidence and provenance. Merge qualification considers identity evidence, source agreement, capability evidence, provenance, confidence and policy. Critical merges may require explicit qualification.

Splits preserve historical evidence, repair references, preserve provenance and audit the correction.

## 7. Provenance and evidence

Significant facts must answer:
source → time → adapter/document/authority → model/actor → transformation.

Evidence classes remain distinct:
VERIFIED, OBSERVED, USER_ASSERTED, DEVICE_REPORTED, PROVIDER_REPORTED, DERIVED, INFERRED, PREDICTED, UNKNOWN.

AI confidence is not authorization and does not convert inference into verified fact.

## 8. Temporal knowledge

The platform supports historical queries for installations, configurations, documents and relationships. Stale knowledge is explicitly marked and cannot be represented as current operational truth.

Versioned changes carry version, timestamp, actor, source, reason and provenance. Snapshots support recovery, audit, migration and engineering baselines.

## 9. Documents / OCR / structured extraction

Pipeline:
Document → Parse → Structure → Extract → Validate → Provenance → Knowledge Candidate.

OCR preserves text, confidence, source location, document/page and extraction model. Equipment lists, part numbers, dimensions, addresses, configurations, wiring and inventories remain qualified candidates until promoted by the relevant authority/policy.

## 10. Domain boundaries

- Smart Home: graph contextualizes devices/rooms/zones/scenes/automations; HA remains operational authority.
- Media: graph links media/person/album/series/genre/source/device/user; Media Platform owns lifecycle.
- Documents: graph indexes relationships; Document Platform owns content.
- Engineering/Digital Twin: graph connects equipment, systems, rooms, circuits, cables, ports, controllers, projects and documents; Twin retains engineering/spatial semantics.
- Network: graph represents topology; Network Architecture owns operational state.
- Energy: graph represents meters, batteries, inverter, solar, generator, UPS and consumers; operational values remain domain-authoritative.
- Security: graph correlates devices/events/incidents/zones/policy references; Security controls remain authoritative.
- Events/tasks/projects: graph stores contextual/historical relationships; workflow systems own operational state.

## 11. Credentials and policies

Only credential references may appear. Secrets, tokens, private keys and plaintext passwords never enter the graph.

Policy references may contain policy ID/version/scope. The graph is not the policy engine.

## 12. Search and retrieval

First-class deterministic full-text search is retained. Supported retrieval modes:
- keyword/full-text;
- entity lookup;
- relationship traversal;
- semantic similarity;
- natural-language query;
- structured filters;
- temporal queries;
- hybrid structured + full-text + semantic + graph traversal.

Every query is identity-, authorization-, policy-, capability-, classification- and audit-aware. No raw database exposure.

## 13. AI / RAG boundary

Pipeline:
User → Identity → Policy → Retrieval → Knowledge Graph → Provenance → AI Context → Response.

Retrieved content is untrusted data. Prompt injection in documents/media/external content must not become executable instruction.

AI may query, summarize, classify, infer, detect inconsistency and propose candidates. AI cannot directly commit knowledge or authorize tool execution.

Write path:
Candidate Knowledge → Validation → Policy → Commit.

Tool path:
AI → Tool Gateway → Identity → Policy → Authority.

Only minimum necessary authorized context is supplied to AI.

## 14. Conflict resolution

Conflicting sources are retained with provenance. Resolution considers:
domain authority → source trust → verification → timestamp → policy → semantic scope.

No arbitrary last-write-wins/source-wins/confidence-wins rule. Canonical fact materialization is a reference/projection; canonical ownership remains with the source domain.

## 15. Storage and indexes

Storage is capability-driven. Candidates include relational/hybrid, property graph, RDF/triple store and graph-specific storage. A dedicated graph database requires demonstrated need across query complexity, traversal, scale, performance, operations, backup, migration, consistency, integration, licensing and maturity.

Vector indexes are derived, rebuildable and model/version aware. Full-text remains first-class.

## 16. Consistency, distribution and failure

Consistency classes:
- authoritative reference;
- transactional relationship;
- eventual derived relationship;
- rebuildable index.

Partition behavior preserves local knowledge with explicit staleness; critical canonical changes require authority. Merge uses provenance, versions, authority and deterministic conflict policy.

Graph failure must not stop source domains. Recovery:
Storage → Graph Core → Indexes → Derived Data → Semantic/Vector Indexes.

Integrity checks include checksum/integrity, schema violations, broken references, impossible relations and orphan entities. Orphans are preserved and marked unresolved.

## 17. Ontology and extensibility

Ontology is versioned and defines entity types, properties, relations, constraints and semantics. Changes require compatibility, migration, query, AI and policy impact analysis.

Plugins may add qualified domain-specific entities through controlled namespaces. No arbitrary production schema mutation.

## 18. Import/export/interoperability

Import:
Validate → Classify → Map → Conflict Check → Qualify → Commit.

Export respects ownership, privacy, classification, access and provenance. Supported exchange may include JSON, CSV, RDF, property-graph formats and qualified engineering/API formats.

## 19. Security / privacy / residency

Threats include poisoning, false relationships, malicious documents/metadata, impersonation, provenance forgery and unauthorized inference.

Mitigations: source trust, provenance, validation, authority separation, anomaly detection and quarantine.

The graph is highly sensitive because it can correlate people, rooms, routines, devices, cameras, documents, energy and security. Default exposure is minimum necessary.

Family/child/private information, location and camera-derived relationships inherit user/profile/classification policy.

No implicit complete-graph cloud upload. Residency, purpose, provider, egress and authorization are evaluated before external processing.

Developer Cloud receives only approved schemas, synthetic/sanitized/corporate data and never the user Knowledge Graph.

User Knowledge Graph is not Developer AI training data.

## 20. Observability, quality and testing

Observe graph size, query latency, relationship growth, conflict rate, orphan rate, provenance completeness, extraction accuracy and index health.

Quality gates include referential integrity, schema/ontology validation, duplicate detection, conflict detection, provenance completeness and stale-relation detection.

Synthetic graphs cover apartment, house, enterprise, industrial, media and Smart Home scenarios.

Tests cover entity matching, relationship inference, temporal queries, conflicts, import/export, partition, recovery, poisoning and privacy filtering.

## 21. Resource, performance and scale

Measure entity lookup, traversal, search, hybrid query, indexing, ingestion, extraction, merge and recovery.

Support apartment, house, office, industrial object, multi-building and complex-site profiles within qualified resource pools.

Knowledge workloads consume Section 24 resources and do not create a competing scheduler. Embedding/extraction may run local, cluster or controlled cloud subject to data boundary.

## 22. API, events and workflows

Public API exposes entity lookup, relationship lookup, search, context retrieval, provenance, temporal query and authorized context assembly.

API requires identity, authorization, capability, policy, rate limiting, audit and classification.

Knowledge events are versioned/correlated: entity-created, entity-updated, relationship-added/removed, provenance-added, candidate-created/confirmed, conflict-detected and reclassified.

Durable workflows govern ingestion, extraction, reconciliation, ontology migration and index rebuild.

## 23. Qualification and production admission

Production admission sequence:
Schema Qualification → Storage Qualification → Security Qualification → Privacy Qualification → Performance Qualification → Recovery Qualification → Policy Admission → Production.

Qualification never implies production/release authorization.

## 24. Cross-MH invariant

Knowledge Platform is subordinate to State Authority, Security, Policy, domain authorities, Smart Home/HA Core, Media, Documents, Engineering/Digital Twin, Network, Persistence and Recovery.

No graph component may become a competing singleton authority.

## 25. Qualification waves

1. Exact revision/tree/ancestry/provenance.
2. Authority boundary and canonical-reference semantics.
3. Entity model and schema constraints.
4. Identity correlation, merge and split.
5. Relationship model and controlled vocabulary.
6. Temporal validity and historical queries.
7. Provenance/evidence/confidence.
8. Verified facts vs derived/inferred/predicted knowledge.
9. Documents/OCR/structured extraction.
10. Engineering/Digital Twin boundary.
11. Smart Home/HA boundary.
12. Media/Documents/Network/Energy domain boundaries.
13. Security/credential/policy references.
14. Search/full-text/semantic/hybrid retrieval.
15. AI/RAG minimum-context and prompt-injection boundary.
16. Conflict resolution and canonical materialization.
17. Storage and graph-database decision evidence.
18. Index/rebuild/consistency/partition semantics.
19. Ontology/versioning/plugin/extensibility.
20. Import/export/interoperability.
21. Privacy/residency/cloud/developer/training isolation.
22. Observability/performance/scale/recovery/migration.
23. Independent cross-MH contradiction analysis and closure.

## 26. Known qualification gaps

G-01: fresh repository evidence for the complete MH-19 architecture artifact lineage.
G-02: implementation evidence for entity/relationship persistence.
G-03: production identity-correlation implementation and merge/split evidence.
G-04: provenance storage and temporal query implementation evidence.
G-05: document/OCR/structured extraction qualification evidence.
G-06: Digital Twin / Smart Home / Media / Network domain integration evidence.
G-07: search/RAG/API authorization enforcement evidence.
G-08: storage technology decision evidence; no graph DB assumption accepted.
G-09: partition/recovery/migration implementation evidence.
G-10: ontology governance and controlled extension evidence.
G-11: poisoning/prompt-injection/privacy/residency enforcement evidence.
G-12: synthetic graph, performance, scale and resource qualification evidence.
G-13: independent cross-MH contradiction and dependency evidence.

## 27. Closure state

Architecture target: ETALON BASELINE / RECONCILED.
Qualification: QUEUED / NOT YET EXECUTED.
Production: NOT AUTHORIZED.

Closure artifact:
MH-19 Knowledge Architecture Closure

Handoff target:
MH-20 — Architecture Audit.
