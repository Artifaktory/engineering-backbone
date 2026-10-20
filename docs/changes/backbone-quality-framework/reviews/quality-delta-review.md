# Quality framework repair Delta

Both independent read-only reviewers conclude:
**Q-B-1 FIXED. NO ADDITIONAL CONFIRMED IN-SCOPE FINDINGS.**

Prior Full head `b22fd3e2f60d93ea6053f1df09bd6d079ce8c69f`, repaired head
`6446da63ec222fb0c3d1b09d883437c3f94d2b26`, tree
`aa63cedb6ef2454a96bc7b21988146a41fbd36b7`, Delta SHA256
`75e1ac5212ef5418993d1a601f81cc7edd7389437c6db968b95c34f39b935560`;
unchanged base `2cd4d9bd947fbd1aff25c6bec28e98f3fc1b1c13`, full patch SHA256
`416048661531a45e16b33dfff97e662478a16727dcd17942bc9b2d56bbd558fc`.

Scope: confirmed dependency mapping repair, its six-case regression, compiled
propagation, rendered fingerprint and directly introduced regressions. No
unchanged surfaces or new requirements were reopened. Source/authority boundaries
and the seven retained merged fingerprints remain unchanged. Both reviewers
rechecked exact clean snapshot identities; neither made edits or commits.

| Independent reviewer | Actual verification |
| --- | --- |
| `quality_full_behavior` | New six-case regression: exit 0, 0.110s; quality compiler and Delta hygiene: exit 0 |
| `quality_full_behavior` | Six actual reusable-workflow shell executions: dependency/container with PR+maintenance passed; missing either phase failed as required; no candidate quality or project check code executed |
| `quality_full_security` | New six-case regression: exit 0, 0.124s; six temporary container probes: exit 0 |
| `quality_full_security` | Quality compiler, rendered fingerprint and Delta hygiene: exit 0 |

Both inspected the independent repaired full-suite evidence: 278 tests in
655.696 seconds, OK, log SHA256
`d5ae1f63bb071504e4c25df6cad30c44895bf2f753faf22e9a5f1dc68d2e0f23`.
They did not repeat that full suite. The explicit dependency mapping restores the
existing contract while preserving mandatory PR and maintenance coverage and the
existing container mapping. Both compiled copies match the trusted function.
Current tooling SHA256 is
`88d2d1e89cbff9fd925cac1a235de60867ae90a9ae231cde6cbc0a5eed8ee9b2`.
Triage preceded repair and the records preserve the initial finding/check history.

The local functional chain is complete. Evidence-only closeout and actual
publication/hosting results remain separate. Hosted CI, live clients, downstream
activation, authenticated approval and certification are not established by this
Delta. This is not human merge/release approval.
