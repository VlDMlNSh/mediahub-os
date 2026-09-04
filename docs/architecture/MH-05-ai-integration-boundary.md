# MH-5 — AI Integration Boundary

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

AI/Agent output is untrusted, inert proposal data.

```text
AI / Agent
 → proposal / recommendation
 → bounded validation
 → policy
 → explicit authorization
 → command conversion
 → P0-05 Consumer Boundary
 → P0-04 State Authority
```

AI receives no direct mutation primitive, unrestricted shell, unrestricted filesystem, unrestricted credentials, or unrestricted device control. Cloud AI is an external execution environment even when authenticated and connected through a trusted transport.

Prompt content, retrieved documents, model output, tool results, and agent plans cannot grant capabilities or turn observations into commands. Any action requires the same explicit authorization chain as other consumers.
