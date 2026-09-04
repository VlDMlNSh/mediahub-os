# MH-15 — Evidence Register

| Area | Status | Required evidence |
|---|---|---|
| Repository | VERIFIED | Current GitHub repository state |
| Host boundary | PROPOSED | Runtime/host implementation evidence |
| Hardware identity | UNKNOWN | Read-only forensic inventory |
| Firmware/EFI | UNKNOWN | Firmware evidence |
| OS/kernel | UNKNOWN | Current host inventory |
| systemd | UNKNOWN | Current service configuration |
| Containers | UNKNOWN | Runtime inventory if present |
| Filesystem/mounts | UNKNOWN | Read-only mount/permission evidence |
| Devices | UNKNOWN | Device inventory and access controls |
| Network/firewall | UNKNOWN | Interface/routing/firewall evidence |
| Sandboxing | UNKNOWN | Current sandbox/MAC configuration |
| Secrets | UNKNOWN | Non-secret permission/configuration evidence |
| CI/runner | REQUIRES VERIFICATION | Current qualification evidence |
| Supply chain | PROPOSED | Provenance/SBOM/signature evidence |
| Update | UNKNOWN | Update mechanism evidence |
| Recovery | UNKNOWN | Recovery design/test evidence |
| Resources | PROPOSED | Limits and exhaustion tests |
| Thermal/power | UNKNOWN | Safe hardware measurements |
| Time | UNKNOWN | Clock/NTP configuration evidence |
| Observability | PROPOSED | MH-11 integration evidence |
| Failure domains | PROPOSED | Runtime fault-injection/test evidence |
| Production qualification | NOT ESTABLISHED | Full qualification record |

Unknown values MUST NOT be promoted to production claims without evidence.
