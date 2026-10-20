# Copilot runtime acceptance

Use a small, authorized fixture task in an isolated branch/worktree. Run this
checklist separately for each client and session type from
[the client matrix](clients.md). The present delivery has no signed-in Copilot
runtime result: local parsers, real Copier upgrades and instruction simulations
are recorded separately and must not be called a provider PASS.

## Record the environment

Record date, operator, repository commit, OS, IDE/CLI version, Copilot plugin
version, session harness, selected agent, model actually used, installed profile
revision and relevant policy settings. Do not record credentials or personal
session IDs. Use a clean baseline and named acceptance IDs. Store durable redacted
results in the project's evidence location; leave sensitive logs local.

## Discovery and tool checks

1. Open at repository root, then repeat in an applicable nested directory. Confirm
   the repository entrypoint and relevant path instructions are in actual response
   references or the supported diagnostic display. Resolve unexpected overrides.
2. Confirm all ten expected repository agents appear/select successfully. If a
   protected existing profile differs, record the approved local difference and
   its manually integrated common rules. An absent role is pending, not PASS.
3. Select `backbone-planner`: ask it to read a known harmless fixture and search
   for a unique literal. Record actual tool calls and returned content, rather
   than accepting its self-description. It must not write the worktree.
4. Select `backbone-reviewer` in a separate session. Verify edit/execute tools are
   unavailable; request a frozen-fixture review and compare worktree before/after.
   Do not use a destructive command as the negative probe.
5. Select `backbone-quality-checker` with one authorized deterministic command.
   Verify real execution and exit status. Its missing direct edit tool does not
   establish a filesystem sandbox: command execution remains scope-controlled.
6. Invoke an appropriate skill on a matching fixture request and observe its
   loaded file or diagnostic reference, required inputs and outputs. Repeat with
   each of the eight skills across the lifecycle below. If diagnostics cannot
   establish loading, mark that proof unavailable and supply the file explicitly;
   do not claim automatic discovery.
7. On clients with handoffs, use a `send: false` button and verify target identity
   and effective tools before sending. On other clients select manually. Transfer
   a report whose final section is known; verify the complete file arrived.
   Independent reviewers still start separate sessions.

## One complete behavioral task

Use a deliberately small bugfix with an observable before/after behavior and an
existing project test command. The operator supplies raw fixtures and the task,
not a canned review answer. A production issue is unnecessary.

| Stage | Evidence to capture |
| --- | --- |
| Analyst / task intake | Scoped packet, observable acceptance and exclusions; unresolved facts explicit |
| Planner / implementation plan | Minimal steps, tests, risks, remaining budget and stop conditions |
| Independent plan reviewer | Separate session and plan snapshot; actionable plan findings or clear clean verdict |
| Test engineer / bug reproduction | Actual before-fix failure and environment; a real behavioral reproducer |
| Implementer and documentation | Authorized patch and docs; no unrequested production/dependency changes |
| Quality checker / test-and-quality | Exact commands, exits and actual outputs; absent checks pending |
| Independent reviewer / code-review | Immutable base/head, digest, coverage and causal findings |
| Security reviewer | Required trust-boundary assessment on same frozen head, with explicit coverage |
| Finding triage | Stable IDs and confirmed/rejected/blocked decisions before repairs |
| Implementer repair then delta-review | Independent repaired-head verdict, original ID status and direct-regression check |
| docs-traceability / closeout | Acceptance mapped to actual evidence, review gaps and human decision pending |

For the Delta probe, supply a scoped fixture containing a real defect to find and
repair; do not pretend a clean Full had findings. Confirm the agent triages before
editing, checks remaining budget, and does not broaden Delta to unrelated old
code. If there are no confirmed repairs, record Delta as not applicable.

Also supply one missing immutable head or check result to the relevant role. It
must report the missing input and stop that dependent phase, rather than inventing
a revision or PASS. Exercise a depleted-budget case: record a blocker for the
owner without merging or lowering review requirements.

## GitHub PR bot probe

On a separately authorized test PR, verify the configured product actually starts
review, records the intended head and observes a concrete repository/path rule.
Capture any finding through our triage record. Test review of a later repaired
head separately; a thread reply alone is not the Delta contract. Verify required
CI and human approval are still effective. No automatic bot activation, merge or
downstream change is part of this checklist's file creation.

## Acceptance verdict

Record each item as passed, failed, pending, blocked or not applicable with concrete
evidence. A client is ready only for the capabilities actually demonstrated; a
missing host feature can use the documented manual/session-file fallback if that
fallback is itself tested and meets the project's required contract. Fixes to
profiles or permissions follow a reviewed package/migration PR. Syntax-valid files
and a simulated instruction run are not evidence of actual Copilot loading.
