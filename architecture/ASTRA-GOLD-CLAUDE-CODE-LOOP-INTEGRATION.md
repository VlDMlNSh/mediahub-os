# ASTRA GOLD — Claudex Loop Integration

Status: REVIEW / QUALIFICATION CANDIDATE + PROJECT-LOCAL TOOLING INSTALLED
Date: 2026-10-02
System: MediaHub OS / MediaHub iOS

## Exact identity

- Upstream: https://github.com/chaseai-yt/claudex-loop
- Plugin: `claudex-loop`
- Upstream plugin version: `2.1.0`
- Upstream commit pin: `main` content was captured file-by-file on 2026-10-02; each vendored file records its upstream blob SHA in the engineering log/commit history.
- License: MIT
- Maintainer/author metadata: Chase AI

## Scope

Claudex Loop is a cross-provider planning/build/inspection workflow. It is installed as project-local tooling for engineering use and remains a qualification candidate, not an ASTRA authority or automatically admitted executor.

The workflow is specifically useful for independent plan review and final-code inspection: the host coordinates, one provider reviews the plan, an authorized builder implements, and the other provider performs fresh inspection. The upstream runtime explicitly requires bounded review/fix rounds and separate proof/inspection. 

## ASTRA boundary

- Human remains final authority.
- A0-ASTRA remains the sole MediaHub State Authority and coordination authority.
- Claudex Loop is methodology/orchestration tooling only.
- It cannot select ASTRA providers as a policy authority.
- It cannot create credentials or expand scopes.
- It cannot change SentinelX policy.
- It cannot self-qualify or self-promote.
- It cannot declare G0-G11 PASS.
- It cannot declare PRE-SOAK, SOAK_24H, LAUNCH_READY or ASTRA GOLD.
- Its reviews are evidence/advice and must be reconciled against canonical ASTRA contracts.

## Installed project-local paths

`.claude/plugins/claudex-loop/`

Includes:
- plugin metadata;
- `claudex-loop`;
- `codex-review`;
- `codex-build`;
- `claudex-route`;
- runtime/build references;
- standard-library runner.

## Qualification treatment

Installation itself is not qualification evidence.

If Claudex Loop is later admitted as a runtime execution component, qualification must cover:
1. exact version/provenance;
2. CLI identity and authentication state;
3. workspace isolation;
4. read-only review boundary;
5. builder write boundary;
6. proof-command enforcement;
7. bounded review/fix/inspection rounds;
8. session identity and replay behavior;
9. timeout/termination;
10. credential/secret isolation;
11. audit/evidence integrity;
12. concurrency/duplicate-controller behavior;
13. worker restart/recovery;
14. independent A3 verification;
15. exact-SHA reproducibility.

For the current ASTRA qualification, Claudex Loop does **not** modify the mandatory five-path executor matrix and does not add itself to the 115 mandatory rounds.

## Matt Pocock Skills relationship

Matt Pocock skills remain a separate engineering-methodology reference. Claudex Loop may use or coexist with them, but neither toolchain supersedes the ASTRA canonical architecture, qualification contract or Human authority.

## Current status

REVIEW / QUALIFICATION CANDIDATE
PROJECT-LOCAL TOOLING: INSTALLED
RUNTIME EXECUTOR ADMISSION: NOT GRANTED
ASTRA GOLD AUTHORITY: NONE
