# MediaHub OS — issuer decision readiness and worker provenance crosswalk — Wave 162

- Date: 2026-10-19
- Status: **SOURCE-BOUND GOVERNANCE CROSSWALK / IMPLEMENTATION BLOCKED / NOT QUALIFIED**
- Repository: `VlDMlNSh/mediahub-os`
- Branch: `docs/contour-a-wave-162-issuer-decision-readiness-20261019`
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- This report is a documentation/evidence artifact. It does not accept the issuer proposal, define a new cryptographic protocol, authorize workflow dispatch, or qualify the worker route.

## 1. Decision

The most useful safe next step is **not** to add an independent HMAC verifier at the worker ingress yet. The current governance sources explicitly leave the issuer, verifier, trust-anchor, revocation, delegation and R-06 audit/privacy decisions open. Adding a new signature field or reusing one of the two existing HMAC envelopes without a compatibility/authority decision would create a parallel trust protocol.

The owner's earlier selection of WB-05 Option C is recorded by [PR #361](https://github.com/VlDMlNSh/mediahub-os/pull/361) as a proposal only: a separately governed MediaHub security authority would own identity/grant/revocation governance, while Jarvis remains mission coordinator, ASTRA A0 owns internal engineering-workflow state, and protected boundaries verify capability provenance. **Option C remains PROPOSED / NOT ACCEPTED / NOT IMPLEMENTED.** This report does not change that status.

Immediate disposition:
1. Keep direct workflow ingress and autonomous worker qualification BLOCKED.
2. Close/record GOV-CAP-01…07 and R-06 through the prescribed governance path.
3. Derive one versioned, accepted envelope/verifier contract and negative-test matrix from MH-12 and the approved WB-05 disposition.
4. Implement only after that accepted contract exists; test with local/pure fixtures before any controlled dispatch.
5. Separately qualify source/run/job/artifact provenance and the actual self-hosted runner isolation boundary.

## 2. Current refs, candidates and evidence status

| Resource | Current evidence at this pass | Interpretation |
|---|---|---|
| `main` | HEAD `c06015e0b1526e0aaa6a522306052b077455aba5` | Runtime source baseline for this review |
| Canonical docs branch | `docs/mediahub-chat-tree-map-20261012`, HEAD `28816f6b523c8cbc878ebd0575b17bc419669889` before the Wave 160 documentation candidate | Distinct from main; do not merge wholesale |
| Issue #301 | Open; last updated `2026-10-18T09:18:18Z` at live read | Ordered gates remain open; the issue text does not itself authorize dispatch, credentials, integration or deployment |
| PR #358 | Open/Draft, head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`, base `main` | Candidate fixes correlation only; not signed ingress |
| PR #361 | Open/Draft, head `a87acd6294fd9f8d9a7e49047dae071a566308e8`, base SHA `28816f6b523c8cbc878ebd0575b17bc419669889` | Option C governance proposal; status endpoint returned zero check runs; not accepted |
| PR #370 | Open/Draft, head `84caaedaabe9081988bda095ad9bf3f319b3479a`, base canonical docs branch | Wave 160 correlation review candidate; Wave 161 source finding is also recorded in [comment #6260974157](https://github.com/VlDMlNSh/mediahub-os/pull/370#issuecomment-6260974157) |
| PR #333 | Open/Draft, head `a83030bc6449109626b072dc0a090a59709b4a5b` | Older admission/issuer evidence vehicle, not acceptance of the issuer contract |

The map Contents API returns an empty content field for the oversized map. Its contents were read through Git blob SHA `5cb5818b827c80875dd95f710a5cc8abb207379f`; the map is not an empty document.

## 3. Source-level boundary findings

### 3.1 Signed command and workflow task are not yet one authorized envelope

Source files on `main`:

- `astra_github_agent.py`, blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`.
- `ops/qualification/run_distributed_local_worker.py`, blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`.
- `.github/workflows/astra-distributed-local-worker.yml`, blob `f650f2416c19dc75b4a0eeec037661c0c6169910`.
- `runtime/mediahub_runtime/autonomous_queue.py`, blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`.

The polling agent's `read_command()` checks the canonical control-command envelope, HMAC, timestamp freshness, current target SHA, node binding and replay marker. The workflow-launched worker is a distinct path: the workflow accepts independent inputs (`command_id`, `target_sha`, `task_id`, `node_id`, `executor`, `task_json`); `load_task()` checks JSON object shape and required task fields; `main()` checks local bindings/current HEAD/clean workspace, then creates a branch and begins builder execution. The inspected path does not verify that `task_json` is authorized by the canonical issuer envelope or bind the input command ID to such a verified envelope.

This is a source-level admission gap, not evidence of an observed exploit. GitHub workflow-dispatch permission is a separate control and does not by itself demonstrate the project's A0 issuer/capability decision.

### 3.2 Write credentials are available across the model execution boundary

The worker workflow declares `permissions: contents: write`; each checkout uses `persist-credentials: true`. The worker allows Claude commands including `Bash(git *)` and executes model-controlled code before post-execution scope/security/verifier gates. Its ordinary completion path later commits and pushes a generated branch (`git push origin HEAD:refs/heads/{branch}`).

The official [actions/checkout documentation](https://github.com/actions/checkout/blob/main/README.md) states that persisted checkout credentials enable scripts to run authenticated Git commands. Therefore the design must treat the working copy as holding a repository-write capability during model execution, not merely as a read-only source snapshot. Branch protections and exact token permissions may constrain impact; their current effective configuration was not established in this pass. No push or dispatch was attempted.

Required follow-up under an accepted workflow contract: isolate model execution from publication credentials. A trusted publication step should receive only the minimal authority needed after independently verified task scope and result checks; do not let model-controlled shell execution inherit a broad persistent write token. Verify protected-ref rules rather than assuming prompts, generated branch names or post-hoc checks constrain earlier side effects.

### 3.3 Correlation is not authentication or attestation

PR #358's exact/fresh/unique run correlation improvement has successful CI bound to head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`: runs [39117895925](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39117895925) and [39117896120](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39117896120). The reported test suite covers the correlation helper; it does not establish issuer authorization, trust-anchor lifecycle, runner isolation, or cryptographic binding of artifacts to a trusted workflow/job.

The queue must verify GitHub-derived run/workflow path, event, ref/source SHA, run ID, job ID, attempt and artifact ID/digest independently of self-asserted JSON fields. A task result must be bound to the accepted envelope digest and exact target SHA. Current main still needs its own source/CI integration checks because PR #358 is not merged.

### 3.4 Runner route classification

The reviewed workflow uses self-hosted labels `mediahub-control`, `mediahub-provider` and `astra-control`; this path must not be called GitHub-hosted ephemeral execution. The latest live SentinelX inventory still reports zero connected hosts: `mh-dev-01` and `mh-dev-02` are disabled in the dashboard and `Voktors-Mac-mini.local` is offline. Registered Codex environments: zero. This describes SentinelX-connected executor availability; separate GitHub Actions runner state was not verified here, and no worker dispatch occurred.

## 4. Governance decisions required before choosing an implementation

| Gate | Minimum accepted decision/evidence | Fail-closed condition |
|---|---|---|
| GOV-CAP-01 — issuer | Accountable issuer/attester role, grant authority and forbidden grants | No trusted-context issuance |
| GOV-CAP-02 — principal lifecycle | Enrollment, activation, suspension, recovery, revocation and authoritative status source | Unknown/unverified principal denied |
| GOV-CAP-03 — verification | Required verification points at external ingress and protected consumer boundary | Caller-supplied fields or Python types are not provenance |
| GOV-CAP-04 — trust anchor | Custody, rotation, compromise response and recovery ownership | Unknown key/issuer or failed verification denied |
| GOV-CAP-05 — expiry/revocation | Freshness windows, clock skew, in-flight rechecks, cancellation and stale status behavior | Stale/unobservable authorization denied |
| GOV-CAP-06 — delegation | Jarvis→A0 audience, operation/resource mapping, attenuation and non-inheritance | No implied corporate or Product State Authority capability |
| GOV-CAP-07 — acceptance | Positive/negative tests, provenance criteria and independent reviewer role | No ingress acceptance/qualification claim |
| R-06 — audit/privacy | Minimum audit fields, redaction, access/retention ownership, privacy classification, operation-specific audit-unavailable behavior and recovery semantics | Protected operation stays blocked when required policy is not defined |

MH-12 security architecture (main blob `cf4ebfd5bf471ca676f075c51d3a24906504e490`) requires issuer/principal/operation/resource/scope/constraints/provenance/lifetime/revocation-bound capabilities, no self-grant, bounded delegation and fail-closed authorization. It deliberately does not select a technology or key store.

The Wave 149 decision matrix (docs branch blob `9c1a02dc125b37abea9284f0c0aa5deb571f13e7`) records all GOV-CAP-01…07 as decisions required and R-06 unresolved. The Wave 150 trust-gap report (docs branch blob `6db13777ecc4e516b00d2f4100993b42d98412a7`) explicitly says not to invent an HMAC envelope or key policy before those decisions. The Wave 153 Option C proposal report blob is `484ef2dee03c332ed409d2268be6e5d29e3dc94a` and remains proposed, not normative.

## 5. Implementation-neutral negative-test matrix to carry forward

These cases can be specified now, but the signed-envelope assertions must not be implemented against an unaccepted wire format.

| Test group | Required rejection or invariant | Evidence source |
|---|---|---|
| Envelope parsing | absent/malformed fields, duplicate/ambiguous representations, oversized payload; no execution/branch creation | Worker-entry contract |
| Issuer/trust | unknown issuer, invalid signature, altered signed field, wrong trust anchor, verifier outage | Accepted issuer contract after WB-05 |
| Principal/capability | inactive/revoked principal, unknown capability, unbounded scope, operation/resource mismatch, self-grant | MH-12 + accepted WB-05 |
| Audience/binding | wrong node/audience/executor/verifier, mismatched command ID, task ID or task digest, wrong repository/ref/target SHA | Accepted task-envelope contract |
| Time/revocation | expired/future/too-stale grant, invalid clock skew, stale revocation source, revoked in-flight task | GOV-CAP-05 |
| Replay/idempotency | reused nonce/idempotency key, duplicate dispatch, retry after expiry, conflicting active claim | Accepted A0 lifecycle |
| Scope and side effects | path traversal, symlink escape, forbidden path, model attempts early push or unrelated ref update | Worker trust boundary + isolation contract |
| Run correlation | empty/malformed IDs, substring collisions, stale/naive timestamps, duplicate exact candidates, invalid run ID mixed with valid candidate | PR #358 helper and Wave 151 report |
| GitHub provenance | wrong workflow path/event/ref/source SHA, mismatched run/job/attempt, artifact not produced by selected run | GitHub-derived API evidence |
| Artifact/result binding | missing artifact, digest mismatch, task/envelope mismatch, schema/status mismatch, worker self-asserted PASS without independent verifier | Evidence-manifest/acceptance contract |
| Lifecycle recovery | lease expiry, cancellation timeout, runner loss, retry after uncertain publication, audit/revocation outage | A0 lifecycle + R-06 |

Parser and pure unit tests should run without a real dispatch, provider call, production credential or runner. Controlled dispatch is a later, separately authorized qualification gate, not a test fixture.

## 6. Next bounded step

1. Process the existing Option C proposal through the defined governance/change-control route; record explicit dispositions and accountable roles for GOV-CAP-01…07 plus R-06. Do not mark PR #361 accepted just because the proposal is open or selected as a direction.
2. Once decisions are accepted, register one versioned envelope/verifier contract with explicit canonical serialization, issuer/trust anchor, audience/node, task digest, source SHA, capability scope, expiry/revocation, replay/idempotency and audit-outage behavior.
3. Implement verifier at the actual worker ingress, before branch creation, model execution or any remote write; use the same accepted contract at every protected consumer.
4. Isolate the builder from publication authority; validate effective token/ref protections and separate artifact publication from untrusted model execution.
5. Add the negative matrix above, exact-head CI, then independent GitHub run/job/artifact-digest checks. Requalify runner isolation before any controlled dispatch.

## 7. Evidence boundary

This wave performed source reads, GitHub status reads and this report preparation. It did not edit runtime code, tests or workflow configuration, read secret values, call model/provider APIs, dispatch workflows, push branches from a worker, change host state, merge/deploy or qualify Contour A.

**Disposition:** HIGH / BLOCKING for trusted autonomous worker ingress qualification. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.
