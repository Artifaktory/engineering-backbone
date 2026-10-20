# Bootstrap Full review and finding triage

Full base: `396737eea7cc2d69b654917dfb62e39541c7ac3a`.
Full head: `fdb9c10b33e209483ef421456fd766bb93c42637`.
Full patch SHA256 (`git diff --binary --full-index BASE HEAD`):
`d6b2b3b1092bd15fd8b2b16a21211eff7f73e449964b2041f83a6ef12fa595b3`.
Two separate read-only sessions inspected that identical snapshot without edits.
Identities: `full_correctness_review` and `full_security_compatibility_review`;
implementers: root coordinator, `agent_adapter_design`, `validation_implementation`.
These are recorded agent-session identities, not authenticated human signatures.

## Confirmed findings, before repairs

| ID | Severity | Reproduction and impact | Triage / required repair |
| --- | --- | --- | --- |
| SEC-01 | P1 | Supported Copier update disabling Codex deletes even preexisting stricter root AGENTS.md; `_skip_if_exists` does not prevent conditional-path deletion | Confirmed. Prevent protected native instructions/profiles/workflows from deletion when choices change; test actual update and reconcile facts explicitly |
| SEC-02 | P2 | Application `examples/api-response.json` and site-absolute README links cause unrelated consumer validation failures | Confirmed. Limit consumer traversal/contracts to backbone-owned or explicitly selected paths; retain checks of managed artifacts |
| SEC-03 | P2 | Local Copilot reviewer `tools: [read]` fails exact default-set comparison | Confirmed. Accept safe stricter consumer subsets while rejecting omitted/unknown/write/delegation tools; preserve exact source defaults |
| COR-01 | P2 | `ready_for_review` Task Packet validates with null base/head revisions | Confirmed. Require immutable revisions for formal-review-ready packets; retain null head for ongoing implementation |
| COR-02 | P2 | Existing consumer `policy/core.json` is mistaken for the backbone source, enforcing source rules on unrelated application policy | Confirmed. Bind source/consumer identity to the executing bundle or an explicit trusted mode, not unrelated candidate file existence |
| COR-03 | P3 | Uppercase 40-hex workflow SHA accepted by Copier is rejected by its generated validator | Confirmed. Normalize or consistently reject accepted references and test the complete generated consumer |

No unrelated debt or additional requirements were triaged as defects. P0/P1 must
be resolved before PR publication. Repairs are limited to those findings and their
direct regressions; freeze the changed snapshot for Delta review by the same
independent sessions. Deterministic checks precede that Delta round.

## Observed validation before repair

- Clean isolated Python 3.12 installation using `--require-hashes`: exit 0.
- Structural validator: exit 0; explicit initial trusted-base limitation emitted.
- Full suite: 38 tests, exit 0.
- Official Actionlint v1.7.12, release artifact checksum verified: exit 0.
- Whitespace/diff checks: exit 0.

The external review reproductions found contract gaps despite those passing tests.
Human merge/release, actual product profile discovery and protected repository
settings remain separate, unresolved readiness controls as documented elsewhere.
