# Codex consolidation: independent Full review and validation

Task: [BB-CODEX-CONSOLIDATION-002](../../plans/codex-consolidation-task.json).
Date: 2026-10-12. Publication of the scoped PR is authorized by the human request;
merge, release and source-project adoption are not authorized by this result.

## Frozen implementation identity

| Identity | Value |
| --- | --- |
| Local trusted base | `8e7213c30e030ad134d339842c8df17b88a7115a` |
| Remote main base | `1371ec770f0d3fa0eb29e7d347afc7b709ffa3ee` |
| Common base tree | `2ca170e862f2bd4549c6db6f9e1a0decd405bbf0` |
| Reviewed implementation head | `72d9c9caefdd12805eed10d6984cf8b19dd9b4bc` |
| Reviewed implementation tree | `e6e56d7572cca0f211f6d875e598ee71fb665d44` |
| Full binary-patch SHA256 | `ddf0d50d44d20f46ed5ee3c6de3330141c353bdbeef78f46bb313f6cec538926` |

The local base and remote main have identical trees. Connector publication uses
remote main as parent and verifies the published tree, rather than claiming local
and GitHub commit metadata must match. Later evidence-only additions do not change
the reviewed implementation files; their hashes are compared before publication.

## Executed checks

Python 3.12 environment was installed from the previously verified hash lock;
dependencies were not changed in this delivery. All listed checks exited 0.

| Check | Actual result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 98 tests passed, 76.025 seconds |
| Final `python -m unittest discover -s tests -p test_codex_consolidation.py -v` | Four tests passed, 4.821 seconds after the final policy additions |
| `python scripts/validate.py` | Structural contracts pass |
| Previous trusted validator with `--root` candidate and `--trusted-base` previous checkout | Trusted-base policy/schema validation passes |
| `python scripts/compile_toolchain_fingerprint.py --check` | Unchanged actual rendered tooling digest `5bca19e704f2e6ca5744cfccb10e52b862dc7b9d4c18ed5f5cb3a6db8aadab4a` |
| Actionlint | Pass; workflows unchanged |
| Staged/committed diff whitespace | Pass |
| Independent pinned-tree re-fetch and path/blob comparison | All 501 Tars and 418 Artifaktory entries match; no missing/extra selected path under independently reconstructed rules |

The four new tests execute real Copier installation for CLI/frontend and every
provider combination, compare source/generated role contracts, and upgrade an
immutable historical bootstrap while retaining byte-identical stronger native
instructions, permissions, configuration, facts and the separately reviewed caller.
Runtime client loading and semantic gate enforcement are not implied by these tests.

## Independent Full reviews

Both reviewers inspected the same frozen head and patch. No edits occurred between
the two reviews. These are separate local AI reviewer sessions, not claims that
GitHub's Codex or Copilot provider bot performed these local reviews.

| Reviewer session | Result | Independent coverage |
| --- | --- | --- |
| `full_review_security` | `NO CONFIRMED IN-SCOPE FINDINGS` | Trusted-base authority, additive policy, unchanged permissions, schema-compatible evidence, Full/Delta bounds, remote advisory limits and preserved local gates; checked all 289 content-inspected source blobs; independently ran four consolidation tests |
| `full_review_mapping` | `NO CONFIRMED IN-SCOPE FINDINGS` | All 919 inventory entries/counts/flags/URLs, section traceability, role parity, preservation and enforcement claims; all 295 retrieved source contents match source blobs/sizes; independently ran four consolidation tests |

The separate plan review found no confirmed blocker in scope, portability or
acceptance coverage, and required honest selection rules/content-inspection limits.

## Triage and Delta decision

No confirmed in-scope finding was produced by either Full reviewer. Triage has no
repair IDs; no repair snapshot or Delta round is fabricated. If the external PR
review produces confirmed findings, they require recorded triage, scoped repair,
rechecks and independent Delta for those repairs and directly caused regressions.
Existing source inconsistencies are extraction observations, not repaired Backbone
findings and not permission to alter the source projects.

## Coverage and remaining checks

The inventories map all selected paths, not every application file. They distinguish
280 full-content inspections, nine excerpts and 630 tree-only entries. Neither
reviewer claims a semantic audit of the uninspected source controllers/tests.
The mapping reviewer did not independently re-fetch the remote trees/main-staging
comparison; the parent recorded the tree-selection and blob verification above.

No source tests/controllers, live provider discovery, signature enforcement,
GitHub protections or downstream rollout were exercised. Existing repository-control
limits remain described in [repository controls](../repository-controls.md).
GitHub PR-CI and the external Codex result are verified after publication and must
be reported separately. Human review/merge/release remain separate decisions.
