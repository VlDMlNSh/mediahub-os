# MediaHub Functional Recovery — Loader / Installation

**Status:** CONFIRMED_ACCEPTED
**Recovery stream:** full-functional-spec
**Date:** 2026-09-05

## Accepted functional requirements

1. Multiboot boot image installable to USB flash drive.
2. Automatic target-hardware testing/detection before installation.
3. Automatic selection of necessary drivers and installation components.
4. Automatic download of the required Linux image.
5. Installation of Linux followed by required MediaHub components.
6. Target platforms include Mac mini, mini PCs, and Raspberry Pi, subject to compatibility.
7. Installation-time disk-space allocation.
8. Dedicated allocation/domain for surveillance recording.
9. Dedicated allocation/domain for Personal Media Library.
10. Automatically allocated system area for operating system, recovery, and backup systems.
11. Surveillance recording storage and Personal Media Library storage remain separate logical domains.
12. Minimalist installer UI with no unnecessary information.
13. Visual language and navigation maximally close to the minimalist macOS installation experience, without implying reuse of Apple's proprietary implementation/assets.

## MediaHub installation/product variants

14. Full MediaHub version for Mac mini.
15. Mac mini version uses the Mac mini's original/standard Apple audio capability as part of the MediaHub audio concept; exact interpretation/technical implementation remains to be detailed.
16. Mac mini MediaHub can form and connect to a MediaHub Hi-End audio system.
17. Minimum Hi-End audio configuration includes a soundbar.
18. Hi-End audio can be expanded with two floor-standing speakers.
19. MediaHub version for mini PC.
20. Simplified MediaHub version for Raspberry Pi.
21. iOS MediaHub version for installation/use on iPhone or iPad located on the object.
22. Raspberry Pi and iOS versions do not include local hard-disk surveillance-stream recording.
23. Raspberry Pi and iOS versions do not include local Personal Media Library storage.
24. Functional differences between product variants must be preserved during later implementation decomposition.

## Cross-lifecycle contextual guidance

25. Across installation, equipment integration, configuration, automation creation/configuration, and external ecosystem export, MediaHub provides small contextual pop-up hints.
26. Activating a hint opens a complete actionable instruction.
27. Instructions are intended to simplify coordination of the user's actions and provide clear step-by-step guidance.
28. This guidance is a cross-cutting MediaHub capability, not an installer-only feature.

## Deferred

Exact Linux distribution/source/version policy, driver mechanism, compatibility matrix, partition/filesystem technology, backup/recovery layout, network requirements, offline installation behavior, encryption, rollback, failure/recovery semantics, exact Apple audio implementation, Hi-End hardware matrix, and variant-specific implementation details remain deferred unless separately accepted.
