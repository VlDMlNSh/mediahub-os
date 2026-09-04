# MH-17 — Device Identity

**Status:** CANDIDATE

Identity layers:
1. `mediahub_id` — MediaHub-assigned logical identity.
2. physical identity — hardware/serial evidence when available.
3. manufacturer/vendor identity — vendor/model identifiers.
4. protocol identity — protocol-specific address/identifier.
5. cryptographic identity — certificate/key/public-key evidence when supported.
6. endpoint identity — network/interface address, treated as locator evidence rather than sufficient trust.

`mediahub_id` is the canonical logical reference. Serial numbers, MAC addresses and protocol addresses are evidence/attributes and must not silently become security authority.

Identity records need provenance, evidence source, observation time and verification status. Mutable metadata must not mutate immutable identity semantics. Rotation/replacement must create an explicit identity transition; cloned or colliding identifiers are security events and require quarantine or operator resolution.

The repository currently has a dedicated identity schema requiring only `mediahub_id`, with vendor/model/serial/vendor_id and protocol/hardware references optional; this is evidence of a foundation contract, not proof of cryptographic enrollment. fileciteturn8file0L2-L5

**UNKNOWN:** exact cryptographic identity mechanisms, certificate lifecycle, revocation mechanism and hardware-backed identity support.