# MediaHub GitHub Free-Model Orchestration

## Purpose

Provide a repository-controlled orchestration contract for optional free/public AI models without making any model authoritative and without placing credentials in GitHub source.

## Authority model

1. Git history and exact commit SHA are the source of truth.
2. Executable CI evidence is required for qualification.
3. Independent review is required for security/Release Gate.
4. Model output is advisory evidence only.
5. A model must never merge, qualify, authorize production, or modify protected baseline history by itself.

## Execution contract

The workflow `.github/workflows/mediahub-free-model-orchestration.yml` creates a deterministic task envelope. The actual model adapter is intentionally not hard-coded because availability, terms, quotas and authentication differ between free providers and can change.

A repository owner may connect a free/public model through a configured runner-side adapter or approved gateway. Credentials, if any, must be supplied only through the runner secret/environment mechanism. Never commit, print, interpolate into prompts, or store API keys/tokens in issues, artifacts, logs or source.

## Parallel role redistribution

### Tier 0 — Orchestrator
Owns task graph, exact SHA, dependency ordering, conflict detection and evidence index. Cannot self-qualify.

### Tier 1 — Fast inventory agents
Run static search, file inventory, contract extraction, test discovery and repetitive documentation checks. These tasks are parallelizable and should use low-cost/free models where an adapter exists.

### Tier 2 — Reasoning agents
Architecture, security semantics, restore governance, evidence causality and release reasoning. Prefer stronger available models; require explicit assumptions and file/SHA references.

### Tier 3 — Adversarial agents
At least two independent model passes for bypass, mutation reachability, malformed input, restore authorization and evidence-integrity attacks. Agreement is not proof.

### Tier 4 — Verification agents
Inspect CI configuration, exact-SHA workflow evidence, test coverage and evidence packet consistency. No inference from implementation alone.

### Tier 5 — Release Gate
Human/independent reviewer role. Consumes the evidence packet and may only approve when all mandatory gates are evidenced.

## Task routing for MH-05

| Workstream | Primary role | Parallel reviewers | Output |
|---|---|---:|---|
| Canonical authority | Architecture | 2 | invariant findings |
| ConsumerBoundary | Contract | 2 | boundary findings |
| Event/provenance | R3-Evidence | 2 | causality/evidence findings |
| Immutability/schema | Immutability + Schema | 1 each | structural findings |
| Restore | R4-Restore | 2 adversarial | restore findings |
| Composition | Composition | 1 | construction graph |
| Bypass | Red Team | 2+ | negative reachability |
| Tests | Test | 1 | matrix gaps |
| CI | CI-Evidence | 1 | exact-SHA execution |
| Evidence | Evidence Reconciliation | 1 | packet reconciliation |
| Independent review | Independent Review | 1+ | non-authoritative review |
| Release | Release Gate | human/independent | decision |

## Safe parallelism

Parallel agents may inspect the same SHA simultaneously. Writes to the same file must be serialized. Code changes must be minimal, scope-local and followed by fresh tests/evidence. Documentation may not claim execution that was not observed.

## Free-model fallback

If no actual model adapter is configured, the workflow must stop at deterministic planning/validation rather than pretending a model was executed. The absence of an adapter is not an execution failure of MediaHub itself; it is an unavailable optional development service.

## MH-05 restrictions

Until MH-05 is qualified: no MH-06 implementation, no persistence/HA expansion, no production authorization, no recovery redesign outside the locked remediation scope, and no mutation of immutable forensic target `25f7e3e50708d4bcad37fa712a5000dd2a7dea06`.
