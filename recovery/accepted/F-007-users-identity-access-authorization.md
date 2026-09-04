# MediaHub F-007 — Users / Identity / Access / Authorization

Date: 2026-09-04
Status: CONFIRMED_ACCEPTED

## Accepted functional requirements

- MediaHub supports multiple users.
- Each user may have a profile, identifier, associated devices, personal settings, preferences, presence zones, permissions, notifications and access to rooms/functions.
- MediaHub distinguishes ordinary user, owner/administrator, engineer/integrator and system/operator contexts; the exact role taxonomy remains a later technical decision.
- Actions capable of changing system state are subject to the permissions of the acting user/context.
- Authorization applies to device control, automations, scenes, schedules, settings, network configuration, integrations, clusters, storage, surveillance, updates, diagnostics and engineering functions as applicable.
- Access may be scoped by room, zone, device group, equipment type, function or other authorized boundary.
- Critical or potentially dangerous operations may require additional confirmation and/or authorization.
- Presence does not itself grant identity or authorization: Presence != Authentication != Authorization.
- Local identification/authorization should be possible for local functions where appropriate; critical local functions should not depend on external cloud when required local infrastructure is available.
- Engineer/Advanced mode may expose technical configuration, diagnostics, integrations, network parameters, events, system state and extended logs; ordinary users should not be forced to manage this complexity.
- Significant user actions should be traceable through an audit/event chain such as User -> Authorization -> Action -> Result.

## Accepted clarification — MediaHub mobile applications and developer instance

### Mobile application architecture

- MediaHub has a mobile application that works remotely, not only while the phone is physically on the local MediaHub network.
- The MediaHub mobile application is divided into two distinct application variants/roles:
  1. User application.
  2. Developer application.
- The user application is the normal remote user control surface for MediaHub.
- The developer application provides expanded developer/operator functions beyond the ordinary user application.

### Developer application

- The developer application exposes expanded functions required for development and operation of the MediaHub development environment.
- These expanded functions include access/control of the cloud development environment and associated cloud development capabilities, subject to the later security and authorization model.
- Developer functions are not exposed to ordinary users through the user application.

### Unique MediaHub Developer instance

- There is a single, unique MediaHub Developer instance with expanded capabilities.
- This unique Developer MediaHub has functions beyond ordinary MediaHub installations, including expanded developer and cloud-development capabilities.
- The exact hardware/software form, ownership, authorization model and full capability boundary of this unique Developer instance remain to be specified in later functional/technical blocks.

## Explicitly not fixed by F-007

- Exact authentication mechanisms (password, PIN, biometric, passkeys, trusted devices, etc.).
- Exact role model and RBAC/ABAC/ACL implementation.
- Guest/emergency access rules.
- Remote authentication/session semantics.
- VPN and remote-access architecture.
- Cryptographic implementation.
- Exact audit-log schema, retention and export.
- Exact boundary and authorization protocol between the developer mobile application, unique Developer MediaHub and cloud development environment.

## Core invariants

1. Presence never automatically equals authorization.
2. User-facing application and developer-facing application are distinct capability surfaces.
3. Remote operation is a first-class MediaHub mobile capability.
4. Developer/cloud-development capabilities are restricted to authorized developer/operator contexts.
5. The unique MediaHub Developer instance is a distinct privileged product/runtime role and must not be treated as an ordinary consumer MediaHub node.
