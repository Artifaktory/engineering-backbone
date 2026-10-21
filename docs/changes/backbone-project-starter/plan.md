# BB-START-018: usable project starter

## Authority, scope and delivery

The user authorized one combined PR on 2026-10-21 for environment/secrets,
local CI readiness, neutral export/update comparison, reproducible development
start and small security/operations templates. Actual merged main is
`4e74c7e5f3a07430768f670c4271c1e1a0e28f68` (PR23); branch
`feat/project-starter`. HIGH risk: executable export and distributed governance.
Publication is authorized; merge/release/deploy, runner registration, repository
permissions/protections and downstream application are not part of this delivery.

Root integrates separate read-only architecture/planning advice. Independent plan
review precedes implementation. Separate authors own environment tooling, runner
readiness, export/update and lifecycle documents. Separate checker and two required
Full reviewers (behavior/traceability and authority/security/compatibility) inspect
the same immutable subject. Separate triage decides findings before repair; Delta
covers confirmed fixes/direct regressions. Maximum two Full rounds and six repair
iterations; broadened trust/scope requires a reviewed plan update.

## Requirements and work packages

- START-01: Root `.env.example` contains harmless comments/placeholders only;
  project-owned `config/environment.json` declares variables, types, contexts and
  secret classification. Source has no invented application credentials. A stdlib
  checker validates actual process values or an explicitly selected literal env
  file, with process values taking precedence. No shell sourcing/interpolation,
  default automatic file loading, secret defaults, raw values, input lines or
  environment dumps in errors. Test required/type/duplicate/malformed/redaction/
  substitution failure paths. Document role-scoped credential delivery, rotation,
  Git hygiene versus OS access and actual framework loader selection.
- START-02: A stdlib local doctor uses fixed argv, bounded timeouts and suppressed
  tool output to check observed OS/architecture, Git/Bash/Python and selected Linux
  Docker or Windows PowerShell prerequisites. It installs/provisions nothing.
  Document exact `backbone-ci` label and repository/group/service checks plus
  actual execution evidence. An inactive local/no-upload consumer example remains
  outside active workflow paths, fails when unconfigured and preserves stricter
  existing workflow/quality gates; it is not a replacement for the activated kit.
- START-03: Implement a real neutral exporter into a new/empty destination with
  canonical product/document/native paths, no source delivery archive, source
  regression/maintenance assets or active source workflows. Generate neutral
  project-owned entrypoints/facts/command map, no foreign active tasks/PASS claims.
  Source-owned neutral seed text lives under `.engineering-backbone/starter/`;
  copied Markdown links to omitted source-only assets become immutable source URLs.
  An executable-owned selection/transform plan and explicit trusted full Git ref
  determine content; candidate manifest/mode flags never waive source validation.
  A separate trusted-source seed verifier reconstructs expected managed bytes,
  checks regular safe files, core floor/project facts/engineering records and
  rejects unsupported active-contract adoption rather than silently ignoring gates.
  Existing source and legacy validators/fingerprints remain unchanged.
- START-04: A read-only three-way update comparison reconstructs old and new
  independently selected trusted snapshots; reports upstream/local changes,
  conflicts, removed/new files and ownership changes. Candidate manifest hashes
  are informational, never executable authority. No automatic apply/delete or
  overwrite. Existing project-owned files remain local. A contributor command
  map states prerequisites, native command, directory, expected result and gaps
  for setup/run/build/test/check; existing workflow kit remains command authority.
- START-05: Original short applicability-based templates cover threat model,
  operating runbook, incident, backup/restore, release/support and local CI evidence.
  Include owners, revisions, triggers, failure/recovery evidence and pending gates;
  justify N/A. No required server/database/container/cloud stack, invented results
  or normative conformity claim. Near-rule official-source hints distinguish our
  choices from OWASP/NIST/GitHub guidance. Keep stricter project controls.

Source root/CONTRIBUTING/adoption/config/scripts/operations/template indexes point
to this kit. Preserve historical files and native ownership. Retained Copier
consumers continue their existing distribution/validation; do not silently switch
an existing source or legacy consumer into the new seed route. The neutral export
is the new route for an unadopted destination, not permission to downgrade an
existing project. Runtime/dependency/container inputs and active CI YAML stay
unchanged absent a confirmed scoped defect.

## Architecture and trust boundaries

The executing reviewed checkout is the export/verification authority. It must
match the explicit immutable ref; read tracked Git blobs, not dirty working-tree
content. Candidate `.engineering-backbone` metadata records provenance and
ownership but cannot choose included obligations or acceptable bytes. Managed
policy/guides/schema/catalog/helpers stay exact; project facts/entrypoints/records
are separately owned and structurally checked with trusted schemas. No candidate
code is imported/executed during seed verification/update comparison. Symlinks,
escaping paths, invalid Git refs and nonempty destinations fail closed before
writes. Exclude actual secrets even if accidentally present/untracked; do not
scan their values into logs. Native files supply restrictive guidance only; no
client launch, provider qualification, credential grant or OS isolation is claimed.

A seed verification result covers only its stated structural baseline; product
behavior, meaningful local instructions, optional activation, real agent discovery,
runner access and hosting enforcement require separate actual evidence. Unsupported
active optional contracts cannot disappear or be accepted under a lesser seed gate.
Existing source validation retains the complete history requirement. The new
verifier refuses source/legacy installations using fixed marker paths. Reserved
optional contract files require a separately reviewed integration; an enabled
quality/workflow/navigation/dependency contract cannot be silently ignored. LF
attributes protect managed export bytes on native checkouts. The project manifest
is informational only; changing it cannot change expected managed membership. Update reports
are advice for a reviewed PR, never an update transaction or new trust root.

## Verification, publication and residual gates

Meaningful positive/negative tests cover actual export, neutral identities, omitted
history/workflows/secrets, link closure, managed tampering even with forged manifest,
project JSON independence, required records/core/schema checks, overwrite/symlink/
path refusal, update conflicts/ownership/deletion and no candidate execution.
Environment tests use fake sentinel credentials and prove no value disclosure.
Doctor tests cover wrong OS/arch, missing executable, timeout, nonzero/daemon
failure and redaction. Exercise the real doctor where available; record native
Windows/Docker/fleet limitations explicitly. Test source and retained real Copier
copy/update behavior; do not rewrite historical fixture bytes or relax assertions.

Freeze a committed subject. Independent checker runs candidate validator, actual
base-owned validator from a separate base checkout with `--trusted-base`, four
compiler checks, source dependencies, complete unittest suite, protected paths and
committed whitespace. Full reviewers see the same base/head/binary patch digest
only after deterministic gates. Triage precedes any repair. Preserve failed runs.

Later evidence-only commits repeat candidate/base-owned checks and actual committed
base/head whitespace. Publish a draft PR if required remote/native/fleet evidence
is pending. Verify exact trees/ordered parents/binary patches if connector commit
metadata changes IDs; read back final PR head/base/paths and actual remote jobs.
Current fleet inventory is unavailable through the connector; queued jobs are not
passing. Do not bypass `backbone-ci`, use deployment runners/hosted fallbacks, upload
artifacts or invent registration/access proof. Recovery is discard of an unadopted
export or a human-reviewed revert; no destructive cleanup/force push.
