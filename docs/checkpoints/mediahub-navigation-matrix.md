# MediaHub Navigation Matrix

Date: 2026-09-30
Status: MH-24 canonical navigation matrix

| Surface | Primary navigation | Secondary/context | Canonical object detail | Global search | Commands | System state |
|---|---|---|---|---|---|---|
| Full desktop | Sidebar | Tabs/sidebar sections | Split detail + inspector | Yes | Yes | Persistent |
| Hub display | Sidebar/tiles | Contextual panels | Focused detail | Yes | Yes | Persistent |
| iPad Core | Sidebar/tab hybrid | Stacks/sheets | Split or stack | Yes | Yes | Persistent |
| iPhone Remote | Root tabs | Navigation stack | Stack detail | Yes | Yes, API mediated | Persistent |
| Developer desktop | Workspace sidebar | Inspector | Detail/evidence | Yes | Yes | Persistent |
| Developer mobile | Workspace roots | Task stacks | Compact detail | Yes | Yes | Persistent |

## Canonical navigation rules

1. Every canonical object has one identity and one authoritative detail contract.
2. Search, Home, notifications and cross-domain links converge on the same canonical object surface.
3. Back navigation returns to the originating context unless a deep link establishes a new root.
4. No domain may expose a hidden alternate mutation path around its contract.
5. System-state surfaces remain reachable even when content domains fail.
6. Security/recovery/update flows may temporarily become modal/rooted workflows but must restore the prior context after completion or explicit exit.
7. Developer surfaces never inherit user-data navigation merely because the referenced object exists.
8. Locked/unlicensed capabilities may be discoverable but cannot become executable without entitlement.
9. Remote Mobile has no local-core navigation assumptions; all remote state/actions use MediaHub API contracts.
10. MediaHub Core on iPad/iPadOS is local Core, not a remote viewer.

## Deep-link contract

Deep links resolve to: product edition → authorized context → canonical object → requested subview/action. Invalid, expired or unauthorized links resolve to an explanatory state, never to a bypass.
