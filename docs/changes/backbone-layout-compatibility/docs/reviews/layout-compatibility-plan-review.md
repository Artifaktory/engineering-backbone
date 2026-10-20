# Independent trusted-layout compatibility plan review

Reviewer session: `corrections_plan_review`, acting only as independent read-only
plan reviewer for [BB-LAYOUT-013](../../plans/layout-compatibility-task.json).
This is a separate scope from the PR 18 correction plan BB-LAYOUT-012.

## Frozen planning subject

- Repository base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Work branch: `fix/trusted-layout-compat`.
- [Plan](../../plans/layout-compatibility.md) SHA256:
  `42790b52ffaab24e27e8ab897f2a869271de3e63805f1033a6577877159fea65`.
- [Task Packet](../../plans/layout-compatibility-task.json) SHA256:
  `f94e086cd4eda2bb34e3532eeefd241ff4e9c0d5fa89c42a2b8ce33d7e8cab13`.
- Frozen new-layout transition subject:
  `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3`.

The reviewer independently verified HEAD, the two planning hashes and the initial
worktree state: only these planning files were untracked. They were not yet
committed; these exact hashes identify the reviewed planning content. Later Full
review must use committed implementation revisions, tree and binary patch digest.

## Scope and authority assessment

Read the old-layout root instructions and canonical policy, the proposed plan and
packet, and the existing validator's policy, schema, adapter, source-walk and
execution paths. Inspected the navigation source-policy location and compared the
old/new core invariant data. The core JSON data is identical between the recorded
base and frozen PR 18 subject. The frozen new-layout validator contains the stated
495 relocation pairs and 88 historical entries; their full provenance comparison
is correctly required during implementation/checking, not inferred from counts.

- The prerequisite retains the old source structure so the actual previous
  validator can validate it. It changes the trusted source checker before that
  checker is used as PR 18's base authority. No PR candidate is permitted to
  replace the running validator, its schemas or policy floors.
- Source versus consumer execution identity remains separate from old versus new
  source path selection. The plan requires a complete explicit source contract
  per root, including independently resolving candidate and trusted base. It
  prohibits fallback after malformed canonical input, ambiguous dual authority,
  mixed layouts and policy aliases.
- Legitimate project-owned root dependency/build files are expressly excluded as
  source-layout selectors. The selected tooling manifests remain required, so
  alternate project files cannot hide missing or conflicting governed inputs.
- Existing stricter policy invariants, enabled adapters, native instruction
  identity, permission limits and failure propagation remain required across
  layout transitions. The unchanged consumer contract is not used as a shortcut
  for a new source tree.
- Historical exemptions are bounded by reviewed executable-owned mappings and
  hashes checked against actual base blobs. The proposed negative cases prevent
  candidate maps, candidate validator/schema content and project flags from
  inventing exemptions. New task/review records and current links remain checked.
- A new helper is permitted only within the executing trusted authority and
  existing standalone compiler boundaries. Copying the current PR 18 validator
  wholesale would incorrectly assume an already-relocated trusted base; the plan
  explicitly excludes that approach. No second editable policy is introduced.
- Compiled guards and rendered-bundle fingerprints are regenerated normally, with
  only the explicitly reviewed previous current identity retained. Existing
  mixed/unknown-version rejection and local-consumer protections are preserved.

## Verification and delivery assessment

The plan separately requires both meaningful transition directions: the actual
previous validator checking the old-layout prerequisite, and the prerequisite's
validator checking the exact frozen new-layout candidate against the old base.
The latter requires recorded source/tree and actual-byte identity; a synthetic
tree, path projection or candidate-executed validator cannot substitute.

Positive and negative cases cover missing/dual/mixed authority, symlink ancestors,
weakened policy, candidate schema replacement, malformed new evidence,
self-review, disabled adapters, broadened permissions, archive/hash/map tampering,
missing targets, current links and dependency masking. Existing initial/update,
historical and fingerprint tests remain, with all 418 original test methods and
assertions retained. The compiler, full-suite, dependency and committed-patch
checks are explicit. New native/container evidence must identify this
prerequisite's head, with unavailable or pending execution left visible.

Separate implementation/test ownership, independent deterministic checking, two
reviewers on one immutable Full snapshot, independent triage and bounded Delta
are required. Review and iteration limits are specified.

Publication is a separate prerequisite PR on `main`; it grants no merge,
settings, release or downstream authority. Human merge of this prerequisite and
a later reviewed integration into PR 18 remain prerequisites to a real green
PR 18 trusted-base check. Local simulation must not be labeled as that completed
transition.

## Outcome

**NO CONFIRMED IN-SCOPE PLAN FINDINGS.**

The plan is suitable to proceed to bounded implementation and its stated
verification/review chain. No implementation, test, workflow, planning-file or
historical-content edits were made by this reviewer. This report is neither
implementation acceptance nor human permission to merge either PR.
