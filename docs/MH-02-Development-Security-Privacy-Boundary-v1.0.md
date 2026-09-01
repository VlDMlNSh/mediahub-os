# MH-02 Development — Security & Privacy Boundary v1.0

## Purpose

This document defines the security, cybersecurity, and personal-data boundary for the development/execution host. It is an operational development control and does not create or modify governance artifacts.

## Core rules

1. Offline-first is the default.
2. No inbound service is enabled by default.
3. External AI/network access occurs only through an explicit adapter.
4. Credentials, API keys, private keys, cookies, tokens, and personal secrets are never stored in the repository, corpus, task packs, result packs, or release packages.
5. Workers are untrusted execution principals and cannot write canonical governance state.
6. Product deployment consumes an explicit release artifact; packaging does not deploy.
7. Release packaging rejects sensitive paths and symbolic links.
8. Hashes provide integrity/identity checks; they do not prove authorization, provenance, or governance approval.
9. Personal data is minimized: transfer only the smallest task-specific artifact/chunk required for execution.
10. Logs and result packs must avoid copying secrets or unnecessary personal data.

## Data-flow boundary

```text
LOCAL SOURCE
    |
    +--> deterministic index/chunk/hash
    |
    +--> MINIMAL TASK PACK
              |
              +--> local worker
              +--> explicit external AI adapter
              |
              +--> RESULT PACK
                        |
                        +--> primary review
                        +--> development integration

SECRET / PERSONAL DATA
    X
external worker unless explicitly required, minimized, authorized, and policy-compliant

WORKER
    X
canonical governance write
```

## Release boundary

`mhx-host package` is a staging operation only. The resulting artifact is identified by SHA-256 and must be separately reviewed before installation on a product target.

The package operation rejects known credential/private-key locations, environment secret files, sensitive local configuration directories, and symbolic links. This is a deny-by-default packaging control, not a guarantee that arbitrary personal or secret data can never exist elsewhere in source content.

## Incident rule

If a secret, credential, unexpected personal-data exposure, suspicious file, or integrity mismatch is discovered: stop transfer/integration, preserve the relevant evidence minimally, rotate/revoke exposed credentials where applicable, and escalate to primary review. Do not copy the secret into chat, issues, commits, or result packs.

## Governance firewall

Security findings may become development evidence. They do not automatically establish validation, baseline status, historical equivalence, or governance approval.

```text
SECURITY OBSERVATION
        |
        v
DEVELOPMENT EVIDENCE
        |
        X
GOVERNANCE CLOSURE
```
