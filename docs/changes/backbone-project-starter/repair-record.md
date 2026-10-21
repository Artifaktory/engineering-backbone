# Full-1 confirmed repairs

This bounded second implementation iteration starts from
`f0230d0da90b17ef52932ff027529acd23d73f51` and implements only the five confirmed
IDs in [independent triage](review-triage.md). The original Full reports and
521-test check record are preserved. The commit containing this record identifies
the repair subject; subsequent independent checks and Delta reports bind its
exact revision, tree and patch digest.

The environment author changed only `environment.py` and its tests. NUL rejection
now precedes comment/blank handling (START-BEH-01). Root and ancestor junctions
are rejected, and resolved input containment is checked before reading the
register or explicit env file (environment part of START-AUTH-02).

The export author changed only `starter.py` and its tests:

- START-AUTH-01: both source/project overlap directions are rejected before the
  OLD descriptor can execute.
- START-AUTH-02: roots, ancestors and file paths reject symbolic links and
  directory junctions; physical containment is checked before reads/writes.
- START-BEH-02: the existing Git-attested `RepositoryValidator.validate_data`
  method is reused with Git-owned schemas, without invoking its constructor or
  full source/history run. Detailed candidate-derived diagnostics stay internal.
- START-BEH-03: explicit nonfollowing directory traversal checks every governed
  entry before JSON selection, including nested and dangling aliases.

Regressions include an actual nested Git descriptor marker that must not execute,
ordinary external OLD/NEW comparison, junction semantics and escaped resolution,
valid record controls and all five cross-field failures, nested/dangling governed
links and ordinary nested malformed records. Product JSON remains independent.
Conditional native Windows junction branches are included; no native Windows
execution is claimed on Linux.

## Author checks

Commands use the existing hash-locked Python 3.12 interpreter in the author
checkout. Raw result JSON/logs are ignored under `artifacts/`.

| Check | Command | Result |
| --- | --- | --- |
| Environment repair | `PY -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_environment.py -v` | 15 PASS, exit 0; 1.214 seconds unittest / 1.287 seconds wrapper |
| Export repair | `PY -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_starter_export.py -v` | 15 PASS, exit 0; 11.934 seconds unittest |

Environment log SHA256:
`88129e18d80c622e6532bfbc14aa4ee3e5ae210f4c799eb854b75adadc5b6a29`.
Export log SHA256:
`a5a62bda71acde10cfe506e276421376bd0b2ca74a1a8dfdfff663ab1a27c130`.
The explicit source `.env.example` check and environment scoped whitespace check
also exited 0; the scoped export whitespace check exited 0.
These are author checks, not independent qualification or review closure.

No source/legacy validator, schema, catalog, active workflow, dependency, container
input, fixture or previous delivery record was changed. Docker, fleet/native and
remote execution limitations remain open; no runner or downstream mutation was
performed. Full required independent checks and both scoped Deltas follow on the
frozen repair subject before publication.
