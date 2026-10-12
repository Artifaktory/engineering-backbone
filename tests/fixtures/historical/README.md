# Immutable historical Copier sources

These fixtures contain the actual minimal template inputs from the three reviewed
Git trees recorded in `manifest.json`. They support real Copier generation and
upgrade checks after a squash merge, shallow checkout or new one-commit repository,
where the original historical Git objects are unavailable.

`bootstrap/` supplies the complete baseline inputs. `pre-attestation/` and
`attested-review/` contain only bytes differing from that baseline; overlay the
selected version directly onto `bootstrap/`. Every stored file is an unchanged
blob from its recorded source tree. No synthetic version or simplified validator
is substituted. Unrelated old repository documentation, tests and workflows are
omitted; all Copier configuration, templates and their included policy, validator,
schema and dependency files remain.

Some historical validators deliberately retain the vulnerabilities covered by
regression tests. These fixtures are test inputs, never current tooling authority
or an installation recommendation. Their exact fingerprints remain the separately
reviewed historical entries in the called workflow; recording a fixture in this
manifest does not authorize a new tooling identity or change the current digest.

The loader checks the reconstructed path set and each original Git blob ID without
calling Git. Tests render each historical source through Copier, compare its
toolchain digest with the manifest and independently with the pinned workflow's
approved historical digests, then execute actual consumer validation and upgrade.
The clean-clone regression repeats generation and upgrade in a single-commit
repository after proving that all three original source tree objects are absent.

| Version | Original source tree | Rendered toolchain SHA256 |
| --- | --- | --- |
| bootstrap | `da5e4b16db198a583ca252f109d33778de0a3f78` | `444494997fb175e75e9fe5031d02e1005db910800711116773c890ea24508566` |
| pre-attestation | `d28d6972fa999e785af13b315ce4daf570c73aea` | `92a5da2f8cbc81f588e231167ae5b66e5f69e255f80be1d13c80ea4152b3dffa` |
| attested-review | `2727bd2a2c0f7a10bca749165f29a9a50021343b` | `ef266be0f22b7e505563e408fe8b93ab6418ec1255bed6c2d6067f9e74be44c9` |

Updating a historical fixture requires recovering the actual reviewed source
blobs, retaining their provenance and reviewing the resulting fixture change.
Do not refresh these files from the current template or alter historical authority
to make a compatibility test pass.
