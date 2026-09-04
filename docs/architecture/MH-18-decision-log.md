# MH-18 — Decision Log

**Status:** PROPOSED / AUDIT PHASE

| ID | Decision | State | Basis |
|---|---|---|---|
| D-18-001 | Media/content is not State Authority | PROPOSED | MH-18 master invariant; consistent with P0-06 single-authority boundary |
| D-18-002 | Media storage is a separate subsystem from canonical metadata/state | PROPOSED | Required authority separation; concrete storage design awaits MH-18 storage analysis |
| D-18-003 | Search indexes and derived artifacts are rebuildable/non-authoritative | PROPOSED | Required resilience model; implementation/evidence pending |
| D-18-004 | AI media analysis produces candidate/derived metadata only until explicit authorized mutation | PROPOSED | Existing AI contract + P0-06 AI inert-data boundary |
| D-18-005 | Codec/media parser execution requires a dedicated security boundary | PROPOSED | Untrusted media/parser attack-surface requirement; technology choice pending |
| D-18-006 | No media technology is canonical yet | PROPOSED | Technology-neutrality requirement |

No decision in this log authorizes production integration. Decisions become authoritative only after the applicable architecture/security/privacy/evidence/ADR/governance gates are satisfied.
