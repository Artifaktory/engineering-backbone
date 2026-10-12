# Copilot development Full-review triage

Full snapshot: `be36b14020a7004471b966709414b8309666c6cc`, tree
`119328e1f8777e33783e8473ad38d9250b3fe2e4`. Base:
`2b48fc01d20648ffeeea94e288e1c7d511bae12b`. Full patch SHA256:
`efaac6d6c2bb4cd4a87def8938fdb7fdcd38d4e406ffe8e5de74c7be8b16c894`.
Two independent sessions reviewed the same frozen snapshot, without intervening edits.

| ID | Severity | Disposition | Evidence and repair scope |
| --- | --- | --- | --- |
| CS-1 | P2 | Confirmed | The pinned workflow accepts an unrestricted `.github/agents/backbone-security-reviewer.md` beside its protected `.agent.md`; the supported alternate spelling is omitted from the new registry. Reject ambiguous/alternate known managed identities, retain unrelated local profiles, and test actual old-base upgrades. |

Security review produced CS-1 only. Behavior review produced
`NO CONFIRMED IN-SCOPE FINDINGS`; it independently passed all eight real
Copier distribution tests and corroborated four pinned source examples.

The security reviewer reproduced workflow exit 0 for the alternate file with no
`tools`, versus exit 1 for an elevated canonical `.agent.md`. GitHub's official
configuration reference supports both suffixes and defaults omitted tools to all.
No undocumented precedence between duplicate files is required to confirm this gap.

## Authorized repair and Delta

Account for both suffixes and case variants of known managed role identities in
the trusted validator and compiled pinned-workflow guard. Reject alternate or
ambiguous declarations instead of widening a role's permissions. Preserve unrelated
project-native roles and the original three-role consumer compatibility. Never
silently delete/overwrite an existing local alternate: fail with a reviewed manual
reconciliation requirement. Regenerate current tooling identity, keeping only the
previously approved historical identities. Do not publish the vulnerable intermediate
tooling identity as an approved compatibility version.

Delta verifies CS-1 and direct regressions in native-name handling, historical
upgrades, unrelated local profiles, preservation and compiled-source coherence.
No other scope or fix is authorized by this triage.

## Repair evidence

Before repair, the new direct and actual old-base workflow regressions failed in
ten alias/case subcases: the unrestricted alternate was accepted and the workflow
returned exit 0. After repair, all 23 targeted validation/workflow tests passed.
Known managed identities use their canonical lowercase `.agent.md` file; alternate
suffixes/case variants fail with an explicit manual-reconciliation message. The
tests verify that the alias bytes are unchanged and unrelated native profiles
remain accepted. A candidate `yaml.py` execution marker remains absent.

Current tooling SHA256 after compilation:
`827c3cc0475146eb5e2b1263f118842e1d12d6a14ac9f6dff3b9d723cc4f466b`.
The four previously approved historical identities are unchanged. The vulnerable
intermediate `82fccd70fafeb68a5060a2418c5ffe65f186c0198e4aa3bb450456f6dfbf3bb6`
is not approved for compatibility.
