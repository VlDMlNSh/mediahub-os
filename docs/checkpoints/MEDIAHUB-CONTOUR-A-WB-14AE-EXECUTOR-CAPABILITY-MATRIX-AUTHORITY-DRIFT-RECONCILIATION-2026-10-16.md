# MediaHub OS — Contour A WB-14AE: Executor Capability Matrix authority-drift reconciliation

- Date: 2026-10-16
- Status: **SOURCE-LEVEL DRIFT CONFIRMED / OWNER-APPROVED SEMANTIC BOUNDARY EXISTS / MAIN SOURCE TEXT RECONCILIATION STILL OPEN**
- Scope: exact-blob comparison of the ASTRA executor capability matrix on `docs/mediahub-chat-tree-map-20261012` and `main`; no source edit or branch integration.

## 1. Exact evidence

| Ref | Blob SHA | Authority-row text |
|---|---|---|
| `docs/mediahub-chat-tree-map-20261012` | `9ad83781a8da53d1a8f540ede54eba95281f01c0` | `ASTRA workflow/control state | A0 Astra | autonomous queue + claim/lease/evidence/gate transitions only; never MediaHub Product State Authority` |
| `main` | `da26185254d9954fcee204f81ecca129bf052e7c` | `Global coordination/state | A0 Astra | autonomous queue + claim/evidence state` |

The docs-branch matrix also contains a scope clarification dated 2026-10-12 stating that “state” means ASTRA's engineering workflow/control state and does not mean MediaHub canonical product state. The main blob has no corresponding clarification section. Both blobs retain the same general capability model and executor-workflow policy status, but the authority row is materially different.

## 2. Interpretation constrained by accepted decisions

- DEC-DEV-02 Option C is already OWNER-APPROVED in the owner decision packet: Jarvis owns corporation-level mission coordination/routing; ASTRA A0 owns ASTRA-internal engineering workflow state; MediaHub Product State Authority alone owns canonical product-state mutation.
- The source-text difference is therefore a **normative wording reconciliation gap**, not an open invitation to re-decide the authority split.
- The main wording “Global coordination/state” is broader and ambiguous against the owner-approved split. The docs-branch wording is better scoped, but branch-local text does not silently become integrated into `main`.
- The branch comparison remains diverged; no merge, rebase, cherry-pick, or source synchronization is authorized or performed by this report.

## 3. Required controlled disposition

1. Preserve DEC-DEV-02 Option C as the semantic authority.
2. Route the main-source wording correction through the repository's explicitly authorized change-control/owner review path.
3. If approved, edit only the conflicting authority row and any necessary directly coupled explanatory text; retain provenance and record exact before/after blob SHAs.
4. Re-read both the modified file and the owner decision source after any authorized edit. Do not infer successful integration from a documentation-branch-only correction.
5. Keep runtime implementation, schema registration, tests, qualification and deployment status separate from this documentary reconciliation.

## 4. Scope and non-actions

This was a read-only source comparison plus a new report artifact. No normative source was changed. No branch integration, code/schema implementation, test, validator, qualification, runtime/host inspection, credential/provider/model call, installation, infrastructure change, migration, or deployment was performed.

## 5. Source anchors

- ASTRA executor capability matrix on docs branch, blob `9ad83781a8da53d1a8f540ede54eba95281f01c0`.
- ASTRA executor capability matrix on main, blob `da26185254d9954fcee204f81ecca129bf052e7c`.
- [Owner decision packet](MEDIAHUB-OWNER-DECISION-PACKET-01.md), §8 for owner-approved DEC-DEV-02 Option C and §6.1 correction history.
- [WB-14AC ingress evidence/qualification boundary](MEDIAHUB-CONTOUR-A-WB-14AC-A0-INGRESS-EVIDENCE-AND-QUALIFICATION-BOUNDARY-CROSSWALK-2026-10-16.md), which first recorded this source drift.
- [WB-14AD governance request](MEDIAHUB-CONTOUR-A-WB-14AD-A0-INGRESS-GOVERNANCE-REQUEST-2026-10-16.md), which remains a request artifact and does not authorize source changes.

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
