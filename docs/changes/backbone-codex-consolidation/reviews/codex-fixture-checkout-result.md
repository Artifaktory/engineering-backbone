# Historical fixture checkout Delta

BB-CX-08-DELTA-01 (P2) was independently confirmed before repair in
[follow-up triage](codex-followup-triage.md). A real source clone with
`core.autocrlf=true` transformed fixture bytes and failed original-blob verification.
The [task packet](../../plans/codex-findings-task.json) covers the direct repair.

## Frozen subject

| Subject | Local commit | Git tree |
| --- | --- | --- |
| Previous snapshot, identical to published `d838c5a` | `aa32b7c3a20856e3c760f82731be536876c83d55` | `af9cb6996b6e0eeaec64d6c282b6260f70310c7d` |
| Fixture checkout correction | `a36d18eac8fd2e4c2cfd27c2c5ca77e0b5cdfd1d` | `f3a380b1f5714e2d5650c0342d53f668388693a6` |

Patch SHA256 from `git diff --binary --full-index BASE HEAD`:
`487c7a63cdb590adc1c27d39ef37747dc4b4aeedae5d7ee5b7e5cfc653407504`.
This subsequent evidence/packet update changes no implementation.

## Independent result and executed checks

Separate read-only sessions `codex_delta_correctness` and `codex_delta_security`
confirmed the finding resolved with no confirmed direct regression, and verified
clean initial/final frozen identities. Neither authored the repair. The Delta
covered only immutable fixture checkout bytes and the new regression test.

- Root integration: **94 tests**, 73.547 seconds, exit 0. Current/preceding source
  validators, fingerprint compiler, Actionlint and whitespace checks passed.
- Correctness reviewer independently repeated the real CRLF checkout: historical
  `bootstrap/copier.yml` retains original blob `0c3488e82dafd159b769cc34410c1c582bfe6038`
  with zero CRLF sequences; ordinary root README still receives CRLF. Historical
  copy, genuine upgrade and CRLF regression: **3 tests**, 11.485 seconds, exit 0.
- Security reviewer ran both clean single-commit checkout modes, including actual
  generation and upgrade. Its real inherited-parent-filter probe preserved all
  **57 fixture files byte-for-byte**, while application content received CRLF and
  smudge output and the inherited diff driver stayed active.

The fixture-local attributes protect exact checkout bytes; all original path/blob
assertions, historical source inputs, manifest and consumer attributes remain
unchanged. Current consumer tooling identity is still
`5bca19e704f2e6ca5744cfccb10e52b862dc7b9d4c18ed5f5cb3a6db8aadab4a`.
No new tooling authority or broader source/application attribute rule was added.

Publication, GitHub CI and final Codex re-review are verified separately on PR 1.
Human merge and release remain separate; no downstream write, merge or release
was performed. Earlier scoped findings/results remain in
[the preceding Delta](codex-final-delta-result.md).
