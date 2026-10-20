# BB-LAYOUT-014 independent quality checks

Checker: `layout_quality`, separate from implementation and Full review.
Date: 2026-10-20. **461 tests passed in 594.405 seconds, exit 0. All 14 additional
commands below returned exit 0.** No confirmed deterministic-check failure remains
on this snapshot. This is check evidence, not semantic Full review or merge approval.

## Frozen identity

- Head: `ab8fa240a1588f68e78d3aebffa0ef531250d638`.
- Tree: `cbad0c7999361481197539e2cad2be0b0eabed65`.
- First parent / starting PR18: `f1c1410cff6407109f286173f1ecc980cd2a14b7`.
- Second parent / actual merged main: `537576f658bbd79c3bc49b26ade948116c664943`.
- Main-to-head binary patch SHA256:
  `28741be9710c86e492f55277df4d2f970af477cd7d12b2d1fcb58531b3a5175a`.
- Starting-PR18-to-head binary patch SHA256:
  `6a5eec34a85b24ab20b113f5a8835d6abc9c7b21f895ac048551f715fdd30c1a`.

The isolated worktree was clean before and after execution. All **587 tracked
input SHA256 values matched** before/after; no source, tests or repository evidence
were edited by this checker. This report is external to the tested tree.

## Executed commands

Commands ran from `CANDIDATE`, the frozen
`/workspace/scratch/6e019b0851cc/backbone-integration-quality` checkout.
`MAIN` was the clean actual
`/workspace/scratch/6e019b0851cc/backbone-main-537576f` checkout.
`python` denotes `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python`,
Python **3.12.14**, with unchanged locked dependencies. Local Git was **2.51.1**.
`HEAD` below means only the exact tested commit above.

| Command | Actual result |
| --- | --- |
| `python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v` | Exit 0; **461 tests, 594.405 seconds, OK**. |
| `python .engineering-backbone/src/validate.py` | Exit 0; structural check without a supplied trusted base. |
| `python "$MAIN/scripts/validate.py" --root "$CANDIDATE" --trusted-base "$MAIN"` | Exit 0; actual main-owned validator checks the exact candidate against actual main. |
| `python .engineering-backbone/src/validate.py --trusted-base "$MAIN"` | Exit 0; additional candidate-owned check, separately identified. |
| `python .engineering-backbone/src/maintenance/compile_navigation.py --check` | Exit 0. |
| `python .engineering-backbone/src/maintenance/compile_quality_framework.py --check` | Exit 0. |
| `python .engineering-backbone/src/maintenance/compile_workflow_kit.py --check` | Exit 0. |
| `python .engineering-backbone/src/maintenance/compile_toolchain_fingerprint.py --check` | Exit 0. |
| `python .engineering-backbone/src/check_source_dependencies.py` | Exit 0; tracked inputs and all 26 locked installed versions consistent. |
| `actionlint -shellcheck= -pyflakes=` | Exit 0; version 1.7.12, optional analyzers unexecuted. |
| `git ls-files --unmerged` | Exit 0; empty output, no unmerged entries. |
| `git diff --check` | Exit 0. |
| `git diff --cached --check` | Exit 0. |
| `git diff --check 537576f658bbd79c3bc49b26ade948116c664943 HEAD` | Exit 0; complete committed main-to-head diff. |
| `git diff --check f1c1410cff6407109f286173f1ecc980cd2a14b7 HEAD` | Exit 0; committed integration delta. |

Checked rendered fingerprint:
`94f8f22f4dd66234d5048f2dee51c897fa7b9406694bf38ce44fef5186421120`.
Fresh-fixture Copier answers-file warnings did not prevent successful completion.

## Independent preservation and regression evidence

- Both recorded parents are actual merge parents. The 29-entry incoming inventory
  exactly covers main's changed paths since the common ancestor; every destination
  exists. All **11 relocated prerequisite records** match their main Git blobs.
- The original **495-entry mapping is byte-identical** to starting PR18. All
  **152 designated preserved blobs** match their recorded original Git identities.
  The executable-owned **88-entry archive authority is unchanged** from main;
  every actual archived file matches its SHA256 and original `212608...` blob.
- All **433 PR18 methods and 1,120 original assertion call ASTs** remain intact and
  ordered. Historical workflow coverage adds assertions. All **441 main method
  identities** remain; its 23 additional transition methods are retained. Of those
  23, 22 assertion sequences are exact; the planned old-layout positive targets the
  verified merged-main fixture instead of the now-new-layout working root, retaining
  the original old validator and positive assertion. The union is 456 methods,
  plus five added cases, giving 461. No claim of identical method-body bytes is made.
- A separate read-only quality helper verified the two original compatibility ZIPs
  and their manifest byte-for-byte against main after relocation. All **62 prior
  PR18 fixture blobs** and **62 prior-main fixture blobs** are preserved; these sets
  overlap. The additional merged-main ZIP's **511 paths, modes, SHA256 values and
  Git blobs** match actual main. Independent tree reconstruction yields
  `10f7147ce5f4c2438cf4e016598a3a05be2c71f8`; ZIP SHA256 is
  `7ba99d70d4a345623bbb30e95e632fceb904927688953dd0a031b7dea92e5a9f`.
  This checker also reverified all 511 actual-main checkout blobs after the suite.
- **275 protected inputs** remain byte-identical to PR18, including policy/schema,
  dependency/container, legacy, native adapter and product-scaffold inputs. Active
  AGENTS, CONTRIBUTING and change-index pointers name **BB-LAYOUT-014**; README
  points to the integration plan. The scoped archive LF attribute is present.

The complete suite passed intact-history positives and rejection of missing
required files/directories, forged candidate mapping, and file/ancestor symlinks.
Its real fresh `core.autocrlf=true` checkout verifies all 88 archive hashes, LF
bytes, nested historical fixture bytes/attributes and successful validation.
Both real predecessor consumer renders, stricter-policy/permission guards, real
Copier updates, Copilot selector/transport regressions and historical clone checks
ran successfully. Actual-main positive validation remains distinct: main still
has the known archive-deletion blind spot and cannot independently certify that
candidate repair. No path projection or candidate-validator substitution was used.

The retained implementation report records the earlier targeted 83-test run with
one invalid Task Packet status failure, independently triaged as INT-CHECK-01.
Its corrected-input checkout rerun passed before this freeze. That pre-freeze
failure remains recorded; the independent complete run above is new evidence.

## Artifact binding and limits

Raw logs and audit JSON are under `/tmp/backbone-integration-quality-artifacts/`.

| Artifact | SHA256 |
| --- | --- |
| `full-suite.log` | `1f55c13857fa31cba8ce2373a496d793b94cb47628e9e64d15142e195c4764b9` |
| `commands.json` | `783977f11f1cf24243663cdcf21bebad27cad51276a570b3132b47d3140abf65` |
| `assertion-audit.json` | `384136f6571ca017e4ee073d1fefcc9b23358d71218806a08c1184f4628781ff` |
| `history-and-scope-audit.json` | `037d7a7b1a6bb264604ba5ca862bc75ce3cef36663fb3652a044435c0010c12f` |
| `fixture-audit.json` | `402609b263a74e68590bb62bf09c7c7f5e1a741bc667346713cf52f272b54aa5` |
| Identical before/after input inventories | `5392c6c8d846b7b3abf3dd142f332f08187d3f580b6017d5d82f40ce153b89d4` |

Docker and Podman are unavailable locally. No actual native client/model session,
container build, or Windows host execution was performed by this checker. Native
smoke unit-test output is not actual native-runtime qualification. Current-head
remote jobs, requested Codex review, and frozen behavior/security Full reviews
remain separate evidence; prior PR18/PR19 results do not qualify this tree.

These committed-diff results bind only `ab8fa240...`. After retaining this report
and review/closeout records, repeat both committed diffs using the actual final
head and recheck live-base freshness. Later source changes require affected
verification; this report does not certify future commits or authorize merge.
