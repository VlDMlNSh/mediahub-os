# MH-17 — Device Model

**Status:** CANDIDATE

A Device is a normalized logical representation of a physical/external device. `mediahub_id` is the MediaHub logical identifier and is not interchangeable with serial, MAC, vendor ID, certificate identity or protocol address.

Required conceptual planes:
- identity: stable identity references and evidence;
- endpoints/bindings: protocol interaction references;
- capabilities: explicit declared/validated operations;
- observed state: normalized facts with provenance and freshness;
- desired state: intent, never proof of application;
- health/availability: operational condition, separate from trust;
- trust/lifecycle: security and onboarding state;
- configuration: MediaHub configuration references, not arbitrary device secrets;
- metadata/relationships: non-authoritative descriptive context.

Existing schema already requires these top-level fields and explicitly requires `mediahub_id`; however many nested structures are intentionally generic objects, so semantic enforcement is incomplete and requires follow-up contracts. fileciteturn6file0L2-L5

Invariant: Device model cannot be used as a direct persistence or authorization primitive. Canonical mutations remain behind State Authority.