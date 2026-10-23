# MediaHub Ollama Cloud route feasibility — Wave 401

Date: 2026-10-23

## Decision summary

**REMOTE INFERENCE IS FEASIBLE; GITHUB-HOSTED CLI AUTHENTICATION AND FREE-ROUTE ADMISSION ARE NOT VERIFIED.**

Ollama officially documents cloud-hosted models that run inference on Ollama's infrastructure, not on the GitHub Actions runner. The runner can host the CLI and task orchestration without an owner-operated physical server. Official docs also document direct cloud API access with `OLLAMA_API_KEY`, using `https://ollama.com/api` or the OpenAI-compatible `https://ollama.com/v1` base URL.

Sources:
- [Ollama Cloud documentation](https://github.com/ollama/ollama/blob/main/docs/cloud.mdx)
- [Ollama API introduction](https://github.com/ollama/ollama/blob/main/docs/api/introduction.mdx)
- [Ollama OpenAI compatibility](https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx)
- [Ollama Cloud models announcement](https://ollama.com/blog/cloud-models)

## Architecture distinction

1. **GitHub-hosted CLI + Ollama Cloud model:** the temporary `ubuntu-latest` runner launches the CLI; Ollama Cloud performs inference. No persistent MediaHub-owned server or local GPU is required.
2. **Direct Ollama Cloud API:** a workflow calls the cloud endpoint with `OLLAMA_API_KEY`; no local Ollama server or CLI is required. This is the documented non-interactive API route.
3. **Local model on GitHub runner:** model weights and inference run on the ephemeral runner, consuming its memory/CPU. This is a different, more resource-constrained route.

## Admission blockers before a CLI workflow can be dispatched

- The current official CLI documentation says cloud models require Ollama account sign-in. A supported non-interactive GitHub Actions authentication path for the CLI has not yet been verified from primary documentation.
- Direct API key support is documented, but that alone does not prove the CLI accepts `OLLAMA_API_KEY` as a substitute for CLI sign-in.
- Current account eligibility, free-tier limits, quotas, and model availability have not been verified for this repository's account. Do not describe this as a guaranteed free route until those terms are confirmed.
- No Ollama API key was inspected or used; no provider request was made.
- No physical server is required for the hosted route, but provider-side execution and provider data-handling policy still apply.

## Existing adjacent implementation evidence

- Draft [PR #502](https://github.com/VlDMlNSh/mediahub-os/pull/502) adds a separate GitHub-hosted FCC/Claude candidate route; it is unrelated to Ollama Cloud and must not be treated as Ollama qualification.
- PR #502 head: `0a4ccf0e95efb5cc134eedb62dd2f9c175a24e20`.
- [PR #502 install-smoke run](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39876277682) completed successfully. Job `120162541784` verified FCC installation and entrypoints only; it made no provider/model request. This is not Ollama evidence.
- Current `main`: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Canonical documentation branch before this report: `c2fdcd640bf2ffa2155aa6c05f49aca7b37ded3a`.

## Safe next step

Prepare a separate, disabled-by-default Ollama Cloud qualification workflow only after choosing one supported route:
- **Preferred for reliable non-interactive CI:** a bounded direct API smoke using `OLLAMA_API_KEY`, if an owner-approved provider key and budget/free-tier policy are available.
- **CLI-specific route:** first prove a documented non-interactive CLI authentication method without printing or uploading auth state; otherwise mark CLI mode BLOCKED and use the direct API route instead.

Any first live request must be manually gated, use a harmless fixed prompt, enforce timeout/output limits, avoid repository-write permissions, and fail closed on quota/auth errors. No paid fallback, secret exposure, or automatic promotion is allowed.

## Status

- Remote inference feasibility: **VERIFIED FROM OFFICIAL DOCUMENTATION**
- GitHub-hosted CLI authentication: **NOT VERIFIED**
- Free-tier eligibility and quota: **NOT VERIFIED**
- Live provider probe: **NOT RUN**
- Workflow implementation for Ollama Cloud: **NOT STARTED**
- Contour A acceptance: **NOT ACCEPTED**
