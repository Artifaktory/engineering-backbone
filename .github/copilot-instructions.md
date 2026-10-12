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
