# Independent deterministic-check triage

Triage session: `layout_triage`, separate from implementation and quality checking.
Date: 2026-10-20. This classifies observed failures before repair; it does not
certify implementation, approve a merge or replace the later frozen Full reviews.

## Snapshot and evidence

- Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Failed candidate: `76f78da89d4646fb6a9332fd2d76d8a4d512647a`.
- Binary patch SHA256 (`git diff --binary BASE HEAD`):
  `0ea8d2bdd030c6d1c030037539e948baf399a76e9c7fa994d486edf99ebe066f`.
- Independent full-suite command: `python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -v`.
- Actual result: exit **1**, **428 tests**, **402.726 seconds**, **34 failures and
  1 error**. Subtest failures are included in those totals.
- Raw full tracebacks: ignored `artifacts/layout-quality/full-suite.log`;
  the quality checker records the execution context in [checks.md](checks.md).
  Full log SHA256: `b91eb1743e1e06a7a74f2ead6d5af3c8f29bccaf0aa8dc073a5d1961d113d772`.

The triage session read the applicable instructions, current Task Packet, reviewed
plan, failed test bodies, canonical/native documents, legacy templates and full
tracebacks. No source, template, fixture or test was edited by this session.

## Confirmed repair scope

All findings below are **P2, high confidence, confirmed**. They are caused by this
layout diff and block the candidate's declared deterministic checks or documented
copy contract. None authorizes weaker runtime guards, fewer preserved historical
files, dropped test assertions, altered permissions or changes outside this PR.

| ID | Category and exact affected location | Trigger, evidence and impact | Bounded repair and verification |
| --- | --- | --- | --- |
| LCHK-01 | Adapter documentation parity: `.engineering-backbone/legacy/templates/_partials/` and its `copilot/` partials | The canonical native files now name `docs/agent-governance/agent-navigation.md`, but 23 retained partials still name the removed source path `docs/agent-navigation.md`. Source/rendered-body equality fails for 3 Codex roles, 18 Copilot roles/skills and the OpenCode procedure test. The installed `.engineering-backbone/navigation-guide.md` reference remains valid. | Retarget only the stale source-guide reference in the shared partials. Keep installed paths, restrictive metadata and exact rendered-body comparisons. Re-run Codex/Copilot/OpenCode distribution parity and consumer validation. |
| LCHK-02 | Test expectation: `.engineering-backbone/tst/test_codex_consolidation.py` at lines 175 and 297; `test_copier.py` at line 114 | These comparisons still normalize `(quality.md)`, while the moved canonical core policy correctly uses `(../quality/policy.md)` and the legacy template correctly renders `(quality-policy.md)`. Five fresh/historical-copy equality subtests fail despite the intended path-only conversion. | Update the expected source-link normalization to the new canonical relative link. Preserve full-byte/full-text policy equality and the actual legacy link. Re-run both affected modules. |
| LCHK-03 | Test expectation: `.engineering-backbone/tst/test_codex_consolidation.py`, line 146 | The source-side `guide_link` passed to the Copilot partial remains `../../docs/copilot/workflow.md`; the native source body now correctly points at `../../docs/agent-governance/adapters/copilot/workflow.md`. LCHK-01 fails earlier in the same test, masking this next exact-body mismatch. | Retarget that source-only expected link. Keep the legacy `../../.engineering-backbone/copilot-guide.md` expectation and exact body equality. Re-run the three-role parity test after LCHK-01. |
| LCHK-04 | Legacy fixture construction: `.engineering-backbone/tst/test_dependency_integration.py`, `PROJECT_DOCUMENT` at line 30 | The fixture was changed to the new source document location `docs/operations/engineering/dependency-compatibility.md`, but legacy output deliberately still installs `docs/dependency-compatibility.md`. Four provider-matrix subtests fail and the update test raises `FileNotFoundError` at line 106 before testing preservation. | Restore the legacy consumer document path in this fixture. Keep canonical source paths where the test reads source policy/schema inputs. Re-run the seed matrix and actual update/preservation checks without weakening protected-file assertions. |
| LCHK-05 | Test fixture isolation: `.engineering-backbone/tst/test_copier.py`, `test_consumer_accepts_unrelated_app_content_and_stricter_native_permissions`, line 345 | The supposedly unrelated application file was mechanically moved from `policy/core.json` to the managed `.engineering-backbone/core.json`. The test overwrites mandatory governance with arbitrary business JSON; the validator correctly rejects it. This is a fixture regression, not a runtime-validator defect. | Restore the unrelated application path `policy/core.json`. Retain the stricter native-permission mutations and the separate managed-contract rejection cases. Re-run the positive isolation test and its negative companion. |
| LCHK-06 | Test selector contract: `.engineering-backbone/tst/test_copilot_distribution.py`, line 192 | Full-header equality assumes source and legacy `applyTo` values are identical. The source governance selector now covers the new canonical paths; the source test selector additionally covers `tst/**` and `**/tst/**`. Legacy consumers retain their established selectors. The two rule subtests fail on those intended path-specific differences. | Assert explicit source and legacy selector contracts for only the governance/tests rules. Preserve equality of all other header fields, all other rule headers, permission/tool metadata and rendered instruction bodies. Do not silently rewrite legacy selectors merely to satisfy this test. |
| LCHK-07 | Copy/adoption contract: `.engineering-backbone/tst/test_reference_layout.py`, `test_product_and_backbone_paths_have_distinct_ownership`, lines 53-60 | The README and `apps/README.md` call product placeholders optional, but the copied tooling suite unconditionally requires all three product apps plus optional directories such as `.vscode`. Independent reproduction copied the frozen tree to a differently named project, changed only its project name, removed `apps/frontend`, then observed copied validator exit **0** and this test exit **1** at line 56. A documented minimal project cannot run the advertised tooling suite. | Treat optional product/IDE placeholders as optional in tooling tests; keep actual Backbone code, dependency, Docker, immutable mapping and governance requirements enforced. Add a regression that removes unused placeholders from a copied tree and verifies the intended copy contract while still rejecting missing/weak governance. Do not make the shared control-plane files optional. |

The full-suite counts are explained by LCHK-01 (22 failures), LCHK-02 (5),
LCHK-04 (4 plus 1 error), LCHK-05 (1) and LCHK-06 (2). LCHK-03 is a masked next
failure established by exact expected/actual path inspection; LCHK-07 has its own
independent temporary-copy reproduction. No unexplained full-suite failure remains
in this classification.

## Additional copy-contract triage before the repaired full run

**LCHK-08 — P2, high confidence, confirmed; test-only ownership restriction.**
The new `test_reference_layout.py` forbids every old migration path from existing
in any copied project, and its ownership check separately forbids root
`requirements.txt`, `requirements.lock` and `Dockerfile`. Those assertions are
present in the frozen candidate above and remained unchanged during the bounded
LCHK-07 repairs. The README and app/infrastructure guides explicitly allow native
workspace manifests and tool-required root discovery files. A migration inventory
cannot permanently reserve those generic names against unrelated product content.

Independent reproduction copied the current tree to a differently named temporary
project, added distinct product-owned root `requirements.txt`, `requirements.lock`
and `Dockerfile`, and changed only the project name. The copied validator returned
**0**. Running `tst.test_reference_layout.ReferenceMappingTests` from that copy's
tooling directory returned **1**: three old-path-absence subtests failed, followed
by the ownership test (**2 methods, 4 failures**). The added files did not change
any canonical tooling manifest, archive, policy or mapped destination.

The bounded repair is to stop the copied-tool tests from treating all old paths as
permanently forbidden product names. Keep all 495 unique mapped destinations, the
reviewed map digest, required canonical tooling files and all 152 byte-preservation
checks. A source-specific migration absence audit may remain separate evidence;
it must not reject ordinary project-owned root files after adoption. Remove only
the root-file absence restrictions from the new ownership check and add a direct
copy regression with distinct root-native files. Bundled dependency and governance
mutations must remain rejected. No original 418 regression assertion, runtime
guard, dependency pin or shared-policy requirement needs changing for this fix.

## Disposition and next gate

The coordinator may assign only these confirmed repairs within the existing plan.
Implementers must preserve existing assertions and consumer protection behavior;
the copied product scaffold is an optional location convention, not a governance
requirement. Run affected regressions and a complete suite on the repaired snapshot
before claiming its deterministic gate passed. The independent Full reviews still
need their own immutable repaired head, patch digest, coverage and findings.

The old trusted-base validator's separately observed path incompatibility is the
reviewed draft migration blocker, not an unexpected test failure to suppress.
Container execution remains unavailable locally. Neither condition is waived by
this triage or by a future passing candidate suite.
