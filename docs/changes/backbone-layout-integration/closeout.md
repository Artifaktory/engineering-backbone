# BB-LAYOUT-014 integration closeout

The user reported conflicts in PR18 after the human merge of PR19. The implementation integrates actual main `537576f658bbd79c3bc49b26ade948116c664943` into starting PR18 `f1c1410cff6407109f286173f1ecc980cd2a14b7` with both parents retained. The reviewed local merge is `ab8fa240a1588f68e78d3aebffa0ef531250d638`, tree `cbad0c7999361481197539e2cad2be0b0eabed65`.

The original copyable layout remains. All 29 incoming prerequisite files are mapped in [incoming-map.json](incoming-map.json). The eleven prerequisite records retain their exact Git blobs and relative topology. All 152 original preserved blobs, 88 archive hashes, original495 crosswalk, existing fixtures and protected policy/permission/dependency inputs remain intact.

The three confirmed Codex findings are repaired: missing archive entries now reject independently of candidate mappings; archived text stays LF in actual autocrlf checkouts; active instructions lead to BB-LAYOUT-014. [Initial triage](initial-triage.md) preserves their reproductions, the duplicate finding and the transient task-status failure before freeze. No failed run is relabeled as a pass.

[Independent quality](checks.md) records **461 tests passed in 594.405 seconds**, 14 additional commands exit0 and 587 input hashes unchanged. Actual-main validation is executed from the real merged base. The new archive-completeness repair is separately established by negative tests; actual main still has that known blind spot until a fix is human-merged.

[Behavior Full](behavior-review.md), [security Full](security-review.md) and [separate final triage](review-triage.md) bind the same immutable code and both patch digests. They identify no unresolved confirmed in-scope finding. No post-Full code repair or Delta was required. The final evidence commit only retains these reports, the review-evidence JSON, this closeout and task state; it does not change runtime, tests or fixtures.

## Acceptance and publication boundary

AC1–AC6 and AC8 are supported by the exact-bound checks, audits and review records above. AC7 remains pending at this evidence commit: publish only the existing PR18 branch with an expected-head lease and no force push, then read back its actual parents/tree/patch, conflict status, current-head CI and requested Codex review. Recheck live main before publication.

After this final evidence commit, run candidate validation and actual-main-owned validation again and check both complete committed ranges from main537576 and startingf1 to the final head. Record those full identities and results in the PR body without a self-referential evidence-commit loop. GitHub may assign different commit metadata; verify equal trees and binary patches, and record local-to-remote commit correspondence explicitly.

Local Docker/Podman and native Windows host execution were unavailable. Container and Windows/Linux claims require the actual current-head remote jobs. Structural checks and AI reviews do not establish native model qualification, human approval, or release authorization. Remote findings still require separate triage.

No PR merge into main, release, deployment, settings change or downstream application was performed. Recovery is a reviewed follow-up/revert; published history must not be force-rewritten. The human decides whether and when PR18 is merged.
