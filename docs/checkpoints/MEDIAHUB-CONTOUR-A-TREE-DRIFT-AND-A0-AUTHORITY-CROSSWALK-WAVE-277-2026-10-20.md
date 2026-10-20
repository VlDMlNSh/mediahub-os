# MediaHub OS — Wave 277: exhaustive branch-tree drift and A0 authority crosswalk

- Date: 2026-10-20
- Status: **SOURCE-BOUND AUDIT / NO RUNTIME ACTION / CONTOUR A NOT PROVEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Gemini transport proposal: https://github.com/VlDMlNSh/mediahub-os/pull/421
- Legacy-workflow retirement proposal: https://github.com/VlDMlNSh/mediahub-os/pull/423

## 1. Exact ref and tree evidence

At this pass, `main` is commit `80be45a70732b1d568164571d4273a6397792c3b`, tree `9ca2461bd2ee3028e43016089cdb39d08802ba52`. The canonical documentation branch is at commit `51d2c0b6e917abb44f11a655aa4c7e68669c4eda`, tree `aac37fffd343fdcb782d6815179386003e065f06`.

The live compare reports `diverged`, **2,835 commits ahead / 44 behind**, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. The compare endpoint returns only 300 file records, so those records were not treated as exhaustive. Instead, the full recursive Git trees were fetched separately; both had `truncated=false`.

| Direct tree comparison | Result |
|---|---:|
| `main` | 828 entries / 748 blobs |
| Documentation branch | 1,500 entries / 1,423 blobs |
| Blob paths only in docs branch | 704 |
| Blob paths only in main | 29 |
| Same path but different blob SHA | 14 |

Conclusion: **do not merge or rebase the documentation branch wholesale**. Apart from the 44-commit divergence, direct tree evidence identifies mainline operational files and tests that are absent from docs, plus shared paths with different content. A path-limited PR is the appropriate integration mechanism for individually reviewed retirements or corrections.

## 2. Main-only workflow and security-test gap

The following main-only paths were verified in the full `main` tree and were absent from the full documentation tree:

- Current controller/agent routes:
  - `.github/workflows/gemini-batch-dispatch-controller.yml` — `99e5a87825aeb239568f96ecef004a102ff3e53b`
  - `.github/workflows/gemini-autonomous-engineering.yml` — `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
  - `.github/workflows/gemini-agent-2.yml` — `259c8c82b8d90a39e1c90e65390e469b241b5581`
  - `.github/workflows/gemini-agent-3.yml` — `91b5397001e088dfae2f450ee77c9c23118b5601`
  - `.github/workflows/gemini-readonly-audit.yml` — `0d10efdda251f2ceca43175981c919102303572b`
  - `.github/workflows/gemini-readonly-audit-retry.yml` — `96fcc9ed4e45659d0118f0b9f3593a0c736200f0`
- Legacy operational paths:
  - `.github/workflows/mediahub-one-time-storage-migration.yml` — `b0f71f515419067c6b1508dc073b2dbce4f2ca7b`
  - `.github/workflows/mediahub-runner-migration-smoke.yml` — `1f6682584d51b8155e66959734d1f335802dde67`
- Security/context files also missing from docs:
  - `tests/test_gemini_transport_controller_contract.py` — `00fcbdb4416031ef6f736661823a7c8b6d93f344`
  - `tests/test_worker_security_gate.py` — `53098d1755518bc9fcd67a2236d874534aeb8fd5`
  - `AGENTS.md`, `GEMINI.md`, `.agents/skills/mediahub-next/SKILL.md`, and `ops/systemd/mediahub-astra-github-bootstrap.service` are also main-only; their absence is a tree fact, not a claim that the old service is installed or running.

### Shared-path deltas that need reconciliation

Fourteen paths have different blob SHAs across the two refs. Two materially security-relevant examples:

1. `.gitignore`: main `d35ed1cb54b4b081e408a1a20d0ccb4477820021`; docs `7aa8240a4ea45d95ba547c39b855b970cfbd7e14`. The main copy ignores `.gemini/` and `gha-creds-*.json`; the docs copy does not include the latter ignore entry.
2. `ops/qualification/run_distributed_local_worker.py`: main `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`; docs `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`. The secret-assignment regex in main uses whitespace escapes `\s*`; the docs version has over-escaped `\\s*`. This is a source-level pattern mismatch, not a test result.
3. `tests/test_worker_security_gate.py` exists on main (blob above) and is absent from docs. It exercises API-key assignment, bearer-token assignment, PEM private-key marker detection, and allowed non-secret text.
4. `tests/test_astra_topology_consistency.py` differs: main `cc5410f631a161b3e3bfb4bae198340f905da6e4`; docs `1362ff8723a63e3594a3559c97dc9e3091d0c674`. The docs copy uses parsed canonical YAML and source-linked values; the main copy uses earlier literal string assertions. This delta needs normal source/test review rather than automatic choice.

Other shared paths with different SHAs: `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md`, `architecture/ASTRA-GOLD-QUALIFICATION-BLUEPRINT.yaml`, `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`, `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md`, `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md`, `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml`, `contracts/README.md`, `docs/checkpoints/mediahub-mh24-traceability-matrix.md`, `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md`, `oss/manifests/components.yaml`, and `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`.

## 3. Legacy workflow disposition

The documentation branch contains explicit retirement commits for the two old-server-only workflows:
- Storage workflow retirement: https://github.com/VlDMlNSh/mediahub-os/commit/8d9dc210b1347cc254dfa745221c1d7857ee1019
- Runner smoke retirement: https://github.com/VlDMlNSh/mediahub-os/commit/5babc50cbf230c72fec2adbdc52c8897cc8ec564
- Source audit: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-WAVE-275-LEGACY-WORKFLOW-RETIREMENT-DRIFT-AUDIT-2026-10-20.md

The storage workflow has a push-to-main path trigger, `contents: write`, a self-hosted `mediahub-control` runner, old-host identity assertions, `rsync --delete`, symlink switching, deletion of a root backup, and a commit/push to main. Its actual enabled/run state is **unknown**. The runner-smoke workflow is manually dispatchable and pins the legacy hostname, UID/GID, branch and commit. Neither was invoked or tested against a host in this pass.

A focused Draft PR #423 was created directly from current `main`, without merging the docs branch:
- https://github.com/VlDMlNSh/mediahub-os/pull/423
- Base: `80be45a70732b1d568164571d4273a6397792c3b`
- Head: `ccb302b03ce224059b898d4ac6599e9f46301721`
- Exactly two files removed; `0` additions / `224` deletions.
- Exact-head runs: [Astra Cloud Runtime Validation #39451818985](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39451818985) and [Astra Verify #39451818611](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39451818611) both report SUCCESS.
- PR remains OPEN / DRAFT / UNMERGED. Review API returned no submitted reviews. CI success does not authorize merge.

This is a proposed source retirement, not evidence of actual host cleanup, workflow deactivation history, release, or acceptance.

## 4. A0 issuer/task/authorization crosswalk

Inspected source refs and their exact blob SHAs:

| Source | Blob SHA | Verified boundary |
|---|---|---|
| `runtime/mediahub_runtime/task_ingress.py` | `59e1254aa61cc8f55f53bd1e179631e81c441393` | File inbox parser for `mediahub.ai.astra-task@1.0.0`; checks request/session/command and caller-supplied approval enum; calls the existing bounded gateway. |
| `runtime/mediahub_runtime/authorization.py` | `4d8df5d3c1c26f7f133a8093cd270635b085f4d5` | Default-deny in-process allow-list over principal + capability + operation. No issuer proof, audience, signature, expiry or replay state in this context. |
| `runtime/mediahub_runtime/astra_gateway.py` | `10985e4ad8f682313d08e7492ecc1856a8bce20f` | Cloud-first gateway; inspected agent selection includes a local Ollama lane. Does not establish the required cross-destination hybrid A0 route. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Filesystem task queue, fixed local executor lane map and local claims; not a globally fenced A0 queue across cloud, user-owned devices and local executors. |
| `runtime/mediahub_runtime/agent_fabric.py` | `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | Task/path/dependency claims and expiry/lease coordination; its own module docstring says claims are coordination state, not domain authority. |
| `ops/federation/federation_admission_poc.py` | `aa39036e0613630dc8649db94626ee6753982d19` | Explicit non-production admission PoC; not wired evidence for this ingress. |
| `ops/mesh/admission.py` | `46e92d3c4f9b9865356443403e9ebd34587996cd` | Separate mesh admission seam; inspected ingress does not invoke it. |
| `ops/qualification/produce_distributed_node_attestation.py` | `d2d423325558e877845f848314ceaf583a71fd8e` | Local node evidence signer with HMAC and identity/head binding; not a trusted issuer or signed hybrid mission envelope verifier. |
| `schemas/identity/identity-boundary.schema.json` | `1d085bb1f2c458faaeff23bd92d83aa5d1bd3879` | Canonical identity-separation schema; not the `astra-task` or hybrid mission envelope. |
| `schemas/ai/ai-provider-registry.schema.json` | `9537a64bc948b1bea3e2a640670f48e107760a50` | Provider descriptor schema, not issuer, mission DAG or destination admission. |
| `profiles/providers/astra-gold-hybrid-agent-fabric.yaml` | `acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181` | Qualification-gated provider/fabric profile; cloud providers mostly NOT_PROVEN. |

### Findings

- This tree contains no separately defined canonical JSON Schema for the `mediahub.ai.astra-task` contract. The ingress enforces a small set of fields procedurally. Provider and identity schemas address different layers and cannot be treated as validating the hybrid mission envelope.
- `approval_state` is supplied in the task file and propagated to the gateway. The reviewed sources do not establish the inbox writer ACL or an independent trusted approval/issuer verifier. Treat this as an **unproven provenance boundary**, not a proven exploit, until the producer and file-writer boundary are traced.
- `AuthorizationContext` is useful as a fail-closed primitive but is not yet evidence of trusted task ingress because the inspected ingress/gateway path does not bind it to signed issuer, audience, scope/resource, freshness and replay protections.
- `profiles/providers/astra-gold-hybrid-agent-fabric.yaml` says both `coordinator: A0-ASTRA` and `state_authority: A0-ASTRA`. That wording is ambiguous against the owner’s explicit boundary between A0's mission/task orchestration and MediaHub Product State Authority. Do not promote this profile to an accepted authority contract without a crosswalk/decision that preserves separation.
- `worker_router.py` (`00ce4d3e96d327baa38de9644e7bff20a79040ed`) rejects a missing adapter when a Claude worker fails; this is not evidence of a qualified Alamo route, and the profile/routing candidate records do not prove provider upstream, authentication/cost class, egress, version or fallback graph.

### Runtime reachability qualifier

The contemporaneous [Wave 276 Task ingress trust-gap audit](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-A0-TASK-INGRESS-ISSUER-AND-APPROVAL-TRUST-GAP-WAVE-276-2026-10-20.md) further inspected the caller path: `runtime/mediahub_runtime/astra_service.py` only constructs `AstraGatewayRuntime` and waits; no `FileTaskIngress` call site was established in the inspected runtime/package sources. The package exports `FileTaskIngress` and `task_to_contract`, but that export is not proof of an active caller. Therefore the approval/issuer issue is a **latent admission-contract gap before wiring**, not a verified reachable production exploit. External callers, inbox ACLs and a trusted approval service remain unknown; this review did not exhaustively inspect every external integration.

The earlier reconciliation is in [Wave 271](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-A0-ISSUER-TASK-CONTRACT-RECONCILIATION-WAVE-271-2026-10-20.md); target routing restrictions are captured in [Wave 274](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-ALAMO-CLAUDE-ROUTER-CANDIDATE-IDENTITY-AND-NONPAID-ROUTE-GUARD-WAVE-274-2026-10-20.md). Wave 269 remains a candidate design, not an accepted runtime schema.

## 5. Gemini transport gate

PR #421 remains OPEN / DRAFT / UNMERGED at head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`. Exact-head runs [Astra Cloud Runtime Validation #39425009654](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009654) and [Astra Verify #39425009644](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39425009644) report SUCCESS. The review API returned no submitted reviews.

Still open:
- genuine independent review from another identity;
- caller-guard semantics, secret-boundary and permissions-ceiling review;
- controlled negative caller-context test that does not launch Gemini;
- governance/branch-protection integration and evidence of required-check policy.

The available connector did not provide authorized evidence for effective Actions restrictions or branch protection, so these controls remain **UNKNOWN**, not disabled. No agent was dispatched. Controller `confirm: yes` remains mandatory after the path is accepted.

## 6. Next bounded work and status classification

1. Trace the *actual* producer/writer of `mediahub.ai.astra-task`, inbox access controls, and trusted approval/attestation verifier. Reconcile that lifecycle to an authority matrix without creating a parallel controller.
2. Resolve the `A0-ASTRA` vs Product State Authority wording before designing the new field contract.
3. Only after that mapping, draft a versioned mission envelope and destination-responsibility matrix. Add schema/static/mock-only denials for missing/untrusted/expired/replayed issuer evidence, audience/resource/capability mismatch, non-admitted destination, incomplete DAG/task identity, duplicate route claims, missing locality/egress policy, and paid/unknown Alamo Claude backend or fallback.
4. Keep PR #421 and #423 Draft until their independent-review requirements are met. Do not run live routes, dispatch agents through another transport, inspect host state, merge, deploy or qualify without their respective gates.

**Explicitly not performed:** no runtime or host tests in this documentation pass; no provider/router call; no secret read; no workflow dispatch; no direct old-workflow execution; no branch synchronization; no merge, release, deployment, Contour A qualification/acceptance or Contour B work.

Contour A remains **NOT_PROVEN / BLOCKED**. Design, implementation, tests, source verification, qualification, release, deployment and acceptance remain distinct states. Contour B remains blocked pending Contour A deployment and independent acceptance.
