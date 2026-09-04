# MH-10 Reverse Master Prompt

Use this record from a development chat to query MH-10 Architecture Authority.

Return only architecture-authorized facts, contracts, boundaries, decisions, evidence, contradictions and unknowns. Do not invent missing details.

For AI implementation requests, verify:
- AI authority boundary;
- P0-03 State Authority;
- P0-05 Consumer Boundary;
- P0-06 Runtime Services;
- P0-07 Policy state;
- MH-8 plugins;
- MH-9 UI;
- MH-11 observability;
- MH-14 persistence;
- MH-21 distributed/hybrid AI records.

Required mutation chain: `Proposal → Policy → Authorization → Command → Consumer Boundary → State Authority`.

If evidence is insufficient, respond `UNKNOWN / REQUIRES VERIFICATION` and identify the exact evidence required. If contradiction exists, STOP and return the contradiction record rather than selecting a convenient architecture.

Development chat may implement only after explicit implementation authorization outside MH-10.
