# Technology/navigation Full round 1

The following two independent reports record the same frozen initial Full snapshot.
Their findings were subsequently classified by [separate triage](technology-navigation-triage.md);
repair and Delta evidence are separate records. No repair occurred between these reviews.
The behavior report's closing reference to human triage does not add a human-only
repair gate: the canonical policy requires separate triage and human merge/release approval,
as explicitly resolved in the triage record.

---

# Independent Full review A — behavior and compatibility

Reviewer: `/root/tech_full_behavior` · 2026-10-14 · read-only Full round 1.

## Verdict

**CHANGES REQUIRED: one confirmed in-scope finding, TNAV-B-1 (P1).**
The new required-context mechanism omits existing project facts and machine core
policy from the automatically resolved document set. A real generated consumer
can change or remove either file and still verify the unchanged handoff receipt.
This is a completeness/invalidation defect in the new feature, not a claim that
the receipt authenticates Git or replaces the separate project validator.

No other in-scope defect was confirmed within the coverage below. This is neither
human merge approval nor certification. No tracked files were edited, and no
commits, remote comments, branches or PRs were created by this reviewer.

## Immutable snapshot

- Base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`
- Tree: `b2bf7b72f878033eafb2d2da4eaa0425fcbdd266`
- SHA-256 of `git diff --full-index --binary BASE HEAD`:
  `f214df661b5d168208e69a90b063cda3b07feb33591bfb71a15dfbdcd761324c`
- Task: `artifacts/technology-navigation/reviewer-a-task.json`

The reviewer independently recomputed these identities and observed a clean
tracked worktree at both the beginning and end of review. The review stayed on
this snapshot. The author disclosed the suspected missing-context issue at task
assignment; the reviewer independently checked its execution path and reproduced
it, without sharing conclusions with the other Full reviewer.

## TNAV-B-1 — bind the mandatory project/core files in resolved context

- **Severity:** P1.
- **Category:** required-context correctness / handoff integrity.
- **Confidence:** high; reproduced through the actual approved CLI against a real
  Copier-rendered consumer.
- **Location:** `scripts/navigation.py:460–472`, especially the automatic mandatory
  policy set at lines 468–472. The same function is compiled into
  `scripts/quality_framework.py`, `scripts/validate.py` and the trusted workflow.
- **Trigger:** an active navigation consumer does not manually repeat the already
  mandatory `.engineering-backbone/project.json` or `.engineering-backbone/core.json`
  in its project-owned routes. Resolve a valid request, then change or delete one
  of those files and verify against the original receipt.
- **Execution path:** `quality_framework.py verify` → `quality_errors` →
  `navigation_context` → automatic `paths` construction → document hashing →
  `expected == context`. The set includes `core.md`, quality/navigation guides,
  workflow/profile/catalog files and the task packet, but neither of the two
  consumer JSON files. Consequently their bytes do not affect the context.
- **Observed evidence:** `review-behavior-probe.json` records initial resolution
  and matching verification both exiting 0. Changing project `base_branch` to
  `release` and `validation_command` to `python tools/new_validation.py` still
  returns verify exit 0. Removing that project file also returns 0. Separately,
  setting core `human_merge_required` to false returns 0, and removing core.json
  returns 0. The unchanged original bytes are restored between independent cases.
  The receipt's actual `included_paths` confirms both omissions.
- **Impact:** a receiving agent following the returned document list is not
  guaranteed to receive the project's authoritative branch/validation facts, and
  the unchanged handoff can appear intact after those required facts change or
  disappear. The existing native essential fragment expressly requires reading
  project facts. Running the full project validator beforehand is valuable but
  does not bind valid project-fact changes into the later receipt comparison.
  This finding does not assert that changing an invariant is otherwise permitted
  by the full governance validator or that hash verification authenticates a
  revision.
- **Acceptance/contract:** plan design step 4 requires automatic mandatory
  core/project/quality documents; AC-2 requires complete required context and
  AC-3 requires stale/incomplete handoffs to fail. Existing `policy/core.md`
  identifies project facts as the source of target branch and validation commands.
- **Current-diff causation:** the new resolver and receipt mechanism introduce the
  incomplete hard-coded mandatory set. The older project facts and policy files
  predate this feature; no unrelated old defect is being reported.
- **Bounded repair direction:** include consumer project.json/core.json as
  mandatory documents, and the source layout's applicable policy/core.json.
  Keep source-vs-consumer layout explicit; do not invent a source project facts
  file where none exists. Regenerate the existing compiled artifacts/fingerprint.
- **Minimal meaningful regression:** resolve a real consumer without explicit
  manifest mappings for these mandatory files; assert both appear in `documents`;
  mutation of each must reject the old receipt and removal must reject resolution.
  Cover the source policy/core.json branch as well, retain valid unchanged
  verification and legacy/inactive behavior, and exercise the installed CLI.

## Actual review and executable coverage

Read the root instructions, common policy, contribution contract, approved plan
and reviewer packet. Inspected the complete canonical resolver (including path,
scope, instruction discovery, activation/inheritance, binding and receipt logic),
navigation schemas, compiler, quality CLI integration, all 28 technology rule
statements and profile decision guidance, catalog provenance structure, navigation
and technology guides, provider/role/skill routing additions and matching template
changes. Inspected Copier preservation and optional-install wiring, generated
entrypoint propagation, and the relevant test changes including script-file
workflow execution and predecessor fingerprint retention.

The compiled large literals were assessed through the canonical source and
compiler/integration identity checks, rather than treating independent copies of
the generated literal as separate semantic implementations. The four compiler,
predecessor/current validator and Actionlint outcomes are recorded by the separate
quality checker; the reviewer read that report and did not re-claim those runs as
his own executions.

The reviewer independently ran the 36 new targeted tests. These exercise
Python/PostgreSQL bugfix, PowerShell/Windows, Bash/Linux/container, architecture
and reviewer routes; overlapping components, include/exclude scope, descendant
instructions, missing/renamed/empty/anchored/case/symlink paths, stale/tampered
receipts, invalid technology/check bindings, authority poisoning, inactive seeds,
enabled-only activation and active inheritance; all provider combinations,
real Copier update preservation, CLI non-execution, and compiler propagation.
The passing suite did not cover TNAV-B-1; the independent probe supplies that gap.

| Independently executed command | Exit | Result |
| --- | ---: | --- |
| `git status --short` / `git status --porcelain` | 0 | No tracked changes, before/after review. |
| `git rev-parse HEAD HEAD^{tree}` | 0 | Frozen identities matched. |
| `git diff --full-index --binary BASE HEAD \| sha256sum` | 0 | Frozen digest matched. |
| `.venv/bin/python -m unittest tests.test_navigation tests.test_navigation_integration tests.test_technology_catalog -v` | 0 | 36 tests in 48.586s; OK. |
| `.venv/bin/python -m artifacts.technology-navigation.review-behavior-probe` | 0 | Real Copier/CLI probe reproduced all four unchanged-receipt false-success cases above. The script's zero exit indicates the diagnostic completed, not acceptance. |
| `git diff --check BASE HEAD` | 0 | No patch whitespace errors. |

`BASE` in the table denotes the exact base SHA above. The probe creates a temporary
render, uses the existing installed-CLI integration setup, obtains a new clean
receipt after that setup, and invokes frozen `scripts/quality_framework.py` with
`--root`, `--request` and `--expected`. It cleans its temporary consumer after use.
Only ignored review evidence was written in the repository.

## Evidence and limits

- `artifacts/technology-navigation/review-behavior-tests.log` SHA-256:
  `314bfafc6128ba891b86ad117137327a0a2e878a12d37ce1c8a2510bd8531d9f`.
- `artifacts/technology-navigation/review-behavior-probe.py` SHA-256:
  `7bd1c68a1f1966d885d8dd88a92d6b8d76c89a485af4f07f74ac69ed81ee6633`.
- `artifacts/technology-navigation/review-behavior-probe.json` SHA-256:
  `6db64ba126b32cd28bd727ac3457c807b77897ad8e91436f36643c2714840a2c`.

Read `quality-gate-report.md`: the completed whole suite is 314 tests in
1063.568s, actual exit 0 at the frozen head. The reviewer did not rerun that suite.
The earlier seven deterministic commands used an earlier head with byte-identical
production inputs; the only intervening change was the documented five-line
source-fixture repair. That distinction is preserved.

Read the actual smoke report: explicit fresh-agent context, 26 documents and
hashes, with a stale mandatory-guide refusal; native Codex startup timed out with
zero model events. The reviewer did not execute a native Codex/Copilot discovery
test and does not call the explicit-context smoke native-client evidence. No
language runtime matrix, PostgreSQL server, native Windows run, real downstream
adoption, repository settings, CI run, publication or remote review was exercised
by this reviewer. Public publisher pages were not independently re-fetched in
this review; provenance claims were checked for bounded scope, internal mapping
and explicit limitations, not external full-clause conformity.

The source policy/core.json omission follows the inspected source branch; the
executable mutation probe covers the installed consumer path. Human triage must
decide TNAV-B-1 before any repair. A bounded confirmed repair needs targeted checks
and an independent Delta review on a newly frozen snapshot.

---

# Independent Full review B — authority and security

Reviewer: `/root/tech_full_authority`; read-only independent session; 2026-10-14.
Task: `BB-TECH-NAV-008-REVIEW-B`.

## Verdict

**Two confirmed in-scope findings require separate triage before repair.** This is
not publication, merge or release approval. No tracked file, commit, branch or
remote object was changed by this reviewer. The other Full reviewer's conclusions
were neither requested nor consulted.

## Frozen snapshot

- Base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`
- Tree: `b2bf7b72f878033eafb2d2da4eaa0425fcbdd266`
- SHA-256 of `git diff --full-index --binary BASE HEAD`:
  `f214df661b5d168208e69a90b063cda3b07feb33591bfb71a15dfbdcd761324c`
- Worktree was clean on entry and after all probes/checks.

The reviewer read AGENTS.md, policy/core.md, CONTRIBUTING.md, policy/quality.md,
the approved technology-navigation plan and the scoped reviewer Task Packet.
The deterministic quality-gate report was read as preceding evidence, including
its exact 314-test PASS and its distinction between check execution and semantic
review. The full suite was not duplicated.

## TNAV-S-1 — Required project/core facts are absent from the receipt

- Severity: **P2**. Category: context completeness / stale handoff. Confidence: high.
- Location: `scripts/navigation.py:460-472`, especially the fixed policy document
  sets at 468-472; propagated through the compiled quality guard and workflow.
- Trigger: a normal consumer uses active navigation without manually registering
  `.engineering-backbone/project.json` and `.engineering-backbone/core.json` as
  extra manifest documents. These are installed files, and the existing native
  essential fragment explicitly directs agents to read project facts.
- Execution path: resolve builds the automatic document set from policy Markdown,
  guides, quality/workflow/catalog files and declared routes, but never adds the
  project facts or machine-readable core contract. Receipt verification therefore
  has no hash to compare for them. The source fixed set similarly omits
  `policy/core.json`.
- Impact: a receiver can successfully verify the old receipt after the project's
  base branch/validation command changes, after core.json changes, or even after
  these required files are deleted. Reading all returned documents still does not
  supply the project facts needed by the inherited operating contract. Prior full
  project validation does not make these documents part of a subsequent handoff.
- Independent reproduction: `full-authority-probes.py` creates a temporary copy
  of the existing active Python/PostgreSQL structural fixture, adds valid project
  facts and the actual policy/core.json, then calls the frozen CLI. Resolve exits
  0, and both paths are absent from `context.documents`. Changing project branch
  and validation command then verifies exit 0 against the old receipt. Changing
  core.json then verifies exit 0. Deleting both also verifies exit 0. Exact argv,
  exits and stdout are in `full-authority-probes.json`.
- Relation/current-diff causation: approved design step 4 requires mandatory
  core/project/quality context; AC-2 requires complete required context and AC-3
  rejects stale/incomplete handoffs. The new resolver's fixed mandatory set is the
  omission. The root disclosed this suspected gap before review; the reviewer
  independently reproduced it rather than treating the disclosure as evidence.
- Minimal regression: actual installed consumer resolution must include both
  required JSON files and their exact byte hashes without extra manual mapping;
  mutation or removal must reject the prior receipt. Cover the corresponding
  mandatory source core contract and document its project-facts source mapping.
  Legacy absence/inactive installations must retain their existing compatibility.

## TNAV-S-2 — Technology checks use candidate definitions instead of approved execution definitions

- Severity: **P1**. Category: check-authority bypass. Confidence: high.
- Location: `scripts/navigation.py:229-235,271-279,451-452,534`; contrast existing
  `scripts/quality_framework.py:933-944` and
  `scripts/workflow_kit.py:227-237`.
- Trigger: an active approved base has an existing workflow check ID, such as
  `reserved`, whose approved kind is `docs`. A candidate adds the PostgreSQL
  technology profile and binds its migration requirement to that ID while changing
  the candidate definition's kind to `migration` and its command accordingly.
- Execution path: existing workflow preparation substitutes the approved base's
  full definition for every existing check ID. Existing core-quality coverage
  likewise uses those effective definitions. New navigation instead builds its
  check map directly from candidate workflows.json, tests technology kind/phase
  coverage against that map, and emits candidate check definitions in the receipt.
- Impact: a mandatory PostgreSQL migration binding passes validation and handoff
  verification even though the actual prepared workflow has no migration-kind
  check. The recipient's supposedly concrete check definition also describes a
  different command from the approved command that the workflow will execute.
  This is a deterministic authority mismatch, not a concern about whether a
  correctly bound command has adequate semantic test coverage.
- Independent reproduction: the temporary base selects Python, has active valid
  quality/workflow/navigation and an unused `reserved` docs check. Database
  capability and the fixture migration check are removed before creating the
  base; base quality validation exits 0. The candidate adds PostgreSQL with
  `test` + `reserved` bindings and relabels `reserved` as migration. Frozen
  `quality_framework.py resolve --trusted-base ...` and `verify` both exit 0.
  Frozen `workflow_kit.py prepare ... --phase pr` also exits 0, but its reserved
  check remains `kind: docs`, command `print("docs-only")`, and the complete
  prepared configuration has **zero migration-kind checks**. The receipt claims
  `kind: migration`, command `print("candidate-migration")`. No project command
  was executed. Exact outputs and the two definitions are in the probe JSON.
- Relation/current-diff causation: design steps 4/6 and AC-2 require actual check
  bindings without weakening trusted execution authority. This new navigation path
  bypasses the approved-definition substitution already present for core quality
  and workflow preparation. It is introduced by this diff.
- Minimal regression: with an active trusted base, relabeling an existing docs
  check as migration must not satisfy a new PostgreSQL technology binding.
  Conversely, a candidate edit must not invalidate coverage still supplied by the
  approved effective definition. Receipt check definitions must match the actual
  approved/prepared definitions for existing IDs; genuinely new IDs retain the
  established workflow contract. Exercise source guard, compiled guard and
  installed CLI, including enabled-only activation and inherited-active cases.

## Coverage and execution

Inspected the whole scoped change by canonical implementation and generated
correspondence, with emphasis on:

- Resolver path validation, exact-case checks, regular files/symlink/reparse
  rejection, root ancestry, bounded traversal, Markdown-anchor limitations,
  Task Packet validation, include/exclude matching, component unions and role
  derivation; explicit non-authentication of declared revisions.
- Inactive/legacy behavior, complete-seed activation, active route/profile/check
  inheritance, mandatory-document selection and whole-context equality.
- Compiler text/AST handling, literal catalog ownership and candidate nonexecution;
  quality validator/CLI integration; generated validator/workflow distribution and
  rendered toolchain identity.
- Both navigation schemas; all 28 rule statements and profile recommendations/free
  choices; source provenance and certification boundaries; PowerShell, Bash,
  PostgreSQL and C++ conflict/tool distinctions.
- Source and template entrypoint/role/skill routing, project-owned Copier preservation,
  adoption/manual native-body merge guidance, source/consumer path correspondence.
- Added navigation/catalog/integration tests and the existing test-harness changes
  needed to avoid single-argument limits. The harness still executes the same
  script text; no assertion/gate deletion was observed.
- Actual quality-gate and explicit-context smoke reports; native-client limitations
  are accurately separate from structural and explicit-context claims.

Executed independently (all from the repository root):

| Command/check | Exit/result |
| --- | --- |
| Git head/tree/full-index patch identity and status | 0; exact frozen values and clean |
| `.venv/bin/python artifacts/technology-navigation/full-authority-probes.py` | 0; assertions reproduce both defects; eight child CLI operations exit 0 as recorded |
| `.venv/bin/python -m unittest tests.test_navigation tests.test_technology_catalog -v` | 0; 31 tests in 5.836s, OK |
| `.venv/bin/python scripts/compile_navigation.py --check` | 0 |
| `.venv/bin/python scripts/compile_quality_framework.py --check` | 0 |
| `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | 0; `f2779766e59c95a83f3ab6871f2435336cd02316ab646145cb591000e357ab06` |
| `git diff --check BASE HEAD` | 0 |

The probe harness was rerun once after restoring the required JSON files before
its second, independent scenario; both findings reproduced identically. All
fixture mutations were in automatically deleted temporary directories. Only
ignored review/probe/log files were written inside the repository.

## Unreviewed and unexecuted boundaries

No fresh re-fetch of all 38 external publisher pages was performed in this Full
review; provenance text and bounded organization-owned adoption were inspected.
No language/database/platform application test suite was run. No native Codex or
Copilot discovery, account login, CI workflow on GitHub, remote review, branch
protection setting or downstream adoption was exercised here. The recorded native
Codex startup timeout remains unverified loading; no native PASS is inferred from
the 26-document explicit-context receiver smoke. Source/browser compatibility is
not certified. Compiler checks establish equality, not semantic correctness.

## Evidence digests

- `full-authority-probes.py` SHA-256:
  `73b07123a43465d9110a3e6814dd668d8f7b2a37f78a0aeb35731039c09e1f77`
- `full-authority-probes.json` SHA-256:
  `5354dfec28ca099e6d6197ccb7013f3e5585a167401ff5270e9dbc76a8100ee6`
- `full-authority-targeted.log` SHA-256:
  `5cdfb0c419e38c4e343ee853fdb16d6dde23d6147bc06db050da5ecf71c11395`
