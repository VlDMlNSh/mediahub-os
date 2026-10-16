# MediaHub OS — Cloud-Agent Registry and Evidence Schemas, Wave 13

- Date: 2026-10-16
- ID: MH-CAF-SCHEMAS-13
- Status: **SCHEMA ARTIFACTS CREATED / 15 STRUCTURAL ASSERTIONS PASSED / FULL JSON SCHEMA VALIDATION PENDING**
- Contour: A — Developer Fabric
- Parent: [Hybrid Distributed Agent Fabric Component Reference Architecture — Wave 11](MEDIAHUB-HYBRID-DISTRIBUTED-AGENT-FABRIC-COMPONENT-REFERENCE-ARCHITECTURE-WAVE-11-2026-10-16.md)
- Queue: [Activation Queue](MEDIAHUB-CLOUD-AGENT-ACTIVATION-QUEUE-WAVE-11-2026-10-16.json)
- Task envelope: [Task Envelope Schema v0.1](MEDIAHUB-CLOUD-AGENT-TASK-ENVELOPE-SCHEMA-V0.1-WAVE-11-2026-10-16.json)
- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Components created

| Component | Blob SHA after read-back | Commit |
|---|---|---|
| [Agent Registry Record Schema v0.1](MEDIAHUB-CLOUD-AGENT-REGISTRY-SCHEMA-V0.1-WAVE-13-2026-10-16.json) | `449a38bc84283f720fe723ea8e3587e6082fdbb4` | `4c85035df5ba2d20fbfcffb5df2ab0dabc2c0327` |
| [Execution Evidence Manifest Schema v0.1](MEDIAHUB-CLOUD-AGENT-EVIDENCE-MANIFEST-SCHEMA-V0.1-WAVE-13-2026-10-16.json) | `9714fd2dd04d401a9a3d1a800cb19d7b69e7e73f` | `b54b02c9f91d1ebfe60ea45588b767fb5c3f0ed7` |
| [Activation Queue](MEDIAHUB-CLOUD-AGENT-ACTIVATION-QUEUE-WAVE-11-2026-10-16.json) | `d6b01b23885d35d30f5f0460b899e073cefd6027` | `9c72154485da216bad8a9c08ba9037f23c37423e` |

The queue preserves all ten original CAF-Q IDs. CAF-Q-004 now includes registry-schema review; CAF-Q-005 points to the evidence-manifest schema; CAF-Q-006 points to the registry schema while retaining the A0/security hard gate.

## 2. Contract content

The registry record captures:
- stable agent identity and exact workflow source SHA;
- task types, path scope, forbidden paths, data classes and allowed effects;
- provider/model route allowlist, task purpose, policy and authorization references;
- concurrency, attempts, timeouts, input/output bounds and isolated-workspace requirement;
- issuer/grant/review references, scope digest, expiry, last review and revocation evidence.

The evidence manifest captures:
- task envelope digest, attempt and idempotency-key digest;
- workflow run/job, execution timestamps, status, retry count and sanitized error class;
- requested ref plus resolved immutable commit SHA, workflow blob SHA, action SHAs and runner metadata;
- normalized input path digests, byte sizes and data classes;
- registry record digest, provider/model identity, task/provider/data/audit policy references;
- artifact digest, byte size, retention class, quarantined promotion disposition and separate reviewer decision.

Both schemas reject unknown properties. The registry requires an isolated workspace and explicit expiry/revocation references. Neither schema embeds secrets or treats a registry status field as an authorization grant.

## 3. Bounded checks performed

A small read-only structural assertion pass parsed the two new schemas, the existing task-envelope schema and the updated activation queue, then evaluated 15 assertions:

1. all four JSON documents parse;
2. both new schemas set `additionalProperties: false`;
3. each top-level required field exists in its properties map;
4. registry lifecycle requires expiry and revocation references;
5. registry execution requires an isolated workspace;
6. evidence manifest separates executor disposition from independent review;
7. all ten queue IDs remain unique and CAF-Q-001…CAF-Q-010 remain present;
8. CAF-Q-005 references the evidence-manifest schema;
9. CAF-Q-006 references the registry schema.

Result: **15/15 assertions passed**. This is a structural smoke check implemented against the retrieved GitHub contents. A standards-compliant JSON Schema validator, negative-instance suite, semantic cross-schema review and independent review remain pending.

## 4. Hard gates retained

- A0 issuer/ingress/queue/lease/cancellation/recovery contract: OPEN.
- R-06 audit/privacy authority, sink/outage/retention/reconciliation disposition: OPEN.
- Accepted MH-12 security authority and admission/revocation contract: OPEN.
- Authoritative runner/workspace/network target manifest: UNKNOWN / BLOCKED.
- Gemini workflow source hardening: proposal exists, source unchanged, execution qualification open.
- Live agent registry, durable queue, scheduler, connected worker, isolated patch execution and PR promotion: UNPROVEN.
- Contour B remains gated on Contour A deployment and independent acceptance.

## 5. Execution boundary and next step

This wave created documentation/schema artifacts, updated the documentary queue, and performed the 15 bounded structural assertions. It did not connect a new agent, create credentials, call a provider, dispatch a workflow, edit workflow source, install software, inspect host/runtime, alter infrastructure, deploy or merge branches.

Next: obtain independent review of both schemas; reconcile their field semantics against the accepted A0 lifecycle and R-06 policy; continue source discovery for the authoritative target manifest. Only after those authority gates close should an implementation patch be prepared for explicit review.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
