# P9.1 — Threat-model refresh

Status: THREAT_MODEL_RECONCILIATION / P9.1 NOT CLOSED

## Scope

Deterministic refresh of documented security/threat surfaces against the current repository architecture. This is a repository evidence reconciliation, not a penetration test and not proof that every runtime path is secure.

## Findings

- Trust boundaries and security invariants are documented across local execution, cloud/provider boundaries, remote policy, credentials, egress and recovery.
- Existing architecture documents contain explicit unknown/gap registers that must remain release considerations.
- Documentation evidence is not equivalent to runtime qualification; negative tests and live endpoint behavior require separate evidence.
- P9.1 remains OPEN until the refreshed threat model is reconciled with current implementation and security-test evidence and all release blockers are classified.

## Source evidence

### docs/architecture/MH-17-threat-model.md
SHA256: 0a792cd0fa4d2c9ab5626fc13ce9ee2a6d769bca4f82f4f5115d3cf2552445d4
- L1: # MH-17 — Threat Model
- L5: Primary assets: device identity, credentials, protocol sessions, commands, capability declarations, telemetry, topology, canonical state, safety controls, firmware, and audit evidence.
- L7: Threats include rogue discovery, identity spoofing, endpoint takeover, credential theft, protocol downgrade, malformed input, replay, command injection, unauthorized capability use, adapter compromise, plugin escalation, AI prompt/control confusion, cloud compromise, firmware compromise, denial of service, and stale/ambiguous state.
- L9: Required controls: authenticated identity where supported, least privilege, default deny, capability validation, replay/idempotency protection, input validation, bounded resources, quarantine, revocation, auditability, fail-closed authorization, and explicit unknown-state handling.
- L11: Concrete protocol-specific threat claims remain subject to technology evaluation and security evidence.

### docs/architecture/MH-21-security-invariants.md
SHA256: 2f59fe51e97a3122f610795d9cf1698a1c5e2966357fb83f50a2dab6e6fbbd13
- L1: # MH-21 Security Invariants
- L5: 1. State Authority remains local and canonical. 2. Cloud/AI/agents are not authority. 3. Network/VPN/mTLS/API keys are not business authorization. 4. Remote results and RAG context are data. 5. Cloud cannot self-authorize or mutate canonical state. 6. Agent capabilities do not self-delegate. 7. Arbitrary egress/fallback is forbidden. 8. Secrets are never unrestricted. 9. Remote compute is bounded, observable and revocable. 10. Cloud failure cannot disable critical local control. 11. Distributed compute does not create distributed authority. 12. Security failures fail closed where applicable.

### docs/architecture/MH-21-security.md
SHA256: d740ce0b41c11e5edf1f01e40e1d3b106d85918dd61a482aead033e3af881f80
- L1: # MH-21 Security
- L5: Threats include compromised providers/models/workers, malicious output, prompt injection, exfiltration, credential theft, tool abuse, agent takeover, supply-chain compromise, DNS/certificate compromise, replay/MITM, API abuse, account takeover, quota/cost/resource exhaustion and model substitution.
- L7: Controls: least privilege, explicit identity, bounded capabilities, default-deny egress, validation, provenance, audit, revocation and fail-closed behavior where applicable.

### docs/architecture/MH-21-network-boundary.md
SHA256: 5cab151b01adf189641e2dee36419764118dad35a59358623ec9f53540a57330
- L1: # MH-21 Network Boundary
- L5: Conceptual topology: MediaHub Core Network → Controlled Egress → External Compute Network → Provider Network → Internet. Prefer controlled outbound communication and minimize inbound exposure. Network reachability never grants business authorization.

### docs/architecture/MH-21-data-egress.md
SHA256: d6a2e980a0237748475f8aa5506b6d19530aa7eb4f5b292fd775e7a56c9fea2e
- L1: # MH-21 Data Egress Gate
- L5: Data → Classification → Purpose → Destination → Privacy Policy → Security Policy → Authorization → Redaction/Minimization → Bounded Transfer → External Compute.
- L7: Default: deny arbitrary egress. AI output, plugin configuration, retrieved documents and external events cannot select arbitrary destinations. Sensitive/private data requires explicit eligibility and authorization. Secrets are prohibited unless a separate narrowly scoped contract explicitly permits them.

### docs/architecture/MH-21-agent-limits.md
SHA256: c3306598ed46a6842791943505693e061c5830a15f542b78f21ba119718d759b


### docs/architecture/MH-21-cloud-boundary.md
SHA256: 83449909fe5402e0036f6c10784224354e4111b007ab1feb1f7fa5291eede41c
- L1: # MH-21 Cloud Boundary
- L5: Local: UI/API/Automation/AI/Plugins → Consumer/Security/Policy → State Authority → canonical state. External: cloud AI/GPU/RAG/providers/agents/tools. The only approved bridge is Controlled External Compute: classify → privacy/security policy → authorization → bounded transfer → adapter → remote compute → DATA result → validation/provenance/policy/authorization → Consumer Boundary → State Authority.

### docs/architecture/MH-21-provider-quarantine.md
SHA256: a56b1feb5b4498805fc124cdeeeeca702d8b9d9d5d739e077068940da5d62b7b
- L1: # MH-21 Provider Quarantine
- L5: Provider lifecycle may transition ACTIVE → DEGRADED → BLOCKED → QUARANTINED. Triggers include security incident, data-handling violation, certificate failure, account compromise, abnormal/malicious behavior or contract violation. Quarantine must be observable, auditable and reversible only through governance.

### docs/architecture/MH-21-remote-policy.md
SHA256: 27138dc6f334263c8a0fbb831f3981e6e77f773a4220b9b9e068ed8c7c5331e9
- L5: Policy defines allowed providers/models/regions/data classes/workloads/tools, resource and cost maxima, duration, retention and emergency restrictions. Policy eligibility is necessary but not sufficient: authorization remains explicit.

### docs/architecture/MH-21-cloud-credentials.md
SHA256: 43c8d2320863c52d673dc5cebebe7e635b8950afbe5ea688d1ab5a4d30684154
- L1: # MH-21 Cloud Credentials
- L5: Separate MediaHub identity, user identity, workload identity, service identity and provider credentials. Credentials must be least-privilege, scoped, rotatable, observable and auditable. AI/agents never receive master credentials or unrestricted device credentials.

### docs/architecture/MH-21-audit.md
SHA256: a1cea3f5d45f8528aa2fb7e25b98fbb553a11263dacde3009b2ff377dad43609
- L5: Audit must establish who requested a workload, what data was used, destination, purpose, policy, authorization, provider/model/version, result/provenance, cost, proposal/command and final outcome. Audit records must themselves obey privacy/security policy.

### docs/architecture/MH-12-recovery-security.md
SHA256: 36353a69e93bcb8897fbeccabb8ceff1a688bdf68a0c8fd8dbfd9023baab6834
- L1: # MH-12 Recovery Security
- L3: Recovery is a separate security boundary with explicit recovery identity/authorization, trusted artifacts, restore authorization, credential/key/certificate recovery, operator separation, audit and post-recovery verification.
- L5: Recovery privilege is not unrestricted runtime authority. Critical recovery operations require separate gates and cannot silently bypass State Authority security.
