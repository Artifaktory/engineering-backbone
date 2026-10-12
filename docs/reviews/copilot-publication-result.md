# Copilot publication follow-up: scoped Delta result

Task: [BB-COPILOT-003](../../plans/copilot-development-task.json).
Date: 2026-10-12. This continues the
[original Full/Delta chain](copilot-development-result.md) and the independently
confirmed [external-review triage](copilot-publication-triage.md) for PR #6.

## Frozen follow-up identities

| Identity | Value |
| --- | --- |
| Initial remote publication | `97882ebdea61b4d948e04542a0feec9d4f79bd60` |
| Tree-equivalent initial local publication | `1e5fb8a418c006657cd47f150ad3b1e7ceac9191` |
| Initial publication tree | `18c52bbf726618c6960db9df9b4382a918d85812` |
| First CS-2 repair, not published | `eadfa186b09ee005e24de7e977ffb30b64a6e2f8` |
| First repair tree | `ad35df295fd1a72b5e7890cee191571e5710fe24` |
| First repair canonical Delta patch | `1cd442f281bb39ea42097a5262d19b61c6e8d3dbea27d292d51cb87d5234a8c3`, 39052 bytes |
| Final fallback repair head | `761620292c8c1c56256617b90051f55bd2bb9303` |
| Final fallback repair tree | `90e9264243278bd9020a015e761684dc9391b8b3` |
| Final canonical Delta patch | `593efb2a01f50dd432ee3ddd5d6203edd26e0e0730d910a5172e7c5087148784`, 22302 bytes |

Both reviewer sessions inspected each fixed Delta snapshot without intervening
edits. These are separate local AI sessions, not actual Copilot runtime sessions.
The canonical patch format is the command in the triage/publication record,
including full indexes, fixed context and Myers diff. Later report/packet additions
receive a separate evidence-only comparison; they do not change implementation.

## Confirmed findings and repairs

External Codex Full produced CE-1 and CS-2 as P1. Independent triage confirmed them
as P2 with concrete evidence; the original attribution is retained. CE-1 is an
exact-publication evidence gap. CS-2 is reserved-role ambiguity under project-named
files; primary host code proves that native headers participate in name resolution.

The first CS-2 repair rejected reserved headers, safely inspected native metadata,
and passed 136 complete tests plus 30/38 independent Copilot tests. Delta still
found CS-2-D1: an explicitly empty header and composite filename could reach a
reserved name through the supported filename fallback. Both reviewers reproduced
direct acceptance and actual old-base workflow exit 0. That snapshot was retained
as evidence and was not published as clean.

The bounded additional repair covers the bridge's first-marker fallback priority
and the present-empty scalar difference between native parsing and PyYAML. A
present PyYAML-null name is conservatively checked as blank; an absent key stays
distinct. Exact legacy `.chatmode.md` exclusion applies only to the new inspected
CLI fallback branch; existing namespace checks remain. The tests preserve alias
bytes and genuine native profiles' metadata, tools and body content. No candidate
module is imported. Canonical roles, ordinary blank/unnamed profiles and explicitly
distinct compound filenames remain accepted.

## Checks and final independent Delta

All listed parent checks exited 0 in the unchanged Python 3.12 hash-locked
environment. Requirements, generic schemas, Codex files and historical fixtures
remain unchanged.

| Check/session | Actual result |
| --- | --- |
| Parent complete suite after fallback repair | 138 tests passed, 135.274 seconds |
| Source and previous trusted-base validation | Structural and trusted-base contracts pass |
| Compiler coherence / rendered tooling identity | Pass; SHA256 `91f4d1d7be5573f0939cdb9f3859d3ff236807504abaa554207dfc1705190321` |
| Actionlint and whitespace | Pass |
| `copilot_full_security` final Delta | CS-2 including D1 repaired; `NO CONFIRMED IN-SCOPE FINDINGS`; 32 tests passed in 22.206 seconds, compiler and patch checks passed; empty/comment/null/block-empty probes rejected conservatively without mutation |
| `copilot_full_behavior` final Delta | CS-2 including D1 repaired; `NO CONFIRMED IN-SCOPE FINDINGS`; all 40 Copilot tests passed in 45.275 seconds; original D1 direct/workflow probe now rejects with exit 1; complete guide and README diagram parity verified |

The four approved historical tooling identities are unchanged. None of the
unmerged vulnerable intermediates was added to that authority list. Independent
coverage remains the confirmed repairs and their direct parser, naming, preservation,
upgrade and compiler regressions; unchanged areas were not reopened as another Full.

## Exact publication binding and remaining external checks

[Immutable publication record 1](https://github.com/Artifaktory/engineering-backbone/pull/6#issuecomment-6125165400)
binds the initial remote base/head/tree, complete reviewer packet and independently
computed base-to-publication patch (`832c7553ad7ed2861d6022b4215bbc31b6a769bee249e51f9c844164184bd5fc`,
308101 bytes). Both reviewers independently verified that record. It addresses
CE-1 for that historical head only.

The committed implementation packet identifies the final frozen implementation
repair. Its own final commit hash cannot be embedded in the same measured tree.
The forthcoming **publication record 2** in
[PR #6](https://github.com/Artifaktory/engineering-backbone/pull/6) must instead bind
the complete remote base/head/tree and canonical full-patch digest, with a complete
publication reviewer Task Packet and independent verification. That immutable
record includes later evidence files and avoids a self-referential commit cycle.
CE-1 remains conditional until that record is verified. GitHub CI and scoped
external Delta on the new head remain pending here and are closed out separately
in the PR, with exact revisions and actual results.

Signed-in Copilot client checks remain unexecuted; the
[client smoke checklist](../copilot/smoke-tests.md) records the required native
abnahme. No live provider discovery, human approval, merge, release or downstream
rollout is implied by structural tests or these local reviewer sessions.
