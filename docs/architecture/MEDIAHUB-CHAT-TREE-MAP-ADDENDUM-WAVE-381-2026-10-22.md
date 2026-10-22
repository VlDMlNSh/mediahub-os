# MediaHub OS — chat tree map addendum, Wave 381

Date: 2026-10-22

Canonical map (unchanged): https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

Detailed report: [Wave 381 — dispatch-unique Gemini child branches](../checkpoints/MEDIAHUB-NEXT-GEMINI-DISPATCH-UNIQUE-BRANCHES-WAVE-381-2026-10-22.md).

## Change summary
- All three Gemini child prompts now request a role-specific branch name incorporating signed `inputs.dispatch_id`.
- Existing transport controller contract tests now assert these per-dispatch branch-name requirements.
- HMAC payload, workflow admission, secret boundaries and controller permissions are unchanged.
- This is a prompt-level guardrail; actual model compliance is not established by static tests.
- PR CI/review/runtime qualification remain NOT VERIFIED until exact-head evidence is available.
