# Canonical map addendum — Wave 327 (2026-10-21)

This addendum links the current admission report without replacing historical IDs.

- **Wave 327 report:** [Gemini and browser admission evidence](../checkpoints/MEDIAHUB-NEXT-GEMINI-AND-BROWSER-ADMISSION-WAVE-327-2026-10-21.md)
- **Canonical map:** https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- **Governance issue:** https://github.com/VlDMlNSh/mediahub-os/issues/301
- **Gemini controller:** https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml
- **Candidate PR #437:** https://github.com/VlDMlNSh/mediahub-os/pull/437

## Status

- Controller and three child workflow source files exist on main. They use GitHub REST workflow dispatch, a dedicated GitHub API token, a separate HMAC key, a trusted main ref, one shared immutable target SHA, and a batch-admission variable.
- Effective secret/variable metadata, token scope, authoritative branch governance, exact-head CI for PR #437 and formal independent review remain NOT VERIFIED. No controller dispatch or Gemini child run was started.
- SentinelX identifies the specified host as `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`. The command `which agent-browser` returned no executable. Agent-browser CLI setup could not proceed because SentinelX policy reload requires a sudo-enabled service restart, but noninteractive sudo is not configured. The narrow allowlist entries `npm install -g agent-browser` and `agent-browser` are staged in the host config but are not active until the owner-authorized SentinelX service restart succeeds.
- `which claude` returned no executable. Ollama discovery timed out; presence is NOT VERIFIED. No physical server was used in the Gemini transport.
- Gemini Agents 1–3 remain NOT RUN. No controller/child run IDs, shared target SHA, artifact digests, qualification or acceptance are claimed.

Next: resolve exact-head CI/review and non-disclosing launch gates; resolve the owner-controlled SentinelX restart path; then run the trusted-main no-secret probe and `agent-browser skills get core` before any provider or child dispatch.
