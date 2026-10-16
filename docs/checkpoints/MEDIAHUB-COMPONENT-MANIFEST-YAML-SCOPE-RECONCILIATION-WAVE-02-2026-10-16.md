# MediaHub OS — Component Manifest ↔ YAML Scope Reconciliation, Wave 02

- Date: 2026-10-16
- Status: **DOCUMENTARY RECONCILIATION / SOURCE-BOUND FINDINGS / SCOPE DECISION OPEN**
- Contour: A — autonomous development environment
- Roadmap area: Phase 06 — component admission and reproducible software bill of materials
- Scope: compare the current canonical text component manifest with `oss/manifests/components.yaml`; identify representation, scope and status drift without editing either source.
- Authority boundary: this report is not a new canonical manifest, does not admit or reject a component, and does not authorize installation, testing, qualification or runtime inspection.

## 1. Live source pins

| Source | Ref | Blob SHA | Declared status / meaning |
|---|---|---|---|
| [Canonical Component Manifest 2.0](mediahub-github-component-final-manifest-2.0.md) | `main` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Calls itself the “single component-selection input”; selection CLOSED, implementation OPEN, production admission QUALIFICATION-GATED. |
| [Machine-readable component manifest](../../oss/manifests/components.yaml) | `main` | `7141dd16e9ce9dba3440b1799a56e2ac4da4106d` | `schema_version: 1`, top-level `status: qualification-gated`, `policy: MediaHub-owned-contracts`; contains a smaller set with its own statuses. |
| [Component Admission Crosswalk, Wave 01](MEDIAHUB-COMPONENT-ADMISSION-CROSSWALK-WAVE-01-2026-10-14.md) | docs branch | `6550062d5fe5af206df5ea987f4c8d8ad287d11e` | Previously recorded the scope relation as unresolved; explicitly prohibited silently copying rows or treating omissions as either defect or approval. |
| [Master Development Roadmap 1.0](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md) | docs branch | `e48c4bb6a02362373b000479e208461de88179d5` | Governs sequence; Phase 06 calls for component admission and reproducible SBOM, with earlier prerequisites still open. |

These are exact blob pins fetched for this pass. No content was changed on `main`.

## 2. Findings

### 2.1 The two artifacts have different apparent purposes, but the contract is not explicit

The text manifest says it is the single component-selection input and defines selection modes, broad domain coverage, whole-product candidates, explicit exclusions and a 17-point production qualification gate. The YAML presents a smaller operationally styled list, a different status vocabulary, and a top-level qualification gate. Neither inspected source explicitly defines whether YAML is:

- a deployment/admission subset derived from the text selection catalogue;
- a complete machine-readable mirror of every selection decision; or
- a separate target-profile manifest with its own intended consumers.

This is a **scope/traceability ambiguity**, not evidence by itself that either file is defective. The Wave 01 crosswalk already raised it; this pass bounds the exact observable differences.

### 2.2 Status disagreements among shared components

| Component/concept | Text manifest (`main`, pinned above) | YAML (`main`, pinned above) | Safe conclusion |
|---|---|---|---|
| PostgreSQL | `EMBED_BLOCK / TARGET-GATED` | `target-gated` | Semantically close; representation is not a declared mapping. |
| pgvector | `EMBED_BLOCK / TARGET-GATED` | `target-gated` | Semantically close; mapping still implicit. |
| OpenTelemetry Collector | `EMBED_BLOCK / SELECTED` | `opentelemetry`, `current-foundation` | Likely related concepts, but canonical ID and mapping are not specified. |
| Prometheus | `EMBED_BLOCK / SELECTED` | `current-foundation` | Status vocabularies differ; mapping not defined. |
| Cosign, Syft, Trivy | `SELECTED` | `current-foundation` | May represent an intentional status translation; no mapping contract is declared. |
| SOPS + age | `SELECTED` as a combined mechanics row | Separate `sops` and `age` rows, both `current-foundation` | One text row maps to two YAML IDs; relation is implicit. |
| Protobuf, gRPC | `SELECTED` | `current-foundation` | Status mapping is implicit. |
| FFmpeg | `SELECTED` | `current-foundation` with `isolation: required` | YAML adds an explicit field/constraint not represented as a field in the text manifest; this does not prove contradiction. |
| S3-compatible object storage | `INTERFACE / SELECTED` | `future_gated` | Material status/scope mismatch unless the YAML entry intentionally means a concrete implementation rather than the selected interface. The sources do not state that distinction. |
| ONNX Runtime, llama.cpp | `TARGET-GATED` | `target-gated` | Status broadly aligns; ID and schema mapping remain implicit. |
| restic, RAUC | `TARGET-GATED` | `target-gated` | Status broadly aligns; traceability remains implicit. |

The word `current-foundation` in YAML is not automatically equivalent to `SELECTED`, `IMPLEMENTED`, `QUALIFIED` or `DEPLOYED`. Any equivalence needs an explicit definition.

### 2.3 Presence/absence differences

| Difference | Examples visible in the pinned sources | What can be concluded |
|---|---|---|
| YAML entries not represented as component rows in the text manifest | Home Assistant Core; OpenBao in YAML `future_gated` | Could be an intentional external-domain authority reference or an omitted selection entry. The files do not resolve which. Home Assistant's authority boundary is described in other architecture material, but that does not establish the intended manifest inclusion rule. |
| Text manifest candidates not represented in YAML | Media sidecars (Jellyfin, Music Assistant, Snapcast, Frigate, Immich); many target-gated media/document/digital-twin/network candidates; future-gated references such as Temporal, NATS JetStream, etcd and several others | Consistent with a smaller subset, but not proof that YAML is intended as that subset. |
| Text-only selected primitives not represented as direct YAML rows | S3-compatible storage is represented only as `future_gated`; several selected media primitives/sidecars are absent | Selection, interface, implementation and runtime-admission semantics may be mixed unless scope is clarified. |
| Row granularity differs | Text groups SOPS + age; YAML splits them. Text has an S3-compatible interface row; YAML has a generic future-gated label. | A stable canonical ID and explicit one-to-one / one-to-many relation are missing from the inspected artifacts. |

Absence from YAML is not proof of exclusion; presence in YAML is not proof of production admission. No complete component inventory or runtime inventory is inferred from either file.

## 3. Decisions required before reconciliation

No owner is inferred. The following are options for the existing governance process, not accepted decisions.

### Option A — YAML is a derived deployment/admission subset (analytical recommendation)

- Keep the text manifest as the complete selection catalogue, consistent with its current “single component-selection input” statement.
- Define YAML as a machine-readable subset for a specifically named consumer and lifecycle stage (for example, candidate admission tracking or a target deployment profile); do not label it a full mirror.
- Add explicit provenance from each YAML row to the text-manifest row or to a separately accepted architecture/domain source when the row is intentionally outside the selection catalogue.
- Define a mapping between status vocabularies, and require an explicit reason for rows with no source-manifest counterpart.
- Define how interface-level selections (such as S3-compatible object storage) differ from implementation candidates, and how grouped rows map to individual IDs.
- Keep absent components absent unless the consumer's defined scope requires them.

**Benefit:** avoids turning a broad architecture catalogue into an accidental deployment allowlist. **Cost:** requires a precise subset purpose and source-traceability contract.

### Option B — YAML is a complete machine-readable mirror

- Enumerate every row and selection mode from the canonical text manifest, including whole-product, conditional, target-gated, future/reference and explicit-exclusion records as distinct statuses/types.
- Add canonical IDs, source-row references and a defined status translation.
- Preserve one-to-many mappings (SOPS + age) and interface-vs-implementation distinctions.
- Add a completeness check only after the owner accepts the schema and mapping rules.

**Benefit:** enables completeness checking. **Cost:** broader schema/change surface; risks implying runtime admission if selection and qualification statuses are not rigorously separated.

### Option C — YAML is a target-profile manifest independent of the catalogue

- Define the target/profile identity and its permitted scope first.
- Bind each row to an accepted target role/profile, source-manifest decision or separate authority source, and qualification status.
- Keep profile-specific selection separate from the canonical component catalogue.

**Benefit:** supports genuinely profile-specific deployment sets. **Cost:** target hardware/OS profiles and profile ownership are currently not fully bound; it must not be used to imply a clean target is already inventoried or qualified.

**Recommendation for owner review:** Option A is the smallest change consistent with the text manifest's existing “single component-selection input” statement, provided the intended YAML consumer is confirmed. Do not implement this recommendation until explicitly accepted.

## 4. Minimum schema/traceability fields to consider (not a schema proposal)

If and only if the owner accepts a scope option, consider documenting the following conceptual fields:

- stable component ID;
- display/name and component kind (library, runtime, sidecar, protocol/interface, reference, exclusion);
- canonical source-manifest reference (path, section/row anchor, reviewed blob SHA) or explicitly named alternate authority;
- selection mode separate from lifecycle/admission status;
- normalized lifecycle vocabulary with documented mapping from existing text/YAML statuses;
- target profile/consumer scope, if applicable;
- qualification gate/reference and evidence pointer, if applicable;
- one-to-many grouping/decomposition relation;
- decision provenance and revision/change-control reference.

This list does not define field names, enum values, YAML schema version 2, or a new registry. No IDs or statuses are being registered here.

## 5. Boundaries and non-claims

- No component was added, removed, selected, excluded, installed, invoked, tested, qualified or admitted.
- No normative text-manifest or YAML edit was made.
- No target hardware, runtime, model, deployment profile or component identity was inferred from historical host records.
- No tests, credentials/provider calls, host/runtime inspection, installation, infrastructure changes, qualification, deployment, migration, merge, rebase or cherry-pick occurred.
- The text manifest's mandatory qualification gate remains controlling for production admission; a YAML status alone cannot waive it.

## 6. Next step

Request an explicit owner/governance disposition selecting the intended relationship among Options A/B/C and naming the YAML consumer/scope. Once accepted, update only the approved source(s), record exact reviewed blob SHAs and compatibility impact, then add an authorized validation step if required. Until then, preserve both files unchanged and record the relation as OPEN.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
