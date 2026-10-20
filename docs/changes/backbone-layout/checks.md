# Layout refactor deterministic check record

Quality-checker session: `layout_quality`. This record reports execution evidence;
it is not independent semantic review, human approval or merge readiness. The
repaired candidate passes all 431 local tests. The legacy trusted-base gate still
fails, and local container execution remains unavailable.

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

## Initial candidate checks

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

## Repaired candidate checks

The independent [check triage](check-triage.md) classified LCHK-01 through LCHK-08
before repairs. It includes copy-portability regressions found beyond the first
suite's failures. Implementers repaired the bounded path/parity/test-fixture issues
and added the copy cases without changing runtime guards, schemas or historical
fixture bytes. The quality checker did not implement those repairs.

Final tested commit: `ee4f7cee7a386edfb5fb43b2763a03596b8eabf1`.
Final tested tree: `3c5db34f0158b74d2735027c31e951715ce0679f`.
All **532** candidate file hashes matched before and after this run; no input was
edited during execution. The initial failures above remain part of this record.

| Re-executed check | Exit | Observed result |
| --- | ---: | --- |
| Exact full-suite command from the initial table | 0 | **431 tests in 436.864 seconds, OK**; all 418 original test methods retained. |
| Canonical source validator | 0 | Structural PASS, without a supplied trusted base. |
| Tracked source dependency check | 0 | 26 installed locked versions and dependency consistency. |
| All four compiler `--check` commands from the initial table | 0 each | Navigation, quality, workflow-kit and legacy toolchain outputs match. |
| `actionlint -shellcheck= -pyflakes=` (1.7.12) | 0 | Workflow syntax check; optional analyzers remain unexecuted. |
| `git diff --check` and `git diff --cached --check` | 0 each | No whitespace errors. |
| Independent baseline-map and byte audit | 0 | 495 unique baseline mappings, 433 relocated old source paths absent, 152 exact preserved blobs. |
| Supplemental exact-main-to-repaired `copier.run_update` experiment | 0 | Local AGENTS instruction and project facts preserved; no rejects; updated legacy validator passed. |
| Actual previous source validator against repaired candidate | 1 | Same 34 path/context errors; blocked legacy trusted-base gate, not PASS. |

The source-only relocation audit checks that the old Backbone files were moved in
this repository. It does not prohibit a later copied product from adding its own
native root `Dockerfile`, dependency manifests or build files. The repaired copy
regressions cover optional product/IDE placeholder removal and native root build
inputs, while the governed Backbone policy and dependency files remain mandatory.
Direct-copy negative cases still reject weakened/missing policy, elevated reviewer
permissions, changed historical bytes and candidate-map attempts to alter the
trusted historical exception authority.

Final full-suite log SHA256:
`6ce78bb7ad8dd2e98671d7d8adf85e8b8a344ee7135421e9e0befbea59ba9487`.
Individual final command-result record SHA256:
`9fd99d93e6f2d9ccd9978f2df131b74402aaec50534f605c7148443621dee775`.
The repeated previous-validator and supplemental update logs have the same hashes
as their initial corresponding logs recorded above and below. Generated legacy
toolchain fingerprint remains
`402e3fa62d99afda07bd2929afef9237e28835b3a3a349e6ca194d01cb58343f`.

These checks establish their exercised structural, migration, direct-copy and
legacy-consumer behavior. They do not replace the independent Full reviews,
human approval, runtime qualification or the intentionally unresolved trust-layout
migration.

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
legacy consumer compatibility and direct-copy smoke are separate from the failed
previous-layout gate. Docker build/offline smoke is still unexecuted locally.
Remote CI results must be recorded separately; no remote PASS is claimed here.
