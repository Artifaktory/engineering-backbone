# Pre-review deterministic-check triage

## CHECK-01 — confirmed test expectation regression

Quality checker: `planning_quality`. Independent triage: `planning_plan_review`.
Inspected implementation: `729531ef541720058c1984e925886dc538e7b77b`;
trusted base: `4394763d03c1d1302b6b37cef142d0f98f848be4`.
Base-to-head binary patch SHA-256:
`0572673366a1c8f544ba5338279d8210e6fc3c176a5cd147ac105bb0069cec93`.

The targeted historical-copy authority test failed at the exact predecessor-set
assertion: the newly retained merged-base digest
`94f8f22f4dd66234d5048f2dee51c897fa7b9406694bf38ce44fef5186421120`
was missing from the test expectation. The independent triager verified that the
immutable trusted base owns that digest. Keeping it in the workflow implements the
approved consumer-upgrade requirement; removing it would break that requirement.

Command, using the locked Python 3.12.14 environment:

```sh
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_workflows.py -k test_approved_historical_copies_match_authority_and_remain_usable -v
```

Result: exit 1, one test, one failure; 7.270 seconds unittest time. The full suite
was stopped after confirmation (exit 130; 229 test starts, 228 completed OK markers).
That incomplete run is **not a passing full suite**. Candidate validation, four
compiler checks, dependency checks, actual base-owned validation, committed
whitespace and protected-path checks passed on this snapshot. A freshly rendered
actual base-to-candidate consumer upgrade executing the candidate workflow payload
also passed (exit 0, 2.388 seconds). Raw logs remain in ignored local artifacts.

Severity: P2. Authorized repair: explicitly pin the proven planning-baseline digest
in the expected set, with source-commit provenance. Preserve exact set equality,
the independently rendered current-digest check and all earlier accepted digests.
Do not derive expected authority from the candidate workflow or modify fixtures.

Root applied only that test correction. The next immutable snapshot must pass the
direct regression, clean single-commit/autocrlf callers and the full suite before
formal Full reviews. This pre-review repair does not consume a Full review round.
