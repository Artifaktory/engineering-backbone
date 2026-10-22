# Ignored artifacts convention plan

Assignment `BB-ART-019`, 2026-10-22. Author/integration owner: repository
maintainer/primary implementation session. Base: `main`
`f6b950b6cc628535062578ef2f4ff3229cc8b59c`. The user authorized this bounded
change and one publication PR on 2026-10-22. Merge, release and downstream
application remain separate human decisions.

## Goal and authority

Define one explicit convention for generated, non-authoritative tool and run
outputs: the repository-level `artifacts/` directory is not itself ignored, its
contents are ignored, one tracked `artifacts/README.md` states the purpose, and
each tool or run uses its own subdirectory. Align the neutral starter, the
governance contracts, the project-mapping templates and the operations/quality
guidance. Preserve the existing source-mode `artifacts/` raw-evidence exclusion,
the managed schemas/catalogs and all stricter project controls.

The convention changes no requirement, schema state or evidence meaning. Generated
outputs remain derived, ignored and unusable as approval, PASS or verification
evidence. No credential, private transcript or personal data belongs there.

## Scope

Update `.gitignore` and add the tracked `artifacts/README.md`. Extend the neutral
starter (`starter.py`, a new `artifacts-README.md.in` and the starter entry
documents) so new exports receive the convention. State the purpose in
`docs/agent-governance/core.md`, `architecture.md`, `planning.md` and
`agent-adapters.md`, add prompts to both project-mapping templates, and align
`docs/operations/project-starter.md`,
`docs/operations/engineering/repository-controls.md`,
`docs/quality/testing.md`, `docs/quality/ci-cd.md` and the operations template
index. Add or adjust focused starter tests.

Excluded: managed schemas, standards, `validate.py`, `source_layout.py`, legacy
Copier assets, historical fixtures, workflows, dependency locks, product
placeholders, other delivery records and any permission, release or runtime
change.

## Acceptance and verification

| ID | Observable outcome | Route |
| --- | --- | --- |
| AC1 | The starter generates `artifacts/*` plus `!artifacts/README.md` and a tracked `artifacts/README.md`; a tool/run subdirectory is documented | Starter export inspection and focused test |
| AC2 | Contracts, templates and operations/quality guidance state the purpose, non-authority, ignored contents and no-secret/no-upload boundary | Document inspection and project checks |
| AC3 | Existing validator exclusion, schemas, managed baseline and stricter gates are preserved; targeted tests pass | `validate.py`, maintenance `--check`s, unittest modules |
| AC4 | Actual checks, frozen content subject, PR identity and remaining independent-review/human gates are recorded | Commands, review record and publication readback |

## Checks

```sh
python .engineering-backbone/src/validate.py
python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check
python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check
python .engineering-backbone/src/maintenance/compile_navigation.py --check
python .engineering-backbone/src/maintenance/compile_quality_framework.py --check
python .engineering-backbone/src/check_source_dependencies.py
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v
git diff --check BASE HEAD
```

The full suite runs in source CI. Independent plan/Full review and triage remain
separate; this plan records no review result. Actual local commands and limits are
recorded in [verification.md](verification.md).

## Risks, budget and recovery

Main risk: a consumer with an existing project-owned `.gitignore` keeps it, so the
new convention reaches new exports and reviewed updates only. The generated
`.gitignore` stays project-owned; the starter README is a new project-owned seed
entry. Managed bytes change only in `starter.py` and the starter `.in` set; existing
consumers adopt them through the normal trusted compare/update route. No automatic
downstream apply occurs.

Budget: three implementation iterations and at most two Full rounds. Stop on scope
or trust expansion, missing required evidence, unresolved confirmed findings or a
need to change schemas, validators or historical fixtures. Recovery is a reviewed
revert of this PR.
