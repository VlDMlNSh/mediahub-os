# MH-04 Master Prompt

Use MH-04 as architectural authority for Security / Trust / Authorization Foundation. Inherit MH-01..MH-03 and P0-03..P0-06. Do not redefine frozen parent decisions. Preserve one canonical mutation path and no second authority.

For implementation work, treat MH-04 as constraints only: establish principal identity, authenticate at the applicable boundary, assign bounded capabilities, evaluate authorization and policy, then submit commands through the inherited Consumer Contract to State Authority. UI/API/device/plugin/AI/cloud/runtime services cannot mutate directly. Unknown or ambiguous security context fails closed; suspicious subjects may be quarantined. Security events/telemetry are facts/observations, not mutation triggers.

Do not choose concrete security technologies without evidence + compatibility + security + ADR. If implementation evidence conflicts with a frozen parent decision, return `CONTRADICTION / GOVERNANCE CHANGE REQUIRED` rather than changing architecture silently.