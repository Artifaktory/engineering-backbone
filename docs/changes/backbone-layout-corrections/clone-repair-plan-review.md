# Independent CI clone-repair plan review

Reviewer session: `corrections_plan_review`. Role: independent read-only plan
reviewer for BB-LAYOUT-012. This reviews the bounded addendum before its
implementation; it does not certify a repaired test, remote CI result or merge.

## Planning snapshot and evidence

- Published baseline: `2ddfa803688c70b556dc83bcf07a4c3911713be5`.
- Baseline tree: `ae42d5f1848b65509e51813b824b7d9c2b61a6cc`.
- Original corrective baseline: `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`.
- [Clone-repair addendum](clone-repair-plan.md) SHA256:
  `d8f3e95d8268a755171d8b589b8fff0bac41f334a247b112af0487fb96f208c2`.
- Original [plan](plan.md) SHA256:
  `88a6a16404ace99048d59a69f5b84212fb641821e753f1776b45750dadd1d6ba`.
- Current [Task Packet](task-packet.json) SHA256:
  `5bdeb1af2d9b4910f6ed25a156541040a86f5502665af68fb8c80e8a7ab9f651`.
- Independent confirmed triage report
  `/tmp/pr18-ci-clone-confirmed-triage.md` SHA256:
  `7c736b514181666ccef118fa5f17cd5c0ce62b89ef098d5e7d5e0ce1851a2248`.

The addendum was uncommitted and its hash was independently verified. The
historical test had no working-tree modification during review. The original
first Full review at `dbe05e14a255488e3416465971ece755fb04aba3` remains historical
evidence; the new repair requires its own frozen second Full snapshot.

## Coverage and observations

Read the root instructions, canonical policy, contributor guide, original plan
and packet, prior Full/triage records, addendum and both clone-failure triage
reports. Inspected the existing historical upgrade test and installed Copier's
Git-source recognition and clone implementation. No implementation or test suite
was executed by this plan reviewer; the disposable tagged probe was performed by
the separate triage session.

- Confirmed triage `COP-CI-02` identifies the same local loose-object copy failure
  in both actual Foundation attempts. The underlying Git/filesystem cause is
  explicitly unproven. The test predates the selector change, and the addendum
  does not falsely attribute that failure to the selector. The repeated failure
  justifies the bounded fixture repair within the user's red-check request;
  another unchanged retry is not part of the plan.
- Installed Copier recognizes `git+file://`, removes the `git+` prefix for Git,
  and passes the resulting URL to clone. Plain `file://` is not equivalent for
  this installed source-discovery logic. The proposed resolved local URI targets
  the same fixture through Git transport, avoiding the observed raw-path local
  copy route without selecting a network service or changing dependency pins.
- The fixture commits and tags both revisions before use. It does not rely on
  dirty-local-HEAD inclusion. Initial copy remains pinned to `v0.1.0`; actual
  update and installation-only negative cases remain pinned to `v0.2.0`.
  Existing local-policy byte preservation, validation and no-rejection checks
  must all remain. This preserves the tested consumer contract.
- The confirmed triage's focused `_src_path` assertion and old/new `_commit`
  assertions fit the addendum's retained contract and provide meaningful
  regression evidence for URL persistence into later updates. The final tag
  assertion already exists. These assertions must inspect actual rendered
  answers; they must not manually construct or overwrite them.
- Triage reports a successful real tagged copy/update probe, but its tiny
  fixture supplied its own answers record. The plan appropriately requires the
  actual historical test, including persisted source binding, and Git trace
  evidence before treating the repair as verified. The probe alone does not
  establish production-fixture persistence or hosted Git 2.55 behavior.
- The affected 41 Copilot tests, structural/compiler/dependency checks and
  committed whitespace checks provide bounded local verification. Independent
  second Full review covers this newly diagnosed repair and direct regressions
  against the published baseline. Existing two-Full/six-iteration limits and
  triage-before-further-repair rules remain explicit.
- Final evidence must bind the repaired commit, tree and patch. Both corrective
  and full-PR committed whitespace checks run after the final evidence commit;
  remote publication is limited to existing draft PR18. A new changed-head
  Foundation result is required before claiming the hosted failure resolved.
  Local Git 2.51.1 and prior-head results cannot substitute for that evidence.
- No runtime authority, workflow gate, native permission, template or dependency
  change is authorized. The separate old trusted-base layout failure and
  BB-LAYOUT-013's human-merge prerequisite remain explicit and unaffected.

## Outcome

**NO CONFIRMED IN-SCOPE PLAN FINDINGS.**

The bounded addendum and confirmed triage are suitable to proceed to the scoped
repair and recorded verification/review chain. This conclusion is limited to the
identified planning snapshot. The reviewer wrote only this report and did not
modify implementation, tests, planning files or the Task Packet. Actual repaired
test behavior, final committed checks and changed-head remote CI remain pending.
