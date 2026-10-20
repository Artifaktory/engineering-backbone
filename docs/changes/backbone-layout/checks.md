# Layout refactor deterministic check record

Quality-checker session: `layout_quality`. This record reports execution evidence;
it is not independent semantic review, human approval or merge readiness.

Base: `212608aa50ee517b3dd3107a9480da997222fd4f`. Candidate snapshot and final
patch identity will be recorded after checks and before independent Full review.

## Baseline and available environment

- Python 3.12.14 in an isolated environment installed from the baseline hash-locked
  requirements. `python -m pip check`: exit 0, no broken requirements found.
- `git rev-parse BASE^{tree} PREMERGE_HEAD^{tree}` independently confirmed that
  base `212608aa50ee517b3dd3107a9480da997222fd4f` and premerge head
  `4e2f1272e34c3472cb1afe559e87347b9e2579ec` both have tree
  `c31ee9b6e418325936b59e31cd7e9b9865ed0064`. Their diff is empty.
- Baseline `python scripts/validate.py`: coordinator executed, exit 0. The validator
  expressly reported no trusted-base comparison and no proof of human approval.
- Baseline `python -m unittest discover -s tests -v`: coordinator executed, exit 0;
  completed log inspected by the quality checker: 418 tests, 373.388 seconds, OK.
- Baseline actionlint 1.7.12 with `-shellcheck= -pyflakes=`: quality checker executed,
  exit 0. Optional ShellCheck and Pyflakes analyzers were not run.
- Docker and Podman were not found on PATH. Container build and offline image smoke
  are unexecuted locally; this does not establish container compatibility.

## Candidate checks

Pending the coordinator's ready signal. No candidate PASS is claimed yet.

## Legacy trusted-base gate

Pending actual invocation of the previous validator against the candidate. The
approved plan expects an incompatible-path failure and preserves it as a blocked
merge gate. No candidate fallback or path projection will replace that result.

## Coverage limits

Native Windows, live OpenCode/model behavior, OS isolation and product runtime
qualification are not established by these checks. Candidate structural checks,
legacy consumer compatibility and direct-copy smoke will be reported separately
from the expected previous-layout gate failure.
