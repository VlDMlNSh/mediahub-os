# Project Map Addendum — Wave 107 (2026-10-17)

## Artifact newline correctness

- Main report: [MEDIAHUB-GEMINI-HTTP-REGRESSION-WAVE-106-2026-10-17.md](../checkpoints/MEDIAHUB-GEMINI-HTTP-REGRESSION-WAVE-106-2026-10-17.md).
- PR #334: https://github.com/VlDMlNSh/mediahub-os/pull/334
- Candidate HEAD: `1e052519f85afb1e9d3b58eb6d05cb45e81c2d73`.
- Workflow blob: `7465ad56496669ea576822109ca34afb47632596`.
- Harness blob: `ade921ade649ddfda42c280759c8455d5e502304`.
- Contract test blob: `809a1ddcf07f40af297182576f1a13fb652243e1`.

The primary workflow's JavaScript source had double-escaped newline sequences in candidate-text joining and Markdown artifact framing. Fixed these to emit actual line breaks. The local HTTP harness now returns two parts and asserts that the resulting artifact contains a real newline between them.

All three CI runs succeeded on the exact candidate head:
- [Gemini Read-only Workflow Contract #39068814327](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068814327)
- [Astra Verify #39068814332](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068814332)
- [Astra Cloud Runtime Validation #39068814337](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068814337)

PR #334 remains OPEN / DRAFT / UNMERGED. No independent review submissions or review threads were present when checked. No provider calls, secret access, queue admission, merge, deployment, or Contour A acceptance.

Next: obtain independent security review and verify repository review/branch protection requirements.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).
