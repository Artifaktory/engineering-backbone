# CI clone repair: independent review and triage

## Full snapshot
- Base: `465d11c31c82e0beae1ddcd54b8eb325ce94c1f3`.
- Reviewed head: `d79f89c06161b870b46193aa4e166553039708ca`.
- Tree: `555de71b248069c77b01135f5317786f8c614094`.
- Full binary patch SHA256:
  `b9b74e20e5e1685e4fe360e0d44bd8f35b33d9244cb6404e88e7c16beb425fbb`.

Both independent reviewers inspected the same immutable checkout read-only after
the required deterministic checks passed. Neither authored the implementation.

## Behavior and compatibility
Reviewer `ci_clone_full_behavior`: **NO CONFIRMED IN-SCOPE FINDINGS**.
Inspected repository instructions, core policy, Task Packet, plan, all six changed
files and historical checkout helpers. Confirmed the original upgrade assertions
for local facts, stricter instructions, coherent tooling and trusted validation
are intact. Inspected Copier 9.11.3: `git+` is normalized to file transport,
the supplied source URL is persisted and actual update reads that saved source.

The aliased object store remains in place for both initial copy and tagged
update. Native local cloning is rejected; real Copier copy/update passes.
The reviewer independently ran the ordinary upgrade and new regression:
**2 tests, 13.175 s, exit 0**, using the isolated Python environment.
Recorded red/green and full 234-test results match the raw logs.

## Test coverage and evidence
Reviewer `ci_clone_full_coverage`: **NO CONFIRMED IN-SCOPE FINDINGS**.
Verified snapshot/patch identity, unchanged gates and original assertions, fixture
isolation, acceptance mapping, cause qualification and raw test evidence.

One bounded in-memory mutation changed only the source URI back to the old raw
path. The new regression then failed at actual Copier adoption with Git's native
local-clone symlink rejection. The mutation harness succeeded because it observed
that expected rejection; it is not recorded as a passing mutated product test.
No tracked files were edited and no full suite was repeated by either reviewer.

## Triage and closeout
No findings were reported in either Full review; zero confirmed findings remain.
No repair after Full review was required. These final evidence/Task Packet changes
receive a scoped read-only evidence Delta; its exact head/digest and outcome are
recorded in the commit-bound publication closeout. A code change would require
renewed relevant checks and review.

AC-1 through AC-3 are evidenced in [checks](ci-clone-checks.md); AC-4 is the
independent plan/Full review and this triage. AC-5 remains pending until actual
GitHub identity, checks and advisory review are observed. The versioned Task
Packet preserves that pre-publication state; the PR comment supplies later proof.

## Limits
The original hosted process changing the loose object is unidentified. The
controlled ENOENT diagnostic and deterministic native negative control show the
affected mechanism, not the original runner's timing. Local tests use Git 2.51.1;
hosted PR CI supplies its own result. A post-merge push can only be observed after
human merge. No human approval, release, downstream adoption or host-rule
enforcement is claimed.
