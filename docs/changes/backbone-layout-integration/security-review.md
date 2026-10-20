# BB-LAYOUT-014 — independent security Full review

Reviewer: `bridge_security_review` (independent of implementation and quality execution). Review round: first Full for BB-LAYOUT-014. Date: 2026-10-20. Verdict: **no actionable P0–P3 findings identified within the reviewed security/trust scope**. Findings: `[]`.

This review began only after the parent supplied the completed independent quality report and explicitly released the frozen implementation for Full review. It does not approve human merge, release, or downstream application. Separate triage and the final committed evidence check remain with the coordinating agent.

## Exact reviewed identity

| Item | Identity |
| --- | --- |
| Frozen checkout | `/workspace/scratch/6e019b0851cc/backbone-integration-quality` |
| Reviewed head | `ab8fa240a1588f68e78d3aebffa0ef531250d638` |
| Reviewed tree | `cbad0c7999361481197539e2cad2be0b0eabed65` |
| Actual merged main | `537576f658bbd79c3bc49b26ade948116c664943` |
| Starting PR18 head | `f1c1410cff6407109f286173f1ecc980cd2a14b7` |
| Main-to-head binary patch SHA256 | `28741be9710c86e492f55277df4d2f970af477cd7d12b2d1fcb58531b3a5175a` |
| Starting-PR18-to-head binary patch SHA256 | `6a5eec34a85b24ab20b113f5a8835d6abc9c7b21f895ac048551f715fdd30c1a` |
| Independent quality report | `/tmp/backbone-integration-quality.md` |
| Quality report SHA256 | `e7cc3c1f9657d762b4d86f7798d91b1c19571226cb7253d6d537ae7eeed9f7ba` |

The reviewer independently recomputed both binary patch digests, verified HEAD/tree, and observed a clean frozen checkout before and after the bounded audit. No source, test, policy, fixture, or repository report was edited by this reviewer. Review artifacts are external temporary files only.

## Context and coverage

Read the applicable `AGENTS.md`, `CONTRIBUTING.md`, `docs/agent-governance/core.md`, the BB-LAYOUT-014 plan, task packet, independent plan review, initial triage, implementation notes, and the actual independent quality report. Reviewed both comparison scopes, using rename-aware main-to-head comparisons to distinguish the transplanted prerequisite from changes introduced by integration.

1. **Executable authority and layout resolution.** Inspected the moved validator's executable-owned source/consumer identity, independently resolved candidate/base policies, schema ownership, policy floor and inherited invariants. The source-layout helper, navigation module and quality module are byte-identical to actual main at their new paths. The helper selects only the two explicit canonical contracts; missing, mixed, ambiguous and symlinked policy authorities fail closed, including dangling alternatives. It does not infer mode from candidate files or product dependency manifests. The CLI has no candidate-controlled mode override. Legacy consumer mode retains its fixed bundle contract.

2. **Generated guards and native permissions.** Inspected the maintenance compiler's fixed input/output relocation and the self-contained compiled guard copies. Independently compared executable ASTs for all ten embedded `source_layout` definitions: navigation 1, quality 2, validator 4, workflow 3. They equal the canonical helper after removing docstrings only. The resolver imports only the standard-library `Path`; candidate helper code is not imported. Policy schemas, core authority, standards, dependency locks, legacy templates, historical/predecessor fixture trees, native agent/profile directories, `opencode.json`, and Copier entrypoint are unchanged from starting PR18. Mandatory native instruction mapping and inherited additional instructions retain the prerequisite behavior; no permission relaxation was introduced by the integration.

3. **Complete immutable history.** Inspected the new `historical_inventory()` call after the walk and before artifact processing. It iterates the executing validator's entire 88-entry authority, rather than the files a candidate happens to expose or its mapping declaration. Missing files, absent directories, non-file leaves, and symlink ancestors produce errors. Existing per-file byte checks and original-context link resolution remain in place. Independently checked that the 88-entry authority and policy floor equal actual main, that every expected hash matches its original Git blob at `212608aa50ee517b3dd3107a9480da997222fd4f`, and that all 88 current files match those hashes. The original 495-entry mapping is byte-identical to starting PR18. No new incoming prerequisite record was silently added to the fixed historical exemption set.

4. **LF checkout behavior.** Reviewed the scoped root `docs/changes/** text eol=lf -filter -working-tree-encoding` rule and the regression test's real fresh checkout with local `core.autocrlf=true`. The test verifies all 88 pinned archive byte sequences, validates the resulting source checkout, and checks that nested historical fixture attributes and bytes retain their separate contract. This repairs checkout transformation rather than changing reviewed hashes or rewriting archives. Execution evidence for that test comes from the independent completed suite, not an additional reviewer rerun.

5. **Actual-main provenance and migration authority.** Inspected the independently pinned snapshot identity and verification-before-extraction fixture logic. Independently compared all 511 merged-main manifest paths, modes and Git blob identities to actual main, verified each ZIP entry's SHA256/Git blob hash and stored mode, and verified ZIP SHA256 `7ba99d70d4a345623bbb30e95e632fceb904927688953dd0a031b7dea92e5a9f`. The manifest's tree equals actual main's `10f7147ce5f4c2438cf4e016598a3a05be2c71f8`. Existing original fixture identities remain separately pinned; the new actual-main snapshot is not a reconstruction from current candidate code.

6. **Workflow fingerprint boundary.** Independently verified that the 13-entry previous list is exactly actual main's previous list plus its actual current digest `a9355b863956489a0da750849dd890cdb8745f64172dedb3449f816e844bb524`; it also equals starting PR18's previous list plus that single digest. The already approved `35678afb51ae9f1c5bc806dd7f1397d4ebde878d3f30adc7685399da386c950b` remains present. No interim PR18 digest was admitted. Current digest is `94f8f22f4dd66234d5048f2dee51c897fa7b9406694bf38ce44fef5186421120`. The independent quality check confirms it against actual rendered tooling. After excluding only the consumer run body and its two fingerprint environment values, parsed workflow content equals starting PR18, preserving action pins, permissions, triggers, checkout settings and source commands. Inspected the consumer guard changes as the relocated prerequisite's self-contained guards.

## Reviewer-executed bounded checks

Command: `/workspace/scratch/6e019b0851cc/backbone-venv/bin/python -B /tmp/backbone-integration-security-audit.py` — final exit 0. Static results and full probe output are in `/tmp/backbone-integration-security-audit.json`.

| Probe | Result |
| --- | --- |
| Current trusted validator checks the intact exact frozen c501 PR18 source tree against actual merged main | Exit 0 |
| Delete unlinked bootstrap task archive, remove its candidate map entry, and replace candidate validator/helper with code that writes a marker if executed | Exit 1 with required-historical-record error; marker absent |
| Replace that required archive leaf with a directory | Exit 1 with required-historical-record error; no traceback; marker absent |
| Replace its parent directory with a dangling symlink | Exit 1 with required-historical-record error; no traceback; marker absent |

The probe candidate files were temporary copies of verified frozen fixture bytes; execution always used the frozen reviewed validator. Candidate substitutions cannot replace its archive authority or execute a candidate helper. The additional non-file and dangling-parent cases complement the committed missing-file, missing-parent and ordinary symlink regressions.

The first audit attempt stopped at a reviewer-side expected-list assertion that mistakenly appended the already-present `35678...` digest a second time. The reviewer corrected that expectation after reading both baseline workflow literals. The final exact-list comparisons passed; no repository change was made or required.

## Independent quality evidence and limits

Read and used the separately authored, exact-bound quality report: 461 tests passed in 594.405 seconds; all 14 additional checks exited 0; all 587 tracked input hashes remained unchanged. That report covers complete suite execution, source validation, actual-main-owned validation against this exact candidate, four compilers, dependencies, actionlint, both committed diffs, preserved assertions/fixtures, archive checkout behavior, and real rendering of approved historical toolchain fingerprints. These are the quality agent's results, not tests claimed to have been run by this reviewer. The reviewer did not duplicate the complete suite.

This Full review targets diff-caused security/trust regressions and the confirmed archive repairs; it is not proof of absence of every repository defect. Actual main's successful validation alone cannot certify the archive-completeness fix because actual main retains the known missing-archive blind spot. The new negative probes and committed regressions address that limitation directly. No native Windows host, Docker/Podman runtime, external model execution, or new hosted CI run was exercised by this reviewer. Local Git's fresh autocrlf checkout establishes the covered byte-conversion behavior without claiming native Windows execution. Historical CI outcomes are not represented as checks of this head.

Later report/triage commits are outside the reviewed tree and require the coordinating agent's final committed-diff/evidence validation. No merge or publication was performed by this reviewer.
