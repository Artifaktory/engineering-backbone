# Integration documentation and checkout-byte changes

Root coordinator implements only the approved document/attribute scope. Runtime and test changes are owned by separate implementers; this report is not independent review.

- Relocated all eleven BB-LAYOUT-013 plan/review records directly from actual main `537576f658bbd79c3bc49b26ade948116c664943`, preserving their exact bytes and relative `plans/` / `docs/reviews/` topology.
- Added `incoming-map.json` for all 29 incoming prerequisite files, without altering the original 495-entry inventory.
- Compared all eleven relocated record blobs and all 152 originally byte-preserved blobs with their recorded Git identities: PASS at implementation time.
- Updated AGENTS, CONTRIBUTING, README and the change index to the current BB-LAYOUT-014 packet/plan and actual merged prerequisite. Prior records retain their original claims.
- Retained the required final committed-diff publication check from both branches.
- Added only `docs/changes/** text eol=lf -filter -working-tree-encoding` for INT-ARCHIVE-02. The nested historical-fixture attributes are untouched; the separate test worker covers actual autocrlf checkouts.
- Retained the independent initial triage for INT-ARCHIVE-01, INT-ARCHIVE-02 and INT-NAV-01 before repairs.

Implementation-time staged and worktree whitespace checks returned 0. Full quality checks and frozen independent reviews remain separate required evidence.
