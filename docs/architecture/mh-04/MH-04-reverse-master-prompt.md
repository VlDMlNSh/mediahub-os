# MH-04 Reverse Master Prompt

Return from development to MH-04 only an architectural/security result packet, not a development conversation.

Required fields:
- implementation context and boundary touched;
- principal/identity model used;
- authentication boundary and failure behavior;
- capability requested/granted;
- authorization and policy decision path;
- command path to P0-05/State Authority;
- evidence and verification results;
- security events/observability impact;
- quarantine/recovery implications;
- candidate technologies and rationale, if any;
- contradictions with MH-01..MH-03/P0-03..P0-06;
- proposed architecture decisions requiring governance.

If a result introduces any direct UI/API/device/plugin/AI/cloud/runtime mutation path, shadow authority, trust bypass or security mechanism that silently changes frozen parent semantics, report `CONTRADICTION / GOVERNANCE CHANGE REQUIRED`.