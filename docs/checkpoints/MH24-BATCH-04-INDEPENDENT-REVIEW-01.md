# MH-24 Batch 04 — Independent Review 01

**Date:** 2026-10-12  
**Status:** DOCUMENTARY REVIEW / OPEN; no baseline or governance change.

## Sources read

| Source | Ref | Blob SHA |
|---|---|---|
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` |
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `f0959168dc4682a29fffeebe0a47b6ee49b96fc5` |
| B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` |
| B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` |
| MH-24 matrix | `main` | `8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6` |
| MH-24 reconciliation report | `main` | `d07d162ebaa57643a7bdd84d6fb13a1102b87bfc` |
| GAP REPORT 01 | `docs/mediahub-chat-tree-map-20261012` | `1f500d468dd7e9a9b9ca477a06344dd850410374` |
| Batch 04 | `docs/mediahub-chat-tree-map-20261012` | `26163e6f60b44e997560212bf7de9900210b7ed3` |
| MH-10 | `main` | `6ea847ddbf1604878303572b21b506102b23c930` |
| MH-21 | `main` | `61d552db4d1a1abefa2cef9f44eebcf634d11111` |
| MH-17 | `main` | `a750ee5b292043a1f1b18ec317a4b5b2c44aad24` |
| MH-03 | `architecture/mh3-runtime-foundation-20260930` | `e99035f596e236645bf8f2235fc4d375716ce476` |
| MH-04 | `architecture/mh-04-security-trust-authorization` | `78b6374daedf30ed9290dde19e7ee43a495faf05` |
| MH-05 | `architecture/mh-05-consumer-integration-boundary` | `6718905825c0f91ef21494d518b7e87dacb26ae0` |
| MH-09 | `architecture/mh-09-presentation-ui` | `b20577df2a4fdd32efc2a040a7b7a1f4a5302dee` |

Branch-only MH sources do not imply acceptance/freeze. MH-04 remains PROPOSED / REVIEW COMPLETE; MH-05 remains PROPOSED / GOVERNANCE REVIEW REQUIRED, implementation NOT AUTHORIZED; MH-09 acceptance remains NOT ACCEPTED.

## 1. Structural check

Batch 04 contains **48 unique atomic IDs**, not 47 as its final sentence says: SA4 7 + HA4 6 + UI4 4 + SH4 7 + AUTO4 5 + LAI4 7 + CLAI4 5 + CDAI4 7 = 48. This is a confirmed editorial count error; the source backlog was not changed. All eight intended section anchors (§§3–6, 12, 15–17) are present. That proves anchor coverage, not literal coverage of every clause/list entry.

## 2. Per-record independent review

Legend: **E** = core invariant explicit in B2; **P** = partial/thematic mapping only; **NL** = exact detail not located in reviewed B2 clauses; **MIXED** = literal B1 requirement is mixed with derived controls; **SPLIT** = compound requirements should be split or separately acceptance-tested. NL does not prove global absence. None of these labels proves implementation.

| ID | B2 disposition | Review finding |
|---|---|---|
| SA4-01 | E | Exact platform authority invariant; retain, implementation evidence open. |
| SA4-02 | P | System state and MediaHub-object state are separable state classes; split/link separate criteria. |
| SA4-03 | P | User configuration and resource lifecycle are separable; SPLIT or distinct clause links. |
| SA4-04 | P/MIXED | Authorization-before-mutation is source-aligned; exact principal→capability→policy trace is a derived control. |
| SA4-05 | P/SPLIT | Consistency, provenance, audit, recovery and migration are five separable obligations. |
| SA4-06 | E | Actor prohibition broadly explicit; map each actor/path to negative tests. |
| SA4-07 | E | Fail-closed/no fallback authority explicit; runtime fault evidence open. |
| HA4-01 | E | HA Core Smart Home authority explicit; contract/evidence open. |
| HA4-02 | P/SPLIT | B2 does not enumerate every HA primitive; map each primitive/category separately. |
| HA4-03 | P | Exact six-stage B1 chain not reproduced by B2 lifecycle; preserve exact sequence and contract every edge. |
| HA4-04 | P | B2 mobile/UI principles do not alone establish full Smart Home UI rule; MH-09 acceptance remains open. |
| HA4-05 | E | AI no-bypass principle explicit; negative-path evidence open. |
| HA4-06 | E | Platform vs Smart Home authority scopes explicit; conflict behavior needs contract. |
| UI4-01 | P | Unified surface principle related; route-level acceptance not established. |
| UI4-02 | NL | Minimal/grey/intuitive visual details not located in reviewed B2; keep for owner/design disposition. |
| UI4-03 | NL | macOS-like UX plus distinct MediaHub identity not located; needs approved review rubric. |
| UI4-04 | P/MIXED | Hiding technical complexity is B1; “without UI authority” is an added derived control. |
| SH4-01 | P | Smart Home lifecycle does not fully specify vendor-neutral adapter contract. |
| SH4-02 | P/SPLIT | Long device/system catalogue not enumerated in B2; disposition every capability. |
| SH4-03 | E/MIXED | “Discovery must not imply trust” is not literal B1 §6, but is supported by B2 §§4, 6, 14 and MH-17; label as derived control. |
| SH4-04 | P | B2 Identify step does not define the four-field device schema; schema remains open. |
| SH4-05 | P/MIXED | Qualification/capability principles support compatibility check; exact “before offering” order is an interpretation needing confirmation. |
| SH4-06 | P/MIXED/SPLIT | Install, configure and user-confirmation scope are separable; confirmation is derived, not literal §6 wording. |
| SH4-07 | P/MIXED | Unified UI requirement is literal; “admitted capability trace” is a derived control. |
| AUTO4-01 | P/SPLIT | B2 does not list every automation primitive; capability matrix needed. |
| AUTO4-02 | NL | Energy/security automation categories not explicit in reviewed B2 clauses; retain as unresolved product scope. |
| AUTO4-03 | P/SPLIT | AI assistance list bundles use cases; B2 only partly maps instructions/device addition. |
| AUTO4-04 | E | AI no-independent-authority explicit; bypass tests open. |
| AUTO4-05 | P/MIXED | Controlled mechanisms align; auditable-result requirement is an added acceptance control. |
| LAI4-01 | P/MIXED | Local execution literal; data-boundary controls are derived from B2 privacy/local-first clauses. |
| LAI4-02 | P/MIXED | Inference/NL literal; qualified backend/resource envelope is derived. |
| LAI4-03 | P/MIXED | Assistance literal; uncertainty/provenance UX is derived, not fully specified by B2. |
| LAI4-04 | P/MIXED | Automation/setup literal; full proposal→policy→authorization path is cross-source derived. MH-05 remains unauthorized. |
| LAI4-05 | P/SPLIT/MIXED | Instructions, search and local data processing are separate; provenance/privacy/access controls need separate criteria. |
| LAI4-06 | P/MIXED | Cross-domain synthesis, not a single literal §15 clause; link separate domain clauses. |
| LAI4-07 | E | Advisory/proposal-only and non-authority explicit; runtime bypass evidence open. |
| CLAI4-01 | P/MIXED | Trusted-cluster intent present; node admission/trust mechanics need exact B2 §10 mapping and qualification. |
| CLAI4-02 | P/SPLIT | Workload list bundles distinct classes; map each to capability and qualification evidence. |
| CLAI4-03 | NL | Named “MediaHub AI Gateway” not located in reviewed B2 text; general policy-based routing does not accept the named component by itself. |
| CLAI4-04 | E/MIXED | Non-authority is explicit in B2; detailed escalation tests are derived acceptance controls. |
| CLAI4-05 | P/MIXED | Scheduler, resource/failure semantics are downstream; label as derived qualification criteria. |
| CDAI4-01 | E | Corporate developer domain distinct from user domain explicit; runtime boundary evidence open. |
| CDAI4-02 | P/NL/SPLIT | Bundled inventory includes named subsystems not established by generic AI/engineering clauses; split items and obtain owner disposition. |
| CDAI4-03 | E/P | Domain separation explicit; direct-access enforcement not proven by architecture wording. |
| CDAI4-04 | E/P | Conditional bounded cloud execution aligns with B2; exact thresholds/reason codes remain unspecified. |
| CDAI4-05 | E | Privacy/residency/egress principles explicit; enforcement evidence open. |
| CDAI4-06 | E/MIXED | Cloud non-authority explicit; “remote results are data” is derived acceptance wording. |
| CDAI4-07 | P/SPLIT/MIXED | Provider qualification, fallback allowlist and local-critical continuity are distinct; not all are literal §17 requirements. |

## 3. Findings and required follow-up

1. **Correct the count in a future controlled documentary edit:** 48, not 47. Do not silently rewrite this historical source.
2. **Split or add explicit sub-criteria** at least for SA4-05, HA4-02, SH4-02, SH4-06, AUTO4-01/03, LAI4-05, CLAI4-02, CDAI4-02/07. Other bundled records also need clause-level links when their elements can pass/fail independently.
3. **Separate literal B1 requirements from derived controls.** Examples: discovery/trust separation, explicit confirmation for integration changes, auditability, uncertainty UX, scheduler failure behavior, provider fallback restrictions and negative tests. These may be justified by B2/MH sources but must not be attributed to literal B1 clauses.
4. **Do not treat thematic B2 mapping as closure.** Exact visual design language, energy/security automation categories, the precise HA chain, the named AI Gateway and parts of the Trusted Sources/AI Human Clone taxonomy are PARTIAL or NOT LOCATED in the reviewed B2 clauses.
5. **Keep governance conflicts open.** Matrix header `RECONCILIATION CANDIDATE` still conflicts with B2/reconciliation-report acceptance declarations. This review does not resolve it.
6. **No implementation claim:** this documentary review does not establish current runtime behavior, tests, independent qualification, release or production authorization.

## 4. Conclusion

**Independent review of all 48 declared Batch 04 IDs is complete; clause-level coverage remains PARTIAL / OPEN.** The eight intended B1 section anchors are present, but the batch contains one confirmed count typo, multiple compound records and several rows mixing literal source requirements with derived acceptance controls. Exact B2 mapping must remain clause-specific, with PARTIAL/NOT LOCATED retained where general principles do not establish details.

No B1, B2, matrix or branch-specific source was changed. No status was upgraded. No tests/qualification, installation, deployment, infrastructure/production action or merge to `main` was performed.

**Next safe step:** run a literal clause-coverage audit of the eight B1 sections, linking each sentence/list/order/prohibition to reviewed records and flagging omissions/derived controls; then consider a separate, traceable backlog correction. Do not close requirements by inference.
