# Contour A worker-ingress authority audit — Wave 159

Date: 2026-10-18
Status: **SOURCE-LEVEL FINDING CONFIRMED / DESIGN GATE OPEN / NO RUNTIME FIX CLAIMED**

## Exact refs and source identity

- Repository: `VlDMlNSh/mediahub-os`.
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Governing issue: [#301 — qualify and operationalize the cloud-agent development fabric](https://github.com/VlDMlNSh/mediahub-os/issues/301), open.
- Correlation fix candidate: [PR #358](https://github.com/VlDMlNSh/mediahub-os/pull/358), open/Draft/unmerged; it addresses run discovery, not issuer authorization.
- Relevant main-branch source blob SHAs:
  - `ops/qualification/run_distributed_local_worker.py`: `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`
  - `.github/workflows/astra-distributed-local-worker.yml`: `f650f2416c19dc75b4a0eeec037661c0c6169910`
  - `astra_github_agent.py`: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`
  - `runtime/mediahub_runtime/autonomous_queue.py`: `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`
  - `tests/test_autonomous_queue_contract.py`: `e3466fd5f8d6d47a846f8ec75b0ab3ca46ed0dc7`
- Prior security findings: [Wave 144 authority/evidence review](MEDIAHUB-CONTOUR-A-WORKER-DISPATCH-AUTHORITY-AND-EVIDENCE-BINDING-REVIEW-WAVE-144-2026-10-18.md) and [Wave 150 signed-ingress trust-gap report](MEDIAHUB-CONTOUR-A-SIGNED-INGRESS-AND-WORKER-TRUST-GAP-REPORT-WAVE-150-2026-10-18.md).

## Source-level trace

### Existing A0 control-command verifier

`astra_github_agent.py` defines `mediahub.astra.control-command.v1`, canonical JSON serialization excluding `signature`, HMAC-SHA256 verification with a node-specific environment key, a configurable maximum command age (default 900 seconds), node binding, target-SHA/current-HEAD binding, and a replay marker under `executed_command_ids`. `read_command()` rejects invalid or stale commands before returning a command.

### Distributed worker ingress

`run_distributed_local_worker.py::load_task()` parses `ASTRA_MICRO_TASK_JSON`, requires task-shape fields, and returns the object. In `main()`, the worker checks configured node, task/node match, executor, 40-hex target SHA, current checkout HEAD, clean worktree and local model. It reads `ASTRA_COMMAND_ID`, but the inspected path does not authenticate the task JSON against the A0 signed command envelope before creating a task branch and executing model-controlled work.

The workflow `astra-distributed-local-worker.yml` exposes separate `workflow_dispatch` fields for command ID, target SHA, task ID, node ID, executor and task JSON. It checks host/user/executor/model and runs on self-hosted labels `mediahub-control`, `mediahub-provider`, and `astra-control`; it is not a GitHub-hosted ephemeral worker path. Workflow dispatch authorization and a title containing a command ID are not substitutes for issuer-level authorization.

## Decision

**Do not implement a second, divergent signing protocol.** The current A0 envelope signs a control command with fields that are not identical to the worker task payload. Directly reusing its HMAC helper without defining the relationship between command and task would leave ambiguity over what exactly was authorized.

Before runtime implementation, the governing contract must specify a single verifiable binding from the signed A0 command to the dispatched task: command ID, task payload digest, target SHA, node ID, executor/verifier, allowed paths/actions and expiry/freshness. The worker must verify issuer authority and node-specific key availability before executing model-controlled code, fail closed on stale/malformed/mismatched envelopes, and durably reject replay. Key delivery must remain runtime-only and isolated; no key material may be embedded in workflow inputs, task JSON, artifacts, logs or Git.

## Required negative tests

1. missing signature/envelope and missing node key;
2. modified task payload with unchanged signature/digest;
3. command ID, task ID, node, executor or target SHA mismatch;
4. expired/future timestamp and malformed timestamp;
5. target SHA differs from checkout HEAD;
6. duplicate/replayed command ID, including concurrent admission;
7. unsupported operation, path grant or action outside the approved capability;
8. signature comparison and parse failures fail closed without leaking key/signature material.

These are acceptance criteria to implement against the canonical contract, not proof that such tests currently exist or pass.

## Verification and scope

- Re-read all five source files above from `main` and compared the code paths with Waves 144/150.
- Confirmed PR #358 is still Draft/open/unmerged; its run-correlation tests do not close the issuer-authentication gap.
- No code, workflow, secret, runner, provider or runtime changes were made in this wave. No live worker was dispatched.
- This is a source-level confirmation, not evidence of an exploit or a live end-to-end qualification.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.

## Next bounded step

Locate and read the normative signed-command, capability/issuer, and task-envelope contracts referenced by the canonical map. Define the minimal cross-envelope binding and test seam in a reviewable contract proposal first; only then implement shared verification and negative tests. Preserve the distinction between Jarvis coordination, ASTRA A0 internal workflow state, and MediaHub Product State Authority.
