# WB-14AF — ASTRA lifecycle cross-route trace

- Date: 2026-10-16
- Status: SOURCE-BOUND / NON-NORMATIVE / NOT IMPLEMENTED / NOT QUALIFIED
- Scope: reconcile ASTRA internal lifecycle policy with the proposed Jarvis → ASTRA A0 ingress. Documentation only.

## Source pins

| Source | Ref | Blob SHA |
|---|---|---|
| `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | main | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` |
| `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md` | main | `7be5fadd3055642e7823c7233f90e978a87e5366` |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | main | `da26185254d9954fcee204f81ecca129bf052e7c` |
| `docs/architecture/MH-12-security-architecture.md` | main | `cf4ebfd5bf471ca676f075c51d3a24906504e490` |
| WB-14AA ingress candidate | docs ref | `030273bfe9fd6d44e78b611c011af95d08c88a45` |
| WB-14AC evidence/qualification crosswalk | docs ref | `d642311d5a487981b6ba79eeb1a49abbb26fd4d3` |
| Identity/lifecycle trace Wave 05 | docs ref | `dc60ccc0af29a74ca3cf88584d66821350b20b9f` |

The main-branch executor matrix has broader A0 wording than the docs-branch context. This source drift is recorded, not silently reconciled. DEC-DEV-02 Option C remains approved: Jarvis coordinates corporation-level missions, ASTRA A0 owns its internal engineering lifecycle, and MediaHub Product State Authority alone owns canonical product-state mutation.

## Cross-route matrix

| Concern | Documented internal ASTRA scope | External ingress gap | Safe conclusion |
|---|---|---|---|
| Identity | Tasks/commands, claims, executor binding, target SHA and evidence are represented. | No accepted request → mission → attempt ID mapping or immutable correlation rules. | Keep request, mission, attempt, lease and evidence IDs distinct. External mapping OPEN. |
| Idempotency | Duplicate-controller rejection, conflict detection and replay idempotency are described as control-plane/qualification concerns. | No accepted key scope, canonical digest, durable uniqueness boundary, conflicting-payload response, lost-ACK reconciliation or retention. | Do not claim exactly-once execution. Admission semantics OPEN. |
| Queue/lease/fencing | Internal queue, claim, lease, heartbeat and recovery are documented. Policy values: heartbeat 120s; lease 600s; executor timeout 900s; result publication 120s; retry backoff 30s; max 3 autonomous claims. | No accepted external fencing/generation contract or stale-result rule. | A0 remains sole internal queue authority. Internal timings are not external TTLs or credential expiry. |
| Cancellation race | Cancellation/recovery are internal lifecycle concerns. | No accepted external cancellation contract, race precedence, late-result disposition or terminal-state rule. | Candidate distinctions such as requested/accepted/completed/too-late/indeterminate remain non-normative. |
| Retry/restart | Bounded retry, stale-claim handling and recovery are documented. | No accepted external attempt-generation, durable restart checkpoint or lost-worker reconciliation mapping. | 30s backoff alone is not a complete retry policy and proves no runtime recovery. |
| Result/evidence | Evidence rules call for target-SHA binding, immutable evidence, provenance and independent A3 verification; self-qualification is disallowed. | No accepted external envelope binding request/digest to mission/attempt, executor, target, evidence, verifier and qualification. | Executor report, evidence completeness, verification, qualification, release and deployment remain distinct. |

## Invariants and open decisions

1. MH-12's identity → authentication → trust → capability → authorization → policy → Consumer Boundary → State Authority chain constrains ingress; authentication alone grants no operation. Ambiguity fails closed.
2. Internal timing bounds do not define request expiry, capability lifetime, replay window, challenge freshness or idempotency retention.
3. Idempotent admission can prevent duplicate logical admission only if key/digest/commit/retention rules are accepted and implemented; it does not guarantee exactly-once side effects.
4. Jarvis coordinates and observes; A0 owns its admitted-work lifecycle. No adapter may become a second queue or lifecycle authority.
5. Engineering ingress remains distinct from P0-07 → P0-05 → P0-04 product mutation.
6. Source documents establish intended policy, not implementation conformance, deployment, runtime reliability or qualification.

Still OPEN: request/mission/attempt correlation; durable commit and uncertain-ACK semantics; fencing and stale-result rejection; cancellation races; restart/retry recovery; external result/evidence envelope; accountable contract owners and acceptance workflow; controlled resolution of source wording drift.

## Disposition

No source-backed, owner-approved residual durability gap justifies selecting Temporal in this pass. It remains FUTURE-GATED / NOT SELECTED / NOT ADMITTED / NOT IMPLEMENTED / NOT QUALIFIED; this does not prove ASTRA durability is implemented. WB-14AA remains PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED. D-ING-01…04, D-ING-05a, D-ING-05b and D-ING-06 remain OPEN.

Next: use this trace to refine the WB-14AA field/state appendix, and keep every external choice explicitly OPEN until owner/governance acceptance. No tests, validators, qualification, provider calls, credentials, host/runtime inspection, installation, infrastructure changes, deployment or branch integration occurred.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
