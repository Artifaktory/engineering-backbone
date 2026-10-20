# OpenCode remote finding: independent authority/security Delta

Date: 2026-10-16. Reviewer: `bb_reconstruction_full_security`.
Mode: **Delta**, limited to separately confirmed `REC-BB-REMOTE-001` and direct
regressions from its repair. This session did not author the repair, its triage
or its independent quality evidence. The earlier closed predecessor findings
are not reopened as unchanged Full-review scope.

## Immutable binding and authority

- Repository: `Artifaktory/engineering-backbone`; Task `BB-OPENCODE-010`.
- Base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Prior remote-reviewed head: `f22ef07ef018f41f487450465b757b658da6b396`.
- Equivalent prior local head: `a821da64c3468ebafe0e8586fc669b062b408907`.
- Both prior commits have tree `ee1db8863633bc54765b32aa15e0a03a0452f57b`.
- Repaired Delta head: `4e4c1f6456bbd349818e5faf8969b938e617ed50`.
- Repaired tree: `dad7809e8ad92d808d1541144406db8ed9d95014`.
- Prior-local-to-repair binary patch SHA-256:
  `3be75432158141d2d3384db2b1096c858ab32d7a41ce747946fecb79b9ed175f`.
- Base-to-repair binary patch SHA-256:
  `d3a3ff4fce3ca105e0a86ab2ddb89b0fe6d0246ce1cf0b239af2a3b8fb6fb47f`.

Read the remote-finding triage, initial remote-check report, repair author record
and independent repair-check record against the previously inspected repository
policy, Task Packet, approved plan and OpenCode contract. Verified both prior
commit trees, repaired head/tree, both patch hashes and clean worktree. Review
used the detached `artifacts/backbone-remote-delta-snapshot`; its binding and
clean state were checked again at close. This report is written outside it.

The quality-tested commit `4a0a4310dc54aba062654ab889ac16f8ac42558c`, tree
`4f573d91ff80039f789866f776d6d4f44bbec1e6`, differs from the reviewed repair only
by the added author and independent quality reports. No product/test change
intervened. The quality report hash matches the supplied
`6442dff53e9f680875467e05e1f8b58dd1982399cbae06a3c6a86ce25445f20f`.

## Finding disposition

**REC-BB-REMOTE-001, triaged P1: repaired and independently verified.**

**NO CONFIRMED IN-SCOPE FINDINGS** in this bounded repair or its directly affected
paths. The incomplete seed-binding trigger is closed at the reviewed snapshot.
Return this result to separate closure triage before updating the PR. This is
neither human approval nor evidence of refreshed remote CI/review completion.

The previous `REC-BB-SEC-001` / duplicate `REC-BB-FUNC-001` remain closed. Their
directly relevant authority-retention and rejection behavior remains intact.

## Semantic repair assessment

Reviewed all seven changed product/test files: navigation source, its compiled
quality/validator/workflow copies, the two OpenCode regression modules and the
workflow authority tests. The other diff changes are evidence/triage records.
The implementation restores the existing activation contract without a new
runtime permission, qualification mechanism or source of authority.

The new gate is inside the existing trusted-base inactive-to-active OpenCode
branch. It independently constructs the seed and candidate input sets using
`opencode_paths` for **all five roles**, rather than the current request's role.
This includes all five primary documents, all eight canonical procedures, root
native configuration, explicit local instructions, operating guide and runner
contract. Both sets must match. The existing safe, bounded `read` function then
compares raw bytes for every member except the companion.

The companion remains subject to exact parsed equality after substituting only
`enabled=True` in the seed. Excluding that one path from raw equality permits
its intended flag change, while the fixed field/key/version validation remains
in effect. A parse-equivalent change to any other input still fails raw equality.
Changes to instruction references fail set equality; even references that happen
to name an already-present input cannot evade the separate native-config byte
comparison. Candidate receipt recomputation occurs only after this gate, so new
candidate hashes cannot substitute for equality with the reviewed seed.

Existing completeness/path validation occurs before the comparison. No candidate
code is evaluated. The condition does not run for inactive seed preparation or
already-active updates. Unrelated repository files are not pulled into the new
comparison. Existing legacy absence and inherited restrictions are preserved.
Ordinary support resources outside the existing `opencode_paths` contract and
AO's broader runtime-input closure are not newly added requirements in this Delta.

The actual compiled workflow regression demonstrates why the trusted copy matters:
an approved older validator alone accepts harmless changed role/skill bytes, while
the candidate workflow rejects those same activation inputs before that validator
can produce structural PASS. The test includes a procedure not selected by its
current implementer task.

## Independent execution and parity

Using Python 3.12 and the hash-locked `engineering-backbone/.venv/bin/python`,
executed from the immutable snapshot:

```sh
PYTHONDONTWRITEBYTECODE=1 <locked-venv>/bin/python -m unittest \
  tests.test_opencode_navigation tests.test_opencode_workflow_guard \
  tests.test_workflows.WorkflowTests.test_approved_historical_copies_match_authority_and_remain_usable \
  tests.test_workflows.WorkflowTests.test_immediate_predecessor_unchanged_and_coherent_current_tooling_pass \
  tests.test_workflows.WorkflowTests.test_immediate_predecessor_unknown_and_mixed_tooling_stay_rejected -v
```

**PASS: 21 tests in 21.697 seconds, exit 0.** No exclusions or added skips.
Coverage includes all 23 tested native/package input mutations, unselected roles
and procedures, added/removed instruction paths, successful flag-only activation,
inactive preparation, already-active updates, unrelated activation edits, existing
legacy/guard cases and the actual compiled workflow with approved old tooling.
Unknown candidate/base and mixed-toolchain negatives remain rejected; the exact
historical authority-set assertion remains enforced.

Also independently ran these checks, each exit 0:

```sh
PYTHONDONTWRITEBYTECODE=1 <locked-venv>/bin/python scripts/compile_navigation.py --check
PYTHONDONTWRITEBYTECODE=1 <locked-venv>/bin/python scripts/compile_quality_framework.py --check
PYTHONDONTWRITEBYTECODE=1 <locked-venv>/bin/python scripts/compile_toolchain_fingerprint.py --check
```

They confirm the navigation/quality entry points and workflow guards match their
reviewed source and that the current fingerprint matches actual Copier rendering.
No compiler write mode or source repair was used during review.

## Fingerprint continuity and supplied quality evidence

Independently compared prior and repaired workflow authority lists: the previous
list retains every old identity in order and adds only the former current digest
`a3cde1a611e3408d2f3801da7d6c0e723a998a98ac3a551b7485413f4d9ef896`.
The merged immediate predecessor `dddb8af676cd793653263cd126d9b2b5e88a053b6525e50d8424876133f1e615`
remains present. The new current identity is
`35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`.

Freshly rendered old and repaired source using the existing actual Copier
`rendered_digest` helper; both digests matched. For old rendering, used the clean
immutable prior Delta checkout `c2c31eed661714c0d8bc2245ff8505ac01a60c9a` and first
verified its only differences from `a821da6...` are review records and Task Packet
acceptance metadata, with no tooling/template inputs changed. This confirms the
retained identity's provenance rather than trusting a newly asserted hash.

Verified the independent quality manifest SHA-256
`62ec19574a1f4b720b71cad2588d1beb6a5a7a400efe904ecf2d33e2cf95334b`, all ten
command-log hashes and their recorded zero exits. The full log hash is
`2af14ce059ae3ee2f1d792e85abfcc263488594762650156188ec4a24f3e5d17` and ends with
**418 tests in 364.422 seconds, OK**. That complete run includes clean-clone and
autocrlf cases; it belongs to the separate quality session, not this reviewer's
focused executions. Its other nine deterministic gates also passed.

## Scope limits and handoff

No unchanged Full-review scope was reopened, and no native OpenCode process or
previously blocked malicious dynamic reproduction was run. Native inputs and the
smoke runner are outside this repair diff. The independent quality report's
Linux/Windows input-continuity checks preserve only the earlier actual native
canned-provider observations; this Delta adds no runtime/model qualification or
OS-confinement evidence.

The five initial remote jobs, including Windows native and container execution,
remain evidence for their original published head. Refreshed PR tree identity,
CI and remote-review outcomes remain publication-phase work after separate closure.
AO implementation/lifecycle and real-model, compaction/resume/delegation
qualification are outside this bounded review. No activation, merge, release,
deployment, settings change, source/test edit, commit or remote write was made.
