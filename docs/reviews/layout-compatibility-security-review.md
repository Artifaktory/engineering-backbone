# BB-LAYOUT-013 independent security Full review

Date: 2026-10-20. Reviewer session: `bridge_security_review`, independent of the
planner, implementers, quality checker and finding triage. The reviewer read only
governance/planning context before the coordinator's GO; formal implementation
review began after the repaired complete suite had passed.

**NO CONFIRMED IN-SCOPE FINDINGS.** No P0-P3 security/trust defect attributable to
this diff was confirmed within the coverage below. This is neither human merge
approval nor a claim that the prerequisite has been adopted by trusted `main`.

## Immutable subject

- Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Reviewed head: `aaa74e3dfc60836f8aae7c2751bc9dd889c52470`.
- Reviewed tree: `fe6da7e734e7d6cdea508dc007649f03b903c423`.
- Binary base-to-head patch SHA256:
  `8f6ca8f0f22fe3065f392aed73c194be8aeebc7e0ee7b74680c871953e671969`.

The reviewer independently resolved HEAD/tree and recomputed the binary patch
digest. The frozen worktree was clean before and after review. No source, tests,
fixture bytes or frozen evidence were edited. The sole repository write is this
report in the live worktree, outside the frozen implementation snapshot.

Read the root and applicable path instructions, canonical governance, dependency
and OpenCode operating/runner contracts, the scoped plan/packet and independent
plan review. Inspected changed runtime/compiler code, generated guard changes,
new transition fixtures/tests, the previous-main consumer coverage, and the
initial failed-run/triage records. The earlier PR18 refactor and external AO
implementation were not reopened as part of this Full review.

## Security and trust coverage

| Boundary | Review conclusion |
| --- | --- |
| Execution identity | Source/consumer mode remains owned by the executing validator bundle. The CLI has no candidate-selected mode override. Trusted schemas and policy floors remain in the executing checkout. |
| Layout authority | Candidate and base roots are resolved independently. Both complete canonical contracts are explicit; absent, dual, mixed, incomplete and symlinked policy authorities remain fatal. Alternate aliases are detected before existence/type filtering, including dangling aliases. Product root manifests do not select a layout. |
| Diagnostic failure path | `diagnose_unselected_policies` runs only after a fatal layout error, checks only fixed regular policy files with trusted schemas/floors, and returns the existing failure. It does not select a fallback mode or turn an error into success. |
| Policy inheritance | The selected base policy is read from its own layout, validated with trusted schemas, and compared without removing stricter inherited invariants. Unreadable/ambiguous base authority remains an error. |
| Native adapters | Required source instruction paths have a fixed positional correspondence between the two reviewed layouts. Additional inherited instructions retain their exact identity; candidate mapping files cannot remap them. Enabled-adapter and permission-budget enforcement remain intact. |
| Activation | The repaired seed/candidate calls receive their respective roots. Existing exact seed input-path and raw-byte comparisons remain, including the enabled-only activation restriction. |
| Standalone guards | Maintenance extracts one undecorated helper function as text rather than importing candidate Python. The canonical resolver is embedded into the validator, navigation, quality and workflow guards. Runtime checks do not import a candidate resolver. |
| History | Archived bytes are checked against executable-owned hashes before historical Markdown links receive original-context resolution. The 495-path crosswalk and 88 archive records are fixed reviewed literals; candidate layout maps grant no exemptions. Current links and named new task/review artifacts continue through normal checks. |
| Consumer compatibility | Consumer paths and source-versus-consumer selection remain unchanged. Existing dependency, policy, schema and adapter constraints are retained. Only the actual previous current tooling identity is added to the previous allowlist. |
| Workflow boundary | Events, permissions, pinned actions, checkout settings and unrelated step content remain unchanged. No fallback, skipped required gate, candidate command execution or automatic merge is introduced. |

## Independent reviewer verification

Read-only Git/AST checks and bounded probes were executed by this reviewer:

- Parsed the static mapping/hash authority without executing candidate code.
  All **495** crosswalk keys exactly match the actual base Git file set; their
  **495** unique destinations exist in the recorded PR18 tree. All **88** archive
  SHA256 values match both the original base blobs and relocated PR18 blobs.
- Compared the canonical resolver's executable AST with all **10** embedded
  copies: navigation 1, quality 2, validator 4, workflow 3. All match. Only
  indentation-dependent docstring text was excluded from that executable-AST
  comparison; compiler synchronization is separately covered by quality checks.
- Compared parsed workflow structure after excluding only the changed generated
  consumer guard script and its fingerprint environment. All other structure is
  identical to the base, including triggers, permissions, pins and other steps.
- Verified that the previous fingerprint list is exactly the old list plus the
  actual old-main current identity
  `35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b`.
  The new current identity is
  `a9355b863956489a0da750849dd890cdb8745f64172dedb3449f816e844bb524`;
  intermediate implementation identities were not added to trusted predecessors.
- Independently integrity-verified the exact old/new ZIP fixtures before making
  disposable probe copies. The frozen bridge validator accepted the unchanged
  new-layout candidate against the old-layout base (exit 0), then rejected all
  five bounded negative probes (exit 1, no traceback): a dangling alternate
  canonical prose alias; a selected policy alias to an internal regular file;
  a conflicting alternate policy directory in the trusted base; a poisoned
  candidate helper accompanied by a weakened mandatory invariant; and candidate
  schema replacement combined with implementer-as-reviewer evidence. The helper
  execution marker was never created. The combined probe command exited 0.

These probes changed temporary copies only. They are focused reviewer evidence,
not another complete suite or native runtime qualification.

## Quality evidence and remaining limits

Read [the independent quality report](layout-compatibility-checks.md) as external
post-commit evidence bound to the exact reviewed head/tree/patch. It records
**441 tests passing in 450.358 seconds**, all four compilers, validator, dependency
check, Actionlint and committed whitespace checks passing. It also records actual
old-main-validator-to-bridge validation, bridge validation against old self and
both frozen PR18 heads, retained original methods/assertions, **413** preserved
existing blobs and **59** preserved original fixture blobs. Those executions are
the quality checker's, not a full-suite rerun by this reviewer.

The first failed 441-test run and all four confirmed causes remain preserved in
[failed-run evidence](layout-compatibility-check-failures.md) and
[separate triage](layout-compatibility-check-triage.md). The reviewed snapshot
includes their bounded repairs; no failing assertion or gate was removed to
obtain the subsequent passing result.

This review did not execute Docker, native Windows/Linux clients, real models,
Copilot loading, deployments or remote bridge CI. PR18's separate current remote
Git clone error does not establish a bridge-specific result. Local transition
success is not proof that trusted `main` already contains this update.

Separate final finding triage and publication checks remain required. Evidence
commits after this frozen head require renewed committed base-to-final-head
whitespace checks and exact remote tree/patch readback. A human must merge the
prerequisite before a later reviewed integration into PR18 can use it as the
actual trusted base; neither merge is authorized by this report.
