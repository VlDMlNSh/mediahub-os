# ASTRA GOLD — Whole-Project Readiness Audit

Status: AUDIT COMPLETE / LOCAL SUITE GREEN / FAIL-CLOSED ON LIVE GATES
Date: 2026-10-02
Scope: whole repository (Python, JSON, YAML, GitHub workflows, contracts, security posture)
Purpose: prepare the project for the transition to 24/7 autonomous hybrid distributed development

This audit is repository-local. It does not and cannot produce provider authentication,
the G4 115-round matrix, integrated A3, or the 24h soak. No gate is promoted by a document.

## 1. Method

1. Compile every Python file in the repository (not just `runtime/`, `tests/`, the agent).
2. Parse every JSON and YAML file, including dot-directories (`.github/`).
3. Parse every workflow, extract test/script/requirements references, and check existence.
4. Classify each workflow by trigger and runner to find auto-run vs dormant checks.
5. Secret scan: private keys, known token prefixes, hardcoded credential assignments,
   secret echoing in workflows.
6. Contract consistency: compare duplicated `contracts/` and `schemas/` trees.
7. Re-verify after every fix until the suite is green (loop).

## 2. Findings

| # | Category | Finding | Status |
|---|---|---|---|
| F1 | Python | 1 syntax failure (Python-3.12-only f-strings in `astra_github_agent.py`). All 121 files now compile. | FIXED (prior pass) |
| F2 | Workflow YAML | `.github/workflows/mh25-dual-local-23wave.yml` was invalid YAML: heredoc bodies sat at column 0, terminating the `run: \|` block scalar. It startup-failed on every push. | FIXED |
| F3 | YAML | `recovery/mh-09-reconciliation-status-2026-09-05.yaml` had a one-space-indented `decision_coverage:` key. | FIXED |
| F4 | Workflow deps | `.github/workflows/federation-admission-poc.yml` ran `pytest` without installing it → guaranteed failure. | FIXED |
| F5 | Workflow trigger | `.github/workflows/mh25-dual-local-executor-23wave.yml` had no branch filter, firing the offline self-hosted job on every branch push. | FIXED (prior pass) |
| F6 | Workflow deps | GOLD workflows ran PyYAML-importing tests without PyYAML; `requirements-dev.txt` added and wired in. | FIXED (prior pass) |
| F7 | Soak pin | The 24h preflight pinned a stale agent blob; re-frozen and guarded by a drift test. | FIXED (prior pass) |
| F8 | Workspace cleanup | Stray `__pycache__/` directories under `ops/federation/` and elsewhere are ignored by `.gitignore`; no action needed. | OK |
| S1 | Security | No private keys, no `ska`/`ghp_`/`gho_`/`AKIA`/`AIza`/`xox` token literals, no hardcoded credential assignments anywhere. | PASS |
| S2 | Security | No workflow echoes `secrets.*`; evidence producers emit `secret_values: SUPPRESSED`. | PASS |
| S3 | Security | No credential/secret files are tracked by Git. | PASS |

## 3. Open register (requires a decision or a live environment)

### D1 — Phantom workflows referencing modules that do not exist in this repository

- `.github/workflows/mediahub-p0-07-verification.yml` → `runtime/mediahub_runtime/{configuration_policy,configuration_policy_authorization,policy_evaluator,configuration_policy_operations,proposal_plugin_boundary}.py`, `tests/runtime/*`
- `.github/workflows/mediahub-p0-08-verification.yml` → `runtime/mediahub_runtime/{plugin_manifest,plugin_capabilities,plugin_boundary,plugin_authorization,plugin_lifecycle,plugin_resources,plugin_proposals}.py`, `tests/runtime/*`
- `.github/workflows/mediahub-bridge.yml` → `tests/runtime/*`
- `.github/workflows/mediahub-live-provider-qualification.yml` → `tests/test_mediahub_*.py`

Only `runtime/mediahub_runtime/proposals.py` exists from that family. These workflows are
**dispatch-only** (they do not auto-run on push/pull_request), so they are dormant, not
failing. They cannot pass until the corresponding P0-07/P0-08 subsystems exist. Resolution is
an A1/Human decision: build the subsystems, or remove the dormant workflows.

### D2 — Duplicated schema trees have diverged

`contracts/` and `schemas/` both carry `ai/*`, `core/*`, `identity/*`. Seven files are
byte-identical; two differ:

- `core/contract-metadata.schema.json` — the `contracts/` copy declares
  `optional`/`constraints` with `additionalProperties: true`; the `schemas/` copy does not.
- `identity/identity-boundary.schema.json` — differs in `$id` namespace, descriptions,
  formatting, and one `type`/`additionalProperties` detail.

`tools/validate_contracts.py` validates only `contracts/`; `tests/schemas/*` validate
only `schemas/`. Both currently pass, so this is a **drift risk**, not a live failure.
Consolidating or designating one canonical tree is an A1 architecture decision; it is left
open rather than silently rewritten.

### D3 — Non-existent trigger path (harmless)

`mh25-dual-local-23wave.yml` lists `ops/agent-fabric/providers/dual-local-executors.yaml` in
`on.push.paths`, but that file does not exist. A non-matching path filter is inert; noted for
cleanup only.

### E1 — Offline self-hosted runners (environment)

Both registered runners (`mh-dev-01-v2`, `Voktors-Mini-Astra-Control`) are **offline**.
Every `[self-hosted, mediahub-runner]` workflow (supervisor, unified qualification, 23-wave,
provider-backend, one-time migration, freellmapi) queues indefinitely. Restoring the runners
is an operator action and a prerequisite for the live soak.

### L1 — Live gates (cannot be satisfied in the sandbox)

Provider credentials, canonical `mh-dev-01` identity, the G4 115-round matrix, integrated A3,
and the 24h soak. Gates G0–G11 remain BLOCKED; `ASTRA_GOLD_ELIGIBLE` is not asserted.

## 4. Verification after the fixes

| Check | Result |
|---|---|
| `compileall` whole repository | PASS |
| YAML + JSON parse (incl. `.github/`) | 0 failures |
| `unittest discover` | PASS (201) |
| `pytest -q tests/` | PASS (232) |
| `tools/validate_contracts.py` | PASS (9 files) |
| soak-pin drift gate | PASS |
| federation tests + PoC scripts | 16 tests PASS, 5 scripts OK |
| rewritten workflow: YAML parse + embedded Python heredoc compile | PASS |
| `qualification_launch_gate.py` | BLOCKED (expected, fail-closed) |

## 5. Truth status

Architecture: READY
Local repository regression: GREEN
Local execution fabric / providers / G4 / A3 / 24h soak: NOT_PROVEN
Transition to 24/7 autonomous hybrid distributed development: READY at the repository level,
gated on D1 (decision), E1 (runner), and L1 (live waves).
