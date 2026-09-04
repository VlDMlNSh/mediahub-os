# MH-12 AI Security

AI is a potentially untrusted computational principal. AI cannot self-authorize, grant capabilities, bypass policy/Consumer Boundary, directly mutate canonical state or treat confidence as authorization.

Canonical path: AI → Recommendation/Proposal → Policy → Authorization → Command → Consumer Boundary → State Authority.

Threats include prompt/indirect injection, tool abuse, exfiltration, model/provider compromise, agent escalation, context/RAG poisoning and secret exposure. Model updates cannot silently expand authority.
