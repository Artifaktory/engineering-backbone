# Full authority/security review — dependency compatibility

Reviewer: independent read-only authority/security session.
Task: BB-DEPS-009-FULL-AUTHORITY.
Base: `229ac884c1a2ac70f0fb5c961bd517c9eaf740af`.
Head: `e6bc0faefe3de7c57e38aa618c4e9653fbe11ba5`.
Patch SHA256: `6f55a2e666e097946585f9990143687e777069cbb3100bfa2217d3e6a8837cd0`.

## Result

**NO CONFIRMED IN-SCOPE FINDINGS.**

This is a scoped independent review, not human merge/release approval, a container
execution result or proof of native agent instruction loading. The broader full
suite was still running in the independent quality record inspected during this
review; its final result remains a publication gate. Docker build/smoke is not
executed locally because the engine is unavailable; actual CI evidence remains
required before claiming container compatibility.

## Authority and coverage

Read root AGENTS.md, CONTRIBUTING.md, policy/core.md, the scoped review packet and
plans/dependency-compatibility.md. Verified the patch hash and clean immutable head
before review and reconfirmed the unchanged clean head at closeout. Source edits,
repairs, external writes, publication and approvals were not performed.

Reviewed these changed trust/control surfaces:

- `scripts/navigation.py` dependency parser, exact-file reader reuse, active
  prerequisite checks, component path routing, effective approved check binding,
  complete-seed activation, inherited requirement preservation and context hashes.
  The compiled copies in the quality guard, validator and reusable governance
  workflow follow the reviewed source additions; independent compiler checks
  report matching outputs.
- `schemas/dependencies.schema.json`, including bounds, exact wrapper/component
  fields, application/tooling resolution requirements and library distinction.
  The compiled guard owns runtime validation and does not execute manifest,
  resolution or candidate package commands while resolving context.
- New dependency tests and integration fixtures covering malformed inputs,
  symlinks/case/path collisions, empty/nonregular/oversized artifacts, mandatory
  check kinds, approved-versus-candidate definitions, activation, inherited gates,
  all role/task routes and stale handoffs. Reviewed Copier preservation and actual
  predecessor upgrade/attestation coverage in the independent quality evidence.
- Canonical policy, source compatibility document, adoption/navigation/workflow
  guides, source and generated agent instructions, Copier preservation and
  inactive seeds. Existing catalog identities, stronger project gates and the
  distinction between structural bindings and behavioral proof are preserved.
- `scripts/check_source_dependencies.py` bounded accepted pin/hash syntax,
  normalized direct-to-resolution matching, installed-version checks, `pip check`,
  real Git-root/index tracking, nonregular/symlink rejection and immutable base
  shape; source failure-path tests. Native version files remain authoritative.
- Source CI checkout of the exact PR head with persisted credentials disabled,
  inherited contents-read permission, clean hash-checked binary installation,
  real image build and network-disabled smoke. No continue-on-error or new
  token/write permission was added. Hosted runner selection is inherited project
  scope; runner migration is explicitly excluded from this task.
- Dockerfile and .dockerignore: immutable official Python base, isolated venv,
  locked/hash-checked binary dependencies, unprivileged runtime account,
  temporary writable test workspaces and excluded Git/local environment/artifact
  data. Git-tree reads confirm the real Dockerfile, .dockerignore, policy and
  compatibility document are tracked regular files at the reviewed head.

## Additional independent probes

Executed `PYTHONPATH=tests .venv/bin/python` with the existing isolated dependency
fixture and six additional direct guard probes. Exit 0; all rejected with no
context:

1. `components=[null]`: missing/unknown component keys.
2. String activation flag `enabled="false"`: invalid schema/activation flag.
3. Object in `runtime_files`: invalid runtime-file sequence.
4. Null check ID: invalid dependency check IDs.
5. Empty compatibility-document path: invalid relative path.
6. Candidate workflow removes the required approved dependency check while the
   inherited active contract retains its ID: invalid dependency check binding.

The fixture and its temporary files were cleaned; the reviewed source was not
mutated. Existing checks are credited to the independent quality checker, not
claimed as rerun by this review.

## Image evidence and limits

Inspected `artifacts/dependency-compatibility/python-full-base-image.json`, which
records the root's independent 2026-10-14T11:10:54.571773Z registry lookup. Registry
header and computed index identity match Dockerfile pin
`sha256:5560e9ab8709f459489e5b8aa696eda8a07ef821e14bb122be62d91234bfa98b`.
The recorded Linux/amd64 manifest is
`sha256:edd0b3ec946cc68bd20e39480bd03929016d0fb6254cbf870cd3bc55ea25116d`;
config identity is
`sha256:61d53b56a648da09aa966c5cc46a7e751aea2b38d01f33b04456a9f289685be9`.
Its metadata reports Python 3.12.15 and Git installation history. This supports
input identity/metadata only, not execution. The earlier slim-image artifact is
an initial rejected candidate and was not used as evidence for the full image.

Unreviewed/unexecuted here: Docker build/run; live GitHub CI/PR tree/Codex results;
native Windows execution; downstream application-specific manifests/resolution
semantics and PostgreSQL combinations; native Codex/Copilot context discovery;
repository protection/human approval configuration. Those remain separately
recorded obligations and are not silently covered by this conclusion.
