# Copilot PR publication review triage

External Codex Full reviewed PR #6 head
`97882ebdea61b4d948e04542a0feec9d4f79bd60`, tree
`18c52bbf726618c6960db9df9b4382a918d85812`, base
`1ffebdfff4f5cc24e7ffcfff5a4dcf88d554f4c8`. Its two P1 comments were independently
triaged before further repairs. Local tree-equivalent head:
`1e5fb8a418c006657cd47f150ad3b1e7ceac9191`.

| ID | Provider severity | Triage | Confirmed issue and bounded repair |
| --- | --- | --- | --- |
| CE-1 | P1 | Confirmed P2 evidence gap | Complete base-to-publication patch digest and exact publication reviewer packet were not durably recorded. Add immutable external publication records that bind remote base/head/tree and canonical patch digest, with independent comparison. No implementation bypass demonstrated. |
| CS-2 | P1 | Confirmed P2 role ambiguity | A project-named file with reserved frontmatter `name` and omitted tools passes the filename-only guard; a supported VS Code CLI bridge resolves/merges agent names from that header. Reserve managed frontmatter names as well as filenames; preserve local files and unrelated native configuration, and execute actual old-base negative regressions. |

CE-1's reference to `5aaf431...` is not the published PR head. The provider's footer
and summary identify `97882eb...`. The source packet intentionally binds the frozen
implementation repair; only independently checked evidence files followed it.
The gap is the missing durable final patch/packet binding, not evidence that the
implementation changed without review. A tracked file cannot contain its own
final commit hash or its own final patch digest. An external publication packet
binds the complete tree without that self-reference cycle.

## CE-1 initial publication binding

[Immutable publication record 1](https://github.com/Artifaktory/engineering-backbone/pull/6#issuecomment-6125165400)
contains the exact remote identities, complete reviewer packet and independently
computed patch SHA256 `832c7553ad7ed2861d6022b4215bbc31b6a769bee249e51f9c844164184bd5fc`
(308101 bytes). Canonical command is `git diff --binary --full-index --no-ext-diff
--no-textconv --no-renames --no-color --src-prefix=a/ --dst-prefix=b/ --unified=3
--inter-hunk-context=0 --diff-algorithm=myers BASE HEAD --`.
Both sessions computed it from matching local trees; the remote tree match was
independently fetched. That record explicitly leaves CS-2 and the gate open.
Each later publication needs a new immutable record and independent digest/tree
verification, rather than editing this historical record.

## CS-2 primary evidence and reproduction

GitHub calls `name` a display name. The inspected primary VS Code implementation
at `microsoft/vscode@3b486b1ff92ac032974c6f589e7d5a46fe486067`,
[`copilotCli.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/extensions/copilot/src/extension/chatSessions/copilotcli/node/copilotCli.ts),
blob `7b767d48b1a47f6f43195f9f29d186308058a14c`, uses header `name` for agent name
and display name, merges names case-insensitively, resolves by name/display name,
and maps missing tools to an unrestricted default. This confirms an actual
supported host resolution path; no universal duplicate-file precedence or live
destructive invocation is claimed.

The security reviewer independently reproduced direct guard `[]` and actual
old-base pinned workflow exit 0 for `local.agent.md` declaring
`name: backbone-security-reviewer` with omitted tools. A candidate-import marker
remained absent. Current canonical source and fixture labels are all
`backbone-<role>`; the earlier extra probe mistakenly treated a local filename as
sufficient evidence of unrelated ownership. This triage corrects that assumption.

## Authorized repair and Delta scope

Parse native agent frontmatter with the trusted parser while scanning both
supported suffixes. Reject reserved header names under noncanonical filenames,
including case variants, without importing candidate code, following symlinks or
changing any local bytes. Retain valid unrelated native agents, including optional
metadata and permissive project-owned tools; this does not make their full content
subject to the managed role registry. Ambiguous/uninspectable native declarations
require manual reconciliation rather than silently passing a namespace check.
Regenerate source/workflow coherence and current tooling identity. Do not approve
the unmerged vulnerable intermediate identities as historical tooling.

Delta is limited to CE-1 publication binding and CS-2/direct namespace, parser,
preservation, legacy upgrade and compiler regressions. Existing reviewed roles,
skills, diagram and generic schemas are unchanged. Deterministic checks precede
two independent Delta reviews, then updated PR CI and a scoped external Delta.

## Repair checks before independent Delta

The added direct/workflow regressions first failed in seven cases across two
tests; the actual historical-base workflow returned exit 0. A delimiter regression
then exposed three whitespace/BOM cases before its correction. After repair,
30 targeted tests passed in 15.954 seconds. They verify reserved names, YAML escapes,
case/whitespace normalization, both suffixes, duplicate/malformed/unsafe YAML,
symlink non-following, byte preservation and unchanged candidate-import markers.
Valid unrelated profiles retain optional metadata, unrestricted tools and their
own body links; optional/no frontmatter keeps the filename fallback.

The pinned VS Code
[`promptFileParser.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/src/vs/workbench/contrib/chat/common/promptSyntax/promptFileParser.ts)
(blob `3b1fc927cca1af30376ce95d179e8745eca13c90`) accepts trailing whitespace on
both YAML delimiters. The namespace scan covers that form. Default discovery in
[`promptFilesLocator.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/src/vs/workbench/contrib/chat/common/promptSyntax/utils/promptFilesLocator.ts)
(blob `feef4a0160db88e3efb5c3ec417b38abdffe47b4`) takes direct agent files and
recurses only for instructions. No nested-agent bypass was established for that
default path; other configured locations are not covered by this observation.

Current compiled tooling identity:
`4ebaea12961b45f6ae4213ca6f7443c5f4300099a83f9a6e0a2f2da4cda4b230`.
The four historical identities are unchanged; unmerged vulnerable intermediates
`82fccd70...` and `827c3cc0...` are not approved.

## CS-2-D1: Delta found an incomplete filename fallback

Both independent Delta sessions reviewed repair
`eadfa186b09ee005e24de7e977ffb30b64a6e2f8`, tree
`ad35df295fd1a72b5e7890cee191571e5710fe24`, canonical Delta patch
`1cd442f281bb39ea42097a5262d19b61c6e8d3dbea27d292d51cb87d5234a8c3`
(39052 bytes). Thirty targeted tests and all 38 Copilot tests passed independently,
but both reviewers reproduced a remaining P2 CS-2 variant: a composite filename
`backbone-security-reviewer.agent.md.local.agent.md` with `name: ""` and omitted
tools still returned direct `[]` and actual old-base workflow exit 0. Local bytes
were preserved. CS-2 remained open; the earlier security clean conclusion is
superseded by that concrete evidence. This repair snapshot is not published.

The pinned core
[`promptsServiceImpl.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/src/vs/workbench/contrib/chat/common/promptSyntax/service/promptsServiceImpl.ts),
blob `338149b1a56ea1f50be73e19244023398f530d12`, preserves an explicit empty scalar
through nullish coalescing. The inspected CLI bridge falls back to the filename for
that empty name, and its helper truncates at the first `.agent.md` substring;
otherwise it tries `.chatmode.md`. This reaches a reserved name even though the
guard strips only the final suffix. An absent header name alone is not claimed as
the bypass: the service supplies its complete cleaned filename first.

Authorized additional repair is this same namespace finding only: inspect the
supported blank-name filename fallback, honoring the bridge's marker priority,
reject a reserved fallback identity without changing bytes, and test direct and
actual historical-base workflow paths. Keep canonical roles, ordinary unnamed
profiles and explicitly distinct project names accepted. Account for both marker
branches exposed by the inspected helper without rejecting unrelated compound
filenames wholesale. Recompile current identity; do not approve the unmerged
`4ebaea12...` intermediate as historical tooling. Repeat deterministic checks and
independent Delta for CS-2-D1 and direct regressions; CE-1 still requires the final
publication record after those checks.

The same pin's
[`yaml.ts`](https://github.com/microsoft/vscode/blob/3b486b1ff92ac032974c6f589e7d5a46fe486067/src/vs/base/common/yaml.ts),
blob `64679352573b69990a3996802f2f24c81c0ae561`, maps a present missing scalar
(`name:` or `name: # comment`) to an empty string and a diagnostic; agent discovery
does not discard the constructed profile for that diagnostic. PyYAML maps this
value to `None`. The reservation therefore conservatively treats a present
PyYAML-null name as blank, while retaining an absent key as a separate filename
default. Explicit `null`/`~` may be nonempty strings in the native lightweight
parser: the conservative rule does not claim all null spellings execute blank.
These are direct parser regressions of CS-2-D1, with the same authorized scope.

The additional regressions first failed in 12 compound-filename cases, four
unquoted-empty direct cases and six quoted/unquoted actual old-base workflow cases.
After the bounded fallback repair, 32 targeted tests passed in 22.573 seconds; the
complete suite passed 138 tests in 135.274 seconds. Source validation, previous
trusted-base validation, compiler coherence, Actionlint and whitespace passed.
The new branch mirrors the inspected CLI's exact legacy `.chatmode.md` exclusion;
existing header/filename namespace checks remain unchanged. Marker priority,
explicitly distinct native names, ordinary blank/unnamed profiles and preserved
bytes/import markers are tested. Current tooling SHA256 is
`91f4d1d7be5573f0939cdb9f3859d3ff236807504abaa554207dfc1705190321`;
the four approved historical identities remain unchanged.
