# BB-LAYOUT-014 independent behavior and compatibility Full review

## Result

**NO CONFIRMED IN-SCOPE FINDINGS.** This review found no concrete P0–P3 defect introduced by the reviewed integration. It covers both the actual-main-to-candidate change and the integration delta from the starting PR18 head. This is the behavior/compatibility Full review, not a security-review substitute, publication approval, or a claim that remote checks have passed.

The review began after the completed deterministic quality gate and the coordinator's explicit Full-review GO. The reviewer did not implement the change, edit source or tests, run the full suite again, commit, publish, or merge. A separate read-only fixture/test subreview contributed the independently attributed evidence below.

## Immutable review identity

| Item | Exact identity |
| --- | --- |
| Frozen checkout | `/workspace/scratch/6e019b0851cc/backbone-integration-quality` |
| Actual merged main | `537576f658bbd79c3bc49b26ade948116c664943` |
| Starting PR18 head | `f1c1410cff6407109f286173f1ecc980cd2a14b7` |
| Reviewed merge head | `ab8fa240a1588f68e78d3aebffa0ef531250d638` |
| Reviewed tree | `cbad0c7999361481197539e2cad2be0b0eabed65` |
| Parent 1 / Parent 2 | Starting PR18 head / actual merged main, respectively |
| Actual-main-to-head binary diff SHA256 | `28741be9710c86e492f55277df4d2f970af477cd7d12b2d1fcb58531b3a5175a` |
| Starting-PR18-to-head binary diff SHA256 | `6a5eec34a85b24ab20b113f5a8835d6abc9c7b21f895ac048551f715fdd30c1a` |
| External completed quality report | `/tmp/backbone-integration-quality.md` |
| Quality report SHA256 | `e7cc3c1f9657d762b4d86f7798d91b1c19571226cb7253d6d537ae7eeed9f7ba` |

The reviewer independently checked the commit, tree, two parents, both binary-diff digests, and quality-report digest. The frozen worktree was clean at the beginning and at final inspection. The reviewed plan remains SHA256 `3a865abe86c39422696c6b0b1b4006307facd14779d1e73516cc8eaeeff94cba`; the current task packet is `active`, with the earlier invalid-status run and correction explicitly retained in separate triage.

## Policy, scope, and evidence inspected

Read applicable `AGENTS.md`, `CONTRIBUTING.md`, `docs/agent-governance/core.md`, the integration plan/task packet/plan review, incoming-file inventory, implementation records, initial triage, completed quality report, and the relevant implementation and test deltas. Findings were limited to concrete diff-caused behavior defects within BB-LAYOUT-014. Prior reviews and prior-head CI were treated as history, not evidence that this head passed.

### Runtime and compatibility

- Compared actual main's runtime with its relocated candidate counterparts. `source_layout.py`, `navigation.py`, and `quality_framework.py` are byte-identical. The validator's bounded differences are its executable-owned relocated-source/legacy-consumer entrypoint identity and the new historical-inventory guard plus its call. The guard runs after traversal and before artifact validation; existing per-file hash and original-context link checks remain.
- Inspected the inventory guard for absent files, absent parent directories, file symlinks, and ancestor symlinks. It uses the executable-owned historical inventory, requires observed regular files, and rejects symlink components. Its applicability is limited to new source layout; old source and generated-consumer behavior remain separate. Candidate mapping cannot redefine this inventory.
- Inspected navigation compilation and propagation: changed physical root/source paths reflect the deeper maintenance location; extraction/replacement behavior remains intact. The other three maintenance compilers and the legacy validator template are byte-identical to starting PR18.
- Parsed and compared the workflow structures. The complete workflow envelope equals starting PR18 after replacing the single generated trusted-consumer-validation step. The shared twelve predecessor fingerprints are retained; the only appended predecessor is actual merged main's current fingerprint, `a9355b863956489a0da750849dd890cdb8745f64172dedb3449f816e844bb524`. The new current fingerprint is `94f8f22f4dd66234d5048f2dee51c897fa7b9406694bf38ce44fef5186421120`. Events, permissions, pinned actions, conditions, checkout arrangement, and gate structure were not broadened by this integration.
- Confirmed the Copilot distribution test file is the exact starting-PR18 blob, preserving the nested-document selector correction and real `git+file://` Copier transport correction. Consumer/native-discovery compatibility was assessed through retained contracts, unchanged protected inputs, and the complete quality evidence; no native client was launched by this reviewer.

### History, checkout behavior, and navigation

- Independently compared executable-owned `HISTORICAL_FILES` and `ORIGINAL_TO_CURRENT` in actual main, starting PR18, and candidate: all retain the same 88 historical entries and 495 original-path mappings. Every required candidate archive file matches the original Git blob and pinned SHA256.
- Compared the incoming inventory against the actual Git change set from the common base to merged main: all 29 incoming paths are accounted for, declared base blob identities match actual main, destinations exist, and entries requiring byte preservation retain those bytes. The eleven incoming plan/review records retain their nested `plans/` and `docs/reviews/` relationship. No candidate-controlled extension of archive exemptions was introduced.
- Inspected the scoped `docs/changes/** text eol=lf -filter -working-tree-encoding` attribute and its relationship to immutable archives. The regression uses an actual fresh Git checkout with `core.autocrlf=true`, independently checks all 88 archive bytes and nested historical fixture attributes, and then invokes source validation. The external quality report records this regression passing.
- Checked active AGENTS, CONTRIBUTING, README, and change-index pointers against BB-LAYOUT-014. Historical records remain historical. Documentation accurately distinguishes actual merged-main validation from the candidate's new archive-completeness protection: actual main still has the pre-existing absent-archive blind spot, so its positive result alone is not presented as proof of this repair.

### Independent fixture and assertion subreview

The delegated read-only fixture/test reviewer independently matched the same head/tree and both patch digests and reported no confirmed in-scope findings. Its audit confirmed:

- Both parents' existing fixture sets retain blob bytes and file modes; the two original snapshot ZIPs and original manifest are unchanged.
- All three snapshot archives match the relevant actual Git path sets, blobs, and modes. The additional merged-main snapshot contains 511 files and pins actual main's tree `10f7147ce5f4c2438cf4e016598a3a05be2c71f8`. Its verifier checks commit/tree/count/archive digest, individual content digests, Git blob identities, modes, and reconstructed tree before use.
- All 433 starting-PR18 test methods and their 1,120 assertion-call ASTs remain in sequence; all 441 actual-main test-method identities are retained. Of the 23 incoming transition methods, 22 assertion sequences are exact; the planned old-layout-positive adaptation now executes the verified merged-main fixture with the actual old validator.
- New actual-main-to-integrated transition coverage and deletion, parent deletion, candidate-map forgery, file-symlink, and ancestor-symlink cases are meaningful. Source fixture adaptations retain the canonical new-layout core marker.
- Actual old and merged-main consumer renders retain fixed expected fingerprints and run the trusted workflow checks before the unchanged exact-set assertion; real Copier upgrade transport is retained.

This subreview performed no source edits or full-suite rerun. Its conclusions supplement the primary review; the recorded 461-test result belongs to the independent quality checker.

## Deterministic quality evidence and limits

Read the exact-bound independent quality report rather than treating an implementation summary as a test result. It records **461 tests passing in 594.405 seconds**, all **14 additional commands exiting 0**, and all **587 tracked input hashes unchanged** across execution. Commands cover candidate validation, actual merged-main trusted validation, candidate validation against that base, all four compiler checks, dependency checks, workflow lint, unresolved-index checks, and working/staged/both committed diff checks.

The report preserves the earlier invalid task-status failure and its separately triaged correction; it does not relabel the failed run as successful. The current packet is valid and active. The reported assertion and fixture preservation checks agree with the independent read-only comparisons in this review.

This review did not rerun the complete suite, container builds, native clients, models, or a native Windows host. Local actionlint evidence excludes optional shellcheck/pyflakes analyzers. Docker/Podman were unavailable to the quality checker. Remote current-head Foundation, trusted-base, container, Windows/Linux, and Codex outcomes remain separate publication evidence. Final evidence-file changes still need their scoped final diff validation and exact remote ancestry/tree/patch readback. Main freshness must be checked at publication; this result is bound to the identities above.

## Disposition

No behavior/compatibility finding requires a source repair or further Full round from this review. Hand this report to the separate triage step together with the independent security review. Preserve the exact reviewed implementation identity when assembling final evidence; any later implementation change requires the applicable scoped review and verification.
