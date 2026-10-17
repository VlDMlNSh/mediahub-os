# MediaHub OS — Python package source audit, Step 1 (2026-10-17)

## Scope

Bounded first step of the next pass: determine whether the earlier `pip-compile --no-index` ambiguity still exists in the current Cloud Agent Fabric dependency-lock workflow. No production or authority configuration was changed in this step.

## Snapshot and evidence

- PR #337 remains open, Draft, and unmerged. Observed PR head: `b74ab89052ce2d023bdbfdd725837b39950b5676`.
- The current generator workflow was read at that head; blob SHA: `c22d820ccb59bcbdbaf4bfa40125063f2c68d8e0`.
- The current committed lock file was read at that head; blob SHA: `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`.
- The lock header now records the explicit command `env -u PIP_NO_INDEX PIP_CONFIG_FILE=/dev/null PIP_INDEX_URL=https://pypi.org/simple ... --no-config --index-url=https://pypi.org/simple ...`. It no longer contains the previously flagged `--no-index` marker.
- The workflow explicitly sets `PIP_CONFIG_FILE=/dev/null` and `PIP_INDEX_URL=https://pypi.org/simple`, removes `PIP_NO_INDEX` for the compile invocation, and passes `--no-config --index-url=https://pypi.org/simple`.
- Latest retrieved generator run: [39048549631](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048549631), event/source SHA `d493b042bdf5bb0259b84f69dc48b43875d77474`, completed successfully. Its job log confirms `pip config debug` reported `PIP_CONFIG_FILE='/dev/null'` and `PIP_INDEX_URL='https://pypi.org/simple'`; no `PIP_NO_INDEX` entry appeared in the filtered configuration output. It emitted input hash `1056b740383d453db32b92c7f24170a952eadf5ffafaaa7875ad58329c313916` and lock hash `f30c923e5bf25777fda85de14fbe1b2cdc33bc57b2a1ff88adc3e2bef5205f29` for that run's checked-out revision.
- Latest validation run found for current PR head: [39050540530](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39050540530), completed successfully. Its source is the current PR head.
- Current generator's push path filter watches the input file and generator workflow, not the lock file itself. This is intentional to avoid a generator-trigger loop; changes to the lock are covered by the separate schema-validation workflow.

## Conclusion

The earlier `--no-index` ambiguity is resolved in the current workflow/lock source snapshot. The observed successful generator log supports the explicit PyPI-source configuration, but that generator run is on an earlier commit than the current PR head. Therefore this step does **not** claim that the lock has been regenerated and hash-compared at current HEAD.

## Next small step

On the current PR head, compare the lock's committed content and SHA-256 with a fresh generator artifact/run, verify the source/input commit identity, and ensure the validation workflow installs the same lock with `--require-hashes`. Keep PR #337 Draft; no merge or deployment is authorized by this audit.
