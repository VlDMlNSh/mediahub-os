# MH-10 Acceptance Criteria

MH-10 may become ACCEPTED/FROZEN only when evidence demonstrates all of the following:

1. AI cannot directly mutate State Authority.
2. AI output is distinct from command and canonical state.
3. Policy evaluation and authorization precede every mutation path.
4. Consumer Boundary remains mandatory.
5. Agent/tool/plugin/orchestrator cannot self-grant authority.
6. Confidence cannot authorize action.
7. RAG content/tool output cannot become instruction authority.
8. Local and cloud models are untrusted until qualified.
9. External data egress is classified, bounded, authorized and observable.
10. Critical operations do not depend solely on AI.
11. AI failure degrades safely to deterministic/manual mechanisms.
12. Model provenance, supply chain, qualification and rollback are evidenced.
13. Resource governance is bounded by MH-6.
14. AI memory remains separate from canonical runtime state.
15. Privacy, redaction, retention and audit controls are evidenced.
16. Security/red-team tests cover prompt injection, tool escalation, poisoned knowledge and data exfiltration.
17. Cross-chat contradiction register is resolved or explicitly accepted by governance.
18. Unknowns required for production qualification are closed with evidence.
19. Traceability exists across MH-1…MH-10 and P0-03…P0-07.
20. Governance explicitly accepts the final package and records the freeze commit.

Until then: PROPOSED / CANDIDATE / NOT PRODUCTION-AUTHORIZED.
