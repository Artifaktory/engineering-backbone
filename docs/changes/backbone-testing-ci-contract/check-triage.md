# Pre-Full deterministic check triage

## TEST-CHECK-01 — confirmed test-only expectation defect

Executor/author: `testing_distribution_tests`. Independent read-only triager:
`testing_check_triage`. Actual trusted base:
`1a740604d4a6a68e500da36c4d99935d04a8ce86`; plan head
`519db0c68e235356fef015f3a05c139f4339afec`.
Root preserved the initial integrated implementation in
`6037d92570d1a22e7c297b9240b295537d5da0b1` before repair. Its base-to-head binary
patch SHA-256 is `539ca884be78ee1618af95e2542559620d6690df638c47901f2167988bc095b9`.
The triager inspected the pre-freeze test bytes, SHA-256
`5a595a03fa69c3592c1e84ab10801731817f352b62613fde1ae30df06d9c2d84`,
which root verified are identical in that preserved commit.

Command, using the existing isolated locked Python 3.12 environment:

```sh
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_testing_documents.py -v
```

Observed first result: 5 tests, 4 passes, 1 failure, exit 1, 23.600 seconds unittest
time; wrapper duration unavailable. Raw output was retained from the existing tool
chunks without rerunning unchanged input in ignored
`artifacts/testing-distribution/initial-targeted.log` and its result metadata.

The new negative test submitted kind `test` in unsupported phase `release`.
The unchanged guard correctly rejected it with
`workflow kit: FAIL: Check kind does not support selected phases`. This diagnostic
path does not include `workflows.json`, but the new test additionally expected that
filename at line 248. The test therefore failed despite the intended rejection.

Classification: **CONFIRMED, P2, test-only expectation defect**. The triager
independently inspected diagnostic construction and verified validator, workflow
runner and workflow schema remain unchanged from the trusted base. No runtime or
schema repair is justified. The initial execution belongs to the test author;
the triager did not claim a second runtime reproduction.

Authorized minimal repair: replace only the filename assertion with assertions for
`workflow kit:` and the exact phase-rejection message. Preserve nonzero exit,
unsupported-phase input and the restored valid-`pr` success check. Recheck the
affected case and five-test distribution suite, then qualify the repaired frozen
implementation with the required independent full suite. This pre-Full correction
does not consume a Full review round or weaken any product gate.

## TEST-CHECK-02 — confirmed incomplete historical-consumer test fixture

Checker: `testing_quality`. Independent read-only triager: `testing_check_triage`.
Failed frozen head: `47cec1a72dbed195cbeb3534f83a80696061e2ff`, against the same actual
base above. Binary patch SHA-256:
`afbb4864ff6bc96d8b09d9e8788ac889743b2ae5ab7357c7bba904745e6b9c36`.

All quick gates passed on that head. The full suite was stopped after confirmed
failures (observed exit 130; 372 test-start markers, 367 OK markers and five FAIL
markers). It is incomplete, not passed; wrapper duration is unavailable. A bounded
diagnostic of `test_valid_inactive_package_passes_without_executing_candidate_guard`
failed with exit 1, one test, 3.401 seconds unittest time / 3.874 seconds wrapper.
The checker retained both logs/results under ignored `artifacts/testing-quality/`.

`QualityWorkflowTests.setUp()` selectively copies current optional quality documents
into a historical pre-attestation consumer. Those documents now link shared context
that its copy list omitted. Six broken-link errors prevented the intended
quality-authority checks from being reached. Normal current rendering includes
these documents; no production distribution defect was demonstrated.

Classification: **CONFIRMED, P2, incomplete test fixture**. The authorized repair
adds only the missing 33-file managed context closure: seven guide/source files
(`architecture.md`, `architecture-sources.md`, `planning.md`, `planning-sources.md`,
`testing.md`, `testing-sources.md`, `ci-cd.md`); architecture/planning/testing template
directories (8/7/8 files); and the three existing pending JSON examples. Keep all
eight attested tooling files and historical `core.md` byte-identical, with an
explicit core-preservation assertion alongside the existing tooling assertions.
Keep poisoned candidate-guard and marker checks, old-validator acceptance and the
actual workflow rejection assertions. Do not change schemas, archives, runtime
guards or workflow payloads.

Independent TEMP-only triage verification added exactly that context without
tracked edits: the actual old validator and current workflow payload both passed,
the candidate-guard marker stayed absent and tooling/core bytes were unchanged
(4.682 seconds investigation). All four historical quality workflow methods then
passed with temporary fixture augmentation, exit 0, 6.360 seconds. This is triage
evidence, not qualification of a later repaired tracked snapshot.

Root applied this authorized document-copy/assertion correction within the accepted
test scope. The repaired historical workflow cases, distribution tests and required
full suite must qualify the next immutable snapshot. This does not adopt a new
historical core, weaken enforcement or consume a Full round.

Tracked repair integration check: all seven tests in `test_quality_workflows.py`
passed, exit 0, 7.181 seconds unittest time, using the locked interpreter. Its log
is retained as `artifacts/testing-distribution/historical-quality-repair.log`.
This author-side regression result remains distinct from independent qualification.
