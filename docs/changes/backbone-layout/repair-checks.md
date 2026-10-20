# Full-review repair checks

Quality-checker session: `layout_quality`, separate from implementation, Full
review and triage. Date: 2026-10-20. This is targeted execution evidence, not Delta
approval, human approval, native runtime qualification or merge readiness.

## Bound repair snapshot

- Prior Full-review head: `54501f1ed542e7f42b5aa315db8863b35e80aeed`.
- Repaired head: `97e68ecefbd21b0d022514f46520a75a6a025536`.
- Repaired tree: `c3ef52a5eaecff857f66ec1599257c2656cc1474`.
- Repair patch SHA256 (`git diff --binary PRIOR_FULL REPAIRED`):
  `19f36e00426e33d9b1e02f82324ad998cf1b9da1e36b4a7faac490e6c3bb6512`.

Read the independent [Full-review triage](review-triage.md). Its confirmed
LBEH-01, LBEH-02 and LBEH-03 cover the moved workflow test invocation, legacy
consumer document path and native smoke's default repository parent depth. The
quality checker changed no source or tests. The repaired working tree was clean
before checks; only this report was subsequently added.

## Actual checks

Commands ran from the repository root in the existing isolated Python 3.12.14
environment. The unittest command below was extracted directly from the checked-in
`Test smoke failure paths` step in `.github/workflows/opencode-native.yml`, then
executed unchanged with the environment's Python on PATH.

| Command | Exit | Result |
| --- | ---: | --- |
| `python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_opencode_native_smoke.py -v` | 0 | **12 tests in 0.685 seconds, OK.** |
| `python .engineering-backbone/src/validate.py` | 0 | Structural PASS; no supplied trusted-base comparison. |
| `actionlint -shellcheck= -pyflakes=` (1.7.12) | 0 | Workflow syntax PASS; optional analyzers unexecuted. |
| `git diff 54501f1ed542e7f42b5aa315db8863b35e80aeed 97e68ecefbd21b0d022514f46520a75a6a025536 --check` | 0 | Repair diff has no whitespace errors. |
| `git diff --check` | 0 | Working diff has no whitespace errors. |

The new regression calls the real CLI argument parsing without `--repo` from a
different working directory and executes the real fixture preparation against the
relocated repository. It verifies root native `opencode.json`, the expected **22**
inputs and canonical policy presence. Download/native execution is replaced by a
bounded fixture-only wrapper; a printed smoke success in this test is therefore
**unit-test output, not an actual native smoke run**. The existing rejection and
protocol checks in the same module also passed.

For LBEH-02, read the repaired legacy-adoption paragraph and independently checked
that its `docs/dependency-compatibility.md` path agrees with the optional legacy
template output and root Copier `_skip_if_exists`. Both corresponding path checks
returned true. No legacy template or preservation rule changed in this repair.

Targeted unittest log SHA256:
`835c3ca302867e4da465bf0aa85efb0d7629677b3be3708fb0cd51619bcd0ed7`.
Individual command-result record SHA256:
`7157e0c674aeec0d099808b1e5b246e4046023fefe961f038aeb7e199cea1942`.
Raw logs remain in ignored run artifacts.

## Evidence boundaries

The previous complete run remains **431 tests passing at**
`ee4f7cee7a386edfb5fb43b2763a03596b8eabf1`, documented in [checks.md](checks.md).
This repair adds one regression, so 432 test methods are now present; **the complete
432-test suite was not run**. Only the affected 12-test module and the checks above
were rerun for these bounded source, command and documentation repairs.

Actual Linux/Windows OpenCode native execution, real-model behavior, OS isolation
and container build/offline smoke remain unexecuted by this repair check. The old
trusted-base validator's disclosed 34 path-related errors remain a separate blocked
merge gate; this targeted PASS does not replace or waive that result. Independent
Delta review and human decisions remain separate.
