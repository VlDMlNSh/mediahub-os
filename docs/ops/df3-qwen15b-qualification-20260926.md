# DF3 Qwen2.5-Coder 1.5B qualification — 2026-09-26

## Evidence
- Runtime: Ollama 0.34.4, localhost API healthy.
- Model: `qwen2.5-coder:1.5b`.
- Size: 986,062,089 bytes.
- Digest: `d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668`.
- Context: 32,768.
- Exact marker: PASS — `MEDIAHUB_MODEL_QUALIFIED_OK`.
- Marker latency: approximately 1.37 s on the successful direct run.
- Coding generation: NOT PASS. The bounded patch probe returned an incomplete fenced diff and stopped at the token limit before the required `+VALUE = 2` hunk was complete.
- Therefore patch application/test qualification is NOT PASS.

## Decision
`NOT_QUALIFIED` for autonomous coding execution.

The model remains eligible for further bounded qualification attempts, but it is not activated as a production autonomous coding provider solely because health/marker checks pass.
