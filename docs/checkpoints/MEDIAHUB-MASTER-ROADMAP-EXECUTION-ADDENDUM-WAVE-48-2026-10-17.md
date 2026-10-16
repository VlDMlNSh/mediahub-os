# Master Roadmap Execution Addendum — Wave 48

- Date: 2026-10-17
- Status: SOURCE-ANCHORED DESIGN PROPOSAL / CANDIDATE REVIEW / NOT QUALIFIED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Primary artifact: [ASTRA Authority Reconciliation and AirLLM Candidate Assessment](MEDIAHUB-ASTRA-AUTHORITY-RECONCILIATION-AND-AIRLLM-CANDIDATE-ASSESSMENT-WAVE-48-2026-10-17.md)

## Roadmap disposition

Wave 48 completed one documentation pass across the unresolved ASTRA authority wording and the requested AirLLM candidate.

### 1. ASTRA authority wording
- DEC-DEV-02 Option C remains the owner-approved split.
- Canonical ASTRA GOLD main prose retains broader A0 “single coordination/state authority” language.
- A proposed correction paragraph now states typed authority boundaries and separates the integrated system boundary from authority over internal ASTRA state and canonical product state.
- This is a proposal only. Primary source text and main remain unchanged; branch integration remains blocked by divergence and absent authorization.

### 2. AirLLM
- Upstream identity: `lyogavin/airllm`, Apache-2.0 project license declaration, active public repository.
- Candidate role: local inference library behind the MH-21 provider-neutral adapter.
- Disposition: **EVALUATION-CANDIDATE / NOT SELECTED / NOT INSTALLED / NOT QUALIFIED**.
- Key fit issue: upstream README states macOS support is Apple Silicon-only; the documented Intel-era Mac Pro 2013/macOS target is outside that documented path.
- Linux/CPU feasibility remains unknown. Layer streaming can reduce VRAM use but increases sensitivity to disk capacity, storage I/O, model architecture, context size and latency.
- Current requirements file pins older dependencies and references mutable Transformers Git main; reproducible dependency pinning, model provenance/license review, SBOM/security review and target-specific performance evidence are admission prerequisites.
- AirLLM does not replace mission orchestration, routing/failover policy, provider identity or MediaHub authority contracts.

## Next bounded work

1. Prepare a controlled change packet with exact before/after excerpts for the ASTRA authority wording conflict, retaining the existing primary source and historical blob lineage.
2. Add AirLLM to the unified local-model candidate matrix with explicit target profiles and evidence gates; keep it unselected until an authorized, bounded qualification can be planned.
3. Keep global qualification at **NO-GO / NOT PROVEN** until the existing ASTRA and Contour A gates are satisfied.

This pass performed public-source/documentation review only. No software installation, tests, model calls, credential access, host/runtime inspection, infrastructure changes, deployment or branch integration occurred.
