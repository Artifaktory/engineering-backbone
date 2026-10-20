# Independent deterministic quality gate

Task: `BB-TECH-NAV-008` · Checker: `/root/technology_quality_gate` · 2026-10-14

## Verdict and boundary

**PASS — deterministic checks for the repaired frozen snapshot.** The only
observed whole-suite failure, QG-001 (root triage ID TQ-1), was diagnosed,
repaired in a source fixture, independently checked, and followed by a successful
complete 314-test run. This permits the planned independent Full reviews to begin;
it does not approve semantics, merge, release, publication, or downstream adoption.

The checker performed no tracked edits or GitHub writes. This ignored report is
the only requested evidence artifact written by the checker. The implementer ran
the complete suites; the checker independently inspected their final logs and the
repaired suite's actual exit sidecar, without restarting either complete suite.

## Frozen identity

- Base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Repaired head: `6e5758deb7767c2915505b9646f1a09e0cc0b174`
- Tree: `b2bf7b72f878033eafb2d2da4eaa0425fcbdd266`
- SHA-256 of `git diff --full-index --binary BASE HEAD`:
  `f214df661b5d168208e69a90b063cda3b07feb33591bfb71a15dfbdcd761324c`
- Previous checked head: `8325771225dd44d27a6eecac31f32652b32ed1e5`
- Previous patch SHA-256:
  `5bc68e6910bbcd76494a3d18924b67ba17ef318fa3c7d2dc334683d3694b17bb`

The checker recomputed the repaired head, tree and patch identity and observed a
clean worktree after the complete repaired run. The exact delta from the previous
checked head is five added lines in `tests/test_quality_framework.py`; production
guards, compilers, workflows, catalogs, templates and dependencies are unchanged.

## Independently executed checks

All commands ran from the repository root with the existing Python 3.12 venv.

| Command | Exit | Observed result |
| --- | ---: | --- |
| `.venv/bin/python scripts/validate.py` | 0 | Structural contracts PASS; command explicitly states no trusted-base history comparison was performed by this invocation. |
| `.venv/bin/python artifacts/trusted-base/scripts/validate.py --root . --trusted-base artifacts/trusted-base` | 0 | Exact predecessor structural and trusted-base compatibility check PASS. |
| `.venv/bin/python scripts/compile_navigation.py --check` | 0 | Compiled technology/navigation authority matches source. |
| `.venv/bin/python scripts/compile_quality_framework.py --check` | 0 | Compiled quality authority and entrypoints match source. |
| `.venv/bin/python scripts/compile_workflow_kit.py --check` | 0 | Compiled workflow-kit entrypoints match source. |
| `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | 0 | Actual rendered tooling matches the pinned current fingerprint. |
| `artifacts/tools/actionlint -shellcheck= -pyflakes= .github/workflows/*.yml` | 0 | Actionlint 1.7.12; external ShellCheck and Pyflakes integrations were disabled in this invocation. |
| `.venv/bin/python -m unittest tests.test_quality_framework -v` | 0 | Independently executed after the exact repair: 31 tests in 2.807s, OK. |
| `git diff --check BASE HEAD` | 0 | Checked both the original and repaired frozen patches. |

The first seven checks ran on the previous frozen head. Their inputs are
byte-identical at the repaired head, verified by the exact one-file test-only
delta; they were not redundantly rerun. The independent 31-test run exercised
the exact working repair subsequently committed as the repaired frozen head.

Rendered toolchain SHA-256:
`f2779766e59c95a83f3ab6871f2435336cd02316ab646145cb591000e357ab06`.

Independent Git tree comparison found all 70 protected entries identical in
blob ID, mode and path: original `standards/sources.json`, `standards/rules.json`,
`standards/profiles/`, `requirements.txt`, `requirements.lock` and
`tests/fixtures/historical/`. This remains true at the repaired head.

## Whole-suite result observed independently

Implementer command:

```sh
PIP_DISABLE_PIP_VERSION_CHECK=1 .venv/bin/python -m unittest discover -s tests -v
```

Final repaired run: **314 tests in 1063.568s, OK; actual exit 0**.
The checker read both `full-tests-repaired.log` and `full-tests-repaired.exit`,
matched the complete final summary, and found no FAIL, ERROR or FAILED summary.
The pip environment flag suppresses the optional pip version self-check; the
test command, dependency installation and required hash checks were retained.

The superseded original run completed 314 tests in 1328.021s with exactly one
failure, QG-001. It is retained as diagnostic evidence and is not the final gate.

## QG-001 / TQ-1 diagnosis and repair

The original `test_real_current_source_catalog_is_checked_without_project_profile`
constructed a central source fixture through `package(central=True)`, which
contained only the original catalog. Source validation now correctly requires
the managed technology extension as well. The missing
`standards/technologies/sources.json` caused the expected-success assertion to fail.

The checker independently reproduced these cases using disposable fixtures:

1. Core-only source fixture: missing-extension rejection.
2. Same fixture plus the actual technology extension: success.
3. Original core rule modified afterward: trusted-authority mismatch rejection.
4. Extension sources removed afterward: missing-extension rejection again.
5. Legacy consumer without navigation: success.

The confirmed repair adds `shutil`, asserts that the incomplete source fixture
is rejected, then copies the actual extension before the success assertion.
The original-rule poisoning rejection is retained. The shared package helper and
legacy consumer fixtures are unchanged; no production gate was weakened.

The independent 31-test run passed the source rejection/acceptance/poisoning
sequence and the existing legacy-absence/inactive-seed compatibility cases.
QG-001 / TQ-1 is resolved for this deterministic gate.

## Coverage inspected

Static inventory: 314 test methods across 20 modules. The checker inspected the
36 added methods: 23 navigation, 5 compiler/Copier/CLI integration, 8 catalog.
Catalog inventory: 28 profiles, 28 mandatory rules, 38 source entries.

Inspected scenarios cover Python/PostgreSQL bugfix and migration obligations,
PowerShell/Windows, Bash/Linux/container, architecture, reviewer role, overlapping
routes, descendant instructions, active inheritance, activation, path/symlink/case
and anchor failures, scope exclusions, stale/tampered receipts, check binding and
catalog authority failures, real Copier combinations/update preservation, isolated
guard execution, and installed CLI command non-execution. These are structural
and fixture tests, not proof that every language toolchain or native client ran.

## Smoke evidence and native-client limits

The checker read the smoke report and result JSON files and independently matched
all 26 selected document byte hashes against the receipt. The smoke guard is
byte-identical to the frozen `scripts/quality_framework.py`:
`eaa066e7363407c3297d45544f90d530b3cf628d6550e1e79a73d5922b5db8b3`.

The recorded matching receipt verification exited 0; modifying the mandatory
technology guide caused unchanged-receipt verification to exit 1. The isolated
explicit-context receiver reports actually reading all 26 documents and stopping
on the altered context. The checker independently verified the file hashes, not
the receiver's internal cognition or an authenticated identity.

Receipt context digest:
`5d6312ec37d6febbe84a90fda51ea41b0876c60d5928699f3e5a1a061453ca8e`.

The fixture uses declared revision `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`;
it is not authenticated Git identity or evidence of real project adoption. No
workflow/application checks were executed by that smoke.

Native `codex-cli 0.159.2` root discovery timed out after 90 seconds with explicit
EOF on stdin, normalized exit 124, zero model/JSONL events and only
`Reading additional input from stdin...` on stderr. An earlier inherited-stdin
attempt also timed out. The startup cause was not established. Nested native
discovery and Copilot native discovery were not executed. Native loading remains
unverified; the explicit-context result must not be called a native-client PASS.

## Remaining independent review and external evidence

This is a deterministic quality-checker verdict, not an independent Full semantic
review. AC2 completeness and correct document selection require those reviews.
The root has specifically raised for Full assessment whether project/core
configuration files are automatically included and bound in handoff context;
that concern was not assessed or triaged by this checker. Passing the executed
tests does not establish that no required project facts are omitted.

Two independent Full reviews, triage and any required Delta work remain separate.
PR identity, CI and requested remote Codex review also remain external publication
evidence, not results established by this report.

## Evidence SHA-256

Paths below are relative to the repository root.

| File | SHA-256 |
| --- | --- |
| `artifacts/technology-navigation/full-tests-repaired.log` | `c2da08a197929049977fc554bb0350259ee032fdee360b5c9d308fd7b3f577d8` |
| `artifacts/technology-navigation/full-tests-repaired.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `artifacts/technology-navigation/full-tests-frozen.log` | `facf9114f9a81e433b20c02c9a645ff1e0f5e3da1fcdf31868cecd04273f7d4b` |
| `artifacts/technology-navigation/source-catalog-diagnostic.log` | `473356f6ecc0be0e79e6253795944807b382157f3af0c08a90610228b7d13350` |
| `artifacts/technology-navigation/quality-source-fixture-repair.log` | `f53055f05e8d2ee8406d1fb67105435dbdae4ec01dbbbc11a0484aa8ab52112b` |
| `artifacts/navigation-smoke/report.md` | `b2b2edeee3bbfd3670ea0bb05b9fcd7fd8d66cb50bac481c3c7ce6b06c8ec73d` |
| `artifacts/navigation-smoke/structural-result.json` | `63ee128245c3a25f565beeb5e92607c7416e28b1e2666532c5ca4a805bb369a1` |
| `artifacts/navigation-smoke/explicit-context-result.json` | `989eec25973a504458eda75972c878ba1c1b36c47d96ce21fe5fae7029cb0425` |
| `artifacts/navigation-smoke/native-result.json` | `25940c77196c4eb8ebd0dc6c1aba108ca68e6f7d644e667df99e7c332c160d69` |
| `artifacts/navigation-smoke/request.json` | `9128f384b9f9a05d8d353cab7654c6453f1cc881063f9c89aa726c9af1c71da8` |
| `artifacts/navigation-smoke/context.json` | `e5206d943027f2d33c1e65a1ac7dc1374d38d452be3d012728c7df96932c78a3` |

The checker command results are additionally retained in this agent's tool
transcript. The source-fixture-repair log in the table is the author's 31-test run
(1.908s); it is distinct from this checker's independent 31-test run (2.807s).
