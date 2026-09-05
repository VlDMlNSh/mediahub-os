# MH-01 → MH-23 Interface Contract

Status: PROPOSED / REQUIRES VERIFICATION.

## Universal contract

Every MH domain MUST preserve: sole State Authority; explicit authorization; deny-by-default; local-first core; AI/cloud non-authority; privacy-by-default; least privilege; explicit trust; observability; recoverability; compatibility-aware evolution; evidence-first engineering.

Every MH MUST return: requirements, architecture rules, implementation constraints, verification method, evidence, decisions, contradictions, unknowns, dependencies and acceptance status.

## Domain contract

| MH | Domain | Input from MH-01 | Required return |
|---|---|---|---|
| 02 | Reference Architecture | charter, scope, authority | boundaries, planes, trust/dependency model |
| 03 | Runtime Foundation | deterministic/local core | runtime architecture and lifecycle evidence |
| 04 | State Authority | sole-authority invariant | state contract reconciliation |
| 05 | Consumer Boundary | bounded mutation path | integration/consumer contract |
| 06 | Core Runtime Services | lifecycle constraints | service architecture |
| 07 | Configuration/Policy | governance/authorization | policy architecture and publication gap disposition |
| 08 | Plugin/Extension | no authority escalation | extension boundary |
| 09 | Presentation/UI | non-authoritative UI | presentation architecture |
| 10 | AI/Intelligence | AI non-authority | inference/proposal architecture |
| 11 | Observability | observable system | diagnostic/event architecture |
| 12 | Security | security invariants | security architecture |
| 13 | Privacy/Data Governance | local/private default | data classification/flow governance |
| 14 | Persistence | persistence ≠ authority | persistence architecture |
| 15 | OS/Appliance | product boundary | platform/appliance architecture |
| 16 | Installer/Recovery/Update | recoverability | recovery/update architecture |
| 17 | Device/Protocol | explicit trust | device/integration architecture |
| 18 | Media/Content | product scope | media architecture |
| 19 | Knowledge/Digital Twin | knowledge ≠ authority | representation/knowledge architecture |
| 20 | Automation/Energy/Self-Healing | safety hierarchy | automation architecture |
| 21 | Hybrid Cloud/Distributed AI | cloud non-authority | controlled external-compute architecture |
| 22 | Production/Qualification | governance gates | qualification/operations evidence |
| 23 | Evolution/Migration | compatibility rules | migration/versioning architecture |

## Non-delegable decisions

MH-01/governance retains exclusive authority over product mission/scope, global safety hierarchy, canonical authority model, global security/privacy posture, cross-MH invariants, frozen-contract protection and change-control/acceptance/freeze semantics.

## No circular authority

A downstream MH may propose a change to MH-01, but cannot enact it. A development chat may return evidence or a change proposal, but cannot promote it to canonical architecture. Promotion requires governance acceptance and repository record.