# Quality framework Full review

Both independent reviewers inspected the same frozen snapshot read-only after
all required deterministic checks passed: base
`2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`, head
`b22fd3e2f60d93ea6053f1df09bd6d079ce8c69f`, tree
`572e9fe1099da111fa040b94ee5a8aca08db1f3f`, full-index binary patch SHA256
`a693e7d51193bd822538905676ba352b9acaec52d3f383651d2b18a177421c49`.
The [independent checks](quality-checks.md) include 277 tests, 461.263 seconds, OK.
Snapshot identities and clean tracked worktree were rechecked after each review.

## Behavior and compatibility

Reviewer: independent `quality_full_behavior`. Coverage: all 12 sources, 16 rules
and nine profiles; governance, schema, diagrams and phase/role responsibilities;
profile activation/inheritance, bindings, exceptions, traceability and evidence;
compiler/workflow authority, real Copier/provider/update preservation, native
context, existing test changes and eight-file compatibility. Public-source spot
checks agreed with the register's edition/scope and reference-only limits.

**Q-B-1, P2, high confidence, functional compatibility.**
Location: scripts/quality_framework.py:309–311, also compiled into the validator
and reusable governance workflow. A valid active complete workflow with
`dependencies` capability and a singular `dependency` check assigned to both PR
and maintenance is rejected by quality-framework adoption, including an inactive
quality seed. The new capability loop requires pairs using plural `dependencies`,
which is not a supported check kind. Existing workflow_kit.py:122–124 correctly
maps that capability to singular `dependency`.

Observed path: quality_errors → validate_content → workflow → required/coverage
comparison. A temporary complete baseline/docs fixture passed the existing kit
validator with exit 0, but the quality guard reported required workflow checks
missing. Removing only the capability made the quality guard return no errors.
An isolated compatibility experiment covered all eight capabilities and all five
workflow profiles; only dependencies diverged. No project commands were executed.
The bug is introduced by this diff and affects AC-2/4 compatibility. Consumers
cannot fix it by adding plural-kind checks because that kind is unsupported.

Minimal repair: explicit capability-to-kind mapping for dependencies/container;
regress a complete dependency-enabled workflow through both guards and missing
required phases. Recompile both entrypoints and current tooling fingerprint.
No additional confirmed in-scope behavior findings.

## Security and trusted authority

Reviewer: independent `quality_full_security`.
**NO CONFIRMED IN-SCOPE FINDINGS** within the recorded snapshot and coverage.

Inspected the entire guard/compiler, both entrypoints, schema, native permission
diffs, installation/preservation contract, relevant tests/docs and retained
fingerprints against base/head policy. Covered bounded regular files and binary
evidence, symlink ancestors, traversal, duplicates/null/malformed inputs, compiled
catalog versus coherent poisoned base/candidate data, activation, inherited
selection/bindings, trusted check definitions, exceptions and expired repair.
The eight-file tuple is intact; dependency manifests/historical fixtures unchanged.

Independent focused execution: `python -m unittest tests.test_quality_framework
tests.test_quality_workflows -v`, exit 0, 37 tests in 13.063 seconds. Temporary
malformed-type probes exited 0: 260 cases returned normally, including nine valid
substitutions. Committed diff hygiene exited 0. No tracked edits or full-suite
repeat. Actual shell and AST tests cover old-validator blind spots and candidate
code nonexecution. QCHECK-1 retains its original assertions.

## Limits and next gate

Actual published CI, live clients, hosting protections, human/evidence
authentication, downstream activation, normative clauses and certification are
unproved by this review. This is not human merge/release approval. At the end of Full, Q-B-1 remained
open pending triage, confirmed repair, relevant checks and independent scoped Delta.
No source repair occurred between the two Full reviewers.

Subsequent [repair Deltas](quality-delta-review.md) close Q-B-1 on the repaired snapshot.
