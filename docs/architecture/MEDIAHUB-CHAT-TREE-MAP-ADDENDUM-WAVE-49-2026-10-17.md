# MediaHub OS — Chat Tree Map Addendum, Wave 49

- Date: 2026-10-17
- Status: CONTROLLED CHANGE PROPOSAL / CANDIDATE MATRIX ADDENDUM
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Current checkpoint: [Wave 49](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-17-wave49.md)

## New primary artifact

- [ASTRA Authority Controlled Change Packet and Local Inference Candidate Matrix](../checkpoints/MEDIAHUB-ASTRA-AUTHORITY-CONTROLLED-CHANGE-PACKET-AND-LOCAL-INFERENCE-CANDIDATE-MATRIX-WAVE-49-2026-10-17.md)

## Result and navigation

### ASTRA authority wording
- The main prose uses “A0 Astra is the single coordination authority”; its diagram uses “coordination/state”. The unified YAML role is `single_coordination_authority`.
- Wave 49 supplies exact before/after proposal text for Markdown and YAML, pins source blobs, and calls out schema/consumer compatibility review.
- This remains a change packet only. Canonical primary files and `main` are unchanged; DEC-DEV-02 Option C remains the governing owner decision.

### Local inference candidate matrix
- Manifest 2.0 already lists llama.cpp and ONNX Runtime as target-gated candidates; vLLM/SGLang are future-gated.
- AirLLM is documented as an additional evaluation candidate in this addendum, not added to the canonical manifest.
- Mac Pro 2013/macOS has a documented path mismatch with upstream Apple Silicon-only macOS guidance.
- Mac mini 2011/Linux compatibility and useful throughput remain unknown.
- AirLLM remains **NOT SELECTED / NOT INSTALLED / NOT QUALIFIED**; MH-21 identity, qualification, security and routing policies continue to govern admission.

No implementation, installation, tests, qualification, model/provider calls, credential access, host/runtime inspection, infrastructure change, deployment or branch integration occurred.
