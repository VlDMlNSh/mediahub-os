# Contour A cloud-pool sequencing — Wave 260 — 2026-10-20

## Owner direction and status

The owner directs a change in execution emphasis: finish the controller-governed setup of the three existing Gemini agents, then move from repeated Gemini-only hardening toward a broader cloud-agent pool; integrate approved agents incrementally during Contour A engineering; only after the cloud pool is deployed and operationally qualified, design and qualify the local-executor and Jarvis reference architecture, then deploy those components. Contour B remains gated on independent acceptance of Contour A.

**Status:** owner-directed development sequence recorded; this is not itself architecture/governance acceptance, provider authorization, budget approval, dispatch evidence, deployment, or qualification.

## Current verified baseline

- Issue #301 remains open: https://github.com/VlDMlNSh/mediahub-os/issues/301. Its ordered acceptance work still includes A0 authority/lifecycle and R-06 gates, accepted runner/workspace/network manifest, standards-compliant schema validation, independent schema review, hardened read-only worker, controlled execution evidence, and admission gates for additional agents.
- PR #421 remains an open Draft: https://github.com/VlDMlNSh/mediahub-os/pull/421. Latest checked feature head: `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`; base main: `80be45a70732b1d568164571d4273a6397792c3b`.
- Exact-head checks succeeded: [Astra Cloud Runtime Validation #39425009654](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009654) and [Astra Verify #39425009644](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009644).
- No independent review is recorded on PR #421. Branch protection API verification previously returned 403 and remains unverified. Static controller contract tests do not prove runtime caller context.
- No Gemini dispatch, secret access, merge, deployment, or Contour A qualification was performed in this wave.

## Sequencing plan

1. **Close the three-Gemini controller transition.** Finish independent review of reusable-workflow caller context, permissions and secret flow; prove the negative caller guard without invoking Gemini; verify branch protection through authorized repository-administration access; satisfy exact-head checks; integrate only through the accepted governance route.
2. **Run one bounded, evidence-producing Gemini batch.** Use the sole controller path after the above gates pass. Assign complementary, fixed-scope work, require immutable source refs and evidence manifests, and treat all agent output as untrusted until reviewed. This is a closure/verification batch, not an indefinite Gemini-only development loop.
3. **Inventory and rank the broader cloud-agent pool.** Use existing project records and stable upstream components first. For each candidate record provider/model, free/quota terms, credential mechanism, GitHub-hosted execution compatibility, data-egress policy, region eligibility without spoofing, capability/issuer boundary, expiry/revocation, rate limits, provenance, costs, and acceptance tests. Do not invoke a provider or access credentials just to complete a paper inventory.
4. **Admit agents incrementally.** Implement registry and route-policy entries only when supported by source evidence; validate schema and negative fixtures; add one provider/agent at a time behind the same controller, isolated job permissions, runtime-only secret injection, explicit budget and fail-closed policy. Preserve no-paid-fallback and no-alternate-launch-path invariants unless a separate authorized decision changes them.
5. **Deploy and qualify the cloud pool.** Separate implementation, tests, runtime verification, qualification, deployment and independent acceptance. Record run/job/artifact IDs, source SHA, artifact digests, redacted logs, failure/recovery behavior, quota exhaustion and provider outage tests. Do not call the pool operational until the acceptance criteria pass.
6. **Only then design local executors and Jarvis.** Produce a source-backed reference architecture and component shortlist for local execution, workspace/network isolation, provenance, recovery and Jarvis mission coordination. Preserve the authority split: Jarvis coordinates missions; ASTRA A0 owns ASTRA-internal engineering workflow state; MediaHub Product State Authority alone mutates canonical product state.
7. **Qualify and deploy local executors/Jarvis.** Keep their readiness, security, rollback, acceptance and deployment gates separate. Do not start Contour B product development until Contour A is deployed and independently accepted.

## Guardrails and stop conditions

- The three Gemini child workflows are not considered operationally approved merely because the PR's CI passes.
- The only allowed cloud-agent launch path remains the GitHub-hosted controller and fixed-scope children; no direct child dispatch, SentinelX/server/local CLI/ad-hoc route, or alternate transport.
- No secrets in repository content, prompts, logs or artifacts; no `secrets: inherit`; no paid fallback without explicit destination-and-budget authorization; no region spoofing or proxy/VPN eligibility bypass.
- Additional agents remain candidates until their identity, capability, route, data policy, quota, expiry/revocation and evidence gates pass.
- This plan does not waive open governance or qualification gates and does not authorize deployment by itself.

## Next bounded action

Continue with PR #421's remaining independent-review and non-invoking negative caller-context evidence. In parallel, use existing project documentation to assemble a source-linked candidate inventory for the broader cloud pool without invoking new providers. The canonical project map remains the navigation entry point: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
