# Canonical map addendum — Wave 287 (2026-10-20)

## Gemini controller exact-head status and caller-context positive-path gap

- **Detailed report:** [Wave 287 exact-head and positive-context gap audit](../checkpoints/MEDIAHUB-GEMINI-CONTROLLER-EXACT-HEAD-AND-POSITIVE-CONTEXT-GAP-AUDIT-WAVE-287-2026-10-20.md), report blob SHA `ecb88790abad4df66c85d287dc690cb6a21f1bfe`, report creation commit `74161fed6bd45ff7009dc1de18bf36ca344b40c8`.
- [Canonical project map](MEDIAHUB-CHAT-TREE-MAP.md); [current continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md); [Master Development Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md); [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301); [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421).
- Verified refs at audit start: main `80be45a70732b1d568164571d4273a6397792c3b`; docs branch HEAD `2b84e27dee1e4825859d03e330d3e26de10e9fc6`; PR #421 head `3141a44370694d78f76779243adb548318a745d7`.
- Exact-head CI on PR #421 is now terminal **SUCCESS**: Cloud Runtime Validation #39462792548; workflow contract validation #39462792571; non-launching negative caller-context probe #39462792657; Astra Verify #39462792590. The last check was refreshed after Wave 286's report, where Astra Verify was still in progress.
- The real PR caller test proves the negative case only: a pull-request event and the probe workflow ref are rejected as untrusted. The static test's positive literal pair is not a runtime observation from the trusted controller. A credential-free positive-path probe remains to be designed and qualified.
- PR #421 remains OPEN / DRAFT / UNMERGED with zero submitted independent reviews. Exact-head CI success is not approval to dispatch Gemini. Do not use existing provider-secret-mapped child jobs for probe-only execution; the safe route must map no provider secret and have no model action.
- Docs branch remains DIVERGED from main, 2,897 ahead / 44 behind at audit start. No merge or rebase occurred. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated.

**Next:** obtain the required independent source/security review, then establish a separate no-credential controller-context probe that exercises only the positive trusted controller context and statically proves all Gemini action jobs are unreachable. Keep all Gemini dispatch gates closed.
