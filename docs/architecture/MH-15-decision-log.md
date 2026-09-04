# MH-15 — Decision Log

## MH15-D01 — Host authority separation

**Decision:** Hardware, firmware, kernel, OS, systemd, container runtime, filesystem, shell, administrator and observability are infrastructure mechanisms, not canonical MediaHub State Authority.

**Status:** ARCHITECTURAL BASELINE / NOT IMPLEMENTATION AUTHORIZATION

## MH15-D02 — Evidence-first hardware qualification

**Decision:** Mac mini Server 2011 remains a candidate platform until forensic and safe qualification evidence exists.

**Status:** PROPOSED / REQUIRES VERIFICATION

## MH15-D03 — Host lifecycle separation

**Decision:** Host boot and MediaHub READY are distinct lifecycle states.

**Status:** ARCHITECTURAL BASELINE

## MH15-D04 — Privileged execution

**Decision:** Arbitrary shell execution from AI/plugin/untrusted paths is forbidden. Privileged operations require explicit identity, authorization, bounded execution and audit.

**Status:** ARCHITECTURAL BASELINE

## MH15-D05 — Lifecycle governance

**Decision:** MH-15 never directly authorizes implementation. Changes follow Architecture -> ADR -> Governance Authorization -> Implementation -> Verification -> Evidence -> Acceptance.

**Status:** ARCHITECTURAL BASELINE
