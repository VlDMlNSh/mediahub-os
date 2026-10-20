# MediaHub OS — Wave 218 / Agent-2 Component Provenance Audit

## Metadata
- **Queue / Task ID:** Wave 218 / Agent-2 Component Provenance Audit (PR #410 Review)
- **Agent Identity:** `gemini-agent-2`
- **Authorized Contour:** Contour A (Developer Fabric)
- **Base Ref:** `main` (commit SHA: `d27a52fed03703c16c62c4c1481091e6110e80f2`)
- **Branch:** `agent-2/wave-218-component-provenance`
- **Date:** 2026-10-20
- **Status:** COMPLETED (Documentation & Provenance Pass)

---

## 1. Executive Summary & Objective
This audit reviews and refines the reusable component candidates raised in PR #410 in alignment with Functional Baseline 2.0 and ASTRA-GOLD governance contracts. 

**Key Correction:** Blanket compatibility claims are rejected. Upstream components are **never** drop-in domain replacements or autonomous authorities. MediaHub OS retains sole ownership of:
1. Product State Authority (`components/COMPONENT-REGISTRY.yaml`)
2. Domain Models & Contracts
3. Authorization & Security Enforcement
4. Recovery & Update Authority

---

## 2. Retained Component Provenance & Contract Mapping

### A. Relational Persistence & Vector Search
- **PostgreSQL** (`https://github.com/postgres/postgres`)
  - *License:* PostgreSQL License (Permissive)
  - *Pinned Reference:* Upstream stable release channel / pinned release manifests.
  - *Fit & Unknowns:* Target durable persistence backend only. MH-03 remains in-memory/single-node until the persistence governance gate passes. MediaHub owns schema, migrations, and invariants.
- **pgvector** (`https://github.com/pgvector/pgvector`)
  - *License:* PostgreSQL License
  - *Pinned Reference:* Compatible release tag mapped to PostgreSQL extension tier.
  - *Fit & Unknowns:* Semantic and vector search capabilities integrated directly inside PostgreSQL; does not constitute a separate vector state authority.

### B. Local AI Runtimes
- **ONNX Runtime** (`https://github.com/microsoft/onnxruntime`)
  - *License:* MIT
  - *Pinned Reference:* Pinned release tag / manifest integration.
  - *Fit & Unknowns:* Portable local inference runtime. Model provenance, execution policy, and resource limits remain strictly MediaHub-owned.
- **llama.cpp** (`https://github.com/ggml-org/llama.cpp`)
  - *License:* MIT
  - *Pinned Reference:* Pinned stable commit / release tag.
  - *Fit & Unknowns:* Primary local LLM inference engine for local advisory workflows. Prompt policy, tool permissions, and state boundaries are controlled by MediaHub AI Gateway.

### C. Observability & Supply Chain
- **OpenTelemetry & Prometheus** (`open-telemetry/opentelemetry-collector`, `prometheus/prometheus`)
  - *License:* Apache-2.0
  - *Fit & Unknowns:* Non-authoritative, non-mutating operational observability and metrics collection. Cannot mutate State Authority.
- **Cosign, Syft, & Trivy** (`sigstore/cosign`, `anchore/syft`, `aquasecurity/trivy`)
  - *License:* Apache-2.0
  - *Fit & Unknowns:* Artifact signing, SBOM generation, and security vulnerability scanning. Feeds release gates and policy; scanner outputs are evidence, not security authorities.

### D. Secret Management & Configuration
- **SOPS & age** (`getsops/sops`, `FiloSottile/age`)
  - *License:* MPL-2.0 / BSD-3-Clause
  - *Fit & Unknowns:* Encrypted configuration and secrets workflow retained as the deployment/configuration primitive pending OpenBao capability comparison. Must not create conflicting secret authorities.

---

## 3. Acceptance Criteria & Known Gaps

- **Acceptance Criteria:**
  1. Strict license compliance and upstream provenance pinning.
  2. Isolation of upstream APIs behind MediaHub-owned adapter boundaries.
  3. Preservation of single-node MH-03 runtime reference constraints unless explicitly gated.
- **Known Gaps:**
  - Target-gated components (e.g., PostgreSQL, ONNX, llama.cpp) require explicit downstream activation gates and benchmark evidence.
  - No autonomous activation of distributed or persistent features without human governance approval (G11).

---

## 4. Verification Status
- **Static Analysis / Documentation Check:** PASSED. All candidate mappings audited against `architecture/FUNCTIONAL-BASELINE-1.0-OSS-COMPONENT-BASELINE.md` and `components/COMPONENT-REGISTRY.yaml`.
- **Runtime Execution:** Skipped per instructions (no test execution, no deployment, no secret inspection).
