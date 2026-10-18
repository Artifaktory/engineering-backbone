# OpenCode reconstruction: independent authority/security Full review

Date: 2026-10-16. Reviewer: `bb_reconstruction_full_security`.
Mode: Full, authority/security focus across the complete Backbone delivery.
This session did not author implementation, change the reviewed snapshot, repair
findings, publish, or provide human merge/release approval.

## Snapshot and authority

- Repository: `Artifaktory/engineering-backbone`.
- Trusted base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Reviewed head: `d6a4af73ed39273383457669d498d9e2d4c3f22a`.
- Reviewed tree: `ce15f563e2656831b48e01cf144fa65650033d80`.
- Binary base-to-head patch SHA-256:
  `01334adf41279a614f05ca011c6a9777078fc7f011f7f29d2982204b7fb98523`.
- Immutable checkout: `artifacts/backbone-full-snapshot`, detached and clean.
- Task: `BB-OPENCODE-010`, `plans/opencode-governance-task.json`.

Read trusted-base and candidate `AGENTS.md` and `policy/core.md`, candidate
`CONTRIBUTING.md`, the approved reconstruction plan, Task Packet, independent plan
review and current verification report. The review uses their scoped authority;
historical lost implementation reviews and PASS claims are not current evidence.
The base/head/tree/patch and clean worktree were checked at review entry and close.
This report is written outside the immutable checkout.

## Conclusion

**One confirmed in-scope finding: REC-BB-SEC-001, P2.** The new workflow rejects
the exact immediate predecessor's otherwise approved consumer tooling. Separate
triage must classify it before any repair, followed by the required verification
and Delta review. No additional authority/security defect was confirmed within
the inspected scope. This is not approval of the paired AO implementation or
completion of pending native-platform, publication or qualification gates.

## REC-BB-SEC-001 — retain the immediate predecessor in workflow authority

- Severity: **P2**. Category: downstream compatibility / trusted-tooling admission.
- Confidence: high; reproduced with real Copier consumers and the actual workflow
  shell payload, without native OpenCode or candidate executable evaluation.
- Location: `.github/workflows/governance-checks.yml:79-80`; rejection path at
  lines 138-142. Related coverage gap: `tests/test_workflows.py:273-286`.
- Trigger: a consumer installed from the exact merged base adopts the new pinned
  workflow, with either unchanged approved predecessor tooling or the coherent
  new tooling. The base consumer's toolchain digest is
  `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`.
- Execution path: the diff replaces that digest in `CURRENT_TOOLCHAIN_SHA256`
  with `a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896`
  but does not add it to `PREVIOUS_TOOLCHAIN_SHA256`. The workflow requires the
  trusted base digest to belong to that combined authority list before running
  its compiled guards or predecessor validator. The exact predecessor therefore
  fails admission.
- Impact: ordinary downstream adoption from the immediately preceding reviewed
  Backbone release is blocked. Updating candidate files together with the workflow
  cannot solve it, because the failing input is the already-installed trusted
  base. Earlier historical fixtures passing does not cover this transition.
- Current-diff causation: the old digest was admitted as the base workflow's
  current identity; this diff removes its only entry from the accepted set.
  This is not a request to admit unknown or candidate-chosen toolchains.
- Acceptance relation: plan step 4 preserves reviewed tooling identities and
  predecessor compatibility; AC-4 and AC-7 require real consumer/update and
  predecessor verification without weakening the trusted guard.

### Observed reproduction

Using Python 3.12 and the hash-locked project environment, copied the exact base
and reviewed source into separate temporary non-Git source directories, excluding
Git metadata, environments and ignored artifacts. Ran actual `copier.run_copy`
with defaults, `quiet=True`, and `skip_tasks=True`, producing `trusted-base` and
`candidate`. Computed their digests with the existing eight-file
`bundle_digest`. Parsed the candidate workflow and executed its exact
`Validate generated consumer with trusted tooling` payload through the existing
`run_shell_payload` helper with its actual authority environment.

| Observation | Result |
| --- | --- |
| Exact base rendered digest | `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615` |
| Candidate rendered digest | `a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896` |
| Unmodified workflow payload and authority | Exit **1**, `Trusted base toolchain fingerprint is not approved by this pinned workflow` |
| Diagnostic: same inputs and payload, append only the exact approved base digest to the previous list in memory | Exit **0**, structural contracts validated |

The diagnostic changed only an in-memory environment value in a temporary fixture;
it was not a source repair or a bypass of an access-control approval. No tracked
source, installed consumer or frozen snapshot was changed. The diagnostic narrows
the cause to the missing reviewed identity; it does not certify an eventual fix.

Minimal repair/regression recommendation for triage: retain this exact predecessor
identity alongside the existing historical identities, update the explicit
authority-set expectation, and exercise the actual reusable-workflow payload on
an exact predecessor consumer upgrading to the current coherent tooling. Keep
unknown and mixed toolchains rejected. Existing clean-clone/autocrlf assertions
that reuse the authority-set test must remain intact.

## Coverage and independent checks

Reviewed the complete 78-file base-to-head diff and traced the relevant callers
and consumers. Coverage includes:

- Separate inactive companion and exact schema; native config and five primary
  permission budgets; source/installed instructions; all eight shared procedures;
  optional Copier installation, local-file preservation and legacy absence.
- The complete self-contained `opencode_errors` implementation and its compiled
  workflow copy: duplicate JSON/YAML rejection, exact keys and versions, portable
  paths, symlink/case checks, instruction inheritance, permission ordering and
  no-weaker comparisons, package removal, aliases, recursive SKILL paths and
  alternate reserved-name detection. The compiled Python runs in isolated import
  mode before the approved predecessor validator, with no candidate import.
- Navigation additions and compiled quality/validator/workflow copies: selected
  role/procedure mapping, reviewer plan procedure, whole-file receipt hashes,
  activation seed inheritance and stale/missing context. Existing schema/catalog
  authority and old fingerprint file membership remain distinct from the new
  optional adapter.
- Compiler changes, reusable/native workflows, distribution/navigation/guard/
  smoke tests and the bounded shared validator fixture repair. The fixture repair
  adds source completeness and an explicit missing-AGENTS negative case rather
  than relaxing production validation.
- Native smoke archive verification/extraction, environment isolation, source
  and fixture hashes, bounded commands and local provider, complete per-request
  instruction observation, exact missing-role preflight and tool-call-linked
  refusal. Reviewed docs, plan/evidence statements and their declared limitations.

Executed independently from the frozen checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 <locked-venv>/bin/python -m unittest \
  tests.test_opencode_validation tests.test_opencode_workflow_guard \
  tests.test_opencode_navigation tests.test_opencode_native_smoke -v
```

**44 tests passed, exit 0, 12.743 seconds.** These are data-only guard/receipt and
portable smoke-unit checks; they do not execute adversarial native configurations.
The separate real Copier/workflow reproduction above fails on the exact
predecessor transition despite these passing focused checks.

Rechecked the recorded full-suite log SHA-256
`2ebc088305f1627873beaf9c9f7d0b909ef66e20584a8bc7deb4f62ac10bb82c`
and its final 412-test PASS. Inspected, but did not rerun, the actual benign Linux
native report SHA-256
`94bf9ce0835c3c216ea3522e93f4316b850b92fff4cd46a7506bd8fc2a1d1b30`:
11 commands, 4 provider requests, six passing cases. All 22 source-input hashes
and the smoke-runner hash match this frozen checkout. The denial is linked to
`call_backbone_smoke_write` and records the native unavailable-tool error; the
unchanged target is additional evidence, not the sole criterion.

Primary-source cross-checks used pinned OpenCode commit
`733b2c627e5aec39cb33cc22373bdce33053ef2c`: local configuration, agent/mode and
skill loaders, instruction/run/debug and npm sources. Also fetched the exact
[`agent/agent.ts`](https://github.com/anomalyco/opencode/blob/733b2c627e5aec39cb33cc22373bdce33053ef2c/packages/opencode/src/agent/agent.ts)
blob `536a642fe49fb5211e66c2e2ad689856a03254c0` and
[`permission/index.ts`](https://github.com/anomalyco/opencode/blob/733b2c627e5aec39cb33cc22373bdce33053ef2c/packages/opencode/src/permission/index.ts)
blob `2e27ff2424dbb000ea9ed7f73471769716ba40a1` via GitHub. The role rules append
after defaults/root rules, merging concatenates rule lists and evaluation uses
the last match. Consequently an omitted role key remains denied by that role's
required wildcard rule; the suspected deep-map-inheritance issue is not a finding.
Recursive name-keyed skills and legacy mode loading support the corresponding
static regressions. Native npm bootstrap uses `ignoreScripts: true`; this review
does not allege arbitrary package lifecycle-script execution.

## Unreviewed execution and limits

No native Windows execution, real-model qualification, OS confinement, live AO
admission/lifecycle, compaction/resume/delegation qualification, remote PR CI or
container execution was established by this review. AO implementation is outside
this Backbone snapshot and needs its own review. The smoke's temporary instrumented
fixture and canned provider do not establish host configuration closure or model
instruction compliance. Global/ancestor/bootstrap/environment input closure is
explicitly a controlled-runner responsibility, not an asserted property of these
repository defaults. Unrelated alternate skills remain permitted by the stated
static adapter contract; governed AO uses its separate stricter closure contract.

The previously blocked malicious native dynamic reproduction was not retried.
Historical skill-identity and mode-layer defects were inspected using pinned
source plus static/data-only regressions only. Windows and other pending evidence
remain gaps, not fabricated PASS or independently proven product defects.

Return this immutable review and REC-BB-SEC-001 to separate triage. This session
does not repair source or approve its own diagnostic as a completed fix.
