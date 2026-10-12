# Codex identity-security Full and Delta result

The [scoped plan](../../plans/codex-security.md) and
[Task Packet](../../plans/codex-security-task.json) retain the three Codex profiles.
This delivery adds managed identity/path checks, trusted historical-tooling
workflow enforcement and accurate runtime boundaries. No role/skill expansion,
dependency/schema/template change or downstream write was performed.

## Immutable review chain

| Phase | Snapshot and result |
| --- | --- |
| Base | `8d4728d92a0125452b223f2fa99226fc8fc8cd0d` |
| Initial Full | Head `c04cc8f966cbb48534e9fc98a4ca408460388c25`; patch SHA-256 `087799c8f6eee49605e8f20f4b0be727f9d48ac3627466281c1d08c5b74ebdfa` |
| Full behavior reviewer | `codex_security_full_behavior`: one P1, CB-1, high confidence; no other confirmed in-scope finding |
| Full security reviewer | `codex_security_full_security`: one P1, CS-1, high confidence; same cause as CB-1; no other confirmed in-scope finding |
| Triage | [Both IDs confirmed before repair](codex-security-triage.md) |
| Repaired Delta | Prior head above, repaired head `168dbc2a498f93261df6541642ec56807743c727`; Delta SHA-256 `3fe3baca91b13dd9d011b2db3227861e90e723a5d2a541bb88b674abea804d93` |
| Behavior Delta | CB-1 fixed; duplicate CS-1 fixed; `NO CONFIRMED IN-SCOPE FINDINGS` |
| Security Delta | CS-1 fixed; duplicate CB-1 fixed; `NO CONFIRMED IN-SCOPE FINDINGS` |

Repaired tree: `c9af1bd968742e7a60db4dc6da54fd4b74ce7675`.
Complete base-to-repaired patch SHA-256:
`cec93081e89b7d5eaa78048effee434440bdbf1e6d3dd3d1463b5d0520d26ae2`.

Both reviewers independently verified the Delta patch hash and inspected frozen
read-only copies. Their disposable reproductions did not change those snapshots.
Each independently executed four targeted tests covering source/consumer path
ambiguity, actual historical-tooling workflow rejection and preservation. Behavior
Delta: 4.836 seconds, exit 0; security Delta: 4.637 seconds, exit 0. Compiler/guard
reconstruction and current pin agreed. Neither reviewer repeated the full suite.

## Coverage and verification

Full coverage included the scoped diff, name/config-file identity and fallback,
recursive/nested native discovery, Unicode/case semantics, unsafe native paths,
adapter flags, candidate import isolation, old-tooling workflow enforcement,
compiler/fingerprint authority, preservation tests and documentation limits.
Delta covered only CB-1/CS-1, their repair and directly affected code, compiled
workflow, tests, pin and evidence. No unchanged area was reopened.

The case-path repair is ten production lines plus compiled text, regression
tests and accurate evidence. Native container/config spelling is checked across
case-insensitive-host ambiguity while role names and exact `.toml` discovery
extensions remain case-sensitive. Local valid roles/settings and stricter
implementer defaults retain their bytes. See [actual check results](codex-security-checks.md):
33 focused tests and 171 complete-suite tests pass, along with source/old-base
validation, rendered fingerprint, actionlint and whitespace checks.

Reviewed fingerprint before the external CP-1 repair:
`302ff94fc067313877a8047456ed354707701e9b50e2c1f8445acfd1a8aeba73`.
The five reviewed previous identities are retained; no unmerged intermediate
identity was approved. One Full round and one confirmed repair round were used.

## External CP-1 and bounded repair Delta

Published head `d61f96a6ff0816255a7371f0e0b4c7328ac51962` matched local final
`ed780777a59c6e84c556f72239f300a49d274a36` exactly by tree. Its advisory provider
Full identified [CP-1](codex-security-triage.md#external-published-full-cp-1), P2:
case-variant files/symlinks-to-files were omitted from the directory-only casing
check. Independent triage confirmed this portable checkout/availability defect.

The two-line production repair inspects `subdirs + filenames` without following
links or changing names/extensions. Repaired local head:
`2f6bfc0335eb0bba85c69cb7d72c53053517f6c1`.
Prior-to-repaired Delta SHA-256:
`a9f8ffca284cebef02fd66c04ffe3af47e7211605b35e6377a1f7c3d5b233828`.
Both independent reviewers verified that hash and reported **CP-1 FIXED;
NO CONFIRMED IN-SCOPE FINDINGS** in the repair/direct regressions.

Behavior Delta independently ran four tests in 4.142 seconds, exit 0; security
Delta ran four tests in 2.723 seconds, exit 0. Both verified the compiled repair
and preservation. Broader checks were pending during those reviews and were not
fabricated as PASS. The later complete retry passed 173 tests in 170.547 seconds;
the initial environmental storage failure remains in the check record. Focused
suites passed 35 tests in 14.140 seconds. Publication was held until the actual
complete success.

Current fingerprint:
`ac82ff9e47346f754865aa322db29089281569e1cf432edd43c624026f8ad3fb`.
Five approved historical identities remain; neither unmerged intermediate pin
is promoted to history. The chain used one local Full round, one advisory
published Full and two confirmed repair rounds with bounded independent Deltas.

## Publication and remaining evidence

This report and Task Packet closeout metadata follow the reviewed implementation
snapshot; the publication record must bind the final commit/tree and full patch
hash, including this evidence-only change. Remote CI/provider status belongs to
that immutable PR record, not a mutable placeholder or inferred PASS. AC-8 remains
pending in the source packet until actual PR publication/remote observations are
recorded. Local independent review is complete; human merge/release remains separate.

No live CLI/IDE, Windows/macOS role selection or write-denial test was performed.
The case-insensitive-host consequence is supported by released source and
executed structural/workflow counterexamples. Host/global/live overrides and
arbitrary generic application cwd aliases are not certified. Source artifacts
retain the documented discovery exclusion; explicit references remain inspected.
These reports are independent review advice, not authenticated human approval.
