# Ignored artifacts convention verification

Content subject: `e87c5e4c97d2b42d518302e7ed8d3164c09a40a7`. Candidate base
`main` `f6b950b6cc628535062578ef2f4ff3229cc8b59c`. Commands ran on 2026-10-22
with Python 3.12.13 and the reviewed tooling lock. The full suite runs in source
CI; this record keeps the local deterministic results and limits.

| Check | Actual result |
| --- | --- |
| `python -I .engineering-backbone/src/validate.py --root CANDIDATE` | Exit 0; structural contracts validated |
| Trusted-base validator from `f6b950b` against the candidate | Exit 0; no policy weakening detected |
| `compile_toolchain_fingerprint.py --check` | Exit 0; fingerprint matches rendered tooling |
| `compile_workflow_kit.py --check` | Exit 0 |
| `compile_navigation.py --check` | Exit 0 |
| `compile_quality_framework.py --check` | Exit 0 |
| `check_source_dependencies.py` | Exit 0; 26 installed locked versions consistent |
| `tst.test_starter_export` (new `test_export_seeds_ignored_artifacts_convention`) | New test PASS; export generates `artifacts/*`, `!artifacts/README.md` and the tracked README |
| `tst.test_architecture_documents`, `tst.test_testing_documents`, `tst.test_consumer_artifacts` | PASS |
| `tst.test_reference_layout` | 14 of 14 PASS |
| `tst.test_validation` | 50 of 54 PASS; four adapter/symlink cases fail identically on pristine `main` in this Windows environment and are not caused by this change |
| `tst.test_planning_documents`, `tst.test_starter_export` environment cases | Four Windows-only failures (symlink privilege, autocrlf fixture, cp1252 read, trusted-blob fixture) reproduce on pristine `main`; not caused by this change |
| `git diff --check` | Clean |

The starter export and its verifier run from a copied source fixture, not from a
published consumer update. Independent plan/Full review, triage and the actual PR
readback remain separate; no human approval or downstream application is claimed.
