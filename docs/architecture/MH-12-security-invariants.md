# MH-12 Security Invariants

Status: PROPOSED → READY FOR GOVERNANCE REVIEW.

SI-01 State Authority is sole canonical mutation authority.
SI-02 Authentication ≠ authorization. SI-03 Identity ≠ privilege. SI-04 Authorization does not bypass State Authority.
SI-05 Reachability ≠ trust. SI-06 localhost ≠ trust. SI-07 VPN ≠ authorization.
SI-08 Capability cannot self-grant. SI-09 Capability cannot silently expand.
SI-10 AI cannot self-authorize. SI-11 Plugin cannot self-authorize. SI-12 Cloud cannot become local authority.
SI-13 Observability cannot become authority. SI-14 Diagnostics cannot bypass normal mutation path.
SI-15 Recovery cannot silently bypass security. SI-16 Update cannot silently increase privilege.
SI-17 Secrets never become ordinary telemetry. SI-18 malformed security input fails closed. SI-19 ambiguity fails closed.
SI-20 unknown entities are not silently trusted. SI-21 security failure cannot become authorization success.
SI-22 enforcement remains separate from reporting. SI-23 no second State Authority.
SI-24 delegated authority cannot exceed delegated scope. SI-25 attenuation cannot increase authority.
SI-26 one failure-domain compromise cannot automatically compromise another.
SI-27 signed provenance does not by itself establish runtime trust.
SI-28 authentication context remains bound to principal and applicable security context.
SI-29 security-sensitive operations require explicit authorization. SI-30 security ambiguity resolves to safest applicable outcome.
