# Publication identity and first PR readback

PR: https://github.com/Artifaktory/engineering-backbone/pull/24 (draft, open).
Target `main`, actual base `4e74c7e5f3a07430768f670c4271c1e1a0e28f68`.
First readback: published reviewed code
`ff1279c0c6bf250c28195ba92262e85554522913`, mergeable true;
GitHub reported mergeable state `unstable`, with no completed CI result.
No merge/release/deployment was performed.

## Exact correspondence

Connector author/committer metadata changes commit IDs. After publishing, a real
Git fetch and byte-for-byte binary-diff comparison independently confirmed all
four local/published trees, ordered mapped parents and base-to-head patches.
Every committed base/published-head whitespace check exited 0.

| Stage | Local commit | Published commit | Identical tree | Base patch SHA256 |
| --- | --- | --- | --- | --- |
| plan | `3982016b6aad28271b524fd0fa68be20f390e1f2` | `371182b7b06e7b5ef4677c70a9c0ba883c7cb3e1` | `b81a7e3d6cc54db58e7ff4c22838928aea4b46b3` | `5b8cb597c1786c6159e0fc68803647b8dbeb92bc4e56d2029e7e2242bac22c66` |
| implementation | `00b758e2f30f85d3c05930d5a08ec21403bb3f75` | `8e2d985a920131ed44a0f5b07742feaa81ca5331` | `98838273f88666dbbe03f797342fd5655ef00d0a` | `21b2893c840ee044645e74a2fdc252644b735e65872931d4b63eff4d86c3fa47` |
| repair | `f0230d0da90b17ef52932ff027529acd23d73f51` | `774256303b13b8751eaf113c6842c6f28e178f2e` | `ff9d9c860682c3ed8531a9b085f9ee75678c725d` | `ba6eeafe17d91ca46c3b8b695e7e18f4372703d1419712b4d6c9654b865e7f34` |
| full-repair | `bb794a6b05e35f168ee90d4dcbe5055f674eeead` | `ff1279c0c6bf250c28195ba92262e85554522913` | `b96337072a048afa37eee2135f3fafeaa76f8782` | `fba134f81573d5100933bf63a2df6ac169c6ab8d34c90df1b86e9cd6b0abbfc9` |

The final implementation review subject is local `bb794a6...` / published
`ff1279c...`, not this later report-only commit. Its code and all protected inputs
remain unchanged. The Task Packet's head binds that published reviewed subject.
Later evidence-only commits require both validators and actual committed
base/head plus implementation/report-head whitespace checks. The PR body records
the final tip/tree/patch and mapping after those checks, avoiding a self-referential
commit hash inside its own file.

## Actual first jobs readback

Read both Actions runs and their complete job API responses at the code head:

- [OpenCode native discovery, 39593709955](https://github.com/Artifaktory/engineering-backbone/actions/runs/39593709955): two jobs queued.
- [Backbone quality, 39593710120](https://github.com/Artifaktory/engineering-backbone/actions/runs/39593710120): three jobs queued, including trusted-base policy.

All five jobs had no assigned runner and zero steps. Windows native smoke requests
`self-hosted, Windows, X64, backbone-ci`; all other jobs request
`self-hosted, Linux, X64, backbone-ci`. The old display names `windows-latest` and
`ubuntu-latest` do not select hosted runners; actual labels were read from the API.
Queued is not PASS. Runner fleet administration is unavailable through this
connector, so missing registration, offline service, label/group access and busy
capacity cannot be distinguished here. No provisioning, permission change,
hosted fallback or artifact upload was used. Final-tip jobs are read back in the
PR body after publication of these records; this first readback is historical.
