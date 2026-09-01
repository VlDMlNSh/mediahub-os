# MH-02 Development — Development Host Architecture v1.0

## Scope

The Mac mini 2011 is the permanent development/lab/execution host. A modern Mac is the first product target. The host is not a production substitute and has no product-deployment authority by itself.

## Topology

```text
DEV HOST (Mac mini 2011)
  repository workspace
  MHX / local tools
  corpus / indexes / cache
  build / test
  worker adapters
        |
        v
BUILD ARTIFACT
        |
TEST / REVIEW
        |
RELEASE CANDIDATE
        |
PACKAGE
        |
MODERN MAC PRODUCT TARGET
```

## Filesystem boundary

The host layout is declared in `config/dev-host.json`. Development state, build outputs, packages and backups are separate. Secrets are never stored in the repository; adapters must resolve credentials through the OS Keychain or environment injection.

## Offline-first

Local operations are the default. Network access is explicit and adapter-scoped. Inbound services are disabled by default. Research/AI access is an external worker concern, not part of MediaHub OS authority.

## Build / deploy separation

`repository -> build -> test -> package` is a development pipeline. Installation on the modern Mac is a separate release operation consuming a packaged release artifact. The development host does not silently deploy working-tree state.

## Recovery

Every release package carries a SHA-256 digest. The product rollback unit is the previous known release artifact, not an arbitrary development workspace snapshot.

## Resource policy for the 2011 host

Prefer deterministic local work, bounded concurrency and incremental processing. Heavy builds are manual/scheduled. AI inference is disabled by default on this host; external AI workers are reached only through explicit adapters.

## Authority boundaries

```text
LOCAL TOOLS / WORKERS
        |
        v
UNTRUSTED RESULT
        |
        v
MHX REVIEW / INTEGRATION
        |
        v
DEVELOPMENT STATE

DEVELOPMENT STATE
        X
GOVERNANCE AUTHORITY
```

No host operation creates VAL identities, changes governance gates, claims historical equivalence, or approves a baseline. Development integration remains distinct from governance approval.

## Product migration path

1. Build and test on the development host.
2. Produce a release candidate.
3. Package deterministically and record its digest.
4. Review the package and retain the previous package for rollback.
5. Install explicitly on the modern Mac product target.
6. Verify product runtime independently from development state.

No automatic network deployment is part of v1.0.
