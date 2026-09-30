# MediaHub Platform UX Matrix

Date: 2026-09-30
Status: MH-24 platform adaptation baseline

| Capability | Full desktop | Hub | iPad Core | iPhone Remote | Developer desktop | Developer mobile |
|---|---|---|---|---|---|---|
| Local canonical state | Yes | Yes, profile-dependent | Yes | No; remote API | Developer environment only | Developer environment only |
| Smart Home local operation | Yes | Yes, profile-dependent | Yes | Remote control only | Authorized developer APIs only | Authorized developer APIs only |
| Media | Full profile | Profile-dependent | Local Core capability | Remote/API control | Engineering/development scope | Engineering/development scope |
| Documents | Yes | Profile/entitlement | Yes | Authorized remote subset | No by default | No by default |
| Knowledge | Yes | Profile-dependent | Yes | Authorized remote subset | Sanitized/approved only | Sanitized/approved only |
| Digital Twin | Entitlement/profile | Usually hidden/locked | Entitlement/profile | Remote authorized view | Engineering domain | Engineering domain |
| Engineering | Entitlement/profile | Hidden/locked unless relevant | Entitlement/profile | Authorized remote subset | Yes | Yes |
| AI | Local-first profile | Local/profile | Local-first | Remote assistant via API | Developer AI context | Developer AI context |
| Network | User-facing admin | Profile-dependent | Local admin subset | Remote diagnostics subset | Developer network only | Developer network only |
| Security | Full local controls | Profile controls | Local controls | Session/security controls | Developer security controls | Developer security controls |
| Updates | Local lifecycle | Profile lifecycle | Local lifecycle | Remote initiation/status | Developer deployment lifecycle | Developer deployment lifecycle |
| Recovery | Local recovery | Profile recovery | Local recovery | Remote status/initiation | Developer recovery/evidence | Developer recovery/evidence |

## Edition rule

Differences are capability/edition/role gating over one architecture, not separate UX products.
