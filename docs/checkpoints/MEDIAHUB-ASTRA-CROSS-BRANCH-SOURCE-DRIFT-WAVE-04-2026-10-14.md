# MediaHub OS — ASTRA cross-branch source-drift audit wave 04

- Date: 2026-10-14
- Repository: `VlDMlNSh/mediahub-os`
- Scope: compare the current `main` and documentation-branch blobs for five ASTRA GOLD architecture sources after the prior consistency wave.
- Status: **CROSS-BRANCH DOCUMENTARY AUDIT / DIVERGENCE CONFIRMED / NOT ACCEPTANCE**
- No merge, rebase, cherry-pick, tests, qualification, or normative correction performed.

## 1. Ref state

- `main` HEAD: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- `docs/mediahub-chat-tree-map-20261012` HEAD at start of pass: `c1f38da3e7b28d63138c9e052f49c24b940d4ea0`.
- Compare status: DIVERGED; docs branch ahead 781 / behind 2; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- The two commits unique to `main` are not architecture reconciliation commits; the merge-base-to-main comparison shows only `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`. This does not authorize branch integration.

## 2. Exact source comparison

| Source | `main` blob SHA | Documentation-branch blob SHA | Observed difference |
|---|---|---|---|
| `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` | `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1` | `4c977539d837292d9a0a65435159e2b81311865a` | §1 on docs branch explicitly limits A0 to ASTRA-internal queue/claim/gate state and denies MediaHub Product State Authority. Main still says “single coordination and MediaHub State Authority.” §14 still says maximum 2 autonomous claims on both refs. |
| `architecture/ASTRA-GOLD-QUALIFICATION-BLUEPRINT.yaml` | `d74a3aaf06246b0de42f21b4dc8f8907948b6443` | `9f199ba8e872d5ae188fcdac9635a53f16973534` | Docs-branch `state_authority` line clarifies ASTRA-internal queue/claim/gate state only; main line says simply `A0-ASTRA`. |
| `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` | `aef6229477ed8ec45e45170f98ea87f7ba75ca29` | `0b86b07dfa916d4485ce1f8f54d19de136d98491` | Docs-branch `state_authority` line adds the ASTRA-internal scope comment. Both refs specify `max_parallel_autonomous_claims: 3`. |
| `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md` | `7be5fadd3055642e7823c7233f90e978a87e5366` | `c93f69599fd6974847dd86c35af3f7955fccab96` | Docs branch scopes A0 to ASTRA GOLD engineering coordination and internal queue/claim/gate state; explicitly says it is not MediaHub Product State Authority. Main retains broader “single MediaHub coordination and state authority” wording. |
| `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` | `e2067dc41b52983fc4e0b2549fb6af3c099cbc60` | `c3453cc1c25709fd11a287e753b6f4435be1065d` | Both retain “A0 Astra is the single coordination authority”; that statement alone does not specify product-state ownership. Keep it in the broader reconciliation set; do not infer a conflict beyond its wording. |

## 3. Provenance of documentation-branch authority clarifications

GitHub history for the documentation branch identifies these commits:
- `1ef90ec5efb0630899758e2ee3366dd88d51a54b` — “docs: clarify Astra and MediaHub state authority boundary” (2026-10-12).
- `8324892c8458dcba41c1adfa045b4c51f535f112` — “docs: scope Astra coordinator state to Astra internals” (2026-10-12).

These commits establish that the narrower wording exists in the documentation branch history. They do **not**, by themselves, prove an owner-approved architecture decision, acceptance, qualification, or integration into `main`.

## 4. Corrected interpretation of the previous wave

The previous consistency wave correctly identified the authority wording present on `main`, but its shorthand that the wording conflict “remains open” needs branch scoping. On the documentation branch, the component scheme, qualification blueprint, launch schema, and reference architecture already contain clarifying wording. The unresolved project-level issue is therefore **cross-branch normative alignment and approval/acceptance status**, not absence of clarifying text on every branch.

The earlier report's concurrency finding remains fully current: component scheme §14 says 2 on both refs, while the launch schema and governance registry specify 3. The governance registry explicitly says the concurrency bound mirrors the qualification schema. No numeric correction was made here.

## 5. Qualification and authority status

- `main` CURRENT-TRUTH blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` still reports G0–G11 BLOCKED and overall NOT_PROVEN/BLOCKED.
- Clarifying comments in documentation are not runtime evidence, independent A3 review, acceptance, or proof of enforced authority boundaries.
- Do not merge, rebase, cherry-pick, edit `main`, or claim global resolution without explicit authorization and the required owner/governance evidence.

## 6. Findings and next bounded step

1. **Cross-branch authority wording drift — CONFIRMED.** Docs branch contains narrow A0 wording; main retains broader wording. Preserve refs and seek the project-authorized review/acceptance/integration path rather than assuming which branch wins.
2. **Concurrency ceiling 2 vs 3 — CONFIRMED on both refs.** Requires controlled source-of-truth disposition; do not choose the value here.
3. **Qualification remains BLOCKED / NOT_PROVEN on current-main truth.** No qualification was run.

Next: reconcile the status and intended disposition of the existing documentation-branch authority clarification, while keeping the numeric concurrency discrepancy separate. Qualified independent P0-07 D2 review and owner/governance decisions remain independent blockers.
