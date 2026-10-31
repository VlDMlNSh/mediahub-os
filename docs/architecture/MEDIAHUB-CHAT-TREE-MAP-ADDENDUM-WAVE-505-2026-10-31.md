# Wave 505 — two Ubuntu Hosted Runner placement audit

- Detailed report: [Wave 505 two-runner placement audit](../checkpoints/MEDIAHUB-TWO-UBUNTU-RUNNER-PLACEMENT-AUDIT-WAVE-505-2026-10-31.md).
- Owner-required architecture: VM 1 = Alamo FCC/ECC + Claude Code only; VM 2 = three Gemini CLI roles + mini-SWE-agent + Aider + OpenHands SDK + Goose.
- PR #610 currently co-locates both groups. Exact PR run 41191982864 passed contract/no-op validation only; all live runtime steps were SKIPPED and no artifacts were produced. VM 1 runtime is NOT RUN.
- Existing Gemini controller dispatches three separate child workflows, each on its own ubuntu-latest runner. Shared VM-2 co-location is NOT IMPLEMENTED and requires a reviewed controller/child contract extension.
- PR #613 exact required contexts 5/5 SUCCESS but independent review NOT VERIFIED; PR #610 required contexts NOT VERIFIED. No controller dispatch, secret read, provider call, live runtime, merge or deployment.
- SentinelX has one operational host and zero free-plan slots; this does not establish either hosted Ubuntu runner.
- Disposition: **VM 1 PR CONTRACT PASS / VM 1 RUNTIME NOT RUN / VM 2 CO-LOCATION NOT IMPLEMENTED / TWO RUNNERS NOT QUALIFIED**.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).