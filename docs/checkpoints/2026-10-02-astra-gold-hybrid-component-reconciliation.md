# ASTRA GOLD — Hybrid Distributed Development Component Reconciliation

Date: 2026-10-02
Status: READ-ONLY INVENTORY PASS + ARCHITECTURE UPDATE

## 1. Canonical rule

ASTRA GOLD remains the single distributed development system and A0 Astra remains the only coordination authority. Discovery, registration, installation, credential presence, or process visibility never equals qualification.

## 2. Desktop reconnaissance

### Voktors-Mini.Dlink
- macOS Darwin 23.6 / arm64.
- Codex CLI 0.157.1 discovered.
- Claude Code 2.1.282 discovered.
- OmniRoute 3.8.50 discovered and a running OmniRoute process was observed.
- Ollama 0.34.4 discovered and a running Ollama server was observed.
- Node.js 22.23.3 discovered.
- OpenFlux executable/process/path was not discovered by the bounded scan.
- This node is discovery evidence only; no qualification is inferred.

### mh-dev-01
- Ubuntu Linux 6.8.0-139 / x86_64.
- Codex CLI 0.151.0 discovered.
- Claude Code 2.1.280 discovered.
- OmniRoute 3.8.50 discovered.
- FCC Codex/Claude launchers discovered, but their proxy endpoint 127.0.0.1:8092 was unreachable during the probe.
- Ollama executable discovered, but no running Ollama instance was reachable during the version probe.
- Bun 1.4.0 and Node.js 22.23.2 discovered.
- Astra service, command bus, executor discovery and guard processes were observed.
- OpenFlux executable/process/path was not discovered by the bounded scan.
- This node is the canonical active qualification target; the probe did not modify it.

### mh-dev-02
- Ubuntu Linux 6.8.0-142 / x86_64.
- Ollama 0.34.4 discovered and running on 127.0.0.1:11434.
- Astra node agent, command bus, executor discovery, orchestrator, guard and GitHub agents were observed.
- OpenFlux executable/process/path was not discovered by the bounded scan.
- No OpenFlux installation evidence was found.

## 3. OpenFlux identity decision

The architecture records EDEAI/OpenFlux as the current candidate identity. Its public repository describes a Tauri v2 desktop AI-agent client with multi-agent collaboration, multi-LLM support, MCP/tool integration, browser and desktop automation, memory, sandboxing and workflow scheduling. Those capabilities make it relevant as a possible desktop execution surface, but they are not MediaHub qualification evidence.

Other unrelated projects using the name OpenFlux must not be conflated with this candidate. Network-tunnelling projects and observability/cost-tracing projects using the same name are separate identities and require independent admission if later considered.

## 4. ASTRA GOLD placement

OpenFlux -> candidate desktop agent -> admission gate -> isolated workspace -> bounded task execution -> result validation -> A3 -> integration

OpenFlux is not:
- A0 coordination authority;
- A1 architecture authority;
- A2 unrestricted implementation authority;
- A3 verification authority;
- provider/state authority;
- credential-creation authority;
- transport/state authority.

Current state: NOT_PROVEN.

## 5. Qualification gates for OpenFlux

1. Identity and exact source provenance.
2. Installed version and executable integrity.
3. Tool/permission boundary inspection.
4. Sandbox/isolation verification.
5. Non-mutating startup/probe.
6. Isolated repository execution with a deterministic marker task.
7. Timeout/non-zero/malformed-result handling.
8. Workspace isolation and write-boundary enforcement.
9. Recovery after worker interruption.
10. Evidence publication with exact source SHA and executor identity.
11. Independent A3 verification.
12. Only then: ASTRA GOLD eligibility consideration.

No OpenFlux qualification result is asserted by this checkpoint.

## 6. Existing fabric reconciliation

The currently evidenced desktop fabric includes Codex, Claude Code, OmniRoute, FCC launchers, Ollama, Bun/Node and Astra control-plane processes on the inspected nodes. ECC remains an auxiliary non-authoritative component in the canonical registry. OpenFlux is now explicitly represented as a qualification-gated desktop-agent candidate rather than being silently treated as an executor or authority.

## 7. Evidence integrity

The reconnaissance was read-only. Credentials and secret values were not collected or emitted. The local mh-dev-01 checkout contained pre-existing untracked .autonomous/ and .hybrid-development/ paths; they were not modified.
