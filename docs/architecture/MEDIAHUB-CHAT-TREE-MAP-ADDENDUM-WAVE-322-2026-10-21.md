# Wave 322 map addendum — Gemini dispatch and Alamo executor admission (2026-10-21)

- Report: [Wave 322 controller and executor admission check](../checkpoints/MEDIAHUB-NEXT-GEMINI-AND-ALAMO-ADMISSION-WAVE-322-2026-10-21.md).
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Candidate repair: [Draft PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437).
- Live controller blob on `main`: `9453403bba899a2400ee3fb874d32badd034c704`; transport contract test blob: `01ddae5e1d7fd0e49ffa651da9655a5ad7a8d5`.
- The controller source uses GitHub API dispatch with `MEDIAHUB_GITHUB_TOKEN`, separate HMAC key, three fixed child workflows and one immutable target SHA. Effective permissions/secrets and positive trusted-main dispatch remain unverified.
- PR #437 is Draft; exact-head CI was not verified in this pass and the review API returned zero formal reviews. Gemini controller/child runs: NOT RUN.
- SentinelX shows only Voktors-Mini.Dlink operational; no host is verified as Alamo/server 3. Claude Code and agent-browser on Alamo: NOT RUN. Do not substitute another host.
- Contour A remains NOT QUALIFIED / BLOCKED; Contour B remains gated.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).
