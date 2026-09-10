# Wave 10 priority: bounded Execution Adapter boundary

Current checkpoint: 9ac6fb5527ed6d27137249174d9821b6387a9f81
R4: 471f709f5633feab7aeb62dd3ea52effad6d2bc4

Primary task: implement the smallest provider-neutral ExecutionProposal contract inside the existing execution boundary. The proposal must carry request identity, workload identity, source provenance and provider identity; validate all fields; and be incapable of network access, credential retrieval, State Authority mutation, Home Assistant access, or real execution.

Acceptance gates:
1. Existing tracked file only for each autonomous increment.
2. Deterministic negative tests for missing proposal identity/provenance/provider.
3. No network/provider execution side effects.
4. No direct State Authority or Home Assistant access.
5. R4 ancestry preserved and worktree clean after each committed increment.
6. Full regression plus ruff/mypy/bandit/pip-audit/semgrep/diff-check.
7. Commit each verified increment; never force-push or rewrite history.
8. Preserve provenance and stop on ambiguity.

Follow-up priority: add focused tests for the ExecutionProposal contract, then connect proposal admission to existing cluster recovery evidence without performing arbitrary real execution.

# Initial priority: controlled Cloud Development adapter and isolated cloud-development sandbox

Before adding any external cloud AI provider, implement and qualify a provider-neutral Cloud Development Adapter and an isolated Cloud Development Sandbox. The adapter MUST be deny-by-default, non-authoritative, policy-gated, auditable, provenance-bound, and incapable of direct access to MediaHub State Authority, Home Assistant authority, production devices, secrets, or unrestricted local filesystem/network.

Required first-wave scope:
1. Define provider-neutral adapter contract: request classification, capability declaration, authorization, data minimization, egress policy, residency/policy checks, timeout/retry, response provenance, audit events, metering, revocation and fail-closed behavior.
2. Define isolated sandbox boundary for cloud-development workloads: separate identity, filesystem/worktree, network egress boundary, credentials broker boundary, resource limits, secret scanning/DLP hook points, artifact/result quarantine and deterministic teardown.
3. Implement only the smallest repository-native contract/adapter/sandbox skeleton justified by the existing architecture; do not add provider-specific bypasses or credentials.
4. Add deterministic unit/negative-path tests for denied authority escalation, denied secret exposure, denied unrestricted egress, denied production access, malformed provider responses, timeout/retry, revocation and sandbox teardown.
5. Record provenance/evidence and preserve R4 ancestry. No release/production authorization.

Second wave is explicitly gated on first-wave tests and security checks: integrate Claude, Codex and other approved available models ONLY through the same Cloud Development Adapter and Sandbox. No direct provider integration into core/runtime authority. Provider access must remain replaceable and policy-controlled.

# Local autonomous engineering queue — canonical passport aligned

The approved MediaHub OS passport is the sole functional baseline. Do not introduce requirements that contradict it.

1. Reconcile AI escalation path: Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI; Mobile Access Layer is access layer, not AI compute tier.
2. Preserve two-app Mobile Access Layer: MediaHub Core and separate Remote Mobile Application; do not collapse them or invent a Mobile AI tier.
3. Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.
4. Preserve Cloud Development AI as corporate-only infrastructure; ordinary users have no direct access. Escalation requires authorization, data minimization, egress/residency, audit and metering.
5. Preserve AI Human Clone as a separate Cloud Development AI subsystem with consent/authorization, provenance, scope, audit and revocation.
6. Preserve Trusted Sources Intelligence Engine as a first-class Cloud Development AI subsystem for discovery, retrieval, verification, provenance, evidence and knowledge.
7. Preserve Home Assistant Core as Smart Home source of truth; MediaHub UI must not bypass HA Core; MediaHub State Authority remains canonical platform authority.
8. Before dependencies: demonstrated capability gap → mature component → license/security/provenance → adapter → benchmark → adoption.
9. Continue contracts, invariants, negative tests, recovery/evidence, adapter boundaries and deterministic validation for AI, cluster, Smart Home and mobile.
10. Independent review remains external evidence. Autonomous agents may prepare evidence but must not self-qualify, unlock release or authorize production.
11. Each downstream change must be small, reproducible, testable, security-checked and provenance-bound. Stop on architectural ambiguity or a hard governance gate.
