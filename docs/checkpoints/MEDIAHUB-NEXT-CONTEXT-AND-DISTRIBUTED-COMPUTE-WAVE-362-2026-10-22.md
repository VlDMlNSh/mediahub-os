# Wave 362 — compact context and user MediaHub compute requirements

- Date: 2026-10-22
- Status: **PROPOSED IN WORKING BRANCH / IMPLEMENTATION NOT VERIFIED / NOT ACCEPTED**
- Working branch: docs/user-mediahub-compute-context-wave-362-20261022
- Base canonical documentation commit: 937b6fa164d0e89e5e5781bf8c236e4fb862ad56
- Canonical documentation branch: docs/mediahub-chat-tree-map-20261012

## Owner-directed decisions captured

1. A large task may originate from ChatGPT or Jarvis.
2. ASTRA GOLD A0 performs decomposition into many bounded subtasks and distributes them across admitted cloud executors, user-owned MediaHub compute nodes and qualified local executors.
3. GitHub Supervisor supplies execution/control-plane capabilities. It is not the independent authority that decomposes and routes the original large task; that responsibility belongs to A0.
4. User-owned MediaHub contributes compute capacity to the corporation only within explicit admission, consent, capability, quota, privacy and revocation rules.
5. The intended model strategy combines quantized representations with task-time selective/streamed loading or offload when supported by the selected model and runtime. Only the parts needed for the active stage should be resident in RAM/VRAM where technically supported.
6. The installer must configure a dedicated, bounded and visible disk-space allocation for model assets, staging, cache and operation-temporary data. A storage quota does not imply permission to repartition disks or use unbounded space.
7. The compact machine-readable context state is proposed at docs/context/MEDIAHUB-CONTEXT-STATE.json. It stores pointers, invariants, statuses, evidence and the next action; it is not a serialized copy of ChatGPT's private internal compressed context and does not supersede source-of-truth contracts.

## Files in this proposal

- Architecture contract: ../architecture/MEDIAHUB-A0-USER-MEDIAHUB-DISTRIBUTED-COMPUTE-AND-MODEL-LOADING-REQUIREMENTS-WAVE-362-2026-10-22.md
- Map addendum: ../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-362-2026-10-22.md
- Machine-readable context: ../context/MEDIAHUB-CONTEXT-STATE.json
- Canonical map: ../architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: ../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Current checkpoint: mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Pull request tracking

- Draft PR: [#485 — user MediaHub compute and compact context](https://github.com/VlDMlNSh/mediahub-os/pull/485).
- PR is open and unmerged; independent review and CI are not yet verified.
- Canonical documentation branch remains docs/mediahub-chat-tree-map-20261012; this branch is an unaccepted proposal.

## Evidence and limitations

- Bootstrap was read from the repository; its existing protocol already requires Wave 272/273 constraints for A0/user MediaHub/local route changes.
- Canonical map blob SHA read: ba5731256321251b6a92b35d51f5bd0f2c1d4e86. The Contents API returned an empty body; the blob endpoint returned the map. The map is very large, so this candidate adds a dated map addendum and prepends a direct Wave 362 index while preserving the full map body; read-back via blob verified the resulting map length and index.
- Issue #301 remains open and governs Contour A qualification.
- No runtime code, installer, model runtime or worker was changed. No model was selected. No tests or benchmarks were run in this documentation pass.
- No Gemini controller, child workflow or local executor was launched in this pass.
- CI and independent review of this branch are not yet verified.

## Next

1. Review the architecture proposal against the current A0 issuer/task and user MediaHub contracts.
2. Validate the JSON state schema and add positive/negative tests.
3. Define hardware profiles, model/runtime shortlist, license/data route, storage quota and cache eviction policy.
4. Implement one bounded admission/scheduling slice and installer quota behavior only after contract review.
5. Preserve all gates for controller, local executor and independent acceptance.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
