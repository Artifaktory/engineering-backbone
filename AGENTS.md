# Engineering Backbone agent instructions

Read [policy/core.md](policy/core.md), [CONTRIBUTING.md](CONTRIBUTING.md), the active
Task Packet and project instructions before non-trivial work. This repository is
the shared agent/engineering control plane: its changes are HIGH risk by default.

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

## Repository commands

Install `requirements.lock` with `--require-hashes` in an isolated Python 3.12 environment. Run:

```sh
python scripts/validate.py
python scripts/compile_toolchain_fingerprint.py --check
python -m unittest discover -s tests -v
git diff --check
```

Changes target the project-configured base branch (`main` for this repository).
Run evidence belongs in ignored `artifacts/` directories; durable redacted review
records belong in `docs/reviews/`. This bootstrap PR was explicitly requested by
the human task owner; that authorizes publishing its scoped changes for review.
