# MediaHub MH-24 — Final Visual Baseline / Transition to MH-25

Date: 2026-10-01
Status: **Defined / MH-24 visual baseline closed for implementation transition**

## Final visual decisions

- Developer Mobile is **iPhone / iOS only**. Android is explicitly out of scope.
- Mobile visual language is unified across Developer Mobile, Remote Mobile and Core iOS/iPadOS.
- Visual reference: Claude mobile interface conventions: light surface, message composition, window treatment and restrained neutral presentation.
- Orange is not used. Replace it with a neutral accent compatible with the MediaHub palette.
- The same palette and semantic state language is used across MediaHub OS and all MediaHub applications.
- Visual inspiration is reference-level only; proprietary assets and source UI are not copied.
- MediaHub OS navigation follows a familiar macOS-style desktop model.
- MediaHub OS top-left menu provides system/application settings and global controls.
- MediaHub OS waiting/home screen presents installed applications, configurations and system entry points as rounded launchers in a desktop-like environment.
- Remote Mobile uses the same visual language and intuitive navigation.
- Smart Home inside Remote Mobile follows the familiar interaction structure of Apple Home/HomeKit while retaining MediaHub's own palette, components and semantics.
- Platform adaptation changes layout mechanics, not domain semantics, authority, terminology or security boundaries.

## MH-25 transition

The functional architecture and unified functional contract are already reconciled.

MH-25 implementation begins from the existing repository and must preserve:
- MediaHub State Authority as canonical platform state authority;
- Home Assistant Core as Smart Home operational authority;
- AI/Local Assistant as non-authority;
- UI as non-authority;
- Developer Mobile as a developer control plane;
- Remote Mobile as an authenticated remote user surface;
- credential-reference/capability model;
- authorization gates;
- offline revalidation;
- evidence-first implementation.

## Developer Mobile platform scope

Supported:
- iPhone
- iOS

Not supported:
- Android
- Android-specific UI or runtime

## Implementation rule

Do not reopen visual architecture unless implementation exposes a concrete contradiction. Resolve implementation details through the fixed visual baseline and existing functional contracts.

Next execution phase:
**MH-25 autonomous implementation → implementation evidence → tests → verification → qualification.**
