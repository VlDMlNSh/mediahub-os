# MediaHub OS — Wave 276: A0 Task ingress, issuer and approval trust-gap audit

- Date: 2026-10-20
- Status: **SOURCE-LEVEL FINDING / TRUST BOUNDARY NOT PROVEN / NO RUNTIME ACTION**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Wave 275 predecessor: [legacy workflow retirement drift audit](MEDIAHUB-CONTOUR-A-WAVE-275-LEGACY-WORKFLOW-RETIREMENT-DRIFT-AUDIT-2026-10-20.md)

## Executive result

The source currently exposes a file-based local Task Contract ingress and a gateway, but this pass did not find a canonical JSON Schema for the hard-coded `mediahub.ai.astra-task@1.0.0` contract or a verifier that authenticates the issuer/approval record before the task reaches the gateway. The runtime code accepts `approval_state: "approved"` as a string and the gateway uses that string to bypass its sensitive-action approval gate. This is a potential trust-boundary defect unless the inbox and approval field are protected by an independently enforced, trusted writer/approval mechanism outside the inspected code. That external mechanism, its ACLs and evidence were not verified here.

This is a high-priority admission question, not proof of an exploit or proof that any sensitive operation executed. Do not add a new accepted A0 contract or modify execution behavior merely to make the design look complete: first resolve the authoritative issuer/approval contract and owner/governance boundaries, then add fail-closed tests against it.

## Exact source snapshot

- Default branch `main`: `80be45a70732b1d568164571d4273a6397792c3b`.
- `runtime/mediahub_runtime/task_ingress.py` blob: `59e1254aa61cc8f55f53bd1e179631e81c441393`.
- `runtime/mediahub_runtime/astra_gateway.py` blob: `10985e4ad8f682313d08e7492ecc1856a8bce20f`.
- `runtime/mediahub_runtime/authorization.py` blob: `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`.
- `schemas/identity/identity-boundary.schema.json` blob: `1d085bb1f2c458faaeff23bd92d83aa5d1bd3879`.
- `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` blob: `8d831c2a8fa333977dd86524099568bae2a8db0e`.
- `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` blob: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`.

Links:
- [Task ingress implementation](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/task_ingress.py)
- [Astra gateway implementation](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/astra_gateway.py)
- [Authorization policy seam](https://github.com/VlDMlNSh/mediahub-os/blob/main/runtime/mediahub_runtime/authorization.py)
- [Security / Trust / Authorization contract](https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md)
- [Canonical governance registry](https://github.com/VlDMlNSh/mediahub-os/blob/main/architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml)

## Data flow established from source

```text
JSON file under FileTaskIngress inbox
  -> FileTaskIngress._read
     -> hard-coded schema_id/version/owner + field/type checks
     -> AstraTaskRequest (approval_state is carried as a plain string)
  -> FileTaskIngress.run_pending_bounded
  -> AstraGatewayRuntime.run_bounded
     -> _validate_task
     -> AstraGatewayRuntime.run
        -> _classify(user_command)
        -> sensitive action allowed when approval_state == "approved"
        -> provider selection/execution
```

## Findings

### F1 — No canonical schema found for the file ingress contract

`task_ingress.py` hard-codes `schema_id = mediahub.ai.astra-task` and `schema_version = 1.0.0`. It performs hand-written field checks but does not load or validate against a JSON Schema. Inventory of `schemas/ai/` on `main` returned seven files (inference request/response, model, capability, provider/adapter/registry); none is an Astra Task Contract schema. `contracts/README.md` names `schemas/` as the only canonical schema tree. The separately named `mediahub.agent-fabric.task.v1` queue files are task-coordination artifacts and must not be silently treated as this runtime Task Contract.

### F2 — Approval is represented as caller-supplied state, not verified evidence in the inspected path

`FileTaskIngress._read` requires `approval_state` to be one of `not_required`, `approved`, `pending`, or `rejected`, then copies that value directly into `AstraTaskRequest`. `task_to_contract` serializes the same field. No issuer identity, signature/attestation, approval event ID, approval expiry, target-SHA binding, operation/capability scope or replay/revocation evidence is carried or verified by this module.

### F3 — The gateway gates sensitive actions on a string and lexical matching

`AstraGatewayRuntime.SENSITIVE_ACTIONS` contains `host_install`, `credential_change`, `production_deploy`, and `destructive_action`. `run()` rejects a recognized marker only if `task.approval_state != "approved"`. The check is a substring classifier over the natural-language command; it is not an authorization decision derived from an authenticated principal and a capability grant. `run_bounded()` validates task shape and runs the same gateway path; it does not itself authenticate the task issuer or approval.

This contradicts the security design rule in the inspected Security / Trust / Authorization contract that AI/integration requests are not authorization decisions, default is deny, and authorization is evaluated before mutation. That document explicitly labels itself a **PROPOSED ARCHITECTURAL BASELINE**, so it is cited as a security requirement but not falsely represented here as final acceptance evidence. The ASTRA GOLD governance registry separately calls for fail-closed handling, human authority over launch approval, approval freshness tied to source SHA, credential boundaries and audit evidence.

### F4 — A distinct authorization seam exists but is not connected in this path

`runtime/mediahub_runtime/authorization.py` implements a fail-closed allow-list over `(principal, capability, operation)`; an empty grant policy denies. The inspected `task_ingress.py` and gateway path do not invoke this policy for Task Contract issuer/approval admission. This is a source-level call-graph observation, not a claim that no other service exists elsewhere.

### F5 — Direct unit coverage for Task ingress was not found in the main test inventory

The root test inventory contains gateway/provider, queue, command-auth, cloud-admission and identity-boundary tests, but no `test_task_ingress.py` or directly named TaskIngress test suite. The path `tests/test_task_ingress.py` returned NOT_FOUND. Existing tests therefore do not establish negative coverage for forged approval state on this ingress path. This inventory result is bounded to the paths inspected; it is not proof no indirect test exists.

## Required resolution before runtime behavior changes

1. Identify the authoritative A0 Task Contract producer/writer and the trust boundary of its inbox. Record principal identity, repository/workflow/source provenance, and how the file becomes eligible for ingestion.
2. Establish governance-approved approval evidence: issuer/principal identity, capability and resource scope, operation, approval event ID, timestamp/expiry, exact target/source SHA, signature or independently authenticated authority, revocation semantics, and replay protection.
3. Make validation fail closed before provider selection/execution. A field supplied by the task file must never be sufficient by itself to authorize a sensitive action.
4. Add static/mock-only negative tests: string `approved` without evidence; unknown/untrusted issuer; forged/invalid signature; wrong request/target SHA; expired/revoked approval; replay; scope mismatch; malformed/missing contract; ambiguous action; authorization backend unavailable. Each must prove no executor was called.
5. Keep MediaHub Product State Authority, Jarvis and ASTRA A0 powers distinct. Task issuer validation must not grant a worker authority over canonical state or promote an executor into an approver.
6. Do not claim runtime qualification, authenticated approval, provider-route safety or deployment from the current source-level finding.

## Verification boundary

This pass read source files, schema inventories and the documented governance/authentication contracts on `main`. It did not run unit tests, access an inbox or host, invoke a provider/model, read secret values, launch agents, mutate runtime state, merge branches, deploy or qualify Contour A. The existence and configuration of external inbox ACLs, producer identity and approval services remain unresolved.

## Next bounded step

Trace the caller/producer of `FileTaskIngress` and the configured inbox path, then identify whether a governance-approved external approval verifier already exists. If it does, attach it and prove its call order with negative tests; if not, propose the smallest versioned contract/governance change before implementing new authority semantics.


## Traceability and review pointer

- Canonical map entry: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md), Wave 276.
- Continuation checkpoint: [current checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md).
- Master Roadmap addendum: [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md).
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Runtime admission changes are deliberately deferred until the trusted writer/issuer and approval-authority contract are identified. The report is a source audit, not runtime qualification evidence.


## Runtime wiring follow-up (same audit pass)

A follow-up read of the resident service entrypoint narrows runtime reachability:

- `runtime/mediahub_runtime/astra_service.py` blob `6aa2d09fc8737ccc0ba7f05bd13a15a0ebde7129` instantiates `AstraGatewayRuntime()`, prints a READY marker and sleeps. Its comment explicitly says it is intentionally inert until an application/API boundary submits Task Contracts. It does not instantiate or call `FileTaskIngress`.
- `runtime/mediahub_runtime/__init__.py` blob `4ff499f8e489e60e344283ee01e4dad5e72a2646` exports `FileTaskIngress`, `TaskIngressError` and `task_to_contract`.
- No in-repository call site for `FileTaskIngress` was established by the inspected package/runtime files. Code search results were unavailable/empty, so this must not be interpreted as exhaustive proof that no application or external caller exists.
- Classification refined: **latent admission-contract gap before ingress wiring**, not a verified currently reachable production exploit. The resident service path does not establish active Task Contract intake. The approval field must still not become authority when future API/inbox wiring is implemented.



- Runtime wiring follow-up commit: 8672be82b8a56c40221114ddcfad78d50d13892e; revised report blob `761dd2fc267260f39f6b8a63ce37f5e846725262`. Resident service not calling the ingress is recorded as a reachability qualifier, not proof no external caller exists.
