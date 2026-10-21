# Independent pre-Full check triage

Separate read-only session `starter_check_triage`. Inspected implementation
`00b758e2f30f85d3c05930d5a08ec21403bb3f75`, actual base
`4e74c7e5f3a07430768f670c4271c1e1a0e28f68`, binary patch SHA-256
`21b2893c840ee044645e74a2fdc252644b735e65872931d4b63eff4d86c3fa47`.
Head/patch/clean worktree independently matched. No tracked edits by triage.

| ID | Severity/category | Confirmed trigger, impact and authorized minimal repair |
| --- | --- | --- |
| START-CHECK-01 | P2; test fixture; high confidence | The comparison fixture removes `docs/templates/testing/review.md` in NEW source. The nominal local-only file `docs/quality/testing.md` links there, so its export also changes upstream through immutable source-URL rewriting. Local plus upstream changes correctly produce `conflict`. Use unchanged non-Markdown managed `requirement.schema.json` for the local-only case; do not change comparison behavior. |
| START-CHECK-02 | P1; trust boundary; high confidence | `trusted_validator()` and `environment_structure()` attest `.py` bytes, then use Python's cached loader. Timestamp-valid poisoned `.pyc` can execute despite unchanged approved source. Execute the actual attested Git blob through `compile` in a fresh `types.ModuleType` namespace with correct `__file__`; no SourceFileLoader or helper cache use. Add both-helper poison-cache nonexecution and no-cache-write regression evidence while valid helpers still run. |
| START-CHECK-03 | P2; test expectation; high confidence | The broad current `owner == project` preservation assertion also includes an intentional managed-to-project ownership transition, whose correct action is `manual-review`. Base preservation on OLD trusted ownership and explicitly require `manual-review` for that transition. Retain upstream/conflict/new/removal/read-only assertions. |

The initial author's ten-test run remains nine passes/one failure, exit 1,
4.485 seconds; wrapper duration was unmeasured, not invented. Log SHA-256
`1e6e06c0b4758fe2be309af1f8c64ddee2bb5a0d3070aa62099e8d7f6d3cb196`;
ignored `artifacts/starter-export/initial-tests.log` and result JSON preserve it.

Independent TEMP-only proof: both helper caches executed poison markers while
their `.py` bytes remained unchanged (0.893 seconds). Correcting only CHECK-01's
fixture passes that assertion and exposes CHECK-03. Both precise expectation
corrections make the entire affected comparison test pass: one test, 1.637 seconds,
exit 0, retaining all other behavior/ownership/no-write assertions. These are
triage experiments, not repaired tracked implementation results.

All three minimal repairs fit the accepted plan and are authorized together in
one pre-Full repair iteration. After repair, run affected cache/comparison cases,
the complete export suite and required independent deterministic checks. Both Full
reviewers must inspect the repaired frozen subject. No Delta is substituted for
their first Full; no source/legacy/schema/catalog/workflow/history gate may change.

Repair completion and final quality belong in later check records. This triage is
not a final PASS, remote CI result or human merge/release approval.

## Authorized author-side repair result

After independent triage, `starter_export_impl` applied only the three confirmed
repairs. Both trusted helpers now compile the actual attested Git blobs into fresh
module namespaces; cached `.pyc` code is neither loaded nor rewritten. The regression
test supplies poisoned caches for both helpers and proves marker nonexecution,
cache-byte preservation and successful valid helper execution. CHECK-01 now uses
an unchanged managed schema for local-only comparison; CHECK-03 retains preservation
assertions based on old ownership and explicitly requires manual reconciliation
for the ownership transition. Comparison behavior was not weakened.

The complete repaired exporter suite passed: **11 tests, zero failures/errors/skips,
exit 0, 6.251 seconds**; wrapper duration remains unmeasured. Log SHA-256
`d31757004fd302b3ff392e436a1a3d05202c5710afb049e894ce0a015cb4db1c`,
ignored `artifacts/starter-export/repaired-tests.log` and result JSON. The original
failure remains separate. Scoped committed-content preparation whitespace passed.
The guide also clarifies manual update integration via a new temporary export;
it introduces no automatic apply or new trust boundary. Independent final quality
and both first Full reviews still must qualify the new frozen subject.
