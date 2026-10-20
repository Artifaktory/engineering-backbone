# PR 18 Foundation local-clone error triage

Date: 2026-10-20. Independent triage session: `correction_triage`.
Scope: the single Foundation error on corrected PR 18 head
`2ddfa803688c70b556dc83bcf07a4c3911713be5`, tree
`ae42d5f1848b65509e51813b824b7d9c2b61a6cc`.
Workflow run: `39422351687`; failed job: `118626214062`.
This is a scratch diagnostic report, not a source change or merge approval.

## Actual failure and inspected path

Read the supplied complete error traceback in `/tmp/pr18-foundation-error.log`.
The run executed 433 tests in 516.322 seconds and ended `FAILED (errors=1)`.
The sole error is the `copilot_python_profile` subtest of
`test_historical_upgrade_adds_package_without_replacing_local_authority`.
At test line 341, Copier's `run_update` clones its reviewed old template while
loading configuration, before the expected installation-only contract rejection:

```text
/usr/bin/git clone --no-checkout /tmp/copilot-distribution-i57de58z/upgrade-source /tmp/copier._vcs.clone.ats_22nf --filter=blob:none
fatal: failed to copy file to '/tmp/copier._vcs.clone.ats_22nf/.git/objects/33/6e5ddae79ad00fc8794277035d0deb5a023914': No such file or directory
```

Git exits 128; Plumbum propagates `ProcessExecutionError`. This is an external
local Git object-copy failure, not an assertion failure or a reported violation
of the optional-profile, local-authority or native-discovery contracts. The
preceding warning explicitly says filtering is ignored for this local clone.
The remote log reports Git 2.55.0 and Python 3.12.15.

Read the frozen test's fixture creation, update and cleanup paths and the complete
corrective test diff. The fixture's source and target use a per-test temporary
directory; the historical source commits/tags are complete before the update.
There is no newly introduced source modification or cleanup overlapping this
clone in the inspected code. The failing test method's AST is byte-for-byte
equivalent, excluding source positions, to corrective baseline `c501087...`.
The Copier entrypoint, legacy templates, historical fixtures and dependency lock
are unchanged between that baseline and the corrected head. The new selector
regression is a separate method and changes no Git lifecycle operation.

## Bounded diagnostic execution

Independently verified frozen head/tree and clean worktree, then ran exactly the
failing existing method once at that head:

```text
PYTHONPATH=.engineering-backbone /workspace/scratch/6e019b0851cc/backbone-venv/bin/python -m unittest tst.test_copilot_distribution.CopilotDistributionTests.test_historical_upgrade_adds_package_without_replacing_local_authority -v
```

Result: **exit 0; 1 test in 6.592 seconds; OK**, including both optional-profile
subtests and the actual historical upgrade checks. Local Git is **2.51.1**;
the existing isolated Python environment is 3.12.14. This does not reproduce the
remote Git/Python environment and is not a remote Foundation PASS.

## Disposition

**No confirmed diff-caused defect. Suspected transient local-clone execution
failure; exact filesystem/maintenance cause remains unproven.** The error alone
does not prove a particular race, Git defect or missing fixture source blob.
The inspected unchanged execution path, precise external copy error and successful
same-head isolated execution support one bounded diagnostic rerun of the failed
Foundation job on the unchanged commit and workflow, using a fresh runner/temp
filesystem. That environmental reset is the stated changed input; this is not
permission to retry repeatedly until green.

No source patch, relaxed assertion, skipped test, retry loop inside the test,
changed dependency pin or waived gate is justified by the current evidence.
Record the original failure and the single rerun's actual conclusion separately.
If the same clone error recurs, stop retries and investigate the actual Git/temp
filesystem lifecycle with preserved diagnostics. Any different failure receives
its own triage before repair.

The old trusted-base layout failure is independent and unchanged. Rerunning
Foundation cannot resolve or waive that merge gate. No remote rerun, repository
edit, merge or setting change was performed by this triage session.
