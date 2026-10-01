# MediaHub — Dots Continuous Development Integration Blueprint

Status: DESIGN COMPLETE / PLATFORM-CONNECTION BLOCKED
Date: 2026-10-01
Repository: VlDMlNSh/mediahub-os

## 1. Decision

Dots are treated as a supervisory/specialist agent layer above the existing MediaHub autonomous development control plane. A Dot must never become an architectural, security, state, release, recovery, update, identity, or qualification authority.

Current platform constraint: OpenAI documents state that Dots are not available to users under 18. Therefore no Dot has been connected or represented as connected in this repository. No age, account, or platform restriction is bypassed.

## 2. Target topology

MediaHub Authority
  -> Astra Autonomous Control Plane
    -> Dot Supervisor
      -> Specialist Dots
        -> Codex tasks / GitHub transport / CI
          -> Verification
            -> Qualification
              -> Evidence
                -> MediaHub release authority

Dots are orchestration and specialist execution participants. MediaHub remains the authority.

## 3. Persistent specialist roles

DOT-00 SUPERVISOR
- Owns queue decomposition, dependency ordering, bounded concurrency, escalation.
- Cannot approve architecture or production admission.

DOT-01 DEVELOPER-FABRIC
- Developer cloud/fabric, worker identity, task leases, fencing, capability scheduling.

DOT-02 IOS
- iOS Developer Mobile, iOS/iPhone build/test/release integration.
- Android is out of scope.

DOT-03 CORE
- Contracts, state boundaries, persistence, security/privacy, policy interfaces.

DOT-04 MEDIA
- FFmpeg/OpenCV and target-gated media sidecars.
- Whole-product sidecars remain behind MediaHub contracts.

DOT-05 KNOWLEDGE-AI
- Documents, OCR, vector/knowledge, Digital Twin, model/runtime qualification.
- AI never becomes authority.

DOT-06 INFRA
- Network, object storage, backup/restore, OTA, observability, artifact supply chain.

DOT-07 QUALIFICATION
- Functional, negative/failure, recovery, upgrade/rollback, performance, provenance evidence.
- Cannot self-certify its own implementation.

DOT-08 INDEPENDENT-REVIEW
- Fresh independent verification of gates and evidence.
- Must be separated from implementation ownership.

## 4. Scheduling policy

Priority:
P0 invariants/security/corruption/recovery/update
P1 autonomy prerequisites and blockers
P2 core implementation
P3 qualification/hardening
P4 optimization/documentation

Concurrency:
- 2-4 independent implementation workers maximum.
- Sequential execution where shared state or dependency ordering is material.
- One supervisor integrates.
- Independent reviewer is not concurrently allowed to approve its own implementation.

## 5. Mandatory work contract

Every Dot task must contain:
task_id
objective
acceptance criteria
owner
files/paths
dependencies
capability gap
risk
component/version/provenance
tests
negative tests
recovery/rollback
verification evidence
commit SHA
result state

Allowed states:
READY -> CLAIMED -> IMPLEMENTING -> VERIFYING -> QUALIFIED -> DONE
or BLOCKED / REJECTED / DEFERRED.

## 6. Hard safety boundaries

No Dot may:
- modify Functional Baseline 2.0 without an explicit architectural-change stage;
- transfer MediaHub authority to a third-party component;
- introduce an unqualified runtime dependency;
- access or mix user-data domains during development qualification;
- declare production qualification from its own worker report;
- create a second state, recovery, OTA, deployment, relational DB, vector DB, or message authority;
- bypass failed gates;
- silently broaden permissions;
- merge unverified destructive changes.

## 7. Current queue

P0:
1. Monitor GOLD #178 and preserve evidence.
2. After GOLD completion, independently verify G8.
3. Close G9 only through fresh independent verification.
4. Reconcile G0-G4 autonomy blockers.

P1:
5. Canonical Astra worker identity.
6. Autonomous task queue/state contract.
7. End-to-end worker execution.
8. Scheduler E2E.
9. Multi-node fencing.
10. Recovery/backup/restore.
11. Target-gated dependency qualification.
12. 3-node qualification where distributed claims are required.

P2:
13. Developer Fabric implementation.
14. iOS Developer Mobile.
15. Contract/build/test/evidence pipeline.
16. Media implementation slices.
17. Knowledge/Digital Twin/AI slices.

P3:
18. Production admission qualification.
19. Upgrade/rollback qualification.
20. Performance/resource qualification.
21. Security/provenance hardening.

P4:
22. Optimization.
23. Documentation reconciliation.
24. Continuous maintenance.

## 8. Continuous loop

DISCOVER
-> GAP
-> PLAN
-> CLAIM
-> IMPLEMENT
-> TEST
-> VERIFY
-> QUALIFY
-> COMMIT
-> READ-BACK
-> RECONCILE
-> SELECT NEXT
-> REPEAT

Any failed critical gate returns the item to GAP/REPAIR. No loop may convert an unresolved blocker into DONE.

## 9. Platform integration status

Required before real persistent Dots operation:
- Dot availability for the account/workspace.
- Authorized connection to the required Codex cloud environment.
- GitHub connection with least-privilege write permissions.
- Explicit Dot custom rules matching this blueprint.
- A persistent Supervisor Dot plus specialist Dot definitions.
- First dry-run with no production writes.
- Independent verification of task ownership, permissions, fencing and evidence.
- Only then enable continuous development duties.

Current status: these platform-side Dot prerequisites cannot be completed from this account because OpenAI currently states Dots are unavailable to users under 18.

## 10. Acceptance criteria for declaring the Dot architecture ready

READY means:
- role boundaries are explicit;
- no authority duplication exists;
- queue contract is machine-readable;
- worker ownership/fencing is defined;
- GitHub write/read-back protocol is defined;
- qualification and independent verification are separated;
- recovery and rollback are mandatory;
- user-data boundary is explicit;
- platform eligibility is satisfied;
- first dry-run produces fresh evidence.

PRODUCTION-CAPABLE is a separate state and requires all MediaHub G0-G9 gates applicable to the intended scope.
