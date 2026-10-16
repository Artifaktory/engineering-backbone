# OpenCode activation repair author record

Date: 2026-10-16. Responsibility: implementer for separately confirmed
`REC-BB-REMOTE-001` only. This record is not independent quality verification,
Delta review, runtime qualification or human approval.

## Authority and change

Read `AGENTS.md`, `CONTRIBUTING.md`, `policy/core.md`, Task `BB-OPENCODE-010`,
its approved plan, the OpenCode workflow/runner contracts and the completed
remote-finding triage section before editing. The triage report at handoff had
SHA-256 `e58683ca35771be2e02539d44007527ea7806730181befe3184372d2cca0255a`.
The remote-reviewed head was `f22ef07ef018f41f487450465b757b658da6b396`,
tree-equivalent to local `a821da64c3468ebafe0e8586fc669b062b408907`
(`ee1db8863633bc54765b32aa15e0a03a0452f57b`).

The inactive-to-active branch now derives the complete package path union across
all five roles independently for the reviewed seed and candidate. Membership must
match; every input except the companion must retain identical raw bytes through
the existing bounded safe reader. The companion retains its separate exact parsed
comparison allowing only `enabled` to change. The gate applies only to activation.
Inactive seed preparation, already-active updates, unrelated repository edits and
the existing legacy-absence behavior retain their prior contracts.

The source change is thirteen lines in `scripts/navigation.py`. The documented
navigation, quality and toolchain compilers regenerated its three trusted copies.
No generated guard was edited manually. Required native instructions, configuration,
role files, skills, native smoke runner and historical fixtures were not changed.
The existing operating documentation already states the restored flag-only rule,
so no user contract change was needed.

The compiler changed the current rendered-tooling fingerprint from
`a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896` to
`35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`.
The explicitly reviewed former current identity was retained in the workflow's
previous list, alongside all existing identities including merged predecessor
`dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`.
The exact authority-set assertion was updated without weakening membership or
mixed/unknown-tooling rejection.

Fresh rendering independently re-established the retained `a3cde1...` digest from
the clean frozen prior Delta checkout `c2c31eed661714c0d8bc2245ff8505ac01a60c9a`,
tree `15bf96a0d003cc6b9d20dc1482d250b35dbbb44b`. A Git comparison confirms that
its only differences from `a821da6...` are review records and Task acceptance
metadata; tooling/template inputs are unchanged. This is the reviewed pre-repair
PR identity, not a claim that the PR has merged.

The seven product/test files are `scripts/navigation.py`,
`scripts/quality_framework.py`, `scripts/validate.py`,
`.github/workflows/governance-checks.yml`, `tests/test_opencode_navigation.py`,
`tests/test_opencode_workflow_guard.py` and `tests/test_workflows.py`.
Their binary diff against `a821da6...` has SHA-256
`b6c4c2bf4a998439e165a7cf967ab2027442ed865f84b4ac33f7395f1f469b52`
(189 insertions, 6 deletions). This record is added separately from that source
patch. The orchestration owner committed the repaired source as
`4a0a4310dc54aba062654ab889ac16f8ac42558c`, tree
`4f573d91ff80039f789866f776d6d4f44bbec1e6`. Including the separately committed
remote-triage record, the prior-reviewed-to-repair binary patch SHA-256 is
`d0822498a021c948f3dfee1a42475b1940d003419a1576f8f048eef3ffdf64d1`;
base `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a` to repair is
`b1e4eeb7b0477b40c4ccad6456103237a7f8826cfb9b075a75bfe819c1f34a16`.

## Executed author checks

All commands ran from the repository using its locked Python 3.12 virtual
environment. Tests use bounded data-only fixtures and the actual trusted workflow
shell payload; no native OpenCode or adversarial native configuration was run.

Before the source repair, this command exited **1**, with four tests in
**5.376 seconds** and **27 expected failing subcases**:

```sh
.venv/bin/python -m unittest \
  tests.test_opencode_navigation.OpenCodeNavigationTests.test_opencode_activation_binds_every_reviewed_package_input \
  tests.test_opencode_navigation.OpenCodeNavigationTests.test_opencode_activation_rejects_added_or_removed_instruction_paths \
  tests.test_opencode_navigation.OpenCodeNavigationTests.test_opencode_seed_preparation_active_updates_and_unrelated_activation_edits_remain_valid \
  tests.test_opencode_workflow_guard.OpenCodeActivationWorkflowTests.test_compiled_workflow_binds_activation_before_approved_old_validator -v
```

The pre-fix resolver wrongly accepted mutations to all 23 covered package inputs,
including every role, every canonical skill, explicit instructions, native config
and runner/guide inputs; it also accepted added/removed instruction references.
The real compiled workflow wrongly accepted the changed implementer role and
nonselected finding-triage skill. The approved older validator passes those two
cases, establishing why the new trusted compiled check is necessary. The positive
non-activation/unrelated-edit control passed before the repair.

Generation commands each exited **0**:

```sh
.venv/bin/python scripts/compile_navigation.py --write
.venv/bin/python scripts/compile_quality_framework.py --write
.venv/bin/python scripts/compile_toolchain_fingerprint.py --write
```

After the repair, both affected OpenCode suites passed: **18 tests in 17.192
seconds**, exit **0**, without skips or exclusions:

```sh
.venv/bin/python -m unittest tests.test_opencode_navigation tests.test_opencode_workflow_guard -v
```

The new regressions now reject all changed input/path cases before returning an
activation receipt, including roles/procedures outside the implementer request.
An unchanged seed plus flag still passes. Inactive edits, active updates and an
unrelated application edit during activation pass. The actual compiled workflow
rejects both changed-instruction cases before the older validator can report its
structural PASS.

The focused authority/upgrade checks passed: **3 tests in 6.965 seconds**, exit
**0**, without skips or exclusions:

```sh
.venv/bin/python -m unittest \
  tests.test_workflows.WorkflowTests.test_approved_historical_copies_match_authority_and_remain_usable \
  tests.test_workflows.WorkflowTests.test_immediate_predecessor_unchanged_and_coherent_current_tooling_pass \
  tests.test_workflows.WorkflowTests.test_immediate_predecessor_unknown_and_mixed_tooling_stay_rejected -v
```

These retain exact historical authority and exercise approved predecessor tooling,
coherent current-tooling upgrades, unknown candidate/base rejection and mixed
approved-tooling rejection. `git diff --check` also exited **0**.

| Local raw evidence in `artifacts/` | SHA-256 |
| --- | --- |
| `opencode-remote-activation-before.log` | `8bd37e71b95b27fd8e096f484b73562bc95ee384762cf1427d4ba59eeb9f77a8` |
| `opencode-remote-activation-after.log` | `49bbf4ad7b508f971e171ecaec18c28a1e5546a676cf3d2a845c2f7e7f3c584d` |
| `opencode-remote-activation-authority.log` | `b971c25fdcfc000434b704fc65119a65181c0ece529083673ceda00bdc554194` |
| `opencode-remote-activation-authority-provenance.json` | `3f50577789a065df6b11a7e78604879fe928cda5f8839116496739aff0b930b0` |

## Required handoff

Product/test source is frozen after these checks. A separate quality session must
run the complete suite, current and exact predecessor validators, all four compiler
checks, source-dependency check, Actionlint and whitespace check on the committed
repair. Then independent Delta reviews `REC-BB-REMOTE-001` against the recorded
remote-reviewed head or its explicit local tree equivalent, including complete
seed binding, companion exception, generated parity and direct update/fingerprint
regressions. This author record does not close the finding or substitute for those
gates. The earlier fingerprint finding stays closed; this repair preserves it.

Actual refreshed PR CI and remote review remain publication-phase work. Native
inputs are unchanged; earlier native evidence remains limited to its recorded
platforms and observations. No runtime/model qualification, activation, merge,
release, deployment, settings change or downstream adoption is authorized here.
