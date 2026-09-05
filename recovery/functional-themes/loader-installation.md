# MediaHub Functional Recovery — Loader / Installation

**Status:** DRAFT — USER REVIEW
**Recovery stream:** full-functional-spec
**Date:** 2026-09-05

## Scope

The MediaHub loader is a multiboot installation image intended to initialize compatible MediaHub hardware and install the complete MediaHub software environment.

## User-dictated functional requirements

1. The loader is distributed as a **multiboot boot image** that can be installed onto a USB flash drive.
2. The multiboot environment can **automatically test/detect the target hardware** before installation.
3. It can **select the necessary drivers and installation components** for the detected hardware.
4. The image can **automatically download the required current/appropriate Linux image**.
5. The installer installs the Linux operating system and then installs the **required MediaHub components** on top of it.
6. The installation process is intended for hardware including **Mac mini, mini PCs, and Raspberry Pi** (subject to hardware compatibility).
7. The installer provides disk-space partitioning/storage allocation during installation.
8. The user can allocate one storage volume/domain for **video-surveillance recording**.
9. The user can allocate a second storage volume/domain for the **Personal Media Library**.
10. A third storage area is allocated automatically for **the operating system, recovery systems, and backup systems**.
11. The surveillance-recording storage and Personal Media Library storage are conceptually separate allocations/domains.
12. The installer UI is **minimalist** and intentionally avoids unnecessary information.
13. The visual language and interaction model should be **maximally close to the minimalist macOS installation experience**, without implying reuse of Apple's proprietary implementation or assets.

## Important preservation notes

- This document records the functional requirements as dictated by the user; implementation details not explicitly specified remain deferred.
- Exact Linux distribution/image source, version-selection policy, driver mechanism, hardware compatibility matrix, partition/filesystem technology, backup layout, recovery layout, network requirements, offline installation behavior, encryption, rollback, and failure/recovery semantics remain **DEFERRED** unless separately accepted.
- The loader must not silently collapse the three conceptual storage purposes into one undifferentiated allocation during later architecture/development work.

## Acceptance

Not yet accepted. Awaiting user review and explicit `Утверждаю`.
