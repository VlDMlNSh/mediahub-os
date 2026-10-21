# Wave 328 — Gemini dispatch and Voktors-Mini executor blockers

Date: 2026-10-21. This addendum links the [Wave 328 report](../checkpoints/MEDIAHUB-NEXT-GEMINI-AND-VOKTORS-DISPATCH-BLOCKERS-WAVE-328-2026-10-21.md) from the [canonical map](MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

- Current main HEAD: `79196054d84b1197cea1447dd1db5ad075302834`; controller blob SHA `9453403bba899a2400ee3fb874d32badd034c704`.
- PR #437 remains Draft/open at `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; no formal reviews and no check runs were returned for that exact head.
- `main` is currently unprotected in the GitHub branch response; required status checks are disabled.
- Controller run [39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179) was SKIPPED; all four jobs were skipped. No Gemini child workflow IDs or artifacts exist for this pass.
- Owner reports HMAC and batch flag settings exist, but effective values and transport-token permissions cannot be verified through the connected read-only API. No secret values were read.
- SentinelX host `Voktors-Mini.Dlink` (`host_5f7264034bdf0b51`) pinged successfully, but capability/state calls timed out or disconnected. Diagnosis: host_overloaded. agent-browser and Claude/FCC remain NOT RUN; no alternate host or transport was used.
- Next: formal independent review, exact-head CI, branch governance, secret-scope verification and trusted-main no-secret probe; then one controller-only batch on a single immutable SHA. Restore host stability and read installed agent-browser core instructions before browser work.


Additional owner clarification and independent recheck: [Wave 328 Gemini transport and Voktors recheck](../checkpoints/MEDIAHUB-NEXT-GEMINI-TRANSPORT-AND-VOKTORS-RECHECK-WAVE-328-2026-10-21.md), blob SHA `047c504d1869c15219936bb497f6f35b8964690c`.

- Controller uses the exact ASCII identifier `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`; owner typed `MEDIAHUB_DISPATCH_НМАС_KEY` with Cyrillic characters in the HMAC segment. Verify the configured secret name only; never read or print the value.
- Current recheck found PR #437 still Draft/open with no exact-head workflow runs/statuses and zero formal reviews. Gemini Agents 1–3 remain NOT RUN. No controller trigger was posted.
- SentinelX ping succeeded once, but follow-up capabilities and bounded script execution timed out again. agent-browser core instructions remain unretrieved and Claude/FCC free route remains NOT VERIFIED.
