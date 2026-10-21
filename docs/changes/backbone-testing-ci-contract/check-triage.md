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
