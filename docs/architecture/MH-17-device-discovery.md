# MH-17 — Device Discovery

**Status:** CANDIDATE

Discovery is an observation mechanism only. It may produce candidate endpoints, vendor/model hints, protocol identifiers and reachability evidence, but never trust or control authorization.

Discovery sources may include local/network service discovery, protocol discovery, manual enrollment, QR/NFC-like out-of-band evidence, static configuration and controlled cloud discovery. Each source must declare provenance and confidence.

Required controls:
- bounded scan scope;
- explicit network/interface scope;
- rate and concurrency limits;
- bounded response/message size;
- parser isolation and malformed-input rejection;
- privacy minimization;
- observable audit trail;
- duplicate/collision handling;
- no automatic command capability.

Security invariants:
`Discovery ≠ Trust`, `Presence ≠ Authentication`, `Reachability ≠ Authorization`.

**UNKNOWN:** repository contains no verified discovery implementation or simulator; no specific discovery protocol is currently selected.