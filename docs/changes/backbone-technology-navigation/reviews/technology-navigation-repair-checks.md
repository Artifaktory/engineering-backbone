# Independent repaired-snapshot deterministic quality gate

Task: `BB-TECH-NAV-008` · Checker: `/root/technology_quality_gate` · 2026-10-14.

## Verdict and exact snapshot

**PASS for the bounded repaired-snapshot deterministic gate.** All nine requested
command groups completed with actual exit 0, including 83 targeted tests. This is
quality-check evidence for the confirmed repairs, not independent Delta approval,
semantic certification, publication permission or a replacement for human merge
and release gates. The checker made no tracked edits or GitHub writes.

- Upstream base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Prior independently Full-reviewed head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`
- Repaired head: `4722d46e220ee34fb649c787d19f75f77447ca0b`
- Repaired tree: `ea5e2b47728d3fea7ba4a217e3ce4ac3a16fc48b`
- SHA-256 of full `git diff --full-index --binary BASE HEAD`:
  `0a576467bdcd34bc9638ef3dfbe16d665297921c627006f12b014ec80775582c`
- SHA-256 of `git diff --full-index --binary PRIOR_REVIEWED_HEAD HEAD`:
  `0081f46e538998bcafaa10ba790d63b1bab68a3cce792d6acdc3e3eb74b404f5`
- Frozen `scripts/quality_framework.py` SHA-256:
  `32d818cbe4acab3c94de68aa89f27c587be355689fcab6870105544d0107ffd3`
- Actual rendered tooling fingerprint confirmed by the compiler:
  `a64a6c70e9ac9949322ca46a67401d45b9a1486c8f056b80447de5f277e4c9d1`

The checker independently matched head/tree/full/delta identities before executing
checks and again afterward. The tracked worktree remained clean. The repair delta
contains canonical resolver/guide/tests, generated guards/workflow and earlier
review evidence. The original catalog, dependency and historical-fixture authority
remains unchanged: all 70 protected entries retain identical Git blob IDs, modes
and paths versus the upstream base.

## Commands and actual results

Each command ran independently from the repository root after FROZEN READY.
The process harness streamed output into an ignored log and wrote `.exit` and
`.json` sidecars only after the subprocess completed. JSON records contain exact
argv, actual return code, elapsed wall time, frozen head and output SHA-256.
`PIP_DISABLE_PIP_VERSION_CHECK=1` was set; required installation/hash checks were
retained. No complete-suite run was repeated.

| Command | Exit | Wrapper wall time (seconds) |
| --- | ---: | ---: |
| `.venv/bin/python scripts/validate.py` | 0 | 1.834 |
| `.venv/bin/python artifacts/trusted-base/scripts/validate.py --root . --trusted-base artifacts/trusted-base` | 0 | 1.509 |
| `.venv/bin/python scripts/compile_navigation.py --check` | 0 | 0.12 |
| `.venv/bin/python scripts/compile_quality_framework.py --check` | 0 | 0.282 |
| `.venv/bin/python scripts/compile_workflow_kit.py --check` | 0 | 0.125 |
| `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | 0 | 2.575 |
| `artifacts/tools/actionlint -shellcheck= -pyflakes= .github/workflows/governance-checks.yml .github/workflows/quality.yml .github/workflows/workflow-kit-maintenance.yml .github/workflows/workflow-kit-pr.yml` | 0 | 0.128 |
| `git diff --check edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12 4722d46e220ee34fb649c787d19f75f77447ca0b` | 0 | 0.05 |
| `.venv/bin/python -m unittest tests.test_navigation tests.test_navigation_integration tests.test_technology_catalog tests.test_quality_framework tests.test_quality_workflows tests.test_workflows.WorkflowTests.test_real_copier_upgrade_accepts_coherent_tooling_and_preserves_local_facts tests.test_workflows.WorkflowTests.test_real_copier_upgrade_without_local_object_copy -v` | 0 | 112.371 |

Current validation explicitly reports that its no-base invocation does not perform
history comparison; the separately executed exact predecessor command supplied
`--trusted-base` and passed. Actionlint is version 1.7.12; its external ShellCheck
and Pyflakes integrations were disabled explicitly. Its expanded argv covered all
four current source workflow YAML files. Compiler checks prove generated-byte
agreement and the actual rendered fingerprint, not semantic correctness.

The targeted unittest run reports **83 tests in 110.900s, OK; actual exit 0**.
Its wrapper duration was 112.371s. The checker verified the final summary, actual
exit sidecar and log digest. No failures, errors or skip summary were present.

Targeted scope:

- `tests.test_navigation`: 28 tests.
- `tests.test_navigation_integration`: 7 tests.
- `tests.test_technology_catalog`: 8 tests.
- `tests.test_quality_framework`: 31 tests.
- `tests.test_quality_workflows`: 7 tests.
- Two actual Copier upgrade tests from `tests.test_workflows.WorkflowTests`:
  `test_real_copier_upgrade_accepts_coherent_tooling_and_preserves_local_facts`
  and `test_real_copier_upgrade_without_local_object_copy`.

## Confirmed repair coverage

The separate triage confirmed `TNAV-B-1` / `TNAV-S-1` as one mandatory-context
omission and `TNAV-S-2` as effective-check authority mismatch. This checker read
that triage and inspected the exact regression-test delta before assessing results.

The passing checks cover mandatory consumer project/core JSON inclusion without
manual document mapping; exact byte hashes; unchanged verification; valid fact
mutation and deletion rejection; and the source `policy/core.json` counterpart
without inventing a consumer project file for source mode. Existing legacy absence,
inactive seeds, stronger consumer files and Copier update preservation remain
covered in the executed modules and two real upgrade checks.

The checks also cover candidate relabeling of approved docs checks as migration,
candidate PR-phase additions to approved non-PR definitions, preservation of all
approved definition fields despite candidate kind/phase/command/cwd/timeout edits,
normal active-base and enabled-only activation paths, and genuinely new check IDs.
Installed CLI receipts are compared against actual `workflow-kit.py prepare`
output without executing application check commands. Candidate configuration edits
still invalidate receipts even when approved effective execution stays unchanged.

The prior whole-suite result, **314 tests in 1063.568s, exit 0**, belongs only to
`6e5758deb7767c2915505b9646f1a09e0cc0b174`. It is retained unchanged as prior evidence,
not relabeled as a complete repaired-head run. The agreed bounded gate executes the
affected authority, compiler, consumer, activation and upgrade coverage above.
The earlier QG-001 / TQ-1 source-fixture correction remains covered by all 31 quality
framework tests; its production guard was never weakened.

## Refreshed structural smoke evidence

The checker independently inspected `artifacts/navigation-repair-smoke/structural-result.json`,
the candidate receipt, prepared workflow and actual fixture files. All **28/28**
receipt document hashes match current bytes; both mandatory
`.engineering-backbone/project.json` and `.engineering-backbone/core.json` appear.
All four selected receipt check definitions equal the complete corresponding
prepared workflow definitions. The smoke guard bytes match the frozen guard SHA
above. The recorded resolve, verify and prepare operations exited 0; verification
of an unchanged receipt after project-fact tampering exited 1.

Fresh context digest:
`fe2403ff298a4bdcda3030e361f34ea5411c53f6504461de10fe7bc3948bdedf`.
Receipt file SHA-256:
`953a045bca8b4a18165fa2192938b053ed01523c08679e1bd3ffcce6c0413f11`.

The completed fresh receiver report and result JSON were subsequently inspected.
They record a fresh `fork_turns=none` receiver reading all 28 selected documents
(129,240 bytes), independently matching 28/28 hashes, reporting the actual project
branch and validation command, all seven core invariants and the four approved
check definitions. Its positive verification exited 0; project-fact tampering was
independently rejected with exit 1 and the receiver stopped. The receiver retained
permitted implementation choices in its grounded hypothetical review decision.

The checker's independently established scope is the file hashes, mandatory path
presence, guard identity and all-four receipt/prepared-definition equality described
above; the agent-reading/decision observations are attributed to the separate fresh
receiver evidence, not authenticated cognition or native discovery. This is an
isolated structural/explicit-context fixture; its declared revision is not
authenticated Git identity. Application checks were not executed. The preservation
record reports all 150 previous-smoke files unchanged; earlier evidence remains
attributable to its original snapshot.

Native instruction discovery remains unverified. The earlier native Codex attempt
produced no model events and timed out; nested discovery and Copilot discovery were
not executed. The repair smoke does not replace or upgrade those native results.

## Remaining gates

Independent Delta reviewers must assess both confirmed repairs and directly caused
regressions on this exact head/delta. This deterministic PASS is not their verdict.
PR identity, remote CI and requested Codex review remain separate publication
steps. No merge, release, deployment or downstream adoption is authorized here.

## Raw evidence hashes

The following files are under `artifacts/technology-navigation/`. Each corresponding
`.exit` contains the actual numeric return code followed by a newline; each `.json`
contains the recorded exact command and run metadata.

| Log | SHA-256 |
| --- | --- |
| `repair-validator.log` | `07604dad0ce23e9a3291888da5b1f5fb1e48d63eee763a517af23015c68eb6af` |
| `repair-predecessor.log` | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| `repair-navigation-compiler.log` | `f5acf715a03db96a191bdf0d036c4cfc8708079fafa3e08f149ee51564b2fbf2` |
| `repair-quality-compiler.log` | `649ebe6bdb8a344d0a7dec260dd3e57744a59dfc34f6d35c64ad36271a92d6b5` |
| `repair-workflow-compiler.log` | `eb9708a2e83615ae1bec5707088a89f48ffbd2b83a3c0623dca3b8a138175cd4` |
| `repair-fingerprint.log` | `a7898ee5be254fdbdf3fecf572078f2efaca44d5fbb113a8f6496bdc81a34969` |
| `repair-actionlint.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `repair-diff.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `repair-targeted-tests.log` | `ab69ae4a8330e891bdd081126551f0d62d99f69a4a4e28236471ad6e244a075c` |

Additional smoke and triage evidence, relative to the repository root:

| File | SHA-256 |
| --- | --- |
| `artifacts/technology-navigation/full-review-triage.md` | `b8f0e358ac6ae0f2630bc5499061ab751a424a5ee72dbb89246042ee2e073ce7` |
| `artifacts/navigation-repair-smoke/structural-result.json` | `586d29fda8e25a31642ef6068099c054c498be54dd1831a607ddcf170a83d390` |
| `artifacts/navigation-repair-smoke/context.json` | `953a045bca8b4a18165fa2192938b053ed01523c08679e1bd3ffcce6c0413f11` |
| `artifacts/navigation-repair-smoke/prepared-workflow.json` | `12e89d398d09bfe11daa6d94ea172a421f8c81c26b9bcbf57254608da0147968` |
| `artifacts/navigation-repair-smoke/previous-smoke-preservation.json` | `e519fc11e1a9f28746f621ee2719df23bf6e4e675f744846eb6bc7a64ab7a808` |
| `artifacts/navigation-repair-smoke/report.md` | `fa7917f8525bd50f5d0f2ae84c3f711b896e1729e5bfcad7194864392bf2b3e8` |
| `artifacts/navigation-repair-smoke/explicit-context-result.json` | `6114d252fefdc578374783c1283b76ced5a067aae67f4f6b970e4d82b1380ef3` |
