# MH-21 Security Invariants

Status: PROPOSED.

1. State Authority remains local and canonical. 2. Cloud/AI/agents are not authority. 3. Network/VPN/mTLS/API keys are not business authorization. 4. Remote results and RAG context are data. 5. Cloud cannot self-authorize or mutate canonical state. 6. Agent capabilities do not self-delegate. 7. Arbitrary egress/fallback is forbidden. 8. Secrets are never unrestricted. 9. Remote compute is bounded, observable and revocable. 10. Cloud failure cannot disable critical local control. 11. Distributed compute does not create distributed authority. 12. Security failures fail closed where applicable.