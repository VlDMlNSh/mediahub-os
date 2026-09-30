# MediaHub Unified Visual & Navigation Architecture

Date: 2026-09-30
Status: MH-24 architecture baseline — reconciliation result
Scope: MediaHub OS / MediaHub iOS unified UX, navigation and interaction architecture

## 1. Authority and scope

This document defines UX/UI architecture only. It does not change State Authority, Home Assistant Core authority, security enforcement, privacy boundaries, cloud boundaries, developer boundaries, migration authority, or qualification authority.

Architecture state remains distinct from implementation, testing and qualification.

## 2. Reconciled UX baseline

The repository's current Functional Baseline 2.0 records UI as reconciled but planned/partial, with a unified MediaHub UI that hides implementation topology and avoids exposing backend components as separate user products. Product editions are already architecturally defined; mobile is split into local Core and Remote Access roles; developer applications remain separate from user-data domains.

The MH-24 canonical UX principle is:

**Simple outside / sophisticated inside. Local-first / authority-explicit / state-visible.**

## 3. Unified information architecture

Canonical top-level user domains:

1. Home
2. Smart Home
3. Media
4. Documents
5. Knowledge
6. Digital Twin
7. Engineering
8. AI

Canonical system/service surfaces, normally outside the primary content hierarchy:

- Devices
- Network
- Storage
- Security
- Cluster
- Updates
- Recovery
- Diagnostics
- Settings
- Administration

These service surfaces are cross-cutting and should not duplicate domain authority screens. They are exposed according to edition, role, capability and permission.

Developer products use a separate developer information architecture; they may reference qualified MediaHub objects through authorized APIs but do not inherit user-data visibility.

## 4. Navigation model

### Primary navigation

Desktop Full: persistent sidebar + content/detail split view.
iPad Core: sidebar where space permits; otherwise tab/sidebar hybrid with persistent hierarchy.
iPhone Remote: compact tab/root navigation plus stack navigation.
Developer desktop: workspace sidebar + inspector/detail panes.
Developer mobile: compact workspace navigation + task-oriented stacks.

### Secondary navigation

Within a domain, use segmented controls, tabs or local sidebars only when they represent stable sibling concepts.

### Contextual navigation

Contextual actions operate on the currently selected object and remain subordinate to authorization and domain contracts.

### Global navigation primitives

Back, breadcrumb/path context, deep links, search, command surface, notifications and system-state indicator are global primitives.

No navigation element is itself an authority boundary.

## 5. Canonical object navigation

Use the pattern:

**Collection → Object → Detail → Related objects → Action → Result/Evidence**

Cross-domain navigation must use object identity/deep-link contracts rather than duplicate canonical screens.

Example: a device opened from Home, Search or Diagnostics resolves to the same canonical device detail surface, with the originating context preserved.

## 6. Home / Dashboard

Home is a status-oriented entry point, not a second State Authority.

Home presents:
- current system state;
- important rooms/domains;
- active media;
- alerts and actionable issues;
- recent activity;
- shortcuts to frequent authorized actions;
- update/recovery/security state when relevant.

Home must not conceal degraded, offline, quarantined, updating or recovery states.

## 7. System-state UX contract

Canonical states:

ONLINE, DEGRADED, OFFLINE, CONNECTING, UPDATING, RECOVERING, LOCKED, QUARANTINED, UNQUALIFIED, FAILED, MAINTENANCE.

Every state is represented by semantic icon + explicit label/text + accessibility semantics. Color is supplemental only.

State presentation is consistent across dashboard, object detail, notifications, search results and diagnostics.

## 8. Command contract

Every mutating command follows:

**Intent → Authentication/Session → Authorization → Policy → Domain Contract → Execution → Result → Evidence**

UI never performs direct device mutation. AI proposals use the same path. Search and navigation do not imply authorization.

## 9. AI UX contract

AI is presented as Assistant / Copilot / Advisor.

A proposed action must distinguish:

**AI Proposal → User/Policy Authorization → Action Execution → Result**

The UI must not imply that AI owns canonical state, device authority or security enforcement.

## 10. Search

One global search model spans devices, rooms, media, documents, knowledge, settings, system objects, engineering objects, Digital Twin objects, help and diagnostics.

Search results expose object type, state and authorization-aware availability. Search is discovery, not authority.

## 11. Onboarding / device discovery

Canonical UX lifecycle:

Discover → Identify → Authenticate → Capability → Compatibility → Trust → Qualification → Proposal → User Confirmation → Install/Admit → Verify → Operate.

Unknown or unqualified devices are not presented as operationally trusted merely because they are discoverable.

## 12. Security UX

Security-sensitive operations visibly communicate:
- authentication state;
- trust state;
- permission state;
- authorization result;
- session state;
- revocation;
- quarantine;
- denied actions.

Security enforcement remains below the UI.

## 13. Update / recovery UX

Update:

Detect → Qualify → Backup → Stage → Checkpoint → Update → Validate → Requalify → Accept.

Recovery:

Failure → Recovery → Validation → Restore/Rollback → Requalification.

The UI must communicate the current phase, what is blocked, what is safe to continue, and what user confirmation is required.

## 14. Platform adaptation

One information architecture and one interaction contract; presentations adapt to input, display, role, edition and capability.

No platform gets an independent canonical domain model.

## 15. Accessibility

Required across all surfaces:
- Dynamic Type;
- VoiceOver/semantic accessibility;
- keyboard and focus navigation where applicable;
- minimum touch targets;
- contrast;
- reduced motion;
- localization;
- non-color state communication;
- explicit error/recovery communication.

## 16. Qualification model

UX maturity is tracked separately:

UX Defined → UX Designed → UI Implemented → UI Tested → UI Qualified → Production.

Navigation qualification must cover dead ends, authority bypass, permission bypass, hidden state, duplicated canonical screens, deep-link correctness, restart restoration and reconnect restoration.

## 17. Current MH-24 conclusion

The canonical direction is a unified MediaHub information architecture with a Home-centered but domain-oriented navigation model, persistent system-state visibility, one object identity across entry points, API/domain mediated commands, AI as non-authoritative assistant, and edition/capability/role gating.

Visual styling is deliberately deferred to the Visual Design System artifact after this information/navigation baseline.

## 18. Provenance

Primary current repository evidence: Functional Baseline 2.0 reconciliation candidate at commit 26de2e57316155e32e540ce43349b4cd124873c2, plus the implementation blueprint, architecture gap register and network reference architecture present in main at MH-24 start.
