# Dependency compatibility — independent Full behavior review

- Reviewer: `/root/dependency_review_behavior`, independent read-only reviewer.
- Task Packet: `artifacts/dependency-compatibility/full-behavior-task.json` (`BB-DEPS-009-FULL-BEHAVIOR`).
- Base: `229ac884c1a2ac70f0fb5c961bd517c9eaf740af`.
- Reviewed head: `e6bc0faefe3de7c57e38aa618c4e9653fbe11ba5`.
- Patch: `artifacts/dependency-compatibility/full-review.patch`.
- Patch SHA256: `6f55a2e666e097946585f9990143687e777069cbb3100bfa2217d3e6a8837cd0`.
- Mode: Full; behavior, compatibility and delivery-input coverage.

## Conclusion

**NO CONFIRMED IN-SCOPE FINDINGS** within the inspected snapshot and coverage.
This is neither human approval nor a claim that every client, platform, package
combination or container path executed. There are no finding IDs requiring repair
from this review.

## Inspected coverage

- Read root `AGENTS.md`, `policy/core.md`, `CONTRIBUTING.md`, `policy/quality.md`,
  the assigned Task Packet and delivery plan before reviewing implementation.
- Inspected the optional dependency schema and resolver extension, including safe
  exact/nonempty inputs, application/tooling resolution requirements, library
  ranges, duplicate and malformed declarations, active prerequisites, component
  path coverage and required PR check kinds. Required Docker inputs add container
  evidence bindings; the guard does not pretend to execute package tooling.
- Inspected all-role/all-task routing, component selection by declared artifact
  path, inclusion of policy/contract and selected native inputs, actual-byte hashes,
  approved workflow definitions, inherited requirement preservation and stale
  handoff rejection. Existing check IDs retain base-approved definitions.
- Inspected complete inactive-seed/enabled-only adoption, legacy absence, inactive
  optional installation, Copier preservation of project contracts/documents and
  application Dockerfiles, and rendered consumer integration tests. Compared the
  compiler propagation paths into the quality guard, validator and workflow.
- Inspected source pin/hash parsing and source Git-index file checks, installed
  locked-version and declared-requirement checks, negative tests, actual root
  Dockerfile, build-context exclusions, source compatibility documentation and
  agent entrypoint links. Source CI checks tracking outside the image, then builds
  the tracked Dockerfile and runs offline validation/compiler/Copier smoke.
- Inspected Docker smoke feasibility: the image supplies a Python virtual
  environment, Git, an unprivileged user with a home and temporary storage; the
  smoke's Copier tests create their own temporary Git repositories and do not
  depend on the excluded source Git history. This is static feasibility review,
  not executed image evidence.
- Confirmed the shared policy distinguishes declared requirements, repeatable
  installation and actual behavior evidence; source and consumer responsibilities
  remain separate. Routine dependency choices retain scoped agent freedom.

## Evidence and limits

Executed independently on the frozen head:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_dependencies.py' -v
exit 0; 21 tests passed in 5.570 seconds

git rev-parse HEAD
e6bc0faefe3de7c57e38aa618c4e9653fbe11ba5

sha256sum artifacts/dependency-compatibility/full-review.patch
6f55a2e666e097946585f9990143687e777069cbb3100bfa2217d3e6a8837cd0

git status --short
exit 0; no tracked changes
```

The assignment reported pre-review PASS evidence for the relevant guard,
navigation, source and integration tests; source/trusted-predecessor validators;
all four compiler checks; real immediate-predecessor Copier update and workflow
attestation; clean locked installation; Actionlint; and whitespace checks. This
review inspected corresponding code/tests and independently reran the 21 guard
tests; it does not relabel every supplied check as independently rerun.

The broader full regression suite was still running when this review was
assigned. Its result is **pending evidence for this review** and remains a
separate publication gate. No PASS is claimed here.

Actual Docker build and image smoke were unavailable locally and were not executed
by this reviewer. The real CI container result is required before claiming
container compatibility. Native Windows execution, real PostgreSQL application
integration, native Codex/Copilot instruction loading, remote PR tree readback and
GitHub Codex review execution were not exercised by this review. The general
policy mandates component-specific evidence where applicable; this tooling source
does not implement a PostgreSQL application or attest arbitrary consumer stacks.

No source edits or repairs were made. Only this ignored review artifact was added.
