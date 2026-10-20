# MediaHub OS — Wave 278: ASTRA A0 vs Product State Authority cross-contract audit

- Date: 2026-10-20
- Status: **GOVERNANCE / CONTRACT AMBIGUITY — PROPOSAL ONLY**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Prior complete source crosswalk: [Wave 277 — branch-tree drift and A0 authority crosswalk](MEDIAHUB-CONTOUR-A-TREE-DRIFT-AND-A0-AUTHORITY-CROSSWALK-WAVE-277-2026-10-20.md)
- Related ingress trust audit: [Wave 276 — Task ingress issuer and approval trust gap](MEDIAHUB-A0-TASK-INGRESS-ISSUER-AND-APPROVAL-TRUST-GAP-WAVE-276-2026-10-20.md)

## Executive decision

The repository currently uses the label `state_authority: A0-ASTRA` in the canonical qualification-launch schema and hybrid-agent-fabric profile; a canonical drift test enforces the value. The reference architecture also describes A0 as the single “MediaHub coordination and state authority”. Meanwhile, the unified system model describes A0 as the single **coordination** authority and says ASTRA GOLD must not silently become a domain State Authority. These labels admit more than one interpretation.

This audit does **not** declare the existing canonical contract invalid, and it does not change the schema or tests. It records a governance/change-control question: is `state_authority` intended to mean A0's own mission/queue/coordination state, or the MediaHub Product State Authority for canonical product/domain state? Those roles must be distinguished explicitly before A0 hybrid runtime contracts are implemented or admitted.

## Exact source evidence on `main`

Snapshot: `main` HEAD `80be45a70732b1d568164571d4273a6397792c3b`, tree `9ca2461bd2ee3028e43016089cdb39d08802ba52`.

| File | Blob SHA | Source wording / behavior |
|---|---|---|
| [ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml](https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml) | `aef6229477ed8ec45e45170f98ea87f7ba75ca29` | Under `authority`, `coordination: A0-ASTRA` and `state_authority: A0-ASTRA` appear as separate fields. |
| [ASTRA-GOLD-REFERENCE-ARCHITECTURE.md](https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md) | `7be5fadd3055642e7823c7233f90e978a87e5366` | Says “A0-ASTRA is the single MediaHub coordination and state authority”, but separately forbids providers/transports from having MediaHub State Authority. |
| [test_astra_gold_architecture_drift.py](https://github.com/VlDMlNSh/mediahub-os/blob/main/tests/test_astra_gold_architecture_drift.py) | `d6a0e6a6d81dc6e15e343cd80ee950431b1e3b14` | Explicitly asserts qualification `coordination == A0-ASTRA` and `state_authority == A0-ASTRA`; any semantics repair must update this test alongside canonical source(s). |
| [ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml](https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml) | `adc852009c3a79d0e64265a3af8a4910a1388057` | Models A0's role as `single_coordination_authority`; execution and transport classes are not authority classes. |
| [ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md](https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md) | `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | Separates A0 coordination authority from MediaHub domain State Authority; explicitly says ASTRA GOLD must not silently become domain State Authority. |
| [astra-gold-hybrid-agent-fabric.yaml](https://github.com/VlDMlNSh/mediahub-os/blob/main/profiles/providers/astra-gold-hybrid-agent-fabric.yaml) | `acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181` | Qualification-gated profile repeats both `coordinator: A0-ASTRA` and `state_authority: A0-ASTRA`. |
| [state.py](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/state.py) | `a2115b81f52a63feb357e484bd982a6a32641d81` | Defines a `StateAuthority` interface as the canonical boundary for authoritative state mutation. |
| [consumer_boundary.py](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/consumer_boundary.py) | `98bf2da9cea85da2c82145b4baef417c20b9ae73` | Describes a narrow facade preserving State Authority exclusivity and fail-closed access. |
| [lifecycle_service.py](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/lifecycle_service.py) | `0b9d3d888e988615f1ad8cd50b1bef22f2be011b` | Says the lifecycle service coordinates transitions without owning canonical state and publishes via the consumer boundary. |

## Authority crosswalk required by the project

| Domain / role | Intended responsibility | Not granted |
|---|---|---|
| Human | Final global architecture, security, production and launch authority | Does not eliminate required evidence and independent review. |
| ASTRA A0 | Authorized mission decomposition, dependency DAG, queue/claims/leases, dispatch orchestration, retries/recovery, handoff/fencing, reconciliation and evidence aggregation | No implied ownership of canonical MediaHub Product State Authority, no self-approval of disputed changes, and no transfer of global Human authority. |
| MediaHub Product State Authority | Sole canonical owner/path for product/domain state transitions under its own identity/capability/policy boundary | No worker/provider/transport may bypass or replace it. Its exact canonical contract identifier and binding to ASTRA's control-plane state must be pinned. |
| A1 / A2 / A3 | Architecture contracts / bounded implementation / independent verification | None gains state authority by role name, task assignment or successful execution. |
| Cloud/local executors and routers | Task-scoped execution or transport only after admission | No product State Authority, provider-selection authority by implication, credential creation, self-qualification or self-promotion. |
| GitHub / workflow transport | Execution transport and immutable evidence substrate | Not MediaHub domain State Authority. |

The row definitions above are a **proposed semantic crosswalk for review**, not a newly accepted contract. In particular, the current qualification schema's `state_authority` field must not simply be reinterpreted by a code comment while tests continue asserting the old ambiguous value.

## Smallest safe governance resolution

1. Decide whether the current `state_authority: A0-ASTRA` means **A0 control-plane/mission state only** or attempts to name canonical Product State Authority. Record the decision in governance / change-control for Issue #301.
2. If it means control-plane state, rename the field to an unambiguous name such as `coordination_state_authority` / `mission_state_authority` across the canonical qualification schema, reference architecture, unified model and gated provider profile. Keep Product State Authority as an explicit distinct role/contract; agree the stable identifier before committing it.
3. If the canonical schema currently conflates these domains, update canonical source-of-truth documents and their generated outputs atomically in a separate reviewed PR. Update drift/governance tests to prevent reintroducing the ambiguous label. Do not patch only the profile or tests.
4. Add contract assertions that A0 may schedule/reconcile task state but has no implicit Product State Authority; providers, transports, executors and auxiliary components cannot write canonical domain state. Verify the real `StateAuthority` / `ConsumerBoundary` enforcement remains the only permitted mutation path.
5. Make no runtime/dispatch changes until the semantics are resolved; then continue the Wave 276 trusted task-issuer/approval lifecycle, and add static/mock-only negative tests against the approved contract.

## Current workstream gates

- PR #421 is OPEN / DRAFT / UNMERGED at `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`; exact-head Astra Verify #39425009644 and Astra Cloud Runtime Validation #39425009654 previously succeeded. Independent review, caller/secret-boundary review, controlled non-launching negative test and governance/protection evidence remain open.
- PR #423 is the sole current Draft candidate to retire the two old-server-only workflows; it is based on `main` at `80be45a70732b1d568164571d4273a6397792c3b` and removes exactly the two named files. Exact-head checks #39451818611 and #39451818985 succeeded; independent review remains absent.
- PR #422 was closed as an exact duplicate of #423; it was not merged.
- The canonical documentation branch remains materially diverged from `main`. Its exhaustive tree audit found 704 docs-only blob paths, 29 main-only blob paths and 14 shared paths with differing SHAs; do not merge/rebase the entire documentation branch as a shortcut.

## Evidence boundary

This was a source/contract cross-read only. No local or CI test was run by this audit; referenced successes are existing GitHub Actions results. No provider/model calls, secret access, host/inbox inspection, workflow dispatch, PR merge, deployment, qualification or acceptance occurred.

**Disposition:** design/semantic reconciliation required; runtime enforcement and Contour A remain **NOT_PROVEN / BLOCKED**. Contour B remains gated on Contour A deployment and independent acceptance.
