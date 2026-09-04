# MH-12 Threat Model

Status: ARCHITECTURE COMPLETE / GOVERNANCE REVIEW REQUIRED.

Threat domains: compromised local service/plugin/AI/device; stolen session; forged handle; replay; confused deputy; privilege/capability escalation; secret/token theft; malicious update/dependency/package/model/RAG; cloud/network compromise; clock/log/audit tampering; diagnostic/recovery abuse; rollback/downgrade; persistence compromise; physical access; DoS/resource exhaustion; exfiltration; compromised administrator session.

For every threat the required record is: asset, actor, attack surface, preconditions, impact, likelihood, detection, prevention, containment, recovery, residual risk, evidence status. No numerical risk score is canonical without approved methodology.

Primary control: fail closed, explicit identity/authentication/trust/capability/authorization/policy, boundary enforcement, audit, observability, containment and recovery. Missing evidence => REQUIRES VERIFICATION.
