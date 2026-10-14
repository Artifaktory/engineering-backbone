Final functional snapshot: `64133a73668a60cd113e7088925542176d6f6a13`.
This is a continuation of the earlier fresh receiver, not a second fresh receiver claim.

# Final-guard navigation smoke continuation — 2026-10-14

The existing repair-smoke receiver continued read-only against the final captured guard. It verified the new receipt (exit 0), independently checked **28/28 document hashes**, reused **27 previously completed full reads** only after byte equality, and **fully reread the one changed managed navigation guide**. This is not a third fresh full-document smoke or a fresh semantic reread of all 28 documents.

| Identity | Previous repair smoke | Final continuation |
|---|---|---|
| Guard SHA-256 | `32d818cbe4acab3c94de68aa89f27c587be355689fcab6870105544d0107ffd3` | `f4b636346a6e59b6950b00ab465e16c1dbcb15abf32099719ca0ff21ab1f662a` |
| Embedded context digest | `fe2403ff298a4bdcda3030e361f34ea5411c53f6504461de10fe7bc3948bdedf` | `dd97e872b0fceb6eeba329f79fbac8090486281b7d043abffa65e1dcfe011504` |
| Navigation guide SHA-256 | `55f352878d82cf038d898d2e78e757f9a9ba98fa95e5fa960bc57193a8ac7e28` | `f6cf871ac03819b62777db0ee67b4c2e456c5b89a1fceb7ff98aa785c3beddbd` |

Final receipt file SHA-256: `015883f62e90e6be9041a250736dbe25e882344f09c69ee6e8d54658ef5ef134`.

Both copied candidate and trusted-base fixtures differ from their previous counterparts only in `.engineering-backbone/navigation-guide.md`. The selected document set stays at 28 files, now totaling 129,224 bytes. Only the receipt's `documents` and `context_sha256` fields change. The project/core facts, task/role/components/profiles/rules and complete effective check definitions/bindings are unchanged; prior approved-base comparison evidence remains applicable. No project or workflow check commands were executed.

The receiver actually reread and reported the corrected guide contract: source and consumer contexts both include existing `.engineering-backbone/project.json`; consumers add `.engineering-backbone/core.json`, while source contexts use `policy/core.json`. The Task Packet and applicable contribution instructions remain additional scoped fact sources. This consumer-fixture continuation checks guide propagation; it does not exercise source-layout resolution or claim its behavior. Separate repaired regression tests cover that source path.

Both the scripted check and the receiver's independent invocation rejected the previous receipt against the updated fixture with exit 1:

```
Quality framework: Navigation: Navigation: Handoff context differs from recomputed snapshot
```

The receiver declined using the old receipt and took no repair/action on rejection. All **210** files in the previous repair-smoke evidence set remain byte-identical, with no additions. Prior 28-document full-read evidence is retained separately.

Exact command arrays/exits and guard identity are in `structural-result.json`; actual continued receiver observations are in `explicit-context-result.json`. The repeatable bounded harness is `run_followup.py`. This task changed only its new ignored artifact directory, with no tracked edits or commits. Native discovery remains unverified; no unchanged failing native client was retried. Fixture revision remains declared rather than authenticated, and this is not formal Full/Delta approval.
