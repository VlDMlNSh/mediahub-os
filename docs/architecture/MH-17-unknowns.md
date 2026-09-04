# MH-17 — Unknowns Register

**Status:** OPEN / REQUIRES VERIFICATION

1. No verified real-device adapter implementation is visible in the current repository baseline.
2. No verified discovery/enrollment workflow is visible.
3. No verified device credential/certificate provisioning or revocation implementation is visible.
4. No canonical command schema or command lifecycle schema exists in the inspected tree.
5. No canonical telemetry/freshness/sequence contract exists in the inspected tree.
6. No protocol-specific selection ADR is present in the inspected baseline.
7. No verified Matter/HomeKit/MQTT/Zigbee/Z-Wave/ONVIF/BLE/USB/serial implementation is present in the inspected tree.
8. Exact P0-03…P0-05 artifact paths and current governance state require repository-wide historical verification.
9. Exact production network topology, VLANs, firewall rules and cloud relay architecture are unknown.
10. Firmware update semantics for target devices are unknown.
11. Security posture of concrete target hardware is unknown.
12. iOS-specific transport/permission constraints require separate platform evidence.

Unknowns are blockers to `VERIFIED`, `ACCEPTED`, `FROZEN` and `PRODUCTION READY` claims.