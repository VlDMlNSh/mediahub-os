## Wave 362 — user MediaHub compute, selective model loading and compact context (2026-10-22)

- Requirements proposal: [User MediaHub distributed compute and model loading](MEDIAHUB-A0-USER-MEDIAHUB-DISTRIBUTED-COMPUTE-AND-MODEL-LOADING-REQUIREMENTS-WAVE-362-2026-10-22.md).
- Map addendum: [Wave 362](MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-362-2026-10-22.md).
- Compact machine-readable context proposal: [MEDIAHUB-CONTEXT-STATE.json](../context/MEDIAHUB-CONTEXT-STATE.json).
- Large tasks may originate from ChatGPT or Jarvis. ASTRA GOLD A0 decomposes and routes bounded subtasks across admitted cloud workers, user-owned MediaHub compute nodes and qualified local executors. GitHub Supervisor provides execution/control-plane services; it does not replace A0 as decomposition/routing authority.
- User-owned MediaHub are compute contributors only within explicit admission, owner consent, issuer/capability, quotas, privacy/data-egress, revocation and evidence rules.
- Model strategy target combines quantization with selective/streamed loading or offload where the selected model/runtime supports it. Quantization and selective loading are distinct. Installer-managed storage is a visible, bounded quota for model assets/cache/task-temporary data; it is not permission for unbounded disk use or automatic repartitioning.
- This is a design/documentation proposal in branch `docs/user-mediahub-compute-context-wave-362-20261022`; runtime implementation, tests, independent review, qualification and acceptance are **NOT VERIFIED / NOT ACCEPTED**.
- Report: [Wave 362 evidence](../checkpoints/MEDIAHUB-NEXT-CONTEXT-AND-DISTRIBUTED-COMPUTE-WAVE-362-2026-10-22.md).

---

