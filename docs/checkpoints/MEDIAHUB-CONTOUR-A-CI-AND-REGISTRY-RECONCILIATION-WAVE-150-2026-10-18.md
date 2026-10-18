# Contour A CI and provider-registry reconciliation — Wave 150 — 2026-10-18

## Outcome
Two concrete findings were verified against live GitHub:
1. PR #358's dedicated worker-run correlation regression tests DID execute successfully on the exact PR head SHA.
2. The repository already contains multiple distinct registry/schema layers. A parallel provider registry must not be created; the next change must reconcile each layer's authority and purpose first.

## Live refs and status
- `main`: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Documentation branch `docs/mediahub-chat-tree-map-20261012`: latest fetched ref object SHA `268e7eec8c993a239db94169c03fbc4aac411d8e` (refresh before further writes; ref SHA may have moved after this pass's docs writes).
- PR #358: open, Draft, unmerged, mergeable; head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`; base `main` at `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Issue #301: open; last updated 2026-10-18T09:18:18Z. It requires accepted A0 issuer/ingress/lease/cancel/recovery and R-06 gates, target manifest, Draft 2020-12 schema validation, independent review and a controlled evidence-backed worker dispatch.
- PR #333: open, Draft, unmerged, currently `mergeable=false`; head `a83030bc6449109626b072dc0a090a59709b4a5b`, base docs branch SHA `a0c432273914fa5c4bd9e756736f9c9b72b41a77`. Do not integrate without refreshing divergence and required checks.

## PR #358 CI evidence
- Workflow run [39117896120](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39117896120), `Astra Verify`, completed `success` for head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`.
- Job `verify`, ID `117647309406`, completed `success`.
- Decoded job log explicitly shows `python -m unittest discover -s tests -p 'test_worker_run_correlation.py' -v`.
- Exact seven tests passed: duplicate exact runs fail closed; empty command ID rejected; exact fresh title selects single run; invalid run ID ignored; stale run not selected; substring collision does not match; wrong executor rejected. Log: `Ran 7 tests in 0.001s`, `OK`.
- The same job also reports `Ran 429 tests in 3.477s`, `OK` for `python -m unittest discover -s tests -p 'test_*.py'`.
- Workflow run [39117895925](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39117895925), `Astra Cloud Runtime Validation`, also succeeded; its job is a different workflow and does not contain the dedicated regression step.
- This verifies the tests ran in CI against GitHub's PR merge ref `c8024b033e31b1be218921399feefb16edb915b5` (merge of the PR head into base), with the PR head SHA recorded above. It does not qualify or deploy the worker path, and does not prove A0 signed-ingress or full provenance is implemented.

## Registry/source reconciliation
Repository tree at documentation branch tree SHA `268e7eec8c993a239db94169c03fbc4aac411d8e` is not truncated and contains the following distinct existing artifacts:
- `main:profiles/agent-registry.json`, blob SHA `993cbbe1b2b2a88da7d8884a897b404f055981a8`, declares `mediahub.ai.agent-registry` version `1.2.0`; it is an agent catalog and does not prove runtime identity or qualification.
- `main:schemas/ai/ai-provider-registry.schema.json`, blob SHA `9537a64bc948b1bea3e2a640670f48e107760a50`, Draft 2020-12 schema for provider selection (provider ID, enabled, priority, selection policy). The existing Wave 36 source registry addendum explicitly says this schema is insufficient for task admission or data-egress authorization.
- `main:ops/qualification/provider_model_registry.json`, blob SHA `62328126fd2cd8879a73bb6812adcacd3e2abe84`, a qualification/provider-model candidate ordering. It includes cost and persistence labels, but these labels are not current account-quota evidence.
- `docs:docs/checkpoints/MEDIAHUB-CLOUD-AGENT-REGISTRY-SCHEMA-V0.2-WAVE-16-2026-10-16.json`, blob SHA `b49b89b8fbdfc180862e3dc78f8198f35e486035`, proposed cloud-agent registry record schema; its own description says status values are descriptive, not authorization grants. Runtime admission still requires accepted A0/MH-12/R-06 contracts.
- `docs:docs/checkpoints/MEDIAHUB-CLOUD-AGENT-REGISTRY-AND-EVIDENCE-SCHEMAS-WAVE-13-2026-10-16.md`, blob SHA `9496dca37333f6869dce4aff58226268910c3df3`, says full JSON Schema validation remained pending at Wave 13.
- Wave 36 canonical-source addendum blob SHA `1752ae07df96144e36f8a1090dc206bc28896bf9` identifies the existing source artifacts and boundaries.

**Conclusion:** there is no single artifact that can safely be treated as both provider catalogue, account entitlement ledger and A0 authorization registry. Next pass must map ownership/readers/writers and runtime consumers, then choose the existing source of truth per data class. Do not merge provider quota hypotheses into authorization state.

## Next bounded step
1. Refresh docs branch and main refs, PR #333/#358, Issue #301.
2. Inspect all current readers/writers of `profiles/agent-registry.json`, `ops/qualification/provider_model_registry.json`, and `schemas/ai/ai-provider-registry.schema.json`; reconcile with the proposed cloud-agent v0.2 schema and source registry.
3. Produce a field-level authority crosswalk and schema-validation plan; no registry mutation until ownership and consumer contract are unambiguous.
4. Continue issuer-governance dispositions and R-06 closure; maintain all unverified provider routes as BLOCKED.

## Safety / qualification boundary
No provider API or model was called, no credential value was read, no worker dispatch was made, no PR was merged, and no deployment/qualification/independent acceptance occurred. PR #358 remains Draft and unmerged. Contour A is not qualified; Contour B remains blocked.
