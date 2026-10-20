# Pre-refactor main consumer

This is an immutable rendered test input from source commit
`212608aa50ee517b3dd3107a9480da997222fd4f`, tree
`c31ee9b6e418325936b59e31cd7e9b9865ed0064`.

The fixture was produced with the existing hash-locked Copier 9.11.3 from that
clean source checkout, using the exact commit, defaults and `skip_tasks=True`.
The resulting toolchain digest is the former workflow-owned current identity
`35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`.
Only machine-specific Copier installation answers are omitted. The ZIP stores
regular files with fixed timestamps; the manifest records every file hash,
archive hash and the original tooling Git blob identities. The test also pins
the archive hash independently of the manifest.

The workflow regression restores these bytes without Git history, a network
request or executing source-generation code. It exercises the unchanged base and
a real current Copier overwrite-copy refresh, then verifies that a stricter local
policy cannot disappear. Existing historical tests separately exercise
`run_update`. This fixture does not claim native client/model qualification.
