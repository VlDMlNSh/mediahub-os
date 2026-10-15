# MediaHub OS — Contour A WB-14E: Greenfield Topology Exclusion and Provider/Workload Admission Crosswalk

- Date: 2026-10-15
- Status: **SOURCE-BOUNDED DESIGN CROSSWALK / NON-NORMATIVE / NO TARGET NODES ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED**
- Trigger: owner correction that the new system is a clean-slate design for new hardware; previous failed deployments and old server topology are not target baseline.
- Scope: establish how legacy topology references must be treated while reconciling provider identity, local-only routing and heavy-workload admission. No source code or normative contract changed.

## 1. Outcome

The clean-slate direction is already explicit in the Greenfield / Legacy Artifact Ledger, but several current source files and recent analysis reports still quote old node identities because they describe the repository's existing implementation. Those references are **evidence of legacy source content only**, not candidate target topology and not proof that old hosts remain online.

The three names called out by the owner are present in `runtime/mediahub_runtime/autonomous_queue.py` as a hard-coded permanent executor pool. The same implementation declares `github_remote_claude_only` mode. The queue therefore cannot be treated as the new target executor topology. WB-14C correctly identified this as a mismatch, but its repeated names need to remain explicitly labelled **LEGACY IMPLEMENTATION EVIDENCE — EXCLUDED FROM GREENFIELD TARGET** whenever repeated.

No old node has been accepted as part of the new deployment. New target hardware/service placement and runtime facts remain UNKNOWN unless owner-provided and explicitly accepted or later confirmed through an authorized, separately scoped inspection.

## 2. Source pins and bounded evidence

| Source | Ref / blob SHA | Evidence and interpretation |
|---|---|---|
| `docs/architecture/MEDIAHUB-GREENFIELD-LEGACY-ARTIFACT-LEDGER-WAVE-01-2026-10-15.md` | docs branch / `f97d44567328633602cdc2ca52bcd0b20138e082` | Defines TARGET-REQUIREMENT, HISTORICAL-EVIDENCE, LEGACY-OPERATIONAL, CANDIDATE-DESIGN, SHARED-OR-UNKNOWN and TARGET-ACCEPTED. Explicitly says no TARGET-ACCEPTED artifact is established by that ledger. |
| `docs/architecture/MEDIAHUB-JARVIS-ASTRA-DISTRIBUTED-AI-CORPORATION-TARGET-ARCHITECTURE-WAVE-01-2026-10-15.md` | docs branch / `c9f1716de8419d66f181fc0a9c465c65a81c7d5b` | Consolidates owner direction: Jarvis mission coordination; ASTRA bounded engineering workflow; direct heavy workload route is a proposal; local-only must fail closed. Not normative or implementation evidence. |
| `runtime/mediahub_runtime/autonomous_queue.py` | main / `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Hard-coded three-entry executor pool and `github_remote_claude_only` mode. Existing implementation evidence only; not target configuration. |
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-14C-ASTRA-QUEUE-VS-DIRECT-LOCAL-ROUTE-B-SOURCE-COMPARISON-2026-10-15.md` | docs branch / `ceff02cdaf0f02b40a1822ca54a9127ccd542c60` | Confirms Alamo is not present in that fixed pool and a separate Route B lifecycle is not established. The old names are quoted to document the mismatch, not to recommend reuse. |
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-11-PROPOSED-ALAMO-CLAUDE-HEAVY-LOCAL-WORKLOAD-ROUTING-AND-EXECUTOR-SOURCE-TRACE-2026-10-15.md` | docs branch / `b34b50dc749cade5b32e6ed369fe5b430d1a788e` | Alamo/direct heavy-workload route is explicitly a proposal, not accepted topology. “Claude local” is ambiguous between a local client using external service and a local model backend. Backend/provider/data egress are UNKNOWN. |
| `docs/checkpoints/MEDIAHUB-PROVIDER-IDENTITY-AND-EGRESS-CONTRACT-CROSSWALK-WAVE-05-2026-10-14.md` | docs branch / `01b22130e8b5de49782a7241ec14331016259de0` | Provider/gateway classification conflicts remain open; local-only fail-closed is a target invariant, not runtime enforcement evidence. |
| `docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-09-OWNER-DIRECTION-HARDWARE-BASELINE-AND-ARCHITECTURE-INTEGRITY-REVIEW-2026-10-15.md` | docs branch / `b8d6b71d4cdf3a860bca9bc955543fa412221264` | Owner-reported target hardware profiles are not independently inspected or qualified; service placement, OS, network, storage and workload envelope remain open. |

## 3. Greenfield classification rules for future work

1. **Never copy old hostnames, node IDs, user paths, runner labels, model tags, or service labels into a new target manifest by default.**
2. When such values appear in source review, label them as legacy implementation evidence and cite the source path/blob. Do not describe them as current hardware inventory.
3. Keep reusable generic logic (e.g. bounded task selection, claims, evidence digests, validation) in **SHARED-OR-UNKNOWN** until semantics and references are traced. Do not delete shared mechanisms merely because a legacy caller uses them.
4. Treat host-bound service definitions, node maps, runner configuration and fixed pools as **LEGACY-OPERATIONAL** when the ledger identifies them as old-topology-specific. Quarantine/removal still requires dependency and historical-ID review.
5. Keep Alamo as an owner-proposed logical target name only; do not infer hostname, OS, hardware, process, model location, provider, network identity or readiness from that name.
6. Do not call Claude Code client execution “local inference” without evidence of an on-machine model backend. Provider, gateway, upstream and model are distinct identities.
7. LOCAL_ONLY must fail closed and must not silently fall back to cloud. A route cannot be admitted until locality, egress, identity, resource envelope, isolation and required qualification evidence are defined.
8. Preserve the split lifecycle authority: Jarvis coordinates corporation missions; A0 owns ASTRA-internal lifecycle state; MediaHub Product State Authority alone mutates canonical product state.

## 4. Current target admission matrix

| Concern | Current target status | Required evidence before admission |
|---|---|---|
| New target node inventory | UNKNOWN / not accepted | Owner-confirmed inventory and explicit target profile; separately authorized read-only inspection if needed |
| Old executor pool | EXCLUDED FROM TARGET BASELINE | No migration-by-default; source/dependency review before any code retirement |
| Alamo/direct local route | PROPOSED / NOT ACCEPTED | Owner topology decision, executor contract, lifecycle owner, authenticated admission, persistence/fencing, result/evidence adapter |
| Heavy video-generation backend | UNKNOWN | Actual backend/model identity, supported workload, input/output contract, capacity and resource/thermal envelope |
| “Claude local” semantics | UNKNOWN | Distinguish local client from local inference runtime and upstream provider/egress |
| Local-only routing | TARGET INVARIANT / runtime enforcement unproven | Fail-closed policy and route-level evidence; no implicit cloud fallback |
| Provider/gateway identity | OPEN CONTRACT CONFLICTS | Immutable provider/gateway/upstream/model identities and consistent registry/architecture mapping |
| Workload isolation and resources | NOT QUALIFIED | Sandboxing, filesystem/network permissions, resource caps, concurrency, deadlines and recovery evidence |

## 5. Disposition and next work

- WB-14E is a documentation-only crosswalk; no runtime, hardware, credential or provider access occurred.
- No source code, primary normative architecture or deployment configuration changed.
- No tests, qualification, model/provider calls, installation, deployment, migration, branch integration or deletion occurred.
- The existing legacy ledger remains the source of classification vocabulary. This report does not replace it or mark any component TARGET-ACCEPTED.
- Next bounded step: **WB-14F — source-reference census for fixed topology and legacy operational identifiers**, starting with the highest-risk runtime/ops/workflow manifests; report references by file and classification. Do not edit code or delete artifacts in that pass.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
