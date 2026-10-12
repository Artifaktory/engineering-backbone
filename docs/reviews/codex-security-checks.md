# Codex identity-security deterministic checks

Base: `8d4728d92a0125452b223f2fa99226fc8fc8cd0d`.
The scoped [Task Packet](../../plans/codex-security-task.json) and
[independently reviewed plan](codex-security-plan-review.md) define acceptance.

Commands used the isolated Python 3.12 environment. Initial Full-snapshot results
on 2026-10-12 (head `c04cc8f966cbb48534e9fc98a4ca408460388c25`):

| Check | Actual result |
| --- | --- |
| `python -m unittest tests.test_codex_security tests.test_codex_workflow_guard -v` | 31 tests, 8.269 seconds, exit 0 |
| `python -m unittest tests.test_validation -v` | 50 tests, 21.661 seconds, exit 0 |
| `python -m unittest discover -s tests -v` | 169 tests, 157.616 seconds, exit 0 |
| `python scripts/validate.py` | Structural PASS, exit 0 |
| Previous merged base `scripts/validate.py --root candidate --trusted-base trusted-base` | Structural PASS, exit 0 |
| `python scripts/compile_toolchain_fingerprint.py --check` | Compiled guards/current rendered identity agree, exit 0 |
| `actionlint .github/workflows/governance-checks.yml` | Exit 0 |
| `git diff --check` | Exit 0 |

Initial Full-snapshot compiled toolchain identity:
`16b7e4935ba2b385b3c19abbbe18eac3ca65c12a375114892b2b2e9b43ddbd39`.
The prior merged Copilot identity
`91f4d1d7be5573f0939cdb9f3859d3ff236807504abaa554207dfc1705190321`
joins the four already reviewed historical identities. Unmerged intermediate
fingerprints from local development are not approved.

## Confirmed case-path repair checks

After [CB-1/CS-1 triage](codex-security-triage.md), native container/config
case-equivalent aliases were rejected without changing role-name or `.toml`
extension semantics. All three forms and canonical/alias coexistence were tested.

| Check after repair | Actual result |
| --- | --- |
| Focused Codex security/workflow suites | 33 tests, 12.840 seconds, exit 0 |
| Complete unittest discovery | 171 tests, 157.062 seconds, exit 0 |
| Source validator and previous merged-base validator | Structural PASS, exit 0 |
| Compiled guards/current rendered fingerprint | PASS, exit 0 |
| Workflow actionlint and patch whitespace | Exit 0 |

Repaired current toolchain identity:
`302ff94fc067313877a8047456ed354707701e9b50e2c1f8445acfd1a8aeba73`.
The initial unmerged identity above is not retained in the workflow's approved
history. The five already reviewed previous identities are unchanged by repair.
Independent Delta evidence is separate from these deterministic results.

## External CP-1 repair checks

The external published Full found case-equivalent native file/symlink-to-file
entries omitted from directory enumeration. [CP-1 was confirmed before repair](codex-security-triage.md#external-published-full-cp-1).
The same case-path check now examines directories and filenames; no native
role-name, extension or runtime boundary changed.

Focused source/consumer and actual historical-workflow suites: 35 tests,
14.140 seconds, exit 0. Source validator, previous merged-base validator,
compiler/current pin, actionlint and whitespace checks each exited 0.

The first complete rerun executed 173 tests in 168.923 seconds and exited 1:
one fixture checkout failed with `No space left on device`. This environmental
failure is retained rather than reported as PASS. After test cleanup, filesystem
inspection reported approximately 13 GiB available; one abandoned Copier clone
was removed only after confirming its origin was a finished backbone workflow
fixture. The complete rerun with that changed resource state passed: **173 tests,
170.547 seconds, exit 0**. The failed attempt remains recorded. No tests were
removed or skipped.

CP-1 current toolchain identity:
`ac82ff9e47346f754865aa322db29089281569e1cf432edd43c624026f8ad3fb`.
No unmerged intermediate identity is added to approved history.

## Acceptance coverage

- AC-1/AC-2: Root, recursive and nested reserved names, explicit declarations,
  referenced effective names and absent/blank-name fallback are rejected.
- AC-3: Malformed/duplicate TOML, invalid UTF-8, missing/external/NUL references,
  native symlink files/directories/ancestors stop inspection without candidate code.
- AC-4: Canonical references, unrelated valid roles/runtime settings, stricter
  consumer implementer defaults and generic application links retain their bytes.
- AC-5: The actual pinned shell rejects a collision that the unchanged approved
  historical validator accepts. Candidate imports and disabled-provider preflight
  tests cannot bypass the trusted workflow. No candidate validator is executed.
- AC-6: The full suite includes actual Copier create/update and clean/autocrlf
  consumer compatibility; both compiled guards and the rendered fingerprint pass.
- AC-7: Adapter documentation and the primary released source record actual
  parent-permission behavior, cwd alias boundaries and unexecuted client checks.
- AC-8: Implementation Full/triage/Delta and remote publication evidence are
  recorded separately; these deterministic results do not replace those reviews.

Copier emitted its expected missing-installed-answers warning for fresh fixture
copies. It did not fail a check. Initial source validation without `--trusted-base`
explicitly reports that history comparison is absent; the separate old-base check
above performed that comparison.

## Limits

No Codex executable was available in this environment; no live CLI/IDE role spawn,
write-denial probe or global/session discovery check was executed. Structural
tests do not prove runtime confinement, review quality or human approval.
Source-only root raw artifacts are excluded from directory discovery, while
explicit references into them remain checked. Consumer mode has no exemption.
Generic application links are preserved, not certified as agent working directories.
No native role/skill rollout, downstream update, merge or release was performed.
