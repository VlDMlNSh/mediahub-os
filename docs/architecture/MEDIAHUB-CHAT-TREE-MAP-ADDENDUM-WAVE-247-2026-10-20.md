# MediaHub Chat Tree Map — Wave 247 addendum

- Date: 2026-10-20
- Status: SOURCE AUDIT / CONTRACT PROPOSAL ONLY; NOT QUALIFICATION
- Report: [Wave 247 issuer-to-publisher trace](../checkpoints/MEDIAHUB-CONTOUR-A-ISSUER-CAPABILITY-QUEUE-WORKER-TRACE-WAVE-247-2026-10-20.md)
- Issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Working branch: `work/contour-a-wave247-issuer-publisher-trace-2026-10-20`; docs base `577501f8954376b0044de350d6d67e949dfb0fc2`; main `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.

The control workflow gates by GitHub association and task-file shape; the worker loader does not verify a signed issuer/capability decision and still directly publishes source changes. PR #400's verifier and PR #399's `PROPOSED_UNVERIFIED` source bundle remain disconnected proposals.

Required boundary: authenticated issuer/capability/policy and atomic claim/lease first; worker emits only an untrusted patch/manifest; separate publisher revalidates authority, recomputes patch digest, validates exact paths and base, and publishes with its own short-lived credential. Missing authority or provenance fails closed.

No runtime code or tests were changed/run. No Gemini/worker dispatch, secret access, host mutation, merge, deployment or gate promotion occurred. Baseline 2.0 is unchanged. Contour A remains NOT PROVEN / BLOCKED; G0–G11 BLOCKED, G11 HUMAN_ONLY.
