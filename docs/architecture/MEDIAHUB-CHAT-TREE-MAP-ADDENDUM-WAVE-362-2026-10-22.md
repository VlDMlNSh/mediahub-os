# Canonical map addendum — Wave 362

Date: 2026-10-22. This addendum is a working-branch proposal until merged; it does not silently modify the immutable Functional Baseline 2.0.

## New owner-directed requirements

- Large tasks can originate from ChatGPT or Jarvis.
- ASTRA GOLD A0 decomposes those tasks and routes bounded subtasks among admitted cloud executors, user-owned MediaHub compute nodes and qualified local executors.
- GitHub Supervisor supplies execution/control-plane primitives; it does not replace A0 as the task decomposition/routing authority.
- User-owned MediaHub contributes admitted compute capacity. Enrollment does not grant unrestricted access to user data, credentials or product-state authority.
- The model execution target combines quantization with selective/streamed loading or offload where the chosen model/runtime supports it. These mechanisms are distinct; performance and quality require measurement.
- Installer-reserved disk space is a bounded, visible quota for model assets, staging, cache and temporary operation data. It is not an implicit authorization to repartition disks or consume unbounded storage.
- Every task is subject to identity, owner consent, issuer/capability, resource quota, data-egress, licensing, revocation and evidence checks.
- Compact context state is proposed at docs/context/MEDIAHUB-CONTEXT-STATE.json; it is a derived index, not an authority that overrides source contracts or GitHub runtime evidence.

## Artifacts in this wave

- Architecture requirements: MEDIAHUB-A0-USER-MEDIAHUB-DISTRIBUTED-COMPUTE-AND-MODEL-LOADING-REQUIREMENTS-WAVE-362-2026-10-22.md
- Compact context state: ../context/MEDIAHUB-CONTEXT-STATE.json
- Evidence report: ../checkpoints/MEDIAHUB-NEXT-CONTEXT-AND-DISTRIBUTED-COMPUTE-WAVE-362-2026-10-22.md
- Bootstrap, checkpoint and roadmap are updated in this candidate branch to require loading/reconciling these requirements during related /next work.

## Status

**DESIGN REQUIREMENTS RECORDED IN WORKING BRANCH / RUNTIME IMPLEMENTATION NOT VERIFIED / NOT ACCEPTED**

Canonical map branch remains docs/mediahub-chat-tree-map-20261012; this Wave 362 branch is a separate, unaccepted working change until reviewed and merged.
