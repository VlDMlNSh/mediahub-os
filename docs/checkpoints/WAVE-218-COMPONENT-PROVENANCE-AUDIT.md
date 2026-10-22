# MediaHub OS — Wave 218 / Agent-2 Component Candidate Inventory

## Metadata

- **Task ID:** Wave 218 / Agent-2 Component Provenance Audit (PR #410 Review)
- **Agent identity:** `gemini-agent-2`
- **Contour:** Contour A (Developer Fabric)
- **Base ref inspected:** `main`, observed base SHA `d27a52fed03703c16c62c4c1481091e6110e80f2`
- **Date:** 2026-10-20
- **Status:** **UNVERIFIED CANDIDATE INVENTORY — NOT COMPONENT SELECTION**

## Correction to earlier provenance claims

The earlier draft described release channels/tags as “pinned” and stated that provenance passed. Those phrases were not backed by exact upstream commit SHAs, immutable release identifiers, or inspected license-file SHAs. This checkpoint corrects that overclaim.

- No exact upstream commit SHA was captured for the candidates below in this pass.
- No upstream `LICENSE` / `COPYING` file was read back with a source ref and blob SHA for this pass.
- License labels are therefore **not verified here** and are not legal approval.
- Compatibility is a proposal only; no runtime, benchmark, integration, migration, or qualification test was performed.
- No candidate is approved for implementation, runtime activation, or production use by this report.

## MediaHub contracts used as boundaries

1. **Functional Baseline 2.0** — `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. This is the canonical functional reference; component registration does not imply implementation or qualification.
2. **Component Registry** — `components/COMPONENT-REGISTRY.yaml@main`, blob SHA `3ad109ba5ec9b095d0fac851514caadcefbe2f69`. Its stated principle is to reuse mature open-source blocks and patterns rather than adopting whole products without explicit justification; MediaHub retains architectural ownership and authoritative state.
3. **Gemini authority rule** — `GEMINI.md@main`, blob SHA `4c431143aa5c46776e80893bf3c0e5f202e3b76d`: Product State Authority alone owns canonical MediaHub product-state mutation; AI agents, cloud workflows, queues, and adapters do not acquire it.
4. **ASTRA governance contract** — `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml@main`, blob SHA `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`. Any candidate must remain an implementation primitive or adapter and must not gain authority by implication.

## Candidate inventory — every row remains unverified

| Candidate | Upstream repository | Exact commit/release pin | License-file evidence | MediaHub fit status |
|---|---|---|---|---|
| PostgreSQL | https://github.com/postgres/postgres | NOT CAPTURED | NOT INSPECTED | Proposal only; persistence activation remains gated |
| pgvector | https://github.com/pgvector/pgvector | NOT CAPTURED | NOT INSPECTED | Proposal only; extension/schema compatibility not tested |
| ONNX Runtime | https://github.com/microsoft/onnxruntime | NOT CAPTURED | NOT INSPECTED | Proposal only; model/runtime provenance and resource gates open |
| llama.cpp | https://github.com/ggml-org/llama.cpp | NOT CAPTURED | NOT INSPECTED | Proposal only; build/model provenance and resource gates open |
| OpenTelemetry Collector | https://github.com/open-telemetry/opentelemetry-collector | NOT CAPTURED | NOT INSPECTED | Proposal only; telemetry must remain non-authoritative |
| Prometheus | https://github.com/prometheus/prometheus | NOT CAPTURED | NOT INSPECTED | Proposal only; observability must remain non-mutating |
| Cosign | https://github.com/sigstore/cosign | NOT CAPTURED | NOT INSPECTED | Proposal only; signature evidence feeds MediaHub release policy |
| Syft | https://github.com/anchore/syft | NOT CAPTURED | NOT INSPECTED | Proposal only; SBOM output is evidence, not release authority |
| Trivy | https://github.com/aquasecurity/trivy | NOT CAPTURED | NOT INSPECTED | Proposal only; scan output is evidence, not security authority |
| SOPS | https://github.com/getsops/sops | NOT CAPTURED | NOT INSPECTED | Proposal only; must not create a competing secret authority |
| age | https://github.com/FiloSottile/age | NOT CAPTURED | NOT INSPECTED | Proposal only; cryptographic workflow integration remains untested |

## Required evidence before retaining any candidate

For each candidate to be retained beyond inventory, the next pass must record:

1. Canonical upstream repository URL and exact commit SHA or immutable release reference.
2. Exact license file path, blob SHA, and license text identifier; legal approval remains a separate decision.
3. Maintainer/release and security-advisory evidence as of the reviewed ref.
4. Contract-specific fit and incompatibilities against Baseline 2.0 and the component registry.
5. Adapter boundary, configuration/data egress, privilege requirements, rollback, and negative-test cases.
6. Runtime/benchmark evidence only when explicitly within the bounded task; no such evidence is claimed here.

## Disposition

This checkpoint is a corrected candidate inventory, not a completed provenance qualification. PR #417 must remain Draft until the evidence above is added for any candidate claimed as retained. No tests, deployment, secret inspection, or component activation were performed.
