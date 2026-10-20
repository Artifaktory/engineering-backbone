# Draft publication evidence

Published [PR #18](https://github.com/Artifaktory/engineering-backbone/pull/18)
on 2026-10-20 as an open **draft**, targeting `main` at
`212608aa50ee517b3dd3107a9480da997222fd4f`. GitHub confirmed `draft: true`
and `merged: false`. The requested publication is complete; merge readiness is
still blocked by the old trusted validator's disclosed layout incompatibility.

## Exact tree correspondence

Direct `git push` could not authenticate in this environment. The authorized
GitHub connector created blob/tree/commit objects and the isolated branch
`refactor/direct-copy-layout`. Every returned tree SHA was compared with the
local Git tree and matched exactly. Connector-generated author/time/message
metadata produces different commit IDs; these are not claimed to be the same
commits. The local test and review IDs remain intact in their original reports.

| Local snapshot | Published equivalent | Identical tree |
| --- | --- | --- |
| `76f78da89d4646fb6a9332fd2d76d8a4d512647a` | `780da9ef917c2ef40c7c78e3ad35ff7971d4fb98` | `b3477e6366859b8b545ab98edd1fd158cc1b1586` |
| `ee4f7cee7a386edfb5fb43b2763a03596b8eabf1` | `8cb4d61b4783ea21d07d382546595707cab55d5e` | `3c5db34f0158b74d2735027c31e951715ce0679f` |
| `54501f1ed542e7f42b5aa315db8863b35e80aeed` | `ac6bf0da22ae0097cf9e8a67857e18dfa86c75d2` | `09f9a2dacc7943e0e7ce18a97422f801a6f686e2` |
| `97e68ecefbd21b0d022514f46520a75a6a025536` | `8f0665384938316694b1b69d44736fda5c22a09f` | `c3ef52a5eaecff857f66ec1599257c2656cc1474` |
| `ca08d5259fb030ca04752773e8d6ee5246a6d3c7` | `62c0b2e024f8d8348d00b0a55885cffa33b8fb57` | `daaed94b3bfd3bbf8610eb1adb32a33e33c4ac3a` |

The Full review's local `54501f1` corresponds to remote `ac6bf0d`;
the repaired Delta subject `97e68ec` corresponds to remote `8f06653`.
The published implementation is therefore byte-identical to the reviewed one.
The subsequent closeout/publication changes contain documentation/evidence only,
not new implementation. Initial PR head `62c0b2e024f8d8348d00b0a55885cffa33b8fb57`
and its base were independently reread through GitHub PR metadata after creation.

## Observed remote checks

At initial publication head `62c0b2e024f8d8348d00b0a55885cffa33b8fb57`:

| Workflow | Run | Observed status | Conclusion |
| --- | --- | --- | --- |
| Backbone quality | 39418126819 | queued | none yet |
| OpenCode native discovery | 39418126863 | in progress | none yet |

These observations are a timestamped publication snapshot, not a claim that remote
checks passed. This evidence-only follow-up will have a new commit; its exact
remote identity and latest observed CI state are recorded in the PR description
after that update, avoiding a self-referential commit ID in this file.

The local full run passed 431 tests; the later bounded repair check passed its
12 affected tests. Actual remote native/container execution is separate evidence.
The previous base-owned validator remains a real failed migration gate, with no
candidate fallback or bypass. No merge, release, deployment, downstream edit,
repository-setting change or integration activation was performed.

AC-8 is satisfied by this draft publication and exact-tree/check-state evidence.
Completing this scoped delivery does not mark the PR ready to merge or certify
a copied project's operation. See [closeout](closeout.md) for remaining work.
