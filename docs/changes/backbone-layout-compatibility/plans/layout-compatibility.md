# Trusted source-layout compatibility prerequisite

Status: proposed for independent plan review. Task: [BB-LAYOUT-013](layout-compatibility-task.json).
Base: `212608aa50ee517b3dd3107a9480da997222fd4f` on `main` in
`Artifaktory/engineering-backbone`. Work branch: `fix/trusted-layout-compat`.
The user's 2026-10-20 request to correct PR #18's red checks authorizes preparing
this necessary same-repository prerequisite; it does not authorize merge.

## Problem and bounded outcome

[PR #18](https://github.com/Artifaktory/engineering-backbone/pull/18) changes the
source layout. Its published head `c50108773ba3195bf0f7503e5dffb2d7bfc78cd3` passed
432 unit/compatibility tests, the container job and native Windows/Linux smoke.
Its old-main trusted validator nevertheless reports 34 path/context errors.
That validator requires the old policy, dependency and native instruction paths
and interprets relocated history at its new location. The separate whitespace
and Copilot corrections belong to BB-LAYOUT-012, not this implementation.

This prerequisite keeps the **old repository layout** on `main` and teaches its
trusted source checks both old and new canonical layouts with the same policy,
schema, adapter, dependency, link and historical-integrity obligations. The actual
old-main validator must accept this prerequisite at its existing paths. Only after
a human merges this prerequisite may PR #18 obtain the new code from its trusted
base. There is no candidate-code fallback, projected tree, waived error or skipped
gate, and this delivery cannot claim PR #18 green before that base transition.

## Authority and layout selection

1. Keep source-versus-consumer identity owned by the executing trusted bundle.
   A candidate's files, metadata, flags or missing paths cannot select consumer
   mode, suppress source checks or execute candidate validation code.
2. Within source mode only, resolve candidate and trusted-base roots independently
   to one of the two explicit reviewed source contracts. Old policy paths remain
   valid for the prerequisite and its base; new paths apply to the PR #18 tree.
   Reject missing, ambiguous or mixed canonical authorities. No fallback after a
   malformed selected policy and no symlink aliases to make one layout resemble
   another. Product-owned root dependency/build files are not layout selectors:
   the new contract can coexist with those legitimate project files.
3. Keep schemas, policy floors, compiled catalogs and historical exceptions owned
   by the executing reviewed bundle. Read each snapshot's policy from its own
   selected canonical location; preserve every prior stricter invariant and
   enabled-adapter constraint across old-to-new comparison.
4. Retarget source-only native instruction tuples, dependency input locations and
   navigation document paths through the explicit source contract. A new source
   layout never receives the weaker legacy-consumer path contract. Permissions,
   provider activation, native identity and failure propagation stay unchanged.
5. For the new source layout, reuse the previously reviewed 495-path crosswalk and
   88 historical path/hash entries only after comparing them to actual base Git
   blobs. Embed the authority into the executing validator or its compiled trusted
   literals. Candidate `layout-map.json`, candidate code, schema changes or project
   flags cannot create historical exemptions. Verify archived bytes before resolving
   historical links in their original context; current documents and named new
   task/review records still receive normal link/schema checks.
6. Keep existing consumers and their generated paths unchanged. Use existing
   standalone guard/compiler boundaries; any helper required by a compiled guard
   must be included in that guarded executable, not imported from the candidate.
   Do not copy PR #18's validator wholesale: its current single-layout policy
   lookup cannot read an old-layout trusted base correctly.

## Intended implementation ownership and files

- Runtime implementer: `scripts/validate.py` and `scripts/navigation.py`; only
  directly necessary generator changes in `scripts/compile_navigation.py`,
  `scripts/compile_quality_framework.py` or `scripts/compile_toolchain_fingerprint.py`.
  A small source-layout helper is permitted only if its authority and standalone
  compilation are explicit and independently reviewed.
- Generated outputs: `scripts/quality_framework.py`, compiled portions of
  `scripts/validate.py` and `.github/workflows/governance-checks.yml`. Regenerate
  through the maintained compilers. Do not weaken workflow event, repository,
  permission, pin, trust, whitespace or compatibility gates.
- Test implementer: focused source-layout transition cases under `tests/`, plus
  required updates to existing fingerprint/guard expectations. Preserve all 418
  original test methods, assertions and immutable historical fixtures. New test
  data must record exact provenance and must not replace existing fixtures.
- Coordinator/documentation: current task references in `AGENTS.md` and
  `CONTRIBUTING.md`, this plan/packet, and new `docs/reviews/layout-compatibility-*`
  evidence. Historical plans/reviews remain unchanged.

No file relocation, new product scaffold, schema change, core invariant change,
dependency version change, native permission change, adapter activation, repository
setting, artifact service, deployment or external-repository change belongs here.
The existing rendered bundle fingerprint changes when its validator bytes change;
regenerate it and retain only the explicitly reviewed previous current identity
needed by existing consumers. Do not add arbitrary or candidate-derived identities.

## Verification contract

Run checks in the existing isolated Python 3.12 environment using the unchanged
hash-locked dependencies. Start with the new transition cases, then affected guard
and consumer suites, and the complete suite. Required evidence includes:

| Boundary | Positive evidence | Negative evidence |
| --- | --- | --- |
| Prior trust | Actual base `scripts/validate.py` accepts the old-layout prerequisite against the actual base. | No candidate executable, copied policy alias, projection or waived exit code participates. |
| Cross-layout source | Prerequisite validator accepts an exact, separately frozen PR #18 tree against the old-layout base; old-source self/base validation still passes. | Missing or dual canonical policies, partial mixed layouts and policy symlink ancestors fail. |
| Policy and schemas | Prior stricter invariants and valid named new task/review records remain supported. | Removed/weakened invariant, candidate schema replacement, malformed new task/evidence and implementer-as-reviewer fail. |
| Native adapters | Reviewed old/new source instruction tuples pass their respective contracts. | Disabled previously enabled adapters, broadened native permissions and consumer-like metadata cannot bypass source checks. |
| History | Actual reviewed archive bytes and original-context links pass in the new layout. | Changed archive bytes/hash claims, forged candidate mappings, missing mapped targets and broken current links fail. |
| Dependencies | Exact old/new source tooling manifests pass while legitimate new-layout project root files coexist. | Missing, malformed or conflicting selected tooling manifests still fail; alternate root manifests cannot hide them. |
| Consumers and generated guards | Existing initial-copy, real update, historical and fingerprint checks pass; all compilers report exact output. | Existing rejection coverage, mixed/unknown bundle identities and stronger local-policy protections remain. |

The cross-layout fixture or harness must bind its source commit/tree and verify its
actual file bytes; merely naming a test after PR #18 is not transition evidence.
It may read or copy the frozen PR #18 tree, but must execute the prerequisite's
trusted validator and schemas. Never transform the candidate back into old paths
and report that as a successful new-layout validation.

Commands include `python scripts/validate.py`, all four compiler `--check` commands,
`python scripts/check_source_dependencies.py`, and
`python -m unittest discover -s tests -v`. Also run available Actionlint and both
working-tree and **committed base-to-head** whitespace checks. Record each exit
code and exact revisions. The source dependency checker requires tracked inputs;
stage required new inputs before running it.

Use actual container/native CI evidence for this prerequisite when available;
prior PR #18 success does not establish a changed prerequisite's runtime result.
If a local engine or platform is unavailable, record the limitation and observe
its remote job separately. Do not claim model qualification or OS isolation from
structural/unit checks.

## Review chain, budgets and publication order

1. Independent read-only plan review precedes implementation. The planner does
   not certify its own plan and the implementer does not act as its reviewer.
2. Implement bounded runtime and test changes in separate ownership scopes.
   A separate quality checker runs deterministic checks and records actual results.
3. Freeze base/head/tree and a binary patch SHA256. Two independent reviewers use
   that same immutable snapshot: behavior/consumer compatibility and security/trust.
   Report coverage, limitations and concrete diff-caused findings with stable IDs.
4. A separate triage session classifies findings before repair. Repair confirmed
   findings only, recheck affected behavior, then freeze and perform Delta over
   those IDs and direct regressions. At most two Full rounds and six implementation
   iterations apply; changed scope/trust boundaries require explicit new review.
5. Publish the separately scoped prerequisite PR targeting `main`, with exact
   remote head/tree and real check states. No merge, release or downstream apply.
   Record acceptance as observed pass, fail, blocked or pending; no invented PASS.
6. **Human action:** merge the reviewed prerequisite first. A later authorized
   continuation integrates that actual `main` into PR #18 without force push,
   reconciles the moved runtime/compiled files and records needed mappings for any
   new prerequisite evidence. Then rerun the trusted transition, relevant tests and
   remote checks against the actual updated base. PR #18 stays draft/blocked until
   this happens; this preparation does not pre-authorize either merge.

The closeout must identify the remaining human merge dependency and the exact
handoff, so an existing red PR #18 gate is never hidden by a local simulation.
