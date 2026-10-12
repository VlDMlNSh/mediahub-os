# MediaHub MH-24 — Traceability Matrix

**Status:** RECONCILED — FUNCTIONAL BASELINE 2.0 ACCEPTED; IMPLEMENTATION / QUALIFICATION OPEN  
**Baseline:** Functional Baseline 2.0  
**Date:** 2026-10-12

Status reconciliation (2026-10-12): the former `RECONCILIATION CANDIDATE` label was a pre-acceptance status. The MH-24 reconciliation report (main, blob SHA `d07d162ebaa57643a7bdd84d6fb13a1102b87bfc`) records `CLOSED — FUNCTIONAL BASELINE 2.0 ACCEPTED / CANONICAL`, and Baseline 2.0 (main, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`) declares itself accepted and immutable. This updates only the matrix reconciliation status; missing implementation or qualification evidence remains missing, and no runtime/production status is inferred.

Legend:
- **Architecture:** defined/reconciled in the baseline or named checkpoint.
- **Implementation:** only marked when repository evidence is sufficient.
- **Evidence:** qualification/runtime evidence, not documentation presence.
- **—:** no sufficiently specific artifact/evidence identified during this reconciliation pass.

| # | Passport section | Architecture decision / contract | MH source | Canonical document | Implementation artifact | Qualification evidence |
|---:|---|---|---|---|---|---|
| 1 | Назначение | One local-first MediaHub product | MH-1/MH-2 + user passport | Functional Baseline 2.0 §§1–2; master reconciliation retained as provenance | core contracts/runtime | — |
| 2 | Архитектурная модель | One architecture + qualified profiles | MH-2 | Functional Baseline 2.0 §§1, 9–10; master reconciliation retained as provenance | contracts/schemas | — |
| 3 | State Authority | One logical distributed authority; no critical LWW | MH-3/MH-14/MH-20 | Functional Baseline 2.0 §§3–4, 10, 13; MH-03 contracts in their explicit scope | state/domain schemas | — |
| 4 | Home Assistant Core | HA operational authority for Smart Home | MH-5/MH-17 | Functional Baseline 2.0 §§3, 14; `architecture/STATE-HA-INTEGRATION-CONTRACT.md` is a proposed future extension, not current runtime authority | integration contracts | — |
| 5 | UI | Unified MediaHub UI | MH-9 | Functional Baseline 1.0 | — | — |
| 6 | Smart Home | Adapter/integration domain under HA authority | MH-5/MH-17 | Functional Baseline 2.0 | device schemas/tests | — |
| 7 | Manufacturers | Qualification-gated vendor adapters | MH-5/MH-17 | Functional Baseline 2.0 | component registry | — |
| 8 | Kincony/KCS | USB/model/firmware-qualified adapter path | MH-17 | Functional Baseline 2.0 | — | — |
| 9 | Wired protocols | Gateway/adapter boundary | MH-17 | Functional Baseline 2.0 | — | — |
| 10 | Wireless | Seamless coverage as qualified capability | MH-17 + network passport | Network System Passport Extension | — | — |
| 11 | Virtual Ubiquiti | Optional controller; never authority | MH-17 | Functional Baseline 2.0 | — | — |
| 12 | Automation | HA automation + controlled cross-domain orchestration | MH-5/MH-6 | Functional Baseline 2.0 | — | — |
| 13 | Voice | Google → Yandex → Siri interface order | MH-5/MH-10 | Functional Baseline 2.0 | — | — |
| 14 | AI architecture | Local → Cluster → Cloud controlled escalation | MH-10/MH-21 | Functional Baseline 2.0 | AI contracts | provider qualification evidence is separate |
| 15 | Local AI | Advisory/controlled local inference | MH-10 | Functional Baseline 2.0 | execution/backend tests | local AI capability evidence |
| 16 | Local Cluster AI | Qualified distributed AI execution | MH-10/MH-21 | hierarchical cluster architecture | federation/compute POCs | — |
| 17 | Cloud Development AI | Corporate cloud domain; no user-data authority | MH-21/MH-23 | cloud development fabric | cloud qualification workflows | provider qualification evidence |
| 18 | Trusted Sources | Verified evidence/provenance subsystem | MH-10/MH-19/MH-21 | Functional Baseline 2.0 | — | — |
| 19 | AI Human Clone | Separate cloud AI subsystem with consent/provenance | MH-10/MH-21 | Functional Baseline 2.0 | — | — |
| 20 | Mobile Access | Exactly two roles: local Core + remote access | MH-9/MH-10/MH-15 | Functional Baseline 2.0 | — | — |
| 21 | Mobile invariants | Mobile never authority/bypass | MH-9/MH-12/MH-13 | Functional Baseline 2.0 | identity/API tests | — |
| 22 | iPhone Media | AirPlay/4K capability subject to qualification | MH-18 | Functional Baseline 2.0 | — | — |
| 23 | Media System | Local-first media domain; no mandatory TV recording | MH-18 | Functional Baseline 2.0 | — | — |
| 24 | Documents | OCR/search/provenance/workflows | MH-19/MH-21 | Functional Baseline 2.0 | — | — |
| 25 | Digital Twin | Full-edition domain, paid professional boundary | MH-19/MH-21 | Functional Baseline 2.0 | — | — |
| 26 | Engineering | Paid/pro domain, provenance/qualification | MH-19/MH-21 | Functional Baseline 2.0 | — | — |
| 27 | Network | Separate logical planes; direct local data plane | MH-2/MH-17/MH-23 | Network infrastructure reference | network checkpoints | network qualification pending |
| 28 | Equipment discovery | Discover→Identify→Capability→Trust→Qualify→Admit | MH-5/MH-17 | Functional Baseline 2.0 | device/capability schemas | — |
| 29 | Smart Home export | External ecosystems are integrations, not authority | MH-5 | Functional Baseline 2.0 | — | — |
| 30 | Product editions | Unified architecture, hardware-qualified editions | MH-15 | Functional Baseline 2.0 | — | — |
| 31 | Paid functions | Entitlement-controlled professional capabilities | MH-15/MH-21 | Functional Baseline 2.0 | — | — |
| 32 | Update | RAUC target; no competing production OTA authority | MH-16/MH-20 | Functional Baseline 2.0 | update workflows | qualification pending |
| 33 | Backup/Recovery | Recovery preserves authority/provenance | MH-16/MH-22/MH-23 | Functional Baseline 2.0 | recovery workflows | recovery qualification pending |
| 34 | Security | Identity/authz/least privilege/segmentation/egress | MH-4/MH-12 | Security trust contract + CPRG docs | identity/security tests | selected POCs |
| 35 | Cloud security | Egress/minimization/workload identity/revocation | MH-12/MH-13/MH-21 | hierarchical cluster + CPRG | federation/CPRG POCs | partial |
| 36 | Local First | Critical local capability survives cloud loss | MH-1/MH-2/MH-15 | Functional Baseline 2.0 | local capability tests | local qualification evidence |
| 37 | Cluster | One logical cluster, qualified subsystems | MH-2/MH-21/MH-23 | hierarchical cluster architecture | federation POCs | partial |
| 38 | New devices | AI assists; user confirmation/security preserved | MH-5/MH-10/MH-17 | Functional Baseline 2.0 | device schemas/tests | — |
| 39 | Observability | Metrics/logs/traces/audit; privacy bounded | MH-11/MH-12/MH-13 | Functional Baseline 2.0 | observability tests | — |
| 40 | Data/Storage | Authority-first persistence; derived stores subordinate | MH-14 | Functional Baseline 2.0 | domain schemas | — |
| 41 | Knowledge/Search | Knowledge/provenance, not authority | MH-19 | Functional Baseline 2.0 | — | — |
| 42 | AI Escalation | Policy/data-class/resource based | MH-10/MH-21 | Functional Baseline 2.0 | cloud admission/orchestration tests | partial |
| 43 | OSS Foundation | Gap→license→security→provenance→adapter→benchmark | MH-20/MH-23 | implementation blueprint | component registry | — |
| 44 | OSS Adoption Rule | Governance invariant | MH-20 | Functional Baseline 2.0 | architecture governance | — |
| 45 | Architectural prohibitions | No competing authorities/bypasses | MH-20 | Functional Baseline 2.0 | contract/static tests | — |
| 46 | Qualification | Independent, evidence-first, production gate | MH-22 | qualification architecture | Astra/federation workflows | Historical evidence only; `CURRENT-TRUTH.generated.md` reports `NOT_PROVEN / BLOCKED` (blob SHA `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`); no current production qualification implied |
| 47 | Git/provenance | Commit-bound, immutable R4 | MH-20/MH-23 | Functional Baseline 2.0 | GitHub repository | commit/read-back evidence |
| 48 | Autonomous development | AI advisory, traceable, governed | MH-20/MH-23 | Functional Baseline 2.0 | Astra workflows/tests | Historical Astra records only; current generated truth remains `NOT_PROVEN / BLOCKED` until fresh mandatory evidence passes at one exact SHA |
| 49 | Developer ecosystem | Separate developer OS/apps/cloud | MH-21/MH-23 | cloud development fabric | CI/provider workflows | partial |
| 50 | Overall chain | Physical→OS→State→domains→AI→cloud | MH-2/MH-10/MH-21 | Functional Baseline 2.0 | contracts | — |
| 51 | Mobile chain | Local Core vs Remote API chain | MH-9/MH-15 | Functional Baseline 2.0 | API contracts | — |
| 52 | Smart Home chain | Physical→integration→HA→MediaHub→UI/AI | MH-5/MH-17 | STATE-HA integration contract | integration contracts | — |
| 53 | AI chain | User/App→Gateway→Local→Cluster→Cloud | MH-10/MH-21 | Functional Baseline 2.0 | AI contracts/orchestrator tests | partial |
| 54 | Cloud Development structure | Website/Trusted Sources/Human Clone/engineering | MH-21 | cloud development fabric | cloud workflows | partial |
| 55 | UX | Unified backend-hidden UX | MH-9 | Functional Baseline 2.0 | — | — |
| 56 | AI principle | AI advisory/proposal, no authority | MH-10/MH-12 | Functional Baseline 2.0 | AI contracts/tests | partial |
| 57 | Smart Home principle | HA authority, no bypass | MH-5/MH-17 | STATE-HA integration contract | integration tests | — |
| 58 | Mobile principle | Local Core + Remote Access separation | MH-9/MH-15 | Functional Baseline 2.0 | — | — |
| 59 | Cloud AI principle | Corporate cloud, controlled escalation | MH-21/MH-23 | cloud development fabric | cloud admission | partial |
| 60 | Voice order | Fixed interface order | MH-5/MH-10 | Functional Baseline 2.0 | — | — |
| 61 | Update principle | User-confirmed lifecycle | MH-16 | Functional Baseline 2.0 | update workflows | pending |
| 62 | Local-first | Local operation within qualified profile | MH-1/MH-15 | Functional Baseline 2.0 | local tests | partial |
| 63 | Functional model | Smart Home/Media/Documents/Twin/Engineering/AI/Network/Mobile/Cloud | MH-1…MH-21 | Functional Baseline 2.0 | multiple contracts | partial |
| 64 | Architectural invariant | Contract→Adapter→Validation→Integration→Qualification | MH-20/MH-23 | implementation blueprint | contract tests | partial |
| 65 | Qualification | Capability→contract→integration→security→recovery→production | MH-22 | qualification architecture | Astra/federation workflows | partial |
| 66 | Release | Locked until qualification | MH-22/MH-23 | Functional Baseline 2.0 | release workflows | partial |
| 67 | Final architecture | One unified reconciled architecture | MH-20/MH-23 | Functional Baseline 2.0 | — | — |
| 68 | Development chain | Passport→reconciliation→implementation→qualification→production | MH-20/MH-22/MH-23 | Functional Baseline 2.0 | governance/workflows | partial |

## Interpretation

The matrix deliberately contains gaps. A missing implementation or qualification column is an identified gap, not an inferred failure of architecture.

A documentation commit is provenance for a decision/document. It is not evidence that the described runtime behavior exists or is qualified.
