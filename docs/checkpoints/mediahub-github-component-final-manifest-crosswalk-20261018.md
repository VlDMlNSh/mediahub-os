# Checkpoint: Component Manifest & Architecture Crosswalk (PR #352 Follow-Up)

- **Date:** 2026-10-18
- **Task ID / Reference:** PR #352 Review Finding Follow-Up / Blob `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`
- **Agent:** gemini-agent-2 (Research & Architecture, Contour A)
- **Base Ref:** main (SHA: `c06015e0b1526e0aaa6a522306052b077455aba5`)

## 1. Provenance & Retraction Notice
- **PR #352 Clarification:** PR #352 did not itself document or establish the resolved path for the component manifest 2.0 blob.
- **Retraction:** Any prior unsupported claim of "complete reconciliation" or exhaustive automated integration across all candidate subsystems in PR #352 is hereby formally retracted and bounded to this explicit source-to-classification crosswalk.

## 2. Analyzed Artifacts & SHA Citations
1. `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` — Blob SHA: `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`
2. `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` — SHA: `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`
3. `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` — SHA: `aef6229477ed8ec45e45170f98ea87f7ba75ca29`
4. `components/COMPONENT-REGISTRY.yaml` — SHA: `3ad109ba5ec9b095d0fac851514caadcefbe2f69`

## 3. Compact Source-to-Classification Crosswalk

| Component / Subsystem | Manifest 2.0 Status (§2/§3/§4/§5) | Astra Gold Scheme Status (§3/§6/§7/§11) | Component Registry Status | Classification & Authority Tier |
|---|---|---|---|---|
| **PostgreSQL & pgvector** | EMBED_BLOCK / TARGET-GATED | Canonical relational persistence / vector retrieval | `target-selected` (native_future_gated) | Manifest-Declared Decision (Persistence Authority under MediaHub schema) |
| **Protobuf & gRPC** | EMBED_BLOCK / SELECTED | Typed versioned contracts & transport | `selected` (native) | Manifest-Declared Decision (Typed RPC & contract serialization) |
| **OpenTelemetry & Prometheus** | EMBED_BLOCK / SELECTED | Telemetry pipeline & metrics only | `selected` (native) | Manifest-Declared Decision (Observability; non-authoritative) |
| **SOPS + age / OpenBao** | SOPS+age EMBED_BLOCK / SELECTED; OpenBao Reference | SOPS/age configuration; OpenBao target-candidate | `selected` (sops/age); `target-candidate` (openbao) | Manifest-Declared Decision / Recommendation (Secret mechanics; OpenBao requires capability comparison) |
| **Cosign, Syft, Trivy** | EMBED_BLOCK / SELECTED | Supply chain / SBOM / scanning | `selected` (native) | Manifest-Declared Decision (Artifact provenance & vulnerability gates) |
| **S3-compatible storage / Harbor** | INTERFACE / SELECTED | Object contract / OCI registry | `target-interface` (adapter) | Manifest-Declared Decision (Interface contract; concrete implementation replaceable) |
| **FFmpeg & OpenCV** | EMBED_BLOCK / SELECTED | Media & vision primitives | `target-selected` (native_isolated / native_library) | Manifest-Declared Decision (Bounded primitive execution) |
| **Jellyfin, Music Assistant, Snapcast, Frigate, Immich** | Whole-product sidecars (behind MediaHub adapters) | External sidecar ecosystem | Domain-specific integration | Recommendations / Gated Sidecars (MediaHub adapters required; never direct domain state mutation) |
| **OpenOPC, OpenFlux, SoL-Pi, Colibri, unlazy** | Not in Manifest 2.0 core table | `NOT_PROVEN` candidate execution surfaces | Not in Registry | NOT_PROVEN Candidates (Execution surface only; zero state or model authority) |
| **Gemma 4, MiniCPM-V 4.5 8B 1MK, llama.cpp, ONNX Runtime** | llama.cpp & ONNX Runtime selected; MiniCPM-V / Gemma 4 local models | llama.cpp `target-selected`; MiniCPM-V & Gemma 4 `NOT_PROVEN` | `target-selected` (llama.cpp / onnx-runtime) | Manifest-Declared / NOT_PROVEN (Inference runtimes selected; specific local models require G4 qualification) |
| **FreeLLMAPI, free-coding-models** | Not in Manifest 2.0 | `NOT_PROVEN` discovery/routing candidates | Not in Registry | NOT_PROVEN Candidates (Routing/discovery only; no state/credential authority) |
| **Naabu** | Not in Manifest 2.0 | `NOT_PROVEN` security/networking tool candidate | Not in Registry | NOT_PROVEN Candidate (Bounded non-authoritative tool requiring safety review) |

## 4. Acceptance Criteria & Gaps
- **Acceptance Criteria:** Exact source provenance mapping, clear tier separation (manifest decisions vs recommendations vs NOT_PROVEN candidates), and explicit retraction of unverified integration claims.
- **Known Gaps:** Candidate components remain `NOT_PROVEN` and require full 23-wave qualification (`G4_23_WAVE_QUALIFICATION`) and independent A3 verification (`G7_INTEGRATED_A3`) prior to production admission.
- **Verification Status:** Checked against main branch artifacts at specified SHAs; documentation-only checkpoint pass completed successfully under Contour A governance.
