# Independent security Delta review

Reviewer: `layout_security_review`. This is a bounded Delta following the
[first Full security review](security-review.md), not a second Full review,
human approval or release authorization.

## Immutable subject

- Original base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Prior reviewed head: `54501f1ed542e7f42b5aa315db8863b35e80aeed`.
- Repaired head: `97e68ecefbd21b0d022514f46520a75a6a025536`.
- Repaired tree: `c3ef52a5eaecff857f66ec1599257c2656cc1474`.
- `git diff --binary PRIOR REPAIRED` SHA256:
  `19f36e00426e33d9b1e02f82324ad998cf1b9da1e36b4a7faac490e6c3bb6512`.

The detached Delta worktree's identities, patch digest and clean status were
independently checked. The reviewer made no changes to that snapshot. Scope is
the [triage-confirmed](review-triage.md) LBEH-01, LBEH-02 and LBEH-03 repairs and
security/trust regressions directly caused by them. Unchanged Full-review areas
were not reopened.

## Repair assessment

| Confirmed ID | Inspected repair | Security/contract observation |
| --- | --- | --- |
| LBEH-01 | Native workflow discovers the moved `tst` module using the new top-level package root. | The command still executes the failure-path tests and propagates failure. Matrix, permissions, pinned actions, native smoke and artifact handling are unchanged. |
| LBEH-02 | Legacy adoption paragraph names `docs/dependency-compatibility.md`. | This matches the existing generated output and preservation contract; it changes no template, permissions or consumer ownership. |
| LBEH-03 | Native smoke's default repository changes from `parents[1]` to `parents[2]`; regression exercises default argument parsing and real fixture preparation. | It selects the actual repository root for the relocated script. Explicit `--repo`, strict native-config validation, archive verification, timeout bounds, permission checks, exception handling and failure exit behavior are unchanged. |

The only production-code change in this Delta is the one-level default-root
correction. The regression substitutes the download/native wrapper only inside
the test, uses temporary files and the real preparation function, and explicitly
labels its report as fixture-only evidence. It does not add an execution bypass
or relax the production smoke's validation.

Inspected the complete repair diff and surrounding CLI/test code. The accompanying
[repair checks](repair-checks.md) independently record the exact workflow command
passing all 12 affected tests, structural validation, Actionlint and diff checks.
Those checks were performed by the quality checker; this security Delta did not
duplicate them or execute a new native smoke.

## Outcome and limits

**NO CONFIRMED IN-SCOPE FINDINGS** in the security/trust effects of these bounded
repairs. The three confirmed repairs preserve their relevant security contracts.
This closes the security portion of Delta; behavior closure remains with its
independent reviewer.

The earlier complete run contains 431 passing tests. One test was added by this
repair and the affected 12-test module passed; a complete 432-test run was not
performed. Docker, native Linux/Windows OpenCode execution, model behavior, remote
CI and OS isolation remain outside this Delta's executed evidence.

The actual previous trusted validator's 34 layout/context failures remain the
disclosed merge blocker. No candidate-owned fallback, policy projection, gate
waiver, permission change or automatic downstream activation is introduced by
these repairs. The authorized deliverable remains a draft for inspection, with
human merge/release decisions and reviewed trust migration still separate.
