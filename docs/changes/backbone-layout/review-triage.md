# Independent Full-review triage

Triage session: `layout_triage`, separate from implementation, deterministic
checking and the Full reviewers. Date: 2026-10-20. This report classifies supplied
Full-review findings before repair. It does not certify implementation or approve
merge, release or downstream adoption. This session changed no source or tests.

## Bound snapshot and coverage

- Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Full-review head: `54501f1ed542e7f42b5aa315db8863b35e80aeed`.
- Binary patch SHA256 (`git diff --binary BASE HEAD`):
  `3d55fa71f514b9e39f798920188f5186db72b03ef6ea83de576e87f4e8c090bd`.
- Read-only review checkout: `backbone-layout-review`; its HEAD and patch digest
  were independently checked against the coordinates above.
- Local bounded reproductions used Python 3.12 from `backbone-venv` at the review
  repository root. They do not establish native Windows or real-model execution.

Inspected the relevant canonical review rules, Task Packet and plan; the native
OpenCode workflow, moved runner, portable smoke tests, native and companion
configuration; and the adoption guide, legacy dependency template and Copier
preservation list. Compared the affected baseline files and current diff. This
triage is limited to submitted findings and their causal paths, not another Full
review of the entire patch. Read the completed
[behavior Full report](behavior-review.md) and
[security Full report](security-review.md), both bound to this same snapshot.
The behavior report supplies LBEH-01 through LBEH-03. Security reports no additional
confirmed in-scope security finding; its LBEH-01 reproduction is the same issue,
not a duplicate repair item. No submitted finding remains unclassified.

## Finding dispositions

### LBEH-01 — confirmed, P2, high confidence

**Category/location:** CI test discovery;
`.github/workflows/opencode-native.yml:36`.

**Trigger and impact:** The Ubuntu and Windows jobs execute
`python -m unittest tests.test_opencode_native_smoke -v`. This diff relocates the
test to `.engineering-backbone/tst/test_opencode_native_smoke.py`, leaving no root
`tests` package. The ordinary failing test step stops the job before the subsequent
native smoke command. The promised native check cannot run through this workflow.

**Independent evidence:** Running the exact workflow command against the frozen
head returned exit **1**, `ModuleNotFoundError: No module named 'tests'`, and
`FAILED (errors=1)`. The bounded replacement command
`python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p test_opencode_native_smoke.py -v`
returned exit **0**, **11 tests**, **0.677 seconds**, `OK`. This only proves portable
failure-path test discovery/execution; it is not actual native runtime evidence.

**Diff causation/contract:** The original root test package existed at the base;
the relocation changed the import path without updating this caller. The refactor
must preserve runnable existing CI checks.

**Bounded repair and regression:** Update this test invocation to discover the
moved suite, and verify the workflow's actual invocation executes the intended
tests from a clean repository-root context. Preserve the matrix, pinned actions,
permissions, subsequent native smoke and artifact handling. Do not skip failures
or remove tests. LBEH-03 remains an independent downstream blocker after this fix.

### LBEH-02 — confirmed, P3, high confidence

**Category/location:** Legacy consumer adoption documentation;
`docs/agent-governance/adoption.md:357`.

**Trigger and impact:** A user following the explicitly retained legacy Copier
procedure is told the optional quality package supplies and preserves
`docs/operations/engineering/dependency-compatibility.md`. That is the new source
document location, not the generated consumer location. The instruction points
users at a document the described operation does not create or preserve.

**Independent evidence:** The retained template is
`.engineering-backbone/legacy/templates/{% if use_quality_framework %}docs{% endif %}/dependency-compatibility.md.jinja`.
It renders `docs/dependency-compatibility.md` when quality is selected. Root
`copier.yml:31` still protects `docs/dependency-compatibility.md` in
`_skip_if_exists`. The base's `docs/adoption.md` names that correct consumer path;
the move diff changes only the consumer-path text to the new source location.

**Diff causation/contract:** A source-layout path rewrite incorrectly altered
legacy output instructions, contrary to the documented unchanged legacy consumer
layout and preservation contract. This is distinct from the earlier repaired test
fixture issue LCHK-04.

**Bounded repair and regression:** Restore `docs/dependency-compatibility.md` in
this legacy consumer paragraph. Keep canonical source links and actual templates,
preservation behavior and direct-copy layout unchanged. Verify the paragraph
agrees with the template output and the existing dependency preservation checks.

### LBEH-03 — confirmed, P2, high confidence

**Category/location:** Native smoke repository discovery;
`.engineering-backbone/src/opencode_native_smoke.py:480`, with the default caller
at `.github/workflows/opencode-native.yml:38`.

**Trigger and impact:** Calling the moved runner without `--repo` still computes
`Path(__file__).resolve().parents[1]`. Previously, for
`scripts/opencode_native_smoke.py`, that was the repository root. It is now the
`.engineering-backbone` directory. `prepare_fixture()` consequently reads the
descriptive `.engineering-backbone/opencode.json` companion instead of the native
root `opencode.json`. Its strict native-config validation correctly rejects that
different schema. After LBEH-01 is repaired, the workflow still cannot execute its
native evidence cases successfully.

**Independent evidence:** A bounded reproduction called the real `main()` without
`--repo`, substituting only the smoke download/runtime wrapper with a function
calling the real `prepare_fixture()`. It resolved the repository to
`backbone-layout-review/.engineering-backbone`, returned **1**, and wrote
`source native config is outside the smoke contract`. Repeating with an explicit
review repository root returned **0** and recorded **22** fixture inputs. No native
binary, network download or model was executed by this reproduction. Git records
the runner as an exact-byte rename from the base, proving the old parent-depth
assumption remained unchanged through the move.

**Diff causation/contract:** Relocation invalidated an existing default CLI path;
the current workflow legitimately uses that default. Existing native fixture
validation and separation of companion metadata from native configuration must
remain enforced.

**Bounded repair and regression:** Derive the repository root correctly for the
new script location, preserving explicit `--repo` behavior. Add a focused CLI
default regression exercising real argument parsing and real fixture validation
with runtime/download work bounded or substituted. It must select root native
configuration and expected inputs without weakening `prepare_fixture()` checks,
permission restrictions, archive verification or platform/runtime claims.

## Repair gate and retained limitations

The coordinator may assign these three confirmed repairs within the reviewed
scope. Freeze the repaired head and patch digest, run the affected checks, and use
independent Delta review for LBEH-01, LBEH-02, LBEH-03 and direct repair regressions.
Prior passing deterministic tests do not negate these unexercised caller paths.
All three Full findings are confirmed; none is rejected or requires an additional
human scope decision. This immutable-snapshot classification precedes Delta and
does not claim that repairs in the live worktree have passed review.

The old trusted-base validator's known **34 path-related errors** remain the
separate, disclosed draft migration blocker. This report does not authorize
suppressing them, accepting candidate-owned trust, projecting the candidate into
the old layout or broadening the migration. Local container unavailability and
unexecuted native Windows/model qualification remain visible. Passing bounded
tests or this triage cannot waive those limitations or authorize merge.
