# BB-LAYOUT-012: COP-CI-02 implementation evidence

Implementer: `layout_tests`. Published baseline:
`2ddfa803688c70b556dc83bcf07a4c3911713be5`.
The [approved addendum](clone-repair-plan.md) and
[independent plan review](clone-repair-plan-review.md) authorize this bounded repair.

Only the historical-upgrade method in
`.engineering-backbone/tst/test_copilot_distribution.py` changed. Its initial
real Copier copy now receives `"git+" + source.resolve().as_uri()`. Assertions
read the actual rendered answers and require that source URL at both versions,
initial tag `v0.1.0`, and the existing final tag `v0.2.0`. No answers file is
manually changed. All 15 original assertion call ASTs and both original real
`run_update` call sites remain unchanged; three source/tag assertions were added.

Author verification on local Git **2.51.1**:

```sh
PYTHONPATH=.engineering-backbone GIT_TRACE=/tmp/pr18-clone-repair-git-trace.log /workspace/scratch/6e019b0851cc/backbone-venv/bin/python -m unittest tst.test_copilot_distribution.CopilotDistributionTests.test_historical_upgrade_adds_package_without_replacing_local_authority -v
```

Result: **1 test passed in 8.192 seconds, exit 0**, including both existing
installation-only rejection subtests, actual upgrade, local-authority preservation
and trusted validation. The Git trace contains 14 clone commands; all use
`file:///tmp/copilot-distribution-.../upgrade-source`, followed by
`git-upload-pack`. Scoped `git diff --check` passed.

Evidence SHA256:

- Changed test file: `2dc0490bf69ed5986d6379e856543958eb9904f12cafbeacf3f5d224a44c2ce1`.
- `/tmp/pr18-clone-repair-test.log`: `b5b4c8d7c55986356ccd473f5a771f9a98d4e599a6459abc2997558d05ae7005`.
- `/tmp/pr18-clone-repair-git-trace.log`: `ceda06a3fded4a0c0662daca05bd88d8664e3af59256908bcb4d9f6782b69fc8`.

This is author verification of the actual fixture and selected transport. It
does not reproduce Git 2.55 or prove the repeated hosted failure is resolved.
Independent affected-suite checks, frozen review and changed-head Foundation
evidence remain pending. No commit or remote retry was performed by this agent.
