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
