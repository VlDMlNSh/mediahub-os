# MediaHub Astra — GitHub Cloud Boundary

## Zero-cost baseline

Astra is fully functional in local-first mode with Ollama on mh-dev-01. No cloud account, API key, proxy, or paid provider is required for the local execution path.

GitHub Actions is used only for external/cloud operations. Standard GitHub-hosted runners are free for public repositories; GitHub Free private repositories include a monthly Actions quota. No larger runners are used.

## Credential rule

Never place TinyFish, cloud, SSH, PAT, or private cloud credentials on mh-dev-01.

TinyFish Agent API usage is not a permanent free service. The connector is therefore optional and inactive by default. Even when TINYFISH_API_KEY exists in GitHub, execution remains disabled until the GitHub Actions variable MEDIAHUB_ALLOW_METERED_TINYFISH is explicitly set to true.

For cloud providers that support GitHub OIDC, prefer short-lived credentials: GitHub Actions -> OIDC -> cloud IAM role. Store no long-lived cloud secret.

## Deployment boundary

Astra -> Task Contract -> GitHub -> Actions -> TinyFish/Cloud
                                         |
                                         +-> Secrets or OIDC

The repository never contains secret values. Task contracts carry only allowlisted, non-secret inputs.

## GitHub setup

1. Add TINYFISH_API_KEY as a GitHub Actions repository/environment secret only when TinyFish is authorized and needed.
2. For an OIDC cloud provider, establish the provider trust relationship for this repository/workflow and grant only the minimum cloud permissions.
3. Keep paid cloud resource provisioning disabled until the specific provider, account, region, quotas, and budget controls are defined.

The current repository contains the connector contracts and validation guard; it does not fabricate provider accounts, cloud roles, or API keys.

## Free reference invariant

The system must remain operational with Ollama only, a GitHub repository, a standard GitHub Actions runner, no TinyFish secret, and no cloud credentials on the host.

This is the reference deployment baseline.
