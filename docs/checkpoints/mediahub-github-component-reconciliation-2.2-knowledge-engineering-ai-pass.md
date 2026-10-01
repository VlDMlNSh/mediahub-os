# MediaHub OS — GitHub Component Reconciliation 2.2 / Knowledge · Documents · Digital Twin · Engineering · AI

Date: 2026-10-01
Parent baseline: docs/checkpoints/mediahub-github-component-reconciliation-2.1-media-deep-pass.md
Status: QUALIFIED DOMAIN DEEP-PASS

## 1. Purpose

This pass reconciles the remaining high-level implementation domains against mature GitHub components without reopening MH-1…MH-24 architecture.

Domains:
- Documents
- Knowledge
- Digital Twin
- Engineering
- AI

Governing rule:
Use an existing mature component where it removes substantial implementation risk and does not transfer MediaHub authority. Avoid adding a new database, vector store, graph authority, search authority or inference authority without a demonstrated capability gap.

## 2. Documents

### PaddleOCR — RETAIN / TARGET-GATED
Repository: https://github.com/PaddlePaddle/PaddleOCR

Role:
- OCR for image/PDF documents;
- structured extraction;
- multilingual OCR.

Boundary:
OCR output is derived, provenance-bearing data. Original document bytes remain under MediaHub document/storage policy.

Qualification:
model provenance, language/accuracy matrix, CPU/GPU/NPU resource profile, sandboxing, document privacy, deterministic/reproducible output where required, failure/degraded behavior.

### Unstructured — REFERENCE / TARGET-GATED

Repository: https://github.com/Unstructured-IO/unstructured

Role:
- document partitioning;
- structure extraction;
- ETL/chunking patterns for AI ingestion.

Decision:
Useful for ingestion/normalization patterns, but not admitted as a second document authority or mandatory production sidecar. Prefer extracting only the capabilities required by MediaHub contracts.

Reason:
The foundational document substrate remains PostgreSQL + pgvector + MediaHub document contracts. Adding a broad document platform before proving a capability gap would duplicate persistence/search responsibilities.

### Paperless-ngx — RETAIN / CONDITIONAL WHOLE-PRODUCT CANDIDATE

Repository: https://github.com/paperless-ngx/paperless-ngx

Decision:
Remain conditional. It may provide a mature complete document archive/indexing product, but deployment requires an explicit sensitive-document privacy/security/storage review. It must remain behind a MediaHub adapter and cannot become canonical document authority.

### OpenSearch — EXCLUDED FROM FOUNDATION / FUTURE-GATED

Repository: https://github.com/opensearch-project/OpenSearch

Decision:
Do not introduce as the default search authority.

Reason:
MediaHub already has PostgreSQL + pgvector and a document contract. OpenSearch would create a second durable indexing/search subsystem with additional consistency, lifecycle, backup and operational cost.

Activation requires a measured search capability gap (scale, latency, faceting, full-text behavior or workload shape) that PostgreSQL cannot meet after qualification.

## 3. Knowledge

### PostgreSQL + pgvector + MediaHub Knowledge Contract — SELECTED FOUNDATION

Knowledge remains a domain, not an independent authority.

Use:
- relational entities and provenance;
- temporal relations;
- embeddings/vector retrieval;
- document/entity references;
- graph-like relation tables where appropriate;
- canonical source/provenance links.

Rule:
Knowledge is derived/reconstructable where possible and never overrides State Authority or domain authority.

### RDFLib — REFERENCE / TARGET-GATED INTEROPERABILITY PRIMITIVE

Repository: https://github.com/RDFLib/rdflib

Role:
- RDF representation;
- graph interchange;
- semantic-web serialization/query patterns.

Decision:
Do not install by default. Admit only if IFC/knowledge interoperability or standards-based RDF exchange creates a concrete requirement.

Reason:
A Python RDF library does not justify a second graph database or authority. It is useful as a bounded interoperability primitive if required.

### Apache Jena — REFERENCE / FUTURE-GATED

Repository: https://github.com/apache/jena

Role:
- RDF/semantic-web framework;
- SPARQL/linked-data implementation patterns.

Decision:
Reference only at this stage. Do not introduce Jena as a permanent knowledge platform while PostgreSQL remains sufficient.

### Neo4j — EXCLUDED FROM FOUNDATION / FUTURE-GATED

Repository: https://github.com/neo4j/neo4j

Decision:
No second graph database in the foundation.

Activation requires evidence that MediaHub knowledge workloads cannot be satisfied by PostgreSQL relation modeling + pgvector + bounded graph algorithms/interchange.

## 4. Digital Twin / BIM

### IfcOpenShell — RETAIN / TARGET-GATED PRIMARY IFC ENGINE

Repository: https://github.com/IfcOpenShell/IfcOpenShell

Role:
- IFC parsing;
- schema-aware BIM processing;
- geometry and model operations.

Decision:
Primary target for IFC/BIM processing. MediaHub owns project identity, lifecycle, permissions, provenance and canonical domain contracts.

### web-ifc — RETAIN / TARGET-GATED CLIENT-SIDE IFC ENGINE

Repository: https://github.com/ThatOpen/engine_web-ifc

Role:
- browser/client IFC parsing;
- interactive BIM interoperability.

Decision:
Target for iOS/web-adjacent visualization only after platform benchmark. It complements server-side IfcOpenShell; it does not create a second twin authority.

### VTK / vtk.js — RETAIN / TARGET-GATED VISUALIZATION

Repository: https://github.com/Kitware/VTK

Role:
- scientific/engineering visualization;
- geometry and rendering algorithms.

Decision:
Benchmark only against actual MediaHub 2D/3D requirements. No unconditional runtime dependency.

### FreeCAD — REFERENCE
Repository: https://github.com/FreeCAD/FreeCAD

Use:
engineering/CAD algorithms and interoperability patterns.

Decision:
Do not embed as the MediaHub engineering authority. Use only for concrete CAD/engineering capability gaps.

### CloudCompare — REFERENCE
Repository: https://github.com/CloudCompare/CloudCompare

Use:
point-cloud processing and inspection.

Decision:
Reference/conditional tool only. Activate if point-cloud workflows require its measured capabilities.

## 5. Engineering

Engineering remains a MediaHub domain with project state, provenance and controlled artifacts.

Selected implementation pattern:
- PostgreSQL for canonical structured engineering metadata;
- object storage interface for large CAD/BIM/media/artifact payloads;
- IfcOpenShell for IFC processing;
- web-ifc for client-side IFC where required;
- VTK/vtk.js only after rendering benchmark;
- FreeCAD/CloudCompare as specialist/reference tools.

Hard boundary:
Engineering artifacts do not become State Authority merely because an external CAD/BIM tool maintains its own project state.

No second engineering database is admitted.

## 6. AI

### ONNX Runtime — RETAIN / TARGET-GATED GENERAL INFERENCE PRIMITIVE

Repository: https://github.com/microsoft/onnxruntime

Role:
- portable ML inference;
- CPU/GPU/NPU execution where supported.

Boundary:
MediaHub owns model registry, model provenance, admission policy, input/output contracts, resource limits and audit.

### llama.cpp — RETAIN / TARGET-GATED LOCAL LLM ENGINE

Repository: https://github.com/ggml-org/llama.cpp

Role:
- local LLM inference;
- resource-constrained node inference;
- CPU/GPU-oriented local execution.

Boundary:
No direct path from model output to physical authority. Tool calls remain policy-mediated.

### vLLM / SGLang — REFERENCE / FUTURE-GATED SERVER INFERENCE

Repositories:
https://github.com/vllm-project/vllm
https://github.com/sgl-project/sglang

Decision:
Do not add as default duplicate inference runtimes. Benchmark only when high-throughput server inference produces a measurable requirement not met by the selected local/runtime path.

### ComfyUI — REFERENCE ONLY

Repository: https://github.com/comfyanonymous/ComfyUI

Use:
image-generation workflow patterns.

Decision:
No foundation dependency. Activate only for a concrete MediaHub media-generation workflow.

## 7. AI architecture boundary

AI subsystem pipeline remains:

Model Registry → Qualification → Policy Admission → Runtime → Tool/Domain Contract → Result → Provenance/Audit

AI does not become:
- State Authority;
- Policy Authority;
- Smart Home Authority;
- Recovery Authority;
- Update Authority;
- Identity Authority.

External/cloud AI is an escalation path, not a replacement for local authority.

## 8. Domain-wide non-adoption

No new default production dependencies are added for:
- second document database;
- second search engine;
- second vector database;
- second graph database;
- second engineering database;
- duplicate AI runtime for the same workload;
- generic agent framework with authority over MediaHub domains.

These remain future-gated by measurable capability gap.

## 9. Result

Documents:
- PostgreSQL + pgvector + MediaHub contracts = foundation.
- PaddleOCR = target-gated OCR.
- Paperless-ngx = conditional whole-product candidate.
- Unstructured = reference/target-gated ingestion primitive.
- OpenSearch = future-gated, not foundation.

Knowledge:
- PostgreSQL + pgvector + MediaHub Knowledge Contract = foundation.
- RDFLib = target-gated interoperability primitive.
- Jena = reference/future-gated.
- Neo4j = excluded from foundation.

Digital Twin / Engineering:
- IfcOpenShell = primary target-gated IFC engine.
- web-ifc = client-side target-gated IFC engine.
- VTK/vtk.js = target-gated visualization.
- FreeCAD/CloudCompare = reference specialists.

AI:
- ONNX Runtime = target-gated general inference.
- llama.cpp = target-gated local LLM inference.
- vLLM/SGLang = future-gated.
- ComfyUI = reference.

No architecture change was made.

The next reconciliation pass can close Storage → Network → Workflow → Supply Chain → Developer Fabric and then produce one unified component manifest.
