# Integration runtime implementation

The runtime implementer completed the approved BB-LAYOUT-014 runtime/compiler
scope. This record describes implementation-time checks; it is not independent
review or merge approval. The starting PR18 head was
`f1c1410cff6407109f286173f1ecc980cd2a14b7`; the incoming human-merged main was
`537576f658bbd79c3bc49b26ade948116c664943`.

## Changes

- Reconciled the merged-main validator, navigation and quality framework with
  the PR18 physical source layout. The validator derives source identity from
  its executing `.engineering-backbone/src/` location; the legacy installed
  `.engineering-backbone/validate.py` location remains consumer mode.
- Moved the merged-main `source_layout.py` helper unchanged into the source
  directory. Candidate and trusted-base source contracts are still resolved
  independently. Canonical policy presence, completeness and symlink checks,
  permission floors and inherited additional instructions remain in force.
- Updated the navigation compiler's source locations and retained its compiled
  helper synchronization. Regenerated navigation, quality, workflow and
  fingerprint outputs in that order. The workflow retains PR18 source commands
  and executes the actual trusted-base validator for candidate policy checks.
- Repaired INT-ARCHIVE-01 by comparing the complete executable-owned 88-record
  inventory with the observed walk before artifact validation. A missing file,
  missing parent, non-file replacement or symlink in an archive path now fails.
  Existing exact-byte and original-context relative-link checks remain. This
  completeness rule applies to the new source contract; old source and legacy
  consumer contracts are unchanged.
- Kept all 88 historical hashes and all 495 original-to-current path mappings
  unchanged. No candidate mapping data supplies validation authority.
- Preserved the existing approved predecessor list and appended only merged
  main's current fingerprint
  `a9355b863956489a0da750849dd890cdb8745f64172dedb3449f816e844bb524`.
  The generated current fingerprint is
  `94f8f22f4dd66234d5048f2dee51c897fa7b9406694bf38ce44fef5186421120`.

## Executed implementation checks

All commands used the existing isolated Python 3.12 environment. Each recorded
check completed with exit 0:

- `python -m py_compile` for the reconciled runtime and navigation compiler.
- `python .engineering-backbone/src/maintenance/compile_navigation.py --write`,
  followed by quality-framework, workflow-kit and toolchain-fingerprint `--write`.
- Each of those four compiler commands with `--check`.
- `python .engineering-backbone/src/validate.py --root . --trusted-base
  /workspace/scratch/6e019b0851cc/backbone-main-537576f` against the integrated
  worktree: structural PASS.
- `python /workspace/scratch/6e019b0851cc/backbone-main-537576f/scripts/validate.py
  --root /workspace/scratch/6e019b0851cc/backbone-layout --trusted-base
  /workspace/scratch/6e019b0851cc/backbone-main-537576f`: structural PASS from the
  actual trusted main implementation.
- Direct calls to the current executing validator against the unchanged frozen
  c501 PR18 fixture and actual main trusted base: intact fixture PASS; disposable
  copies with the unlinked `backbone-bootstrap/plans/bootstrap-task.json` removed
  or its parent archive subtree replaced by a symlink rejected with the required
  historical-record diagnostic.
- AST comparison of both archive constants with actual main: equal, with 88 and
  495 entries. Byte comparison of the standalone layout helper: equal. Parsed
  fingerprint lists: new predecessors equal main predecessors plus only main's
  current identity.
- `git diff --check -- .engineering-backbone/src
  .github/workflows/governance-checks.yml`.

The separate test implementer owns durable regressions and fixture reconciliation.
The quality checker owns the complete suite and final integrated checks. The
actual main validator still has the confirmed archive-deletion blind spot: its
positive transition result does not certify this candidate's completeness repair.
Independent frozen implementation reviews and final committed-diff checks remain
required after these implementation checks.
