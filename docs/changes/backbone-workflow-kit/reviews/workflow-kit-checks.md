# Workflow kit checks

Base: `1ecbb7a572b3679b422105c557cb88a8bff75dac`. Python 3.12.14 in the existing
reviewed locked environment; source dependency manifests are unchanged.

| Actual check | Result |
| --- | --- |
| Complete `python -m unittest discover -s tests -v` | Exit 0; **228 tests, 296.334 seconds, OK** |
| Engine focused suite | Exit 0; 24 tests, 8.765 seconds |
| Actual workflow payload suite, including historical consumer | Exit 0; 16 tests, 5.606 seconds |
| New/existing Copier suites | Exit 0; 24 tests, 61.926 seconds; 11 new tests included |
| Current validator integration retry | Exit 0; 4 tests, 4.834 seconds |
| Source validator | Exit 0 |
| Merged base-owned validator against candidate with trusted base | Exit 0 |
| `compile_workflow_kit.py --check` | Exit 0; source function exactly matches both workflows and validator |
| `compile_toolchain_fingerprint.py --check` | Exit 0; actual rendered tooling matches current literal |
| Actionlint 1.7.12, all source workflows | Exit 0 |
| Actionlint, rendered PR/maintenance callers and inert delivery examples | Exit 0 |
| Rendered pilot consumer validator | Exit 0 |
| Diff hygiene | Exit 0 before review freeze |

Initial reviewed rendered tooling fingerprint:
`1408a3433b4cfa9b24435b1567b4c48cfcb66c47906dad8e83013bf21ca7bb98`.
The existing eight-file tuple format is unchanged; the merged PR 7 fingerprint
`ac82ff9e47346f754865aa322db29089281569e1cf432edd43c624026f8ad3fb` is retained
alongside the five already approved preceding identities. Unmerged interim tooling
identities are not approved history.

## Coverage

Actual tests execute extracted trusted code and real successful/failing argv,
timeouts/child cleanup, unavailable tools, command/runtime weakening, unsafe paths,
duplicate/invalid config, removed profiles/IDs, incorrect activation, forged report
files, missing/non-success aggregate results, concrete secret patterns and scan
failures. Real Copier copies/updates preserve local config/callers/examples,
enforce installation choices, cover all five declared profiles and an approved
historical consumer. Profile fixture scripts are actual test commands, not evidence
of production compiler/SAST/scanner performance.

The first root integration invocation retained a fixture setup error: a plain copy
included pre-existing empty local template scaffolding with an incomplete Jinja
directory name. Its separately executed historical compatibility test passed.
The integration fixture was corrected to commit Git source before Copier rendering,
matching actual Git distribution which omits empty directories. The four-test retry
and complete 228-test run passed; no production directory was deleted to hide it.
Raw command outputs are retained in ignored `artifacts/workflow-kit/`.

## Operational limits

Local workflow tests emulate artifact byte transfer between fresh job workspaces;
they execute the actual shell/Python payloads. They do not execute GitHub artifact
service transport or runtime setup actions. Pinned download uses the current-run
artifact ID and checksum mismatch failure. Target is GitHub.com hosted runners;
GitHub Enterprise Server is not certified by this delivery.

The built-in scan covers bounded tracked regular files for GitHub token patterns,
AWS access-key IDs and private-key PEM headers; it is not comprehensive history or
provider secret scanning. Project commands remain executable code; schema-valid
commands do not establish safety or semantic acceptance. Human review and hosting
enforcement remain independent. Live downstream activation, production release,
deployment, credentials, approvals and repository protections are unexecuted.
Actual PR/CI and remote review evidence will be added at publication closeout.

## WK-S-1 repair checks

After confirmed triage, three functional line changes distinguish missing files
from parsed JSON null. Five regression test methods were added across standalone,
actual compiled payload and integrated-validator suites. Before compilation refresh,
the two new payload tests reproduced five failing null subcases against the old
compiled function (exit 1); the genuine legacy absence test passed.

The repaired focused suites passed **49 tests in 18.608 seconds**, exit 0.
Source and prior trusted-base validators, both compiler checks, actionlint and diff
hygiene passed. Current rendered tooling is
`7e3d27e21a8db1b1320ded8b8c499dd6033a3f45b0b4b7ff519316612f83ddeb`;
the six approved merged historical identities are unchanged. Initial unmerged
`1408a3433b4cfa9b24435b1567b4c48cfcb66c47906dad8e83013bf21ca7bb98` is not
retained as consumer authority. The repaired complete suite passed **233 tests in
234.476 seconds**, exit 0. Both independent repair Deltas are complete and confirm
WK-S-1 fixed without additional confirmed in-scope findings. Publication still
requires actual remote CI evidence after the reviewed local metadata closeout.
