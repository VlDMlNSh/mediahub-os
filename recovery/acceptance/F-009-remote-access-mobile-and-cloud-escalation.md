# MediaHub — F-009 Remote Access / Mobile / Cloud Compute Escalation

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Functional requirements

### MediaHub User App
- MediaHub User is the normal user-facing mobile application.
- It operates both on the local network and remotely over an authorized protected remote-access path.
- Remote operation uses the same MediaHub functional model as local operation.
- Remote access does not grant privileges beyond those assigned to the user.

### User-facing scope
- Subject to authorization, MediaHub User may access Smart Home, devices, rooms/zones, automations, scenes, schedules, notifications, history, surveillance, local MediaHub Cluster functions, Personal Media Library, permitted multimedia functions, energy functions and permitted diagnostics/other user functions.
- The exact function surface remains subject to the user's authorization scope.

### MediaHub Developer App
- MediaHub Developer is a distinct developer/operator application.
- It provides authorized access to developer, engineering, diagnostics and infrastructure functions.
- It is associated with the unique privileged MediaHub Developer context.

### No user access to Cloud Development
- An ordinary user, including a user with maximum ordinary MediaHub permissions, does NOT receive direct access to Cloud Development.
- MediaHub User App does not expose Cloud Development as a user workspace.
- Users do not directly operate cloud development infrastructure, distributed compute nodes or developer tooling.

### Local-first assistant execution
- Local Assistant first attempts to execute an eligible request using local MediaHub capabilities and resources.

### Cloud Development as internal compute escalation
- MediaHub may use Cloud Development as an additional compute resource when Local Assistant cannot execute the requested task locally, or when expected local processing time is too high.
- The purpose of this escalation is to increase available compute capacity and/or reduce request processing time.
- The decision to invoke Cloud Development is made by the MediaHub system/developer-cloud control path, not by granting the user direct cloud access.
- The cloud execution mechanism, routing and distribution remain internal system behavior and are hidden from ordinary users.
- The result is returned through MediaHub to the user as the result of the original MediaHub request.

### Offline/local continuity
- Loss of Internet connectivity does not make the local MediaHub unavailable when required local infrastructure remains available.
- Cloud escalation is supplemental and must not be confused with the local MediaHub operating model.

## Explicitly deferred technical decisions

1. Remote-access protocol.
2. VPN/direct/relay topology.
3. Cloud gateway architecture.
4. NAT traversal.
5. Cryptographic transport details.
6. Mobile pairing and session protocol.
7. Exact User App API.
8. Exact Developer API.
9. Cloud escalation thresholds and timing model.
10. Cloud task scheduling/routing details.
11. Cloud data-boundary and privacy enforcement details.
12. Failure/fallback semantics for cloud escalation.

## Main invariants

- Remote access does not increase user authorization.
- User access to MediaHub is not user access to Cloud Development.
- Cloud Development is an internal additional compute resource, not a user-facing development workspace.
- Local Assistant attempts local execution first; Cloud Development may be invoked when local execution is impossible or has excessive expected processing time.
