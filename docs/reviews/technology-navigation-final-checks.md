# Independent final source-completion quality gate

Task: `BB-TECH-NAV-008` · Checker: `/root/technology_quality_gate` · 2026-10-14.

## Deterministic verdict

**PASS for the bounded source-completion snapshot.** All nine planned command
groups completed with actual exit 0, including 36 targeted tests. This is
independent deterministic evidence for the remaining source-layout correction;
follow-up Delta finding closure remains the independent reviewers' responsibility.
No tracked edits, implementation changes, GitHub writes or complete-suite rerun
were performed by this checker.

## Exact identity and unchanged authority

- Base: `edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12`
- Prior repair/Delta head: `4722d46e220ee34fb649c787d19f75f77447ca0b`
- Final source-completion head: `64133a73668a60cd113e7088925542176d6f6a13`
- Tree: `dd4be86ee35baaaac3162b3a191db0c2ba5b0976`
- SHA-256 of full `git diff --full-index --binary BASE HEAD`:
  `75215898fe780137f1724fa17497cbd0a4789b1c5bf9c7e8e1f3602b5b2c402d`
- SHA-256 of `git diff --full-index --binary PRIOR_REPAIR HEAD`:
  `2769a01518fe05412585e37525a3048d7f7074f4a039910a92a4733defdef938`
- Compiled quality guard SHA-256:
  `f4b636346a6e59b6950b00ab465e16c1dbcb15abf32099719ca0ff21ab1f662a`
- Confirmed rendered tooling fingerprint:
  `e4cdae824eb4f1ee9286f8fd8253b510a84ea7729e12fa96c8b5289b38d18450`

The checker independently recomputed identity before execution and after completion;
the tracked worktree remained clean. All 70 protected original catalog, dependency
and historical-fixture entries remain identical in Git blob ID, mode and path to
the upstream base. The existing source facts/policy files also remain unchanged:

| File | Unchanged Git blob |
| --- | --- |
| `.engineering-backbone/project.json` | `1de5d9f5dfb428f890896c54ce70679c0a348dca` |
| `policy/core.json` | `70fe8366c79e91a3f8ee248bf1892c3935a4ea87` |
| `policy/core.md` | `143993391266cdfdc948d89cb2ec4a8ef374a55f` |

The exact canonical `effective_workflow` function source span, including its
whitespace, is byte-identical to the prior repair at `4722d46e...`; its SHA-256 is
`4dbd3d05e2a54a859118b22cc03e3af91a6c80475c637543186e89a98f92053b`.
The compiler checks confirm that the reviewed canonical implementation propagates
consistently into the other guards/workflow. TNAV-S-2 is not reopened by this
quality gate; its earlier Delta closure remains attributed to that reviewed scope.

## Independent commands and actual exits

Execution began only after FROZEN READY. Each process streamed to its own ignored
log; its `.exit` and `.json` sidecars were written after completion. All metadata
records bind the final source-completion head and exact argv. The environment set
`PIP_DISABLE_PIP_VERSION_CHECK=1`, without removing dependency installation or
required hash checks.

| Command | Exit | Wrapper elapsed seconds |
| --- | ---: | ---: |
| `.venv/bin/python scripts/validate.py` | 0 | 1.7 |
| `.venv/bin/python artifacts/trusted-base/scripts/validate.py --root . --trusted-base artifacts/trusted-base` | 0 | 2.966 |
| `.venv/bin/python scripts/compile_navigation.py --check` | 0 | 0.303 |
| `.venv/bin/python scripts/compile_quality_framework.py --check` | 0 | 0.244 |
| `.venv/bin/python scripts/compile_workflow_kit.py --check` | 0 | 0.118 |
| `.venv/bin/python scripts/compile_toolchain_fingerprint.py --check` | 0 | 3.919 |
| `artifacts/tools/actionlint -shellcheck= -pyflakes= .github/workflows/governance-checks.yml .github/workflows/quality.yml .github/workflows/workflow-kit-maintenance.yml .github/workflows/workflow-kit-pr.yml` | 0 | 0.153 |
| `git diff --check edde45d7ce79f6c2c3d70bd0b8ece0a8d9eecb12 64133a73668a60cd113e7088925542176d6f6a13` | 0 | 0.084 |
| `.venv/bin/python -m unittest tests.test_navigation tests.test_navigation_integration -v` | 0 | 67.83 |

Current validation explicitly states that its no-base invocation does not compare
policy history; the separately run exact predecessor check supplied the trusted
base. Actionlint 1.7.12 checked all four current source workflow YAML files, with
its external ShellCheck and Pyflakes integrations explicitly disabled.

The final targeted unittest summary is **36 tests in 65.483s, OK; actual exit 0**
(wrapper 67.83s): 28 navigation tests plus 8 integration tests. The checker inspected
the complete final summary and actual exit sidecar. No failures, errors or skip
summary were present. No unrelated language/application commands were run by this
gate.

## Corrected premise and meaningful regression evidence

Separate Delta triage explicitly corrected the earlier mistaken assumption that
source mode lacked project.json. The actual tracked source file already existed
unchanged in the upstream base. The earlier triage/test/guide record remains
preserved; this report does not rewrite its claims as successful source coverage.

The checker read that triage, inspected the exact unit/CLI/guide correction, and
read the retained author red/green evidence:

- Corrected source unit against the prior behavior: one test in 0.441s failed
  because the required project hash was absent; author metadata records exit 1.
- Corrected navigation module after the canonical fix: 28 tests in 1.816s, OK;
  author metadata records exit 0.
- New compiled source CLI regression against the previous guard: one test in
  4.821s, four failing subcases covering inclusion, valid fact mutation and removal
  through resolve/verify.
- The same new CLI regression after normal recompilation: one test in 3.780s, OK.
- This checker's final frozen-head run independently passed all 36 affected tests.

The source unit uses the actual source layout and checks both policy/core.json and
existing project.json hashes, unchanged verification, valid fact mutation rejection,
resolve/verify deletion rejection and restored-byte success. It retains the correct
absence of the consumer core.json path from source receipts. The compiled CLI case
uses actual repository project.json bytes and independently exercises the source
flag, inclusion without manual mapping, schema-valid branch/validation-command
changes, deletion and restoration. Existing consumer mandatory-facts, inactive,
legacy, authority, compilation and real Copier behavior in these two modules also
passed.

The guide now maps the existing project.json in both layouts, policy/core.json in
source mode and installed core.json in consumers. The checker verified that the
managed guide template includes the shared source guide and that the final smoke's
installed guide bytes equal the updated source guide. The passing integration
module includes actual Copier rendering/update propagation checks.

## Evidence attribution across snapshots

The 314-test whole-suite result remains evidence for
`6e5758deb7767c2915505b9646f1a09e0cc0b174` only. The 83-test first-repair result remains
evidence for `4722d46e220ee34fb649c787d19f75f77447ca0b` only. Neither is relabeled as
an execution at this final source-completion head. The scoped follow-up gate runs
the directly affected 36 tests plus required deterministic compilation/compatibility
checks, as selected by separate Delta triage and the orchestration owner.

## Explicit-context smoke continuation and limits

The checker read the completed continuation report and structural result and
independently recomputed all 28 current receipt document hashes. Exactly one
selected document changed: `.engineering-backbone/navigation-guide.md`; the other
27 hashes and all four selected check definitions remain identical to the previous
repair smoke. The captured final guard bytes match the frozen guard SHA above.

This is a continuation by the SAME receiver: it reused 27 previously completed
full reads only after byte equality and fully reread the changed guide. The report
records positive verification exit 0 and old-receipt rejection exit 1, followed by
a stop. It is not a new fresh 28-document semantic reading run. This consumer
fixture checks updated guide propagation, while source-layout runtime behavior is
covered by the separate executed CLI regression.

- Context digest: `dd97e872b0fceb6eeba329f79fbac8090486281b7d043abffa65e1dcfe011504`
- Receipt file SHA-256: `015883f62e90e6be9041a250736dbe25e882344f09c69ee6e8d54658ef5ef134`
- Prior repair-smoke preservation record: 210/210 files unchanged, no additions.

No application checks were executed by that smoke. The fixture revision remains
declared rather than authenticated. Native Codex/Copilot discovery remains
unverified; no unchanged failed client was rerun. Independent follow-up Delta,
remote CI/PR identity and requested Codex review remain distinct later evidence.
This report grants no merge, release, deployment or downstream-adoption approval.

## Raw evidence hashes

Each log below is under `artifacts/technology-navigation/`, with matching `.exit`
and `.json` exact-command records.

| Log | SHA-256 |
| --- | --- |
| `final-source-validator.log` | `07604dad0ce23e9a3291888da5b1f5fb1e48d63eee763a517af23015c68eb6af` |
| `final-source-predecessor.log` | `d28f15ddd16c8ae14e075b85bfff440c3903913fa5ad810e4e6d7e4bc1d229b1` |
| `final-source-navigation-compiler.log` | `f5acf715a03db96a191bdf0d036c4cfc8708079fafa3e08f149ee51564b2fbf2` |
| `final-source-quality-compiler.log` | `649ebe6bdb8a344d0a7dec260dd3e57744a59dfc34f6d35c64ad36271a92d6b5` |
| `final-source-workflow-compiler.log` | `eb9708a2e83615ae1bec5707088a89f48ffbd2b83a3c0623dca3b8a138175cd4` |
| `final-source-fingerprint.log` | `bfc34d5f6a37c6ef5e9eff9c3e4ec97b6a31dd0790975b6bca572cbf86281198` |
| `final-source-actionlint.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `final-source-diff.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `final-source-targeted-tests.log` | `103d90bb78bc9111991edebc9ce90ea5b1a8711604754491b683d8c9f52eeaed` |

Additional retained evidence, relative to the repository root:

| File | SHA-256 |
| --- | --- |
| `artifacts/technology-navigation/delta-review-triage.md` | `66a9fbb0d0049678dfc2272b1e42efa84f7206b8e1daed0b220445ca353cc7f9` |
| `artifacts/technology-navigation/navigation-source-project-red.log` | `4d481a838354272abbc0577a4e6fec22bcea76a804b0ef08b3c2b2fd48bae670` |
| `artifacts/technology-navigation/navigation-source-project-green.log` | `933a7649d4530fad84fe77b1509e4204f0d21c4ac6854a2036cab10c726b797e` |
| `artifacts/technology-navigation/source-project-integration-red.log` | `be8abcbd79911f0f353a2e6e4c44017b24fdd2c34cd384c59d3a8ceb91b95ed3` |
| `artifacts/technology-navigation/source-project-integration-green.log` | `502c4da32d5b617184bb455ecab856e8629e41798f2011a1b30dd5f6a8b36c97` |
| `artifacts/navigation-source-followup-smoke/report.md` | `5fb63150553f5d0221f08781ad9841a0776b95fb4cda9b4567d2f8fbe70518ab` |
| `artifacts/navigation-source-followup-smoke/structural-result.json` | `d74a5e147a73324e6486ad1d41c14b2010310355e96af9608e715de858e42f9a` |
| `artifacts/navigation-source-followup-smoke/explicit-context-result.json` | `2f9348800ec6b58ed4c6e2b69d1bd8f3e6fc9fd233ba2ecc41c0e87851802f99` |
| `artifacts/navigation-source-followup-smoke/context.json` | `015883f62e90e6be9041a250736dbe25e882344f09c69ee6e8d54658ef5ef134` |
| `artifacts/navigation-source-followup-smoke/previous-repair-smoke-preservation.json` | `c96809067a483451a28d0568993feb302efebabef23d8528054b7af236064766` |
