# Copilot development: checks, independent Full and Delta

Task: [BB-COPILOT-003](../../plans/copilot-development-task.json).
Date: 2026-10-12. The human authorized implementation and publication of one
checked, independently reviewed PR. Merge, release and downstream adoption remain
separate decisions.

## Frozen review identities

| Identity | Value |
| --- | --- |
| Local trusted base | `2b48fc01d20648ffeeea94e288e1c7d511bae12b` |
| Remote main base | `1ffebdfff4f5cc24e7ffcfff5a4dcf88d554f4c8` |
| Common base tree | `357d1c3caf05eed442f5b5cc74539437c36bd794` |
| Full head | `be36b14020a7004471b966709414b8309666c6cc` |
| Full tree | `119328e1f8777e33783e8473ad38d9250b3fe2e4` |
| Full binary-patch SHA256 | `efaac6d6c2bb4cd4a87def8938fdb7fdcd38d4e406ffe8e5de74c7be8b16c894` |
| Repair head | `ee4bbd23b663494fc7d413f5338618250a5a9e71` |
| Repair tree | `439c91173382537b947db002285086b9f1919d47` |
| Delta binary-patch SHA256 | `b199f20c33874c5119f6b90fb7e846ebb5ac516e5b1502e33e44ef351cd36caa` |

Each pair of independent sessions inspected the same fixed snapshot without
intervening edits. These are separate local AI review sessions; they are not
claims that GitHub's Copilot or Codex provider bot ran locally. The local and remote
base trees match. Connector publication uses remote main as parent and verifies
tree equality rather than claiming identical commit metadata. Later evidence-only
additions are compared against the reviewed repair before publication.

## Implemented acceptance

Ten native Copilot profiles and eight procedural skills adapt the existing policy
to Copilot's role, skill and scoped-instruction formats. Five path rules include
three core rules and optional Python/frontend installation profiles. Existing
Task Packet enums, Codex profiles, generic schemas, dependency hash lock and
historical fixtures remain unchanged.

The complete review-loop diagram is identical in README and the canonical
[workflow](../copilot/workflow.md). Every generated neutral Copilot guide includes
that workflow, including when Copilot is not selected. Existing native roles,
instructions and skills are preserved on Copier updates; refreshed fragments and
the guide support explicit reviewed integration.

[Source provenance](../copilot/source-provenance.md) records inspected files,
immutable commits/blobs, licenses and locally adapted patterns from Microsoft
VS Code, Microsoft Skills, Awesome Copilot and Spec Kit. Client-specific capability
limits and reported issues remain in [clients](../copilot/clients.md).

## Executed checks

Python 3.12 used the previously verified hash-locked environment. All checks below
exited 0. The complete suite was run once on the Full snapshot and again after the
confirmed repair; the extra tests are direct regressions for that repair.

| Check | Actual result |
| --- | --- |
| Full suite before repair | 126 tests passed, 126.741 seconds |
| `python -m unittest discover -s tests -v` after repair | 129 tests passed, 126.887 seconds |
| `python scripts/validate.py` | Source structural contracts pass |
| Previous trusted validator with `--root` candidate and `--trusted-base` previous checkout | Trusted-base validation passes |
| `python scripts/compile_toolchain_fingerprint.py --check` | Source/compiled guard coherent; rendered tooling SHA256 `827c3cc0475146eb5e2b1263f118842e1d12d6a14ac9f6dff3b9d723cc4f466b` |
| Actionlint over both workflows | Pass |
| Staged/committed diff whitespace | Pass |

The eight distribution tests execute real Copier creation across all 16 provider
and optional-profile combinations, plus historical and extended consumer updates.
They verify byte-identical preservation of stronger native policies, local facts
and the separate reviewed caller; installation-choice changes fail before consumer
mutation. Validation/workflow negatives exercise permissions, malformed metadata,
links, aliases, removals, symlink boundaries and actual old-base upgrades. A candidate
`yaml.py` execution marker remains absent: the pinned guard does not import it.

## Independent review chain

The independent plan review found PLAN-TRUST-1: an old consumer validator cannot
validate newly added native assets. The amended plan requires a workflow-owned,
compiled Copilot guard, used even with approved older trusted-base tooling. The
negative executed-upgrade tests verify that design.

| Stage and reviewer | Result and independent coverage |
| --- | --- |
| Full: `copilot_full_behavior` | `NO CONFIRMED IN-SCOPE FINDINGS`; native role/skill contracts, client limits, diagrams and practical patterns; eight real distribution tests passed; four pinned source examples and reported issues corroborated |
| Full: `copilot_full_security` | One confirmed P2, CS-1: an unrestricted known-role `.md` alternate was accepted by the new registry and actual old-base pinned workflow; an elevated canonical `.agent.md` was rejected |
| Triage and repair | [CS-1 triage](copilot-development-triage.md) authorizes reserved-name reconciliation and direct regressions only; tests reproduced ten failing alias/case subcases before repair |
| Delta: `copilot_full_security` | CS-1 repaired; `NO CONFIRMED IN-SCOPE FINDINGS`; 23 validation/workflow tests passed in 11.548 seconds, compiler and whitespace checks passed; additional symlink-alias and unrelated-identity probes passed |
| Delta: `copilot_full_behavior` | CS-1 repaired; `NO CONFIRMED IN-SCOPE FINDINGS`; all 31 Copilot tests passed in 38.740 seconds; direct Jinja probe verified diagram parity and complete amended guide text; fixed HEAD/tree and clean worktree confirmed |

Copilot accepts both `.md` and `.agent.md` agent files. The guard now rejects
alternate suffixes/case spellings of reserved managed identities while preserving
their bytes for manual reconciliation. Valid canonical and unrelated native
profiles remain accepted. No duplicate-file runtime precedence is assumed. The
vulnerable intermediate tooling identity is not approved; the four previously
approved historical identities remain unchanged. No confirmed in-scope finding
remains open after both Delta reviews.

## Evidence limits and publication checks

The [fresh-session forward check](copilot-forward-check.md) tested the
bug-reproduction skill against raw source and an accepted contract without an
expected fix. It produced real boundary failures without editing implementation.
This measures instruction usability, not actual Copilot discovery or execution.

Signed-in PyCharm, VS Code, CLI and cloud runs were not available here. Their
[smoke checklist](../copilot/smoke-tests.md) is part of the delivery. Tool budgets
and handoffs are host-dependent configuration, not a filesystem sandbox or proof
of independent review. Structural checks do not authenticate review evidence or
replace human approval.

GitHub PR-CI and the external Codex provider result are verified after publication
and recorded separately in the PR closeout. AC-6 remains pending in the committed
pre-publication packet until that evidence exists. No source-project write, live
client result, merge, release or downstream rollout is claimed.
