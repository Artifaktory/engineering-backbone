# BB-LAYOUT-013 independent behavior and compatibility Full review

Date: 2026-10-20. Reviewer session: `bridge_behavior_review`, separate from
implementation, quality checking and finding triage. A delegated read-only
`bridge_behavior_review/fixture_audit` subreview covered test retention and fixture
provenance. Neither reviewer changed implementation, tests or the frozen tree.

**NO CONFIRMED IN-SCOPE FINDINGS.** No P0-P3 behavior or compatibility defect
attributable to this reviewed diff was confirmed. This conclusion is limited to
the scope below; it is not human merge approval or a claim of remote CI success.

## Frozen subject and review sequence

- Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Reviewed head: `aaa74e3dfc60836f8aae7c2751bc9dd889c52470`.
- Reviewed tree: `fe6da7e734e7d6cdea508dc007649f03b903c423`.
- Binary base-to-head patch SHA256:
  `8f6ca8f0f22fe3065f392aed73c194be8aeebc7e0ee7b74680c871953e671969`.

The reviewer independently resolved HEAD/tree, recomputed the full binary patch
digest and matched the supplied patch. The frozen worktree was clean before and
after inspection. Preparation initially read only the permitted instructions,
plan, Task Packet and plan review. Formal implementation inspection began only
after the coordinator reported the repaired full quality run complete and gave
explicit GO. This is the first Full review of this delivery; the earlier failed
quality run and its four triaged repairs preceded it.

Read the root and applicable path instructions, canonical core/quality/dependency
policies, contributor process, approved plan/packet and independent plan review,
plus relevant OpenCode, Copier and source-dependency contracts. The source has no
active navigation seed requiring a task-context receipt for this review.

## Implementation and compatibility coverage

| Boundary | Inspected behavior |
| --- | --- |
| Source identity | The executing bundle retains source-versus-consumer mode authority. The new resolver selects only within source mode and requires one complete canonical source policy contract. |
| Old/new roots | Candidate and trusted base are resolved independently. Missing, mixed, ambiguous and symlinked canonical authorities fail; product-root dependency files do not choose the source layout. Diagnostic inspection after a failed layout adds errors and does not resume validation in another mode. |
| Policy and dependencies | Policy schema/floors and prior stricter invariants remain checked using the executing bundle. Selected tooling manifests move through the explicit contract; root product manifests cannot substitute for them. |
| Native adapter paths | Only the fixed mandatory source instruction tuple receives explicit old/new correspondence. Additional inherited instruction identities and permission comparisons remain. The two activation call sites now pass their own base/candidate roots while retaining the original enabled-only, path-set and byte comparisons. |
| Navigation and quality | Source standards, dependency-policy and native-document references use the selected root contract. Consumer paths and inactive/active contract requirements remain fixed. The source tree itself retains the old physical layout. |
| Compiler propagation | The maintained compiler parses the canonical resolver as text through AST extraction, rather than importing candidate Python. Resolver copies and navigation/quality/OpenCode guards propagate through the existing standalone boundaries. |
| Workflow behavior | Events, permissions, pins, conditions, checkout settings, job/step structure and gate envelope are unchanged. The changed reusable-workflow step contains the regenerated guards and updated reviewed toolchain identity. Its previous identities equal the original list plus only the actual old-main current identity. |
| Historical documents | New-layout history uses executing-validator-owned original paths and hashes. Archived bytes must match before original-context link handling. Current documents retain normal link checks; newly named task/review JSON receives trusted schema and reviewer-independence checks. |

Independent read-only audits additionally established:

- All canonical resolver copies have equivalent ASTs after normalizing only
  docstring indentation: one in navigation, two in quality and four in the
  validator. The initial raw AST comparison distinguished indentation inside
  embedded docstrings; the normalized comparison confirmed no executable drift.
- The embedded relocation/archive literals equal the already reviewed PR 18
  literals. All **495** mapping keys match the actual old-base file set and every
  mapped destination exists in the exact PR 18 tree. All **88** archive entries
  match their actual old Git bytes, new Git bytes and recorded SHA256 hashes.
- Parsed workflow comparison confirms that only the intended generated-consumer
  validation step changed, with the surrounding workflow envelope identical.
  Its previous fingerprint list adds exactly
  `35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`;
  no intermediate implementation fingerprint is admitted.

These audits inspected the frozen files and Git objects and returned exit 0 for
the final identity, normalized-AST, workflow-envelope and archive comparisons.
No complete unit suite was repeated by this reviewer.

## Tests and provenance subreview

The delegated independent fixture audit read all test changes and the complete
new transition suite. Its read-only Git/AST audit confirmed all **418** original
test methods and **1048** original assertion calls remain, while all **59**
pre-existing fixture blobs are byte-identical. Fixture preparation and additional
observed predecessor coverage do not remove the original assertions.

Both new ZIP fixtures independently match their actual Git trees, every file blob
and mode: **495** old-source files and **542** original PR 18 files. The runtime
fixture verifier binds fixed commit/tree/count, archive SHA256, exact path set,
file modes, per-file SHA256/Git blob identity and reconstructed Git tree before
extraction or old-validator execution. The test candidate is not projected back
to old paths. New cases exercise all four source candidate/base combinations and
policy, schema, adapter, permission, dependency, history, ambiguity and symlink
rejections using the bridge-owned validator.

The repaired historical consumer check actually renders the verified old-main
source with tasks disabled, asserts its measured digest against the fixed reviewed
identity, executes the current trusted workflow on that consumer, and only then
adds the observed digest before the unchanged exact-set assertion. Expected
authority is not derived from the candidate's allowlist. Clean single-commit and
autocrlf clone coverage remains. No test-suite execution was repeated by the
fixture subreviewer.

## Quality evidence and limits

Read [the final quality report](layout-compatibility-checks.md) as external evidence
written after the frozen commit and bound to the exact head/tree/patch above.
The separate checker records **441 tests in 450.358 seconds, exit 0**, all four
compilers, validator, dependency consistency, available Actionlint and committed
base-to-head whitespace checks passing. It records all 505 inputs unchanged
during the final run and 413 protected existing blobs retained.

The same checker records actual old-main validator acceptance of this old-layout
bridge and bridge-validator acceptance of its own source, original PR 18
`c50108773ba3195bf0f7503e5dffb2d7bfc78cd3` and corrected published PR 18
`2ddfa803688c70b556dc83bcf07a4c3911713be5`, all against actual old main. These are
the checker's executions, not this reviewer's. The earlier failed run and its
LC-CHECK-01 through LC-CHECK-04 triage remain explicitly preserved.

This review did not execute Docker, native clients, models or Windows runtime
sessions. It does not establish container compatibility or native qualification.
The separate PR 18 remote Git-clone I/O investigation is outside this bridge
snapshot and does not establish bridge remote success or failure. The security
reviewer's broader adversarial assessment is a separate required Full report.

After both Full reports, separate triage and final publication checks remain
required. Later evidence commits are outside this frozen snapshot: rerun the
complete committed base-to-final-head whitespace check and verify published
tree/patch correspondence. The prerequisite still requires human merge before
PR 18 can use its code from actual trusted main, followed by reviewed integration
and current-head checks. No gate, merge, release or downstream authority is
provided by this report.
