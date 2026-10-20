# PR 18 repeated local-clone failure: confirmed bounded repair

Date: 2026-10-20. Independent triage: `correction_triage`.
Snapshot: `2ddfa803688c70b556dc83bcf07a4c3911713be5`, tree
`ae42d5f1848b65509e51813b824b7d9c2b61a6cc`.
This follow-up preserves the original diagnostic report and supersedes its
one-time transient disposition after the permitted single rerun also failed.

## COP-CI-02 — historical-upgrade fixture selects fragile local clone transport

**Confirmed; P2; test fixture portability/reliability; high confidence in the
observed transport failure, not in an unobserved underlying Git/OS race.**

The first Foundation job `118626214062` and its single rerun `118631415944` in
workflow `39422351687` fail at the same first optional-profile subtest and exact
Copier clone path. The second run reports **433 tests in 301.297 seconds,
errors=1**. Both run Git 2.55.0 and Python 3.12.15. The second failure is again
Git exit 128 while copying a loose object into its temporary clone; it names a
different object and temporary directory. Retry traceback SHA256:
`d7eb3a087b8597b50205ebed5b06607bbe54ff3075f46a169233c01bc5053fdc`.

Location: `.engineering-backbone/tst/test_copilot_distribution.py`,
`test_historical_upgrade_adds_package_without_replacing_local_authority`, initial
`run_copy(str(source), ...)` at line 295 and subsequent `run_update` at line 341.
Copier records the raw filesystem source path in its answers file and reuses it
for later template clones. This selects Git's optimized local object-copy mode.
The failure prevents the existing installation-only rejection assertion and
subsequent real upgrade verification from executing normally.

The failing method and transport setup predate BB-LAYOUT-012's selector correction;
there is no demonstrated selector-code cause. Its repeated failure on the current
supported CI runner is nevertheless an actionable failure within the authorized
red-check repair and existing test-file scope. Another same-head retry is not
justified. Do not label a specific Git race or corruption mechanism as proven.

## Transport evidence and minimal repair

Inspected installed Copier `_vcs.py:get_repo/clone`,
`_template.py:local_abspath/url_expanded` and
`_main.py:_answers_to_remember/template`:

- Copier passes its expanded URL directly to `git clone --no-checkout` and, on
  these Git versions, adds `--filter=blob:none`.
- An unadorned `file://` URL without a `.git` suffix is not recognized as a Git
  template by this Copier version. A `git+file://` URL is recognized; Copier strips
  only `git+` before calling Git.
- Answers retain the original `template.url`; `run_update` recovers that URL.
  Thus selecting the transport on the initial copy also governs later updates.
- Both revisions in this fixture are committed and tagged before use. Its
  contract does not require Copier's dirty-local-HEAD inclusion behavior.

The official [Git clone manual](https://git-scm.com/docs/git-clone), OPTIONS
`--local`, states that raw local paths use the object-copy optimization while
URLs use normal transport. This supports choosing a URL to avoid the observed
copy path; it does not identify the exact underlying failure mechanism.

**Minimal permitted repair:** construct
`source_url = "git+" + source.resolve().as_uri()` inside this one historical
upgrade fixture and pass it to the initial `run_copy`. Preserve both tagged
revisions, all real Copier copy/update operations, all existing assertions,
installation-only negative cases and unchanged local-authority checks. Add
focused assertions that the rendered answers retain this `_src_path` and the
requested old/new `_commit` tags, so the tested transport remains explicit.

Do not edit the answers file manually in the real regression, change pins,
global/local Git settings, templates, runtime authority or workflow gates. No
retries, exception suppression, skipped subtests or weakened assertions belong
in this repair. The URI is a local-file transport, not a network service.

## Diagnostic probe and required validation

A disposable tagged Copier fixture probe on local Git 2.51.1 confirmed:
plain `file://` is unrecognized; `git+file://` expands exactly to the file URL;
actual `run_copy` at `v0.1.0` and `run_update` at `v0.2.0` render the expected
versioned content. Probe exit **0**. Its tiny fixture explicitly provided an
answers record; production answer persistence is established by inspected Copier
code and must be asserted in the actual repaired regression. This probe is not
the repaired project test or remote Git 2.55 qualification.

The implementer must run the actual historical-upgrade method and affected
Copilot modules with the repaired fixture, retaining every original assertion.
The independent checker/reviewer then binds the new snapshot and confirms the
bounded transport change. Publication must rerun the final committed-diff checks
and observe the actual changed-head Foundation result under remote Git 2.55.
If that changed-head check fails, diagnose its evidence; do not retry unchanged
inputs again or claim local results certify it.

No repository source/test edits or additional remote retries were performed by
this triage session. The separate old trusted-base layout gate remains blocked
until its reviewed prerequisite becomes actual trusted main code.
