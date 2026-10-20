# Layout refactor deterministic check record

Quality-checker session: `layout_quality`. This record reports execution evidence;
it is not independent semantic review, human approval or merge readiness.

Base: `212608aa50ee517b3dd3107a9480da997222fd4f`. Initial candidate: `76f78da89d4646fb6a9332fd2d76d8a4d512647a`. The quality checker
recorded all 531 candidate file hashes before and after the initial suite: no input
changed during execution. Semantic review uses its separately frozen head/patch.

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

All commands below used the isolated Python 3.12 environment from the repository
root. Exit codes were individually captured. These initial results bind candidate
`76f78da89d4646fb6a9332fd2d76d8a4d512647a`.

| Command | Exit | Observed result |
| --- | ---: | --- |
| `python .engineering-backbone/src/validate.py` | 0 | Structural PASS; no trusted-base comparison. |
| `python .engineering-backbone/src/check_source_dependencies.py` | 0 | Tracked inputs, all 26 installed locked versions and dependency consistency. |
| `python .engineering-backbone/src/maintenance/compile_navigation.py --check` | 0 | Compiled technology/navigation authority matches. |
| `python .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | 0 | Compiled quality catalog/entrypoints match. |
| `python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | 0 | Compiled workflow entrypoints match. |
| `python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | 0 | Rendered legacy bundle fingerprint matches. |
| `actionlint -shellcheck= -pyflakes=` (1.7.12) | 0 | Workflow syntax check; optional analyzers unexecuted. |
| `git diff --check` and `git diff --cached --check` | 0 each | No whitespace errors. |
| `python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v` | 1 | 428 tests in 402.726 seconds; 34 failures and 1 error, including subtests. |

The initial full suite is **FAILED**. Its failures concern source/legacy policy-link
expectations, source/generated native navigation and instruction-glob parity, an
unrelated-application test fixture writing the governed policy path, and legacy
dependency-document fixture paths. Separate triage must classify these before
repairs; no failed check is waived here. The final tracebacks, rather than an early
progress grep, are the authoritative run result.

The independent mapping check compared `layout-map.json` against `git ls-tree -r -l`
at the base: all **495** baseline blobs occur once, all destinations are unique,
regular and present, and all **152** `preserve_bytes` destinations exactly match
their recorded Git blobs. No map claim was accepted without comparing the base.

A separate actual old-main-to-new `copier.run_update` experiment was independently
rerun with the reviewed harness: exit 0. It creates a temporary Git source from the
exact base, tags it, creates an all-options legacy consumer, appends a local
`AGENTS.md` instruction, records project facts, replaces the temporary source with
the candidate and invokes `run_update` with the original answers file. The local
instruction and project-fact bytes survived, no `.rej` files appeared, and the
updated legacy validator exited 0. This supplemental check does not cancel the
full-suite failures or establish the previous source validator's approval.

Harness SHA256: `676a669c99b7a01f4cb33b3ee94cc25f3f5ebf78a290483bc59cbf60b9077c8f`.
Initial full-suite log SHA256: `b91eb1743e1e06a7a74f2ead6d5af3c8f29bccaf0aa8dc073a5d1961d113d772`.
Legacy update log SHA256: `440e03c6fb2e4a4fc73cc501c68c88a6455a1e3f6d8542c3f9dcdad0748ccfd9`.
Raw logs remain ignored run artifacts, not checked-in qualification certificates.

## Legacy trusted-base gate

Executed the actual validator from base
`212608aa50ee517b3dd3107a9480da997222fd4f`, using the equivalent absolute paths for:

```sh
python trusted-base/scripts/validate.py --root candidate --trusted-base trusted-base
```

**Exit 1: 34 structural validation errors.** The old validator requires old
`policy/core.json`, `policy/core.md`, dependency manifests and source instruction
paths; it also interprets relocated historical links in the old path context.
This is the expected incompatible-layout result, and remains a **blocked merge
gate**. It is not PASS. No candidate fallback, projection or suppression ran.

Raw trusted-base log SHA256:
`7e03c0d035111002e72a10a50dc47dbaf9748bda17515fdf951888b4d3c52216`.

## Coverage limits

Native Windows, live OpenCode/model behavior, OS isolation and product runtime
qualification are not established by these checks. Candidate structural checks,
legacy consumer compatibility and direct-copy smoke will be reported separately
from the expected previous-layout gate failure.
