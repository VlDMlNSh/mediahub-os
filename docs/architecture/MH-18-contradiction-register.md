# MH-18 — Contradiction Register

**Status:** OPEN / NO CONFIRMED CONTRADICTION

| ID | Potential contradiction | Evidence | Disposition |
|---|---|---|---|
| C-18-001 | Device lifecycle schema could be mistaken for media lifecycle | `schemas/domain/lifecycle.schema.json` defines MediaHub Device lifecycle | NOT A CONTRADICTION YET; media lifecycle requires separate contract |
| C-18-002 | Media AI could be interpreted as mutation authority | Existing AI inference request contract exists; P0-06 says AI proposals are inert data and services cannot autonomously mutate | CONSISTENT; MH-18 must preserve this boundary |
| C-18-003 | Media storage could become implicit State Authority | P0-06 excludes durable persistence within its scope and preserves sole State Authority | OPEN; requires explicit MH-18 storage/state boundary |
| C-18-004 | Repository absence of media code could be interpreted as proof of global absence | GitHub search/tree only covers inspected repository state | RESOLVED AS EVIDENCE LIMIT; mark unknown, not absent globally |

Future contradictions must cite exact artifact/version/commit and must not be resolved by assumption.
