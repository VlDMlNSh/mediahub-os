# MH-17 — Device / Protocol / Integration Architecture

**Status:** PROPOSED / NOT ACCEPTED / NOT FROZEN
**Phase:** MH-17.1 audit + MH-17.2 contract candidate
**Repository baseline:** `main` @ `6eb2ef9efc3ebe6cb89594a0d7180ed7a4c4cb18`

## Authority invariant
State Authority is the sole canonical mutation authority. Device, protocol adapter, cloud service, plugin and AI are non-authoritative participants.

Canonical control path:
`Intent → Policy → Authorization → Consumer Boundary → State Authority → Adapter → Device`

Canonical observation path:
`Device → Adapter → Integration Boundary → Normalization → Runtime/Event Boundary → State Authority/Consumers`

No component in this architecture may create `Device → DB`, `Device → State Authority bypass`, `AI → Device direct`, `Plugin → Device unrestricted`, or `Cloud → Device direct` paths.

## Boundary model
- **Discovery:** produces untrusted observations.
- **Identity:** binds observed identity evidence to a MediaHub logical device.
- **Enrollment:** creates an explicit trust relationship only after proof and policy checks.
- **Capability registry:** declares what a device/adapter can expose; it does not grant authorization.
- **Adapter:** translates protocol semantics and performs only already-authorized operations.
- **Integration boundary:** validates, normalizes, bounds and attributes external data.
- **State Authority:** accepts canonical mutations under the frozen consumer/security contract.
- **Observability:** observes integration health without gaining control authority.

## State separation
The architecture keeps device-reported, observed, desired, policy-allowed, commanded, committed, applied, confirmed and predicted states distinct. A protocol acknowledgement never becomes canonical state by itself.

## Candidate lifecycle
`Discovered → Untrusted → Identified → Verified → Enrolled → Authorized → Configured → Active → Degraded → Quarantined → Revoked/Removed`

Existing repository lifecycle schema is narrower and therefore remains a compatibility constraint requiring controlled evolution rather than silent reinterpretation.

## Protocol neutrality
HTTP(S), REST, WebSocket, MQTT, TCP/UDP, mDNS/DNS-SD, BLE, USB, serial, Zigbee, Z-Wave, Matter, HomeKit, ONVIF and vendor/proprietary APIs are **CANDIDATE** technologies only. Selection requires requirements, compatibility, security, resource, evidence and ADR review.

## Security defaults
Network reachability, VPN presence and TLS transport are not application authorization. Unknown, malformed, unauthenticated, revoked or capability-mismatched devices are denied ordinary control and may enter quarantine.

## Safety
Critical operations require explicit capability, authorization, policy and safety gates. AI confidence is never an authorization primitive.

## Implementation gate
This document does not authorize real-device pairing, production commands, firewall changes, port opening, broker deployment, credential provisioning or firmware updates.

## Acceptance
**NOT ACCEPTED / NOT FROZEN.** Evidence, contradiction review, security review, contract implementation and governance acceptance remain required.