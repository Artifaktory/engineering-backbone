# CI clone repair: verification evidence

## Snapshot and environment
Implementation: `f6d483bccd1b688c1749ac1dd6ed54080167de92`.
Base: `465d11c31c82e0beae1ddcd54b8eb325ce94c1f3`.
Local Python 3.12.14, Git 2.51.1, locked Copier 9.11.3. Dependencies installed
with `python -m pip install --require-hashes -r requirements.lock`, exit 0.

Independent quality checker `ci_clone_quality` ran the complete suite once and
the five checks below against the clean implementation snapshot. Its monitoring
session resumed after a provider capacity interruption; the existing test process
continued and was not restarted. Raw records are in ignored
`artifacts/ci-clone-race/`.

## Failure and regression
- Original [post-merge run 38291266449](https://github.com/Artifaktory/engineering-backbone/actions/runs/38291266449),
  job 114951680854, failed on Git 2.55.0 in the historical upgrade nested under
  `test_historical_compatibility_survives_autocrlf_source_checkout`.
  Copier's raw filesystem clone reported exit 128 / loose-object copy ENOENT.
- Unmodified targeted autocrlf test locally: 1 test, 33.769 s, exit 0. Therefore
  do not represent the hosted failure as deterministic or caused by CRLF.
- Controlled object-removal experiment: raw local clone exit 128 with the same
  ENOENT message; original source `git fsck --full` exit 0; same injected window
  using file transport clone exit 0, identical HEAD and cloned fsck exit 0.
  `python artifacts/ci-clone-race/deterministic-local-copy-repro.py`, exit 0.
  This one-off diagnostic uses a C interposer; the committed suite does not.
  The original hosted process that removed/moved the object remains unidentified.
- New native Git negative regression before the URI repair:
  `python -m unittest tests.test_workflows.WorkflowTests.test_real_copier_upgrade_without_local_object_copy -v`,
  1 test, 1.548 s, **exit 1 as expected**. Valid source with aliased object store
  rejects raw local copy; unchanged Copier raw-path adoption also fails.
- After repair, run the new regression, existing real-upgrade test, clean
  single-commit checkout and autocrlf checkout together: **4 tests, 92.427 s,
  exit 0**. All existing local-fact, stricter-instruction, policy, attestation and
  trusted-validation assertions remain present and execute.

The object-store alias is solely a deterministic negative control in a disposable
Git fixture; it is not a claim about the original CI timing or production symlinks.

## Required checks
All commands use the isolated `backbone-venv/bin/python` where applicable.

| Command | Result |
| --- | --- |
| `python scripts/validate.py` | Exit 0 |
| `python scripts/compile_toolchain_fingerprint.py --check` | Exit 0 |
| `python scripts/compile_workflow_kit.py --check` | Exit 0 |
| Base-owned `scripts/validate.py --root candidate --trusted-base trusted-base` | Exit 0 |
| `git diff --check 465d11c31c82e0beae1ddcd54b8eb325ce94c1f3 HEAD` | Exit 0 |
| `python -m unittest discover -s tests -v` | **234 tests, 472.570 s, exit 0; no skips** |

Rendered tooling fingerprint remains
`7e3d27e21a8db1b1320ded8b8c499dd6033a3f45b0b4b7ff519316612f83ddeb`.
Workflows, scripts, schemas, templates, dependencies, historical fixtures and
policy are byte-identical to base. No CI gate, retry policy or assertions removed.
The test addition accounts for 233 → 234 tests.

## Acceptance and pending evidence
AC-1 (mechanism and limits), AC-2 (red/green actual upgrade) and AC-3 (required
checks) are supported above. Independent Full review and triage for AC-4 are
recorded in [the review result](ci-clone-result.md).
Actual published identity, CI and advisory review are AC-5 and remain pending
until observed in the commit-bound PR closeout. Human merge is separate.
Post-merge push success is unexecuted before a human merges the repair PR.
