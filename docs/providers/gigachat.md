# GigaChat provider registration

Provider registration only. No qualification or production enablement is implied by this document.

## Identity

- Provider ID: `gigachat`
- Vendor: Sber
- GitHub Actions secret reference: `GIGACHAT_API_PERS`
- Client ID: `01a0e9b4-b923-79b2-9996-e2e33d3fd63f`

## OAuth

- Token endpoint: `https://ngw.devices.sberbank.ru:9443/api/v2/oauth`
- Method: `POST`
- Content type: `application/x-www-form-urlencoded`
- Scope: `GIGACHAT_API_PERS`
- Authorization scheme for token request: `Basic`
- API authorization scheme: `Bearer`
- Access-token lifetime: 30 minutes
- Access tokens must be refreshed and must not be committed, persisted as repository data, or written to logs.

## API

- Base URL: `https://api.giga.chat`
- Model discovery endpoint: `GET /v1/models`

## Security contract

The GitHub secret value is never stored in this repository. Runtime jobs must read it from the GitHub Actions secret store. OAuth access tokens are ephemeral runtime material and must be masked from logs.

## Current state

`registered` only. Qualification is intentionally disabled until the complete provider inventory is assembled.
