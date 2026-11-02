# Wave 511 — FCC dotenv newline correction and exact-head revalidation (2026-11-02)

## Target and current state

- Pull request: [#623](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- Base: \`main\` at \`af200c4323bd4cb7cfa4c47dab4accc10049d1ec\`
- Candidate head after correction: \`5710e8a050e0ceb15ed2d96d77b619e6ffeab4d5\`
- Branch: \`feat/ollama-runner-ecc-wave-510\`
- PR remains OPEN and UNMERGED. Formal independent review: NOT VERIFIED (reviews endpoint returned no submitted reviews).
- Exact-head checks for \`5710e8a050e0ceb15ed2d96d77b619e6ffeab4d5\`: 7 runs QUEUED at report creation; terminal results not yet available.

## Finding and bounded correction

A source-level audit found that the FCC dotenv writer used a double-escaped newline in the shell \`printf\` format. That would write a literal backslash+n rather than terminate the dotenv assignment, potentially making the managed bearer-token file invalid. The PR-only workflow run did not exercise this code: on pull_request the live install/model/FCC/Claude steps were all SKIPPED.

Corrected the writer to use one newline escape:
\`\`\`bash
printf 'ANTHROPIC_AUTH_TOKEN=%s\n' "$ANTHROPIC_AUTH_TOKEN" > "$FCC_ENV_FILE"
\`\`\`

Added a regression test that asserts the real newline escape and rejects the double-escaped form.

## Read-back evidence

- Workflow commit: \`caa46d55dab98d945877a2bcb8745105fbbfe7de\`; resulting workflow blob: \`704e2e3e6fb3b1f94737505ef31cc4e15f568ab9\`.
- Test commit / current branch HEAD: \`5710e8a050e0ceb15ed2d96d77b619e6ffeab4d5\`; test blob: \`d39edf9c32e06acd2a8e2ce1660e4feb5c7754de\`.
- Both files were fetched again from the branch after writes. The corrected line and regression test were present in the read-back.
- Previous exact-head PR run \`41387067193\` completed SUCCESS at the earlier SHA \`2e88a0037892c8dcb1fce982bb17e662b1cc436d\`. Its workflow-contract pytest passed. Its live Ollama/FCC/Claude install and smoke steps were SKIPPED because it was a pull_request event; this is not runtime evidence.
- New exact-head checks are queued; no PASS claim is made for the corrected SHA.

## Runtime and governance disposition

- Ollama install/model pull/inference: NOT RUN.
- FCC runtime/authentication smoke: NOT RUN.
- Claude Code invocation: NOT RUN.
- Gemini controller dispatch: NOT RUN; unrelated controller governance gates remain controlling.
- SentinelX host: one active Free slot, macOS ARM64 host only; not an Ubuntu runner and not used for installation.
- Secrets/credential values: NOT accessed.
- Merge/deployment/qualification/acceptance: NOT performed / NOT QUALIFIED / NOT ACCEPTED.

## Next

1. Reconcile all seven required exact-head checks on the corrected SHA.
2. Obtain independent security review of workflow authority, FCC managed-config/token behavior, no-paid-fallback route, shell quoting and artifact hygiene.
3. Only after CI and governance review, decide whether the bounded workflow_dispatch smoke is admitted. No live dispatch is authorized by this report.

## Canonical references

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
