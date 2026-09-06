# MediaHub Security, Privacy & Legal Baseline v1.0

Status: ACCEPTED GOVERNANCE BASELINE — implementation constraint, not legal advice.

## 1. Security by design
- deny by default; least privilege; explicit authorization.
- Authentication, authorization, trust, health and readiness remain separate concepts.
- No remote access may increase authority.
- No AI, cloud, plugin, cache, telemetry, UI or integration may become a canonical authority.
- Secrets are never committed; production credentials are injected through managed secret facilities.
- Security-sensitive operations require auditable command/correlation identity.
- Fail closed on integrity, authorization, trust, policy, or State Authority failures.

## 2. Privacy by design
- Data minimization and purpose limitation.
- Local-first processing where technically and legally appropriate.
- Explicit classification for personal, sensitive, surveillance and operational data.
- Cloud transfer is disabled unless explicitly enabled, authorized, policy-compliant and auditable.
- Retention must be purpose-bound and configurable; deletion must be verifiable where applicable.
- Export/access/correction/deletion workflows must preserve authorization and auditability.
- Surveillance data requires stricter access, retention, export and integrity controls.

## 3. User rights
The product must support applicable rights according to jurisdiction and product context, including appropriate access, transparency, correction, deletion/erasure, portability, objection/restriction and consent/permission controls where legally applicable. Rights must not be represented as universally identical across jurisdictions.

## 4. Legal/compliance guardrails
- Jurisdiction, controller/processor roles, lawful basis, notices, retention obligations and contractual terms must be determined before relevant production features are enabled.
- Regulatory claims require jurisdiction-specific legal review; engineering must not invent legal compliance certification.
- Child/minor, biometric, health, financial, workplace, residential surveillance and other sensitive contexts require elevated review before production enablement.
- Copyright, licensing, content ownership and export restrictions must be respected.
- Security incident handling must preserve evidence while minimizing unnecessary disclosure.

## 5. Engineering gates
Any feature involving identity, surveillance, cloud egress, personal data, sensitive data, payment, external sharing, automated decisions, or privileged administration requires a threat/privacy/legal impact assessment and explicit acceptance before production enablement.

## 6. Evidence rule
`IMPLEMENTED != VERIFIED != QUALIFIED != LEGALLY COMPLIANT`.
Legal compliance is jurisdiction- and fact-dependent and cannot be inferred solely from tests.
