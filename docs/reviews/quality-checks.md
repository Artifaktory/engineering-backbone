# Quality framework checks

Independent quality checker: `quality_independent_checks`, read-only source.
Python 3.12.14, existing isolated hash-locked dependencies; no manifest changes.
Corrected frozen head `b22fd3e2f60d93ea6053f1df09bd6d079ce8c69f`,
tree `572e9fe1099da111fa040b94ee5a8aca08db1f3f`, base
`2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`, full-index binary patch SHA256
`a693e7d51193bd822538905676ba352b9acaec52d3f383651d2b18a177421c49`.
Start/end identities match; source and trusted-base tracked worktrees stayed clean.

Commands below use `/workspace/scratch/59eed579c382/backbone-venv/bin/python`
from the repository root; the checked trusted checkout is
`/workspace/scratch/59eed579c382/quality-trusted-base` at the stated base.

| Actual command | Result |
| --- | --- |
| `python scripts/validate.py` | Exit 0; source structure, explicit no-history notice |
| `python quality-trusted-base/scripts/validate.py --root engineering-backbone --trusted-base quality-trusted-base` using absolute sibling paths | Exit 0; merged base-owned validator against candidate |
| `python scripts/compile_quality_framework.py --check` | Exit 0; catalog and both compiled entry points match |
| `python scripts/compile_workflow_kit.py --check` | Exit 0; previous kit contracts remain compiled consistently |
| `python scripts/compile_toolchain_fingerprint.py --check` | Exit 0; actual Copier-rendered current tooling matches |
| `python -m unittest discover -s tests -v` | Exit 0; **277 tests, 461.263 seconds, OK** |
| `actionlint .github/workflows/quality.yml .github/workflows/governance-checks.yml .github/workflows/workflow-kit-maintenance.yml .github/workflows/workflow-kit-pr.yml` | Exit 0; official actionlint 1.7.7, all four workflows |
| `git diff --check 2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13 HEAD` | Exit 0 |

Suite Bash wall time: 461.972 seconds. Corrected raw log SHA256:
`1d216e1f78e66b2752cbc068494c1682f2894316258377e0a6ab01a48433d85d`.
Raw outputs remain ignored in artifacts. The initial failed run remains recorded
in [check triage](quality-check-triage.md): 277 tests, 625.998 seconds, exit 1,
22 source-fixture failures. Independent triage preceded the one-line catalog
copy repair; all 50 targeted validation tests then passed in 60.126 seconds.
No production code or assertions were changed for that repair.

## Meaningful coverage

43 new methods cover the new trust contract: 30 engine tests, six real Copier
creation/update tests and seven actual workflow/compiler tests. The complete run
also retains all 234 existing tests. Test selection addresses changed safety,
activation, compatibility and ownership contracts rather than adding a test for
each documentation sentence.

The actual pinned-workflow shell payload runs against immutable historical
consumer tooling. Tests demonstrate that the old validator accepts invalid extra
quality declarations while the current workflow-owned guard rejects them. Valid
inactive installation succeeds; candidate quality marker code never executes.
Historical eight-file tooling bytes/digests remain unchanged in those fixtures.
AST compilation detects drift without importing module-level marker code.

Other coverage includes null versus absent data, coherent catalog poisoning,
bounded regular files and symlink ancestors, duplicate JSON keys, active bindings
and approved-base workflow definitions, complete seed activation, traceability,
binary evidence, exception expiry/removal, all four provider combinations, real
Copier clone/tag updates, legacy answers, local document/profile/native preservation
and source/generated role/skill/path parity. These tests do not validate document
substance or authenticate approval metadata.

Current rendered tooling SHA256:
`d96380dbcf89947fbd66f788889742d2d3a7dd7e0d36d0f33abcb68a84a097a2`.
The eight-file attestation format is unchanged. The merged PR 8/9 tooling identity
`7e3d27e21a8db1b1320ded8b8c499dd6033a3f45b0b4b7ff519316612f83ddeb`
is explicitly retained alongside six already-reviewed historical identities.
Interim unmerged quality fingerprints are not retained.

## Limitations

Copier emits its expected absent-temporary-answers warning during rendering; it
does not invalidate the observed PASS. An initial unavailable `/usr/bin/time`
wrapper exited 127 before tests started; the checker then used Bash builtin timing
to launch each actual complete suite once. ShellCheck is unavailable; no external
ShellCheck coverage is claimed. Official actionlint archive SHA256 was verified:
`023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757`.

Source-only validation does not compare policy history; the separate trusted-base
check supplies that structural comparison. Client loading, full normative clauses,
qualified certification, downstream activation and hosting protection settings are
unexecuted. Project commands run in the existing workflow kit, not the quality
guard. Actual published identity, hosted CI and advisory provider review are
separate publication evidence; no local PASS predicts their result.

## Confirmed Q-B-1 repair checks

After independent Full and [triage](quality-triage.md), the regression first
reproduced the two valid dependency configurations failing the original guard,
exit 1. The minimal mapping repair passed 31 engine tests in 1.843 seconds.
Root's seven actual workflow/compiler tests passed in 15.392 seconds.

The independent checker ran the complete repaired suite once on
`6446da63ec222fb0c3d1b09d883437c3f94d2b26`, tree
`aa63cedb6ef2454a96bc7b21988146a41fbd36b7`: **278 tests, 655.696 seconds,
OK, exit 0**. Bash wall time 657.203s. Source/trusted-base validators, all three
compilers, all four actionlint workflows and committed diff hygiene also exited 0.
Start/end source/base identities stayed clean and unchanged; earlier runs remain
recorded. Repaired raw log SHA256:
`d5ae1f63bb071504e4c25df6cad30c44895bf2f753faf22e9a5f1dc68d2e0f23`.

Final functional rendered tooling SHA256:
`88d2d1e89cbff9fd925cac1a235de60867ae90a9ae231cde6cbc0a5eed8ee9b2`.
All seven merged previous identities are unchanged. There are now 44 new test
methods and all 234 existing methods. [Both repair Deltas](quality-delta-review.md)
are complete with no additional confirmed in-scope findings. Hosting evidence is
recorded separately in the PR discussion after publication.
