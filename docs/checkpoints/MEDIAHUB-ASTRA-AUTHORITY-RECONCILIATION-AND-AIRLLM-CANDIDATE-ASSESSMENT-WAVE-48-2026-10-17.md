# MediaHub OS — ASTRA Authority Reconciliation and AirLLM Candidate Assessment, Wave 48

- Date: 2026-10-17
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY PROPOSAL + UPSTREAM CANDIDATE REVIEW / NO IMPLEMENTATION / NO QUALIFICATION**
- Scope: (A) prepare a source-anchored correction proposal for the ASTRA GOLD authority wording conflict, and (B) assess AirLLM as a possible local inference component against MH-21 and Contour A constraints.
- Safety boundary: public GitHub source review and documentation only. No installation, tests, qualification, model/provider calls, credentials, host/runtime inspection, infrastructure change, deployment, or branch integration.

## 1. Source state and branch integrity

At the start of Wave 48:
- `main` HEAD: `6c2e8dbdee81c798b64e65546e7ded07093f100a`.
- Documentation branch HEAD: `fe4854b5212de5fcbd97e5f1db924c17fc24d420`.
- Compare: **DIVERGED**, ahead 2025 / behind 14.
- Merge base: `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No merge, rebase, cherry-pick or write to `main` is part of this pass.

Project source anchors:
- Owner decision record / DEC-DEV-02: docs-ref blob `70376a2709e055972ceddc4a280d26992977213c`.
- Canonical ASTRA GOLD unified architecture on main: blob `e2067dc41b52983fc4e0b2549fb6af3c099cbc60`.
- Canonical ASTRA GOLD governance contract on main: blob `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`.
- MH-21 local model security: docs-ref blob `2ada0dbbe99a86b7b185272467359c7c3a2acf52`.
- MH-21 model qualification: docs-ref blob `daf2801b0fa930634b4e4c73eb0f1aca184b05ea`.
- MH-21 model routing policy: docs-ref blob `a1ac5afa4f6cd20d384b027df5eab9095efc2bcb`.
- Canonical Component Manifest 2.0: docs-ref blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`.
- Wave 47 source delta: docs-ref blob `37845de1be1136dbfcafb8c3951a087b061832a6`.

## 2. ASTRA authority wording reconciliation proposal

### 2.1 Evidence

The owner-approved DEC-DEV-02 Option C defines the intended split:
1. Jarvis coordinates corporation-level missions and chooses only permitted routes.
2. ASTRA A0 owns ASTRA-internal engineering workflow state under its accepted contract.
3. MediaHub Product State Authority alone owns canonical product-state mutation.

The canonical ASTRA GOLD unified architecture on `main` still describes A0 as the “single coordination and state authority” and presents the integrated ASTRA GOLD control plane broadly. This is a primary-source wording conflict with the later owner-approved split. The conflict is documentary; it does not prove a deployed service or runtime authority.

### 2.2 Proposed correction language

Proposed replacement for the broad A0 authority description, subject to normal source review and acceptance:

> **A0 ASTRA Controller — ASTRA-internal engineering workflow authority.** A0 owns ASTRA GOLD internal queue, claim, lease, heartbeat, retry, cancellation, recovery, and ASTRA-specific evidence/gate transitions under its accepted internal contract. Jarvis coordinates corporation-level missions and submits bounded engineering missions through an accepted A0 ingress contract; Jarvis does not mutate A0-owned lifecycle state directly. MediaHub Product State Authority remains the sole canonical product-state mutation authority. Executors, providers, models, gateways, transports and verification agents gain no authority by implication.

Proposed accompanying clarification:

> “ASTRA GOLD is the integrated developer-fabric design” describes the system boundary and qualification scope; it does not grant every integrated component a shared state authority. Each authority is typed and limited to its accepted domain contract. Route A (Jarvis → A0 engineering ingress) remains distinct from Route B (P0-07 → P0-05 → P0-04 canonical product mutation).

### 2.3 Change-control boundaries

- Apply the proposed wording only through a controlled source change on the documentation ref after source-owner review.
- Preserve historical source text and blob lineage in the reconciliation record.
- Do not modify `main`, merge divergent refs, or imply runtime enforcement.
- The proposal does not accept WB-14AA or choose an ingress transport, endpoint, token, issuer, or schema.
- P0-05 D6 and Route B governance remain separate.

## 3. AirLLM upstream identity and source evidence

Primary upstream: [lyogavin/airllm](https://github.com/lyogavin/airllm).

Public GitHub metadata reviewed:
- Repository: `lyogavin/airllm`.
- Default branch: `main`; active, not archived.
- Latest repository commit observed: `350ca8e7207adb7c95c8ce337c1cf53fe91f6e62` (2026-10-16; star-history refresh commit).
- README blob observed in the main tree: `6a80df35b04013d58105dc4ccf6d94748826c425`.
- LICENSE blob: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`, declared Apache-2.0.
- `requirements.txt` blob: `4bc351cd3410408b9874ed02e5147544278fa9f7`.
- The repository’s latest overall commit is metadata-only; it does not prove that the inference implementation was recently changed or qualified.
- MediaHub repository tree scan found no existing AirLLM path/reference in the reviewed documentation branch snapshot.

Sources:
- [AirLLM upstream repository](https://github.com/lyogavin/airllm)
- [AirLLM README](https://github.com/lyogavin/airllm/blob/main/README.md)
- [AirLLM license](https://github.com/lyogavin/airllm/blob/main/LICENSE)
- [AirLLM requirements](https://github.com/lyogavin/airllm/blob/main/requirements.txt)

## 4. Fit to MediaHub architecture

### 4.1 Intended role

AirLLM is a model-inference library/runtime candidate focused on streaming model layers/experts to reduce GPU VRAM requirements. It is not a corporation mission coordinator, ASTRA queue authority, provider router, agent-controller framework, or MediaHub state authority.

If selected later, place it behind the existing MH-21 provider-neutral local-model adapter and task/model routing policy. Jarvis/ASTRA should see a bounded local executor/model endpoint and its provenance; AirLLM internals must remain behind that adapter.

### 4.2 Potential value

- Could enable evaluation of larger open-weight models when GPU VRAM is the primary constraint.
- Offers a Python inference interface and documents CPU inference support in its history.
- Apache-2.0 covers the AirLLM project source as declared by its repository; each model’s own license, use restrictions and provenance require separate review.
- Could provide a candidate path for local, privacy-sensitive inference where hardware, throughput, and data policy fit.

### 4.3 Material constraints and risks

1. **Hardware mismatch risk:** AirLLM README says the macOS path supports Apple Silicon only. The project’s stated Mac Pro 2013/macOS target is Intel-era hardware, so that documented macOS path is a mismatch. The separate Mac mini Linux target has 16 GB RAM by roadmap, but its GPU, storage, CPU throughput and exact model budget remain unknown.
2. **CPU path is unqualified:** the README history mentions CPU inference support, but current target performance, supported model families and useful token throughput are unknown. Treat CPU execution as research-only until compatibility and resource evidence exists.
3. **Disk and I/O pressure:** model splitting and layer-wise files can consume substantial disk capacity and make disk I/O a dominant inference cost. The README explicitly warns about high disk use; its current large-model examples cite hundreds of GB of checkpoint storage for some configurations.
4. **Dependency reproducibility:** current `requirements.txt` contains old pinned dependencies and points Transformers at mutable Git `main`, while the README advertises newer model families and model-specific dependency constraints. A pinned, compatible release/commit and dependency lock/SBOM are prerequisites for qualification.
5. **Model supply chain:** model weights, remote model code where applicable, tokenizer files, quantization artifacts and each model’s license/provenance need independent review. AirLLM’s Apache-2.0 license does not relicense downloaded models.
6. **Performance uncertainty:** low VRAM is not equivalent to high throughput. Layer streaming, context length, sequence length, model architecture, storage speed and CPU/GPU transfer costs affect latency.
7. **Security boundary:** a local model process is an untrusted inference component. Its filesystem, network egress, tool access, secrets, resource limits and output handling require the controls already stated in MH-21 local-model security.
8. **Interface gap:** the reviewed README documents a Python library API, not an accepted MediaHub provider-neutral service contract. A bounded adapter/API, health semantics, cancellation/timeouts, concurrency limits and provenance schema would be required.
9. **No failover authority:** AirLLM must not select a cloud provider, change data class, or trigger remote execution. Fallback remains explicit policy in the MediaHub router; LOCAL_ONLY must fail closed.

## 5. Candidate disposition

**Disposition: EVALUATION-CANDIDATE / NOT SELECTED / NOT INSTALLED / NOT QUALIFIED.**

Recommended use:
- Keep AirLLM in the MH-21 local inference candidate register.
- Consider it only for a hardware-specific experiment after target inventory is authorized and recorded.
- Prefer an existing qualified local runtime if it already satisfies the workload; AirLLM should be admitted only if it demonstrates a material advantage for a defined model/task and resource envelope.
- Do not make AirLLM the default local runtime, agent framework, or routing layer.

### Required evidence before any admission decision

1. Pin upstream release/commit and dependency set; resolve mutable dependency references.
2. Review source provenance, security advisories/issues, SBOM, transitive dependencies and license obligations.
3. Record target hardware/OS/accelerator/driver, RAM/VRAM, storage free space and I/O profile.
4. Select one permitted model with a pinned model revision, model license and checksum.
5. Define task/data class, context window, expected throughput/latency, concurrency and resource ceilings.
6. Define a provider-neutral adapter, health/readiness, timeout/cancellation, errors, output provenance and audit fields.
7. Verify filesystem/network isolation, secret absence, safe model-loading behavior and fail-closed LOCAL_ONLY routing.
8. Run an explicitly authorized, bounded compatibility/performance/security qualification and obtain independent review before admission.

This report performs none of these runtime activities and records no compatibility result.

## 6. Wave 48 decision and next step

- ASTRA authority reconciliation: **controlled wording proposal prepared; primary sources remain unchanged**.
- AirLLM: **candidate recorded for MH-21 evaluation; no selection or installation**.
- Global qualification remains **NO-GO / NOT PROVEN**.
- Next bounded step: record the proposed ASTRA wording in a dedicated controlled change packet with exact before/after source lines and preserve the AirLLM candidate in the unified component/model matrix, without altering main or initiating runtime qualification.

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
