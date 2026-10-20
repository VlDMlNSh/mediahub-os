# Wave 247 — GitHub Actions execution geography vs. provider region restrictions

- Date: 2026-10-20
- Status: **SOURCE REVIEW COMPLETE; EXECUTION EGRESS GEOLOCATION NOT MEASURED; CONTOUR A NOT PROVEN / BLOCKED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Refs and open governance

- `main`: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- Canonical docs branch before this update: `5d7cd0f580799d8c2691e107728b75899f29a54a`. No merge/rebase.
- Issue #301 and Issue #378 remain OPEN. PR #375, #388, #404 remain OPEN/Draft/unmerged in the current metadata read.
- The canonical map and checkpoint were retrieved by exact blob SHA; complete contents were read before appending.

## Official-source evidence

1. GitHub [GitHub-hosted runners](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners) describes runner machines as the machines that execute jobs and states Linux/Windows runners are hosted in Microsoft Azure. The [runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) explains that hosted runner IPs span many ranges, that ranges are updated weekly, and that larger runners support static IPs.
2. Google's official [Gemini API / Google AI Studio availability list](https://ai.google.dev/gemini-api/docs/available-regions), last updated 2026-04-28, enumerates supported countries and territories. Russia is not listed. The page directs users outside the list to Gemini Enterprise Agent Platform; that is a separate product route whose eligibility, terms, project and regional configuration must be checked. It is not an automatic workaround.
3. Current A1/A2/A3 workflow blobs on `main`:
   - A1 `.github/workflows/gemini-autonomous-engineering.yml`: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
   - A2 `.github/workflows/gemini-agent-2.yml`: `259c8c82b8d90a39e1c90e65390e469b241b5581`
   - A3 `.github/workflows/gemini-agent-3.yml`: `91b5397001e088dfae2f450ee77c9c23118b5601`
   
   All three use `runs-on: ubuntu-latest`, separate secrets `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`, and pass the per-run GitHub Actions `github.token` to the configured GitHub MCP server. None pins a country or static egress IP.

## Answer: the dispatch point is not locationless

The GitHub App/API caller and the Actions runner are different network actors.

- The dispatch request originates from the environment making the API call. When that caller is a hosted integration, it is not the former Russian server's outbound request; its exact egress location was not measured here.
- Once GitHub accepts the event, the job runs on the runner selected by `runs-on`. Current A1/A2/A3 use GitHub-hosted `ubuntu-latest` without an explicit region.
- A Gemini request made by the job originates from the runner's outbound network (unless a proxy/gateway is configured). The dispatch caller's IP/country does not determine the model request's IP/country.
- Thus moving dispatch to GitHub can remove the Russian server from the dispatch path, but does not prove a fixed or eligible provider egress. A larger runner/static IP or approved gateway can improve network predictability, not override provider eligibility. Do not use routing to evade territorial, contractual or sanctions restrictions.

## Qualification result

- A1/A2/A3 dispatch: not performed in this pass; no new run IDs claimed.
- Runner egress country/IP: unknown, not measured.
- Gemini account/project eligibility from that egress: unknown.
- No Gemini API was called; no secret value was read; no dispatch workflow or token workaround was created.
- The worker issuer/capability/replay/revocation and trusted-publisher boundaries remain unresolved.

Next: use an authorized dispatch path and run a bounded no-secret diagnostic on the exact runner class, recording run ID, runner label and independently sourced egress IP/country/ASN metadata without printing credentials. Then verify provider/account eligibility under official terms and separately dispatch each agent. Review artifacts and exact-head CI before any integration.

**Contour A remains NOT PROVEN / BLOCKED. Contour B remains gated on Contour A deployment and independent acceptance.**
