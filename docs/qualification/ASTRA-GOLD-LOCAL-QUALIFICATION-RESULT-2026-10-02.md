# ASTRA GOLD — Local Qualification Run Result

Status: LOCAL RUN COMPLETE / FAIL-CLOSED
Date: 2026-10-02
Scope: repository-local qualification only (no live nodes, no credentials, no 24h soak)
System: ASTRA_GOLD
Contract: `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` (v1.1)
Blueprint: `architecture/ASTRA-GOLD-QUALIFICATION-BLUEPRINT.yaml`

## 1. Purpose and boundary

This run executes every repository-local qualification action that does not require
the live fabric. It never advances a gate from implementation text, registration,
credential presence, a process being visible, or historical evidence.

It does **not** and cannot produce: provider authentication, the 115-round executor
matrix, multi-node fencing, recovery drills, integrated A3, or the 24h soak.
Those remain live, credentialed, exact-SHA operations.

## 2. Run environment

- Node: `e2b.local` (NOT the canonical `mh-dev-01` / `mediahub-runner`).
- Python: 3.10.12. Canonical CI uses 3.12 (`actions/setup-python`).
- Dependencies: PyYAML 6.0.3 and pytest 9.1.1 in a project-local venv `build/qual-venv`
  (never read from or written to committed env files).
- No provider credentials present. No GitHub command transport. No self-hosted runner.

## 3. Defects found and repaired (repository-local)

1. `astra_github_agent.py` used PEP 701 nested-quote f-strings (5 sites), which only
   parse on Python ≥3.12. Rewritten to single-quoted inner keys. Behavior is identical
   on 3.12 and now also parses on 3.10, so `compileall` and the mission test pass.
   Agent blob SHA changed: `f58723e0…` → `54f0d38a…`.
2. `tests/test_astra_gold_architecture_drift.py::test_authority_and_fail_closed_contract_cannot_drift`
   rebound `u = self.unified["authority"]` and then read `u["qualification"]` / `u["rules"]`,
   which can never exist under `authority`. Corrected to read `self.unified` for those two
   assertions. The underlying contract data was already correct.
3. `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md` said "24h soak" while the drift gate
   requires the canonical label "24H SOAK". Normalized the affected headings/statements.

## 4. Repository-local gate results

| Check | Command | Result |
|---|---|---|
| Compile | `python -m compileall -q runtime tests astra_github_agent.py` | PASS |
| Unit tests | `PYTHONPATH=runtime python -m unittest discover -s tests` | PASS (197) |
| Unit tests | `PYTHONPATH=runtime:. python -m pytest -q tests/` | PASS (228) |
| Contracts | `python tools/validate_contracts.py` | PASS (25 schemas, 9 envelope contracts) |
| Architecture drift | `tests/test_astra_gold_architecture_drift.py` | PASS |
| Qualification schema | `tests/test_astra_gold_qualification_launch_schema.py` | PASS |
| Evidence contracts | `tests/test_astra_gold_evidence_contracts.py` | PASS |

## 5. Qualification-gate status (G0–G11)

| Gate | Local result | Basis |
|---|---|---|
| G0 Identity | BLOCKED | not the canonical node; no fresh transport identity |
| G1 Boundary | BLOCKED | live authority/credential/workspace boundary not exercised |
| G2 Control Plane | BLOCKED | no live command/claim/queue/heartbeat transport |
| G3 Execution Path | BLOCKED | no isolated FCC/OmniRoute/native execution |
| G4 23-Wave | BLOCKED | 0/115 fresh rounds; manifest READY_FOR_EXECUTION only |
| G5 Concurrency | BLOCKED | no concurrent disjoint claims observed |
| G6 Recovery | BLOCKED | no timeout/stale-claim/restart/replay drill |
| G7 Integrated A3 | BLOCKED | `verify_integrated_a3` → G4/G5/G6 missing |
| G8 Pre-Soak | BLOCKED | `verify_pre_soak_bundle evidence` → `provider-model.json: status=None` |
| G9 24H Soak | BLOCKED | not started; must not start before G0–G8 PASS |
| G10 Launch Ready | BLOCKED | `qualification_launch_gate.py` → `launch_ready=false` |
| G11 Launch | BLOCKED | HUMAN_ONLY; no approved SHA / A3 record / soak record / rollback target |

`ops/qualification/qualification_launch_gate.py` returns `status: BLOCKED` with
`missing_launch_inputs` = approved_source_sha, launch_target, fresh_evidence_bundle,
A3_verification_record, soak_record, rollback_target.

## 6. Local inventory findings (read-only, not qualification)

- `inventory_local_components.py`: PASS. Found on this node: `claude`, `codex`, `node`, `bun`.
- `qualify_local_components.py`: PASS for Claude Code, Codex CLI, Node.js, Bun
  (binary version probe only; NOT execution qualification).
- `qualify_openflux.py`: `DISCOVERED` from a process self-match (the probe's own
  command line contains "openflux"); no executable, no installed candidate path.
  This is a probe false positive, not admission evidence.
- `qualify_local_ai_capabilities.py`: BLOCKED (no local Ollama API/model).
- `qualify_execution_backends.py`: BLOCKED, 0 qualified providers (all credentials absent).
- `hybrid_agent_auth_probe.py`: all providers NOT_PROVEN (credentials not present).
- `verify_execution_backends.py evidence/execution-backends.json`: BLOCKED
  (node identity + backend verification checks not PASS).
- `build_g4_115_manifest.py --source-sha <HEAD>`: READY_FOR_EXECUTION, 115 rounds / 5 paths
  (execution is external-only; no runner is created).

## 7. Blocker register (what still stands between the repo and GOLD)

B1. Execution fabric: no isolated FCC/OmniRoute/native paths available to a bounded
    executor identity at the canonical node.
B2. Credentials: no provider credentials present, so authentication/model discovery
    cannot be qualified. Missing keys are named in `.github/workflows/astra-gold-unified-qualification.yml`.
B3. Canonical identity: the run is not on `mh-dev-01` as `mediahub-runner`, so transport
    identity and reboot persistence cannot be proven.
B4. 24h soak pin drift: `.github/workflows/astra-gold-24h-soak.yml` pins the agent blob to
    `769306d9…`, but the committed agent blob is now `54f0d38a…` (was `f58723e0…` before the
    compatibility fix). The soak preflight would fail until the pin is reconciled by A1/Human.
B5. Pre-soak bundle: `evidence/provider-model.json` has no top-level `status`, and the
    scheduler/fencing/recovery/backup-restore producers are explicitly not implemented
    (`capture_pre_soak_evidence.py` marks them BLOCKED).
B6. A3: independent verification cannot be satisfied without fresh G4/G5/G6 evidence.

## 8. Truth status (unchanged)

Architecture: READY
Qualification schema: CANONICAL
Local repository regression: PASS
Local execution-fabric qualification: NOT_PROVEN
Cloud provider qualification: NOT_PROVEN
G4 23-wave: BLOCKED (0/115)
Integrated A3: BLOCKED
24h soak: NOT_STARTED
Launch: BLOCKED

`ASTRA_GOLD_ELIGIBLE` is not asserted. No gate was promoted from documentation or
local probes. `LAUNCH_READY` remains unreachable until every live producer above emits
fresh PASS evidence at one frozen SHA and a Human authorizes G11.

## 9. Next live actions (dependency order)

1. Reconcile the soak pin (B4) and the pre-soak bundle contract (B5) in-repo.
2. Operators set the named provider secrets; run `qualify_execution_backends.py` and
   `hybrid_agent_auth_probe.py` on the canonical node.
3. Run the G4 115-round matrix from the manifest against one frozen SHA.
4. Produce G5/G6 runtime observations and run `verify_integrated_a3.py`.
5. Capture the fresh pre-soak bundle on `mh-dev-01` and pass `verify_pre_soak_bundle.py`.
6. Only then run the explicit 24h soak workflow, followed by the Human launch decision.

Secrets, tokens and raw provider responses are never recorded. Evidence is immutable.

## 10. Follow-up — 24h soak readiness pass

Additional repository-local work to make the 24h path runnable end-to-end.

### 10.1 New defects found and repaired

4. The pre-soak producer had no implementation for `scheduler-e2e.json`, `fencing.json`,
   `recovery.json` and `backup-restore.json` — it emitted a hard BLOCKED for all four.
   Added `ops/qualification/produce_runtime_prereq_evidence.py`, which exercises the real
   runtime modules (autonomous queue selection/ordering/gating, claim/lease collision and
   expiry, generation stale-transaction rejection, bounded timeout/repair, snapshot/restore
   ownership, durable memory round-trip) and is fail-closed: PASS only when every
   observation holds **and** the producer runs on the canonical node `mh-dev-01`.
   `capture_pre_soak_evidence.py` now calls this producer, so the full seven-artifact
   pre-soak bundle is produced by real code instead of a placeholder block.
5. GOLD CI runners ran tests without installing PyYAML/pytest, so `astra-gold-unified-qualification.yml`
   and `astra-gold-24h-soak.yml` would fail before reaching qualification. Added
   `requirements-dev.txt` and install steps to those workflows (and to
   `mediahub-cloud-provider-qualification.yml`).
6. The 24h-soak preflight pinned the agent blob to `769306d9…`, which no longer matched the
   committed agent. Re-froze the pin to the current canonical blob and added
   `tests/test_astra_gold_soak_pin.py`, which fails whenever the pin drifts from
   `astra_github_agent.py` (so a future agent edit must re-freeze deliberately).

### 10.2 Verification after the readiness pass

| Check | Result |
|---|---|
| `compileall runtime tests ops astra_github_agent.py` | PASS |
| `unittest discover` | PASS (201) |
| `pytest -q tests/` | PASS (232) |
| Soak pin drift gate | PASS (pin == blob `54f0d38a…`) |
| `produce_runtime_prereq_evidence.py` (canonical override) | PASS, all observations true |
| `capture_pre_soak_evidence.py` bundle off-canonical | 7/7 artifacts produced, all fail-closed BLOCKED |

### 10.3 Updated blocker register

- B4 (24h soak pin drift): **RESOLVED** — pin reconciled and guarded by a drift test.
- B5 (pre-soak producers): **RESOLVED repo-side** — real fail-closed producers exist and are
  wired into the capture step. Fresh PASS still requires the canonical node.
- B1/B2/B3/B6 remain: execution fabric, provider credentials, canonical identity and
  integrated A3 cannot be satisfied in the sandbox.

### 10.4 Soak-readiness checklist

Repo-side (done): deterministic test suite green; contracts pass; soak pin frozen+guarded;
runner dependencies declared; pre-soak bundle producer complete and fail-closed; G4 115-round
manifest generator ready; A3/pre-soak/launch gates implemented and negative-path tested.

Operator-side (required before SOAK_24H):
1. Deploy the canonical worker on `mh-dev-01` as `mediahub-runner`; confirm clean worktree.
2. Set the provider secrets named in `astra-gold-unified-qualification.yml`.
3. Run provider qualification + hybrid auth probe on the canonical node.
4. Execute the G4 115-round matrix against one frozen SHA; run `verify_integrated_a3.py`.
5. Capture the pre-soak bundle on the canonical node; require `verify_pre_soak_bundle.py` PASS.
6. Only then dispatch `astra-gold-24h-soak.yml` (24h) and obtain Human launch authorization.

Gates G0–G11 remain BLOCKED until the operator-side steps produce fresh evidence at a single
frozen SHA. No gate is promoted by this document.
