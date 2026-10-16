# MediaHub OS — ASTRA Authority Controlled Change Packet and Local Inference Candidate Matrix, Wave 49

- Date: 2026-10-17
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **CHANGE PROPOSAL / CANDIDATE MATRIX ADDENDUM / NOT NORMATIVE / NOT IMPLEMENTED / NOT QUALIFIED**
- Scope: exact before/after proposal for ASTRA GOLD authority wording and a source-backed candidate entry for AirLLM aligned with the existing component manifest and MH-21.
- Method: public GitHub source and documentation review only.
- Prohibited actions preserved: no installation, tests, qualification, model/provider calls, credential access, host/runtime inspection, infrastructure changes, deployment, migration, merge, rebase or cherry-pick.

## 1. Current GitHub state

At Wave 49 start:
- `main` HEAD: `6c2e8dbdee81c798b64e65546e7ded07093f100a`.
- Documentation branch HEAD: `d73910ab1301206e3026db6af787cccb1841b496`.
- Compare: **DIVERGED**, ahead 2030 / behind 14.
- Merge base: `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No branch integration or writes to `main`.

### Primary source anchors

| Source | Ref / blob SHA | Evidence relevant to this pass |
|---|---|---|
| Canonical ASTRA GOLD unified architecture | `main`, `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | Diagram calls A0 “coordination/state”; §3 line 138 states “A0 Astra is the single coordination authority.” |
| Canonical ASTRA GOLD unified YAML | `main`, `adc852009c3a79d0e64265a3af8a4910a1388057` | A0 role is `single_coordination_authority`. |
| Canonical ASTRA GOLD governance contract | `main`, `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Provider/transport/model/executor authority exclusions; missing evidence blocks. |
| Owner decision record / DEC-DEV-02 | documentation ref, `70376a2709e055972ceddc4a280d26992977213c` | Option C: Jarvis corporation mission coordination; ASTRA A0 internal engineering workflow lifecycle; Product State Authority canonical product-state mutation. |
| Canonical Component Manifest 2.0 | documentation ref, `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | AI candidates include ONNX Runtime and llama.cpp; new runtime dependency must pass §8 qualification gates. |
| MH-21 model identity | documentation ref, `2e967d73444155c8d58178a504c509d489ccd4d2` | Record provider/model identity, version/digest, request/configuration, timestamp, routing decision and provenance. |
| MH-21 model qualification | documentation ref, `daf2801b0fa930634b4e4c73eb0f1aca184b05ea` | Compatibility, security, privacy, behavior, resource profile, reliability and operational constraints. |
| MH-21 model routing policy | documentation ref, `a1ac5afa4f6cd20d384b027df5eab9095efc2bcb` | Task/data class/security/capability/resources/cost/latency/reliability determine eligibility; fallback requires explicit policy. |
| MH-21 local model security | documentation ref, `2ada0dbbe99a86b7b185272467359c7c3a2acf52` | Local model remains behind explicit security boundary and admission requirements. |
| Wave 48 AirLLM assessment | documentation ref, `87f3f5bc55f9bdab82b41c6bff46900d9149b328` | AirLLM candidate scope, upstream source notes and unresolved compatibility gates. |

## 2. ASTRA authority correction — exact controlled proposal

This section is a change packet. It does not edit canonical primary source files and does not assert owner acceptance of this exact wording.

### 2.1 Unified architecture Markdown

**Location:** `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` on `main`, §2 diagram and §3 Authority model.

**Observed current text:**

```text
A0 ASTRA CONTROLLER
coordination/state
```

And §3, item 2:

```text
2. A0 Astra is the single coordination authority.
```

**Proposed replacement for the diagram role label:**

```text
A0 ASTRA CONTROLLER
ASTRA-internal engineering lifecycle
```

**Proposed replacement for §3 item 2:**

```text
2. Jarvis coordinates corporation-level missions. ASTRA A0 owns ASTRA-internal engineering workflow state under its accepted contract, including queue, claim, lease, heartbeat, retry, cancellation, recovery and ASTRA-specific evidence/gate transitions. MediaHub Product State Authority alone owns canonical MediaHub product-state mutation.
```

**Proposed new authority-boundary item immediately after item 2:**

```text
3. The integrated ASTRA GOLD system boundary does not create a shared state authority. Executors, providers, models, gateways, transports, and verification agents have only their explicitly admitted role authority. Jarvis submits bounded engineering missions through an accepted A0 ingress contract and does not mutate A0-owned lifecycle state directly. Route A (Jarvis → A0 engineering ingress) is distinct from Route B (P0-07 → P0-05 → P0-04 canonical product mutation).
```

Renumber following items as a mechanical edit only; preserve their wording and provenance.

### 2.2 Unified ASTRA YAML

**Location:** `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml` on `main`.

**Observed current text:**

```yaml
astra:
  id: A0-ASTRA
  role: single_coordination_authority
```

**Proposed replacement:**

```yaml
astra:
  id: A0-ASTRA
  role: astra_internal_engineering_workflow_authority
```

If schema consumers depend on the old enum, this change requires a schema/consumer compatibility review before application. This packet does not assert that the proposed role value is currently schema-valid.

### 2.3 Governance and application gates

- Preserve DEC-DEV-02 Option C as the decision source; this packet is a source-text reconciliation proposal, not a new authority decision.
- Review the related reference architecture, qualification schema, tests and all consumers before any source edit.
- Maintain a before/after diff and historical blob SHA; do not rewrite historical records.
- Any accepted correction must preserve human final authority, independent A3 verification, candidate non-promotion, fail-closed admission, and Product State Authority boundaries.
- Keep WB-14AA **PROPOSED / NOT ACCEPTED / NOT FROZEN** until its own governance and contract acceptance.
- Leave `main` untouched; current branch divergence requires a separate explicit integration decision.

## 3. Unified local-inference candidate matrix — addendum only

The canonical Component Manifest 2.0 already lists ONNX Runtime and llama.cpp as target-gated AI candidates and prohibits adding a runtime without a demonstrated capability gap and §8 qualification. Therefore, this report adds AirLLM as a candidate record; it does not modify or supersede the canonical manifest.

| Candidate | Intended role | Current manifest position | Potential advantage | Material constraints | Wave 49 disposition |
|---|---|---|---|---|---|
| **llama.cpp** | Local LLM inference runtime | TARGET-GATED candidate in Manifest 2.0 | Established local inference option; should be baseline comparator for small/quantized models | Target-specific build, supported model, acceleration and performance require evidence | Existing candidate; not qualified by this pass |
| **ONNX Runtime** | General inference runtime | TARGET-GATED candidate in Manifest 2.0 | Broader model/runtime scope than LLM-only layer streaming | Model export/format and accelerator compatibility vary; task-specific benchmark needed | Existing candidate; not qualified by this pass |
| **AirLLM** | Python inference library/runtime using layer/weight streaming | Not currently listed in canonical manifest; this addendum only | Could make a large model runnable where VRAM is the binding constraint | Disk capacity/I/O, context and latency, CPU throughput, model support, old/mutable dependencies, model provenance and runtime isolation | **EVALUATION-CANDIDATE / NOT SELECTED / NOT INSTALLED / NOT QUALIFIED** |
| **vLLM / SGLang** | High-throughput inference serving | FUTURE-GATED in Manifest 2.0 | Potential throughput/concurrency advantage on suitable accelerator hardware | Requires evidence of workload need and target-compatible hardware; adds runtime footprint | Keep future-gated; no new selection |
| **Existing Ollama deployment** | Existing local model serving path where present | Runtime presence is described in Wave 02 inventory; qualification and exact model identity remain separate questions | Avoids adding a second runtime if existing path meets the task | Existing local presence is not proof of qualified model identity, security or performance | Benchmark as incumbent only when an authorized target inventory/qualification is allowed |

### 3.1 Target profile and eligibility

| Target | AirLLM compatibility status | Reason / evidence needed |
|---|---|---|
| Mac Pro 2013 / macOS | **CONDITIONAL-LOW / DOCUMENTED PATH MISMATCH** | Upstream README documents macOS support for Apple Silicon; Mac Pro 2013 is Intel-era. Do not assume support. A separately supported Linux route would require a distinct approved profile. |
| Mac mini Server 2011 / Linux / 16 GB RAM | **UNKNOWN / UNQUALIFIED** | Exact CPU, GPU/VRAM, OS/Python compatibility, storage free space/I/O, supported model and useful tokens/sec have not been evidenced in this pass. |
| Future remote GPU host | **FUTURE-GATED** | Requires an owner-approved hardware/resource profile, network/data-class policy, isolation, pinned model/runtime and qualification evidence. |
| CI / GitHub Actions runner | **NOT A DEFAULT TARGET** | Avoid downloading large weights or running inference in CI by default. Use only an explicitly approved, isolated runner with bounded cache, time, storage, network and data class. |

### 3.2 AirLLM admission gates

Before admission to the canonical component manifest or production runtime, require:

1. Demonstrated capability gap versus the already listed llama.cpp/ONNX Runtime and the qualified incumbent, for a named task/model.
2. Exact immutable AirLLM commit/release, reproducible dependency lock, removal or pinning of mutable Git dependency references, and an SBOM.
3. Target OS/CPU/GPU/driver/RAM/VRAM/storage inventory and compatibility evidence.
4. Pinned model revision, model checksum, source provenance and separate model-license/use-restriction review.
5. Measured first-token latency, steady-state tokens/sec, context behavior, concurrency, disk use, peak RAM/VRAM and failure recovery.
6. Model process isolation, filesystem scope, egress deny-by-default, secret exclusion, resource ceilings and safe artifact loading.
7. MH-21 identity/provenance fields, task/data-class policy, explicit LOCAL_ONLY semantics and policy-controlled fallback.
8. Timeout/cancellation/error/health semantics behind the provider-neutral adapter; inference output has no tool, architecture, provider-selection or product-state authority.
9. Functional, negative, privacy/security, degraded-mode, recovery, upgrade/rollback tests and independent qualification under explicit authorization.
10. Removal/replacement plan and manifest governance acceptance.

### 3.3 Routing rule

AirLLM is an inference implementation, not a router. Model selection and failover remain under the MH-21 routing policy:
- eligibility is evaluated against task, data class, privacy/security policy, model capability, resource availability, cost, latency and reliability;
- LOCAL_ONLY has no implicit cloud fallback;
- a failed local route may transition only to an explicitly authorized fallback set for that task/data class;
- every result preserves model/runtime version, digest where available, request ID, configuration, timestamp, routing decision and provenance;
- a model response never authorizes tools, changes product state or self-certifies qualification.

## 4. Decisions and open items

| ID | Item | Disposition |
|---|---|---|
| ASTRA-AUTH-RECON-01 | Replace broad A0 wording with typed internal engineering authority | **PROPOSED**; needs source-owner review and schema/consumer review |
| AIRLLM-CANDIDATE-01 | Add AirLLM to the evaluation candidate register only | **RECORDED IN THIS ADDENDUM**; canonical manifest unchanged |
| AIRLLM-TARGET-01 | Mac Pro 2013/macOS support | **DOCUMENTED PATH MISMATCH**; no target qualification |
| AIRLLM-TARGET-02 | Mac mini 2011/Linux resource/performance fit | **UNKNOWN**; hardware evidence and explicit qualification authorization needed |
| AIRLLM-ROUTING-01 | Local-only and fallback semantics | Existing MH-21 policy applies; no new routing behavior selected |
| QUAL-ALL-01 | Overall Contour A/ASTRA qualification | **NO-GO / NOT PROVEN** |

No stable canonical decision IDs are minted here; the local identifiers above are report labels only and must be collision-checked before promotion into the owner decision registry.

## 5. Next bounded step

After source-owner review, prepare a compatibility-checked patch proposal for the two ASTRA primary files, including all consumers and tests as affected-source inventory. Separately, enrich the unified local model candidate register with AirLLM and its target/evidence gates, keeping the canonical manifest unchanged until capability gap and admission evidence are accepted.

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Wave 48 prior assessment: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-ASTRA-AUTHORITY-RECONCILIATION-AND-AIRLLM-CANDIDATE-ASSESSMENT-WAVE-48-2026-10-17.md
