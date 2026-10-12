# Engineering Backbone Copilot instructions

Read [policy/core.md](../policy/core.md), [CONTRIBUTING.md](../CONTRIBUTING.md), the
active Task Packet and project instructions before non-trivial work. This
repository is the shared agent/engineering control plane: its changes are HIGH risk.

- Work within an explicitly authorized, scoped Task Packet. Inspect the branch,
  base revision and worktree; preserve unrelated changes and stricter local rules.
- Keep planner, implementer, quality checker, independent reviewer and triage roles
  separate. Reviewers inspect an immutable snapshot read-only; authors do not
  approve their own implementation.
- Run relevant deterministic checks before Full review. Triage before repairs;
  repair confirmed findings only; Delta review covers those fixes and directly
  introduced regressions. Expanded scope or trust boundaries need a new Full.
- Record actual commands, exit codes and acceptance evidence. Unexecuted checks,
  runtime limitations and missing permissions are explicit; never invent PASS.
- Governance, agent permissions, templates, schema and CI changes need downstream
  compatibility and negative tests against the trusted base. Never weaken gates.
- Never commit secrets, overwrite unrelated work, force-push or use destructive
  Git cleanup. A requested PR does not authorize merge, release or deployment.
- Human merge and release approval is mandatory. No automatic downstream apply.

Install with `python -m pip install --require-hashes -r requirements.lock` in an
isolated Python 3.12 environment. Validate with
`python scripts/validate.py`, `python scripts/compile_toolchain_fingerprint.py --check`,
`python -m unittest discover -s tests -v`, and
`git diff --check`. Target the configured base branch; preserve real review evidence.

For PR review, prioritize correctness, security, compatibility and downstream
regressions. Use stable finding IDs, severity, path, trigger, impact, evidence and
validation. Delta review inspects confirmed repairs and directly introduced
regressions; expanded scope requires another Full round. Review instructions
changed in a PR must also be assessed against the trusted base policy.

Custom agent profiles do not activate automatic GitHub PR review. Product review
settings and runtime discovery are separate. AI approval is advice; human merge and
release approval remains required even if a product can submit an approving review.

## Shared source-project operating contract

Discover root and applicable path instructions; adapters and skills follow the
canonical policy. Resolve unexpected repository overrides. Independently review
non-trivial implementation plans before implementation. Record required/optional
reviewers, budgets and stop conditions without broadening authorized scope.

Reviews bind base/head revisions and a patch digest, report coverage/unreviewed
areas, and require concrete execution paths, impact, evidence and diff causation.
Delta uses the prior reviewed head, repaired head and confirmed IDs. Do not reopen
unchanged areas; use at most two Full rounds unless a confirmed blocker, relevant
new changes or a documented human exception justify another. Remote reviews remain
advisory without a separately approved formal project contract; automatic reviews
or fixes never bypass local stops and triage.

Closeout maps acceptance to actual evidence or pending/blocked/failed states.
Preserve installed local Publish-Go, signatures and history gates; the backbone
does not implement or authenticate them. Structural PASS is not semantic review.
