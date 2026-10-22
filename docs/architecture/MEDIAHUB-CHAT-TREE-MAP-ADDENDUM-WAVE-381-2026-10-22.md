# MediaHub OS — chat tree map addendum, Wave 381

Date: 2026-10-22

Canonical map (unchanged): https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

Detailed report: [Wave 381 — dispatch-unique Gemini child branches](../checkpoints/MEDIAHUB-NEXT-GEMINI-DISPATCH-UNIQUE-BRANCHES-WAVE-381-2026-10-22.md).

## Change and evidence
- All three Gemini child prompts now require a role-specific branch name containing the signed `inputs.dispatch_id`.
- Existing transport-controller contract tests assert the per-dispatch branch naming requirements.
- PR [#482](https://github.com/VlDMlNSh/mediahub-os/pull/482), head `cd76cc9c58a192aaae3f38a2ea6a34b5f32ea460`, is open/unmerged.
- Exact-head Astra Verify run 39812234965, Gemini workflow contract validation run 39812235006, Astra Cloud Runtime Validation run 39812235012, and both no-secret caller-context probe runs 39812234998 / 39812235105 completed successfully.
- Contract logs include 12 transport-controller tests, 11 signed-dispatch runtime contract tests, and 2 trigger-path tests, all OK.
- Formal reviews are empty; independent review remains NOT VERIFIED. Actual model compliance with the branch naming requirement remains NOT VERIFIED until runtime evidence exists.
- HMAC payload, workflow admission, secret boundaries and controller permissions were not changed. No child workflow was dispatched.

