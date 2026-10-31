# Wave 489 — Hosted runner manifest reconciliation

- [Wave 489 runner/workspace/network manifest v0.2](../checkpoints/MEDIAHUB-RUNNER-WORKSPACE-NETWORK-TARGET-MANIFEST-WAVE-489-2026-10-31.json)
- Reconciles the Wave 478 single-profile candidate with the Wave 488 source-verified standard GitHub-hosted runner catalog.
- Keeps `ubuntu-24.04` x64 as the only default candidate; ARM64, Windows and macOS remain secondary/specialist profiles, not reserved capacity.
- Explicitly records account plan, effective concurrency, artifact retention and destination-level egress enforcement as NOT VERIFIED.
- Separates ephemeral hosted jobs from self-hosted identities and persistent GUI workers.
- No dispatch, provider call, secret access, benchmark, merge, deployment, qualification or acceptance occurred.
- Status: documentation candidate only; independent review and schema validation NOT RUN.
- Branch: `docs/wave489-hosted-runner-manifest-reconciliation-20261031`, based on PR #601 head `02f0988cdeac2c6b360946c9a62b7a56f21c142d`.
- Report: [Wave 489 reconciliation report](../checkpoints/MEDIAHUB-HOSTED-RUNNER-MANIFEST-RECONCILIATION-WAVE-489-2026-10-31.md)
- Canonical documentation map remains on `docs/mediahub-chat-tree-map-20261012`; this addendum is not indexed into that canonical branch yet.
