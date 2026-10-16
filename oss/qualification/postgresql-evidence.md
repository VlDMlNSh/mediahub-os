# PostgreSQL 18.6 qualification evidence

Status: target-gated / not production-active

## Upstream artifact

- Component: PostgreSQL
- Version: 18.6
- Artifact: `postgresql-18.6.tar.gz`
- Upstream distribution index confirms the artifact and its `.sha256` companion.
- Exact SHA-256 remains pending independent artifact verification and is therefore not asserted here.

## License

- PostgreSQL 18.6 is governed by the PostgreSQL License.
- License evidence is recorded in `oss/manifests/qualification.json`.

## Security baseline

- PostgreSQL 18.6 was released with security fixes recorded by the PostgreSQL security registry.
- The MediaHub qualification state records this as vulnerability evidence, not as a claim of zero future vulnerabilities.

## Qualification boundary

PostgreSQL is a persistence implementation under the MediaHub State Authority. It is not a State Authority itself.

The component cannot become `active` until all mandatory evidence is independently satisfied:

- exact version or immutable digest;
- upstream provenance;
- license record;
- SBOM;
- vulnerability report;
- MediaHub adapter;
- functional tests;
- negative tests;
- degraded/recovery tests;
- rollback tests;
- independent review.

Current state deliberately remains `target-gated`.
