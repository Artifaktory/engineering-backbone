# Workflow kit finding triage

Full base `1ecbb7a572b3679b422105c557cb88a8bff75dac`, head
`60611c3fde6435adfac6e84d8f34437bda86d889`, tree
`8e96e3852c67bf9a98e9bd6a791d42c5984ef964`, patch SHA256
`e1e890e70b2e80cb03032cfd097da2bcbcae7607492bc649d372285798607d2a`.

## WK-S-1: confirmed P2, configuration validation

Independent security reviewer found that `configuration()` conflates missing file
with a regular configuration containing JSON `null`, because `read_json` returns
Python None in both cases. Schema rejects null, but standalone and integrated
validation incorrectly report a legacy/structural PASS. Root independently
reproduced both exit-zero results on the same frozen checkout in a disposable
fixture. This contradicts AC-1 malformed-contract rejection. Active preparation
still fails; no active-kit merge bypass was demonstrated.

Decision: **confirmed**, before repair. Minimal authorized repair distinguishes
missing-file state from parsed JSON values. Add standalone, compiled workflow and
integrated validation regressions for candidate/base null while preserving genuine
legacy absence, inactive seed and activation behavior. Refresh compiled copies
and the current tooling fingerprint; retain only the six merged historical
identities, not the unmerged initial kit fingerprint.

Repair implemented: distinct missing-file sentinel; existing null reaches object
validation. Standalone, compiled-payload and integrated regressions were added.
Focused 49 tests passed in 18.608 seconds; compilation, source/base validators,
actionlint and diff hygiene passed. Complete repaired suite: 233 tests, 234.476s,
exit 0. Both independent Deltas confirm WK-S-1 fixed and no additional confirmed
in-scope findings. No unchanged-scope Full reopening or unrelated repair.

Delta prior `60611c3fde6435adfac6e84d8f34437bda86d889`, repair
`1ee3df6df160203bcca7f63d9ff7135b423b9e57`, tree
`ef86f0d1656edb3327bb215c426670d439f499be`, delta SHA256
`78c00716e90658835a169dbd594a1427f5a8529293142e9d16c0b0078cac34f5`.
Behavior reviewer independently ran nine scoped tests in 2.641s, exit 0;
security reviewer ran eight in 3.294s plus compiler check, exit 0.
Their snapshots correctly recorded the complete suite as pending at review time;
the later successful complete result is separate readiness evidence.
