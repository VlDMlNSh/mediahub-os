# MH-19 Master Prompt — Canonical Architecture Query

Use this artifact from a development chat when MH-19 authority is needed.

Rules: treat GitHub artifacts in `docs/architecture/mh-19/` as canonical architecture evidence for MH-19; do not infer missing capabilities; preserve UNKNOWN/REQUIRES VERIFICATION; never treat PROPOSED/CANDIDATE as accepted; never implement architecture-chat discussion as code here.

Core invariant: Knowledge Graph/Digital Twin are semantic/read/projection layers and never State Authority, Policy Engine, Authorization Engine or Device Control Authority.

Development requests must map implementation to the relevant MH-19 artifact and preserve MH-01…MH-18 and P0-03…P0-07 boundaries. Any conflict must be raised rather than silently resolved.

Lifecycle: Evidence -> Canonical State -> Decision -> Architecture -> Implementation -> Verification -> Governance Acceptance -> Freeze.