# Neutral project export and reviewed updates

This route creates an **unadopted new project**, in the same canonical directory
shape as Backbone. It supplies shared policy and original document kits without
Backbone delivery history, old active Task Packets, source regression/maintenance
assets, Copier compatibility assets, source validator or active source workflows.
It does not convert an existing source/legacy installation or replace its gates.
Use it with [adoption](../agent-governance/adoption.md),
[configuration](configuration.md) and [development](development.md).

## Select the source authority first

Use a separately reviewed source checkout and an immutable full 40-character Git
commit. The executing checkout's HEAD and `starter.py` bytes must match that
commit. Selected data are read from tracked Git blobs, not dirty working files.
The trusted native validation helper is also Git-attested; its approved Git source
is compiled directly, ignoring local bytecode caches. Schemas come from trusted
Git blobs. Use the source's hash-locked Python environment and isolated
`-I` invocation. The interpreter, installed dependencies and host themselves must
be trusted; a ref check cannot authenticate arbitrary Python startup injection. An agent cannot
make a candidate manifest or a claimed hash into an approved source authority.

```sh
python -I TRUSTED_SOURCE/.engineering-backbone/src/starter.py export \
  --source-ref FULL_SHA --destination NEW_PROJECT --project-name example
python -I TRUSTED_SOURCE/.engineering-backbone/src/starter.py verify \
  --source-ref FULL_SHA --root NEW_PROJECT
```

The destination must be outside the trusted source, new or empty, with no symlinked
ancestors. The exporter calculates the complete plan before writing and uses
exclusive file creation. It never overwrites existing files. An interrupted export
may leave an unadopted partial directory; inspect/discard that new destination
rather than treating it as a completed installation. No automatic host, provider,
runner, CI, optional profile, release or downstream apply is launched.

Only reviewed selected source files are exported. Real `.env` files, private-key
formats and credential filenames are excluded; do not put secrets into any tracked
source document. A filename filter is not a secret detector. Product placeholders
and native profiles remain available but do not prove a working application or
actual client discovery/permissions.

## Ownership and structural scope

| Content | Ownership and treatment |
| --- | --- |
| Common policy, schema/catalog, templates, native roles and included helpers | Managed: exact expected bytes reconstructed from trusted source; local changes require a reviewed common-baseline migration |
| Project entrypoints/facts, environment register/examples, development map and product placeholders | Project-owned: preserve edits; required supported records and canonical context references remain checked |
| Root `artifacts/` convention | Project-owned: tracked README; ignored contents; one subdirectory per tool or run; not evidence, approval or upload material |
| `.engineering-backbone/starter-manifest.json` | Informational provenance/ownership inventory, never the selector of acceptable content or omitted checks |
| Source-only Markdown targets | Rewritten deterministically to immutable source URLs; common local links stay local |

Project code/manifests/tests stay in native component paths. Remove unused product
placeholder folders and extend the project. Add stricter local rules in project
instructions/companions without weakening managed core. All distributed Codex and
Copilot profile selectors remain true under this bounded profile; unused hosts need
not be launched. Changing that installed baseline needs a reviewed integration.
The inactive OpenCode companion is not a switch controlling native file discovery.

Verification checks managed regular files and bytes, safe paths/case identities,
core invariants, project facts, supported governed JSON records, canonical-entrypoint
references, local Markdown closure and trusted native identity/permission guards.
Ordinary JSON fixtures under product directories are not governance artifacts.
An edited provenance hash cannot authorize a modified policy or omitted managed file.
LF attributes keep managed bytes stable in autocrlf checkouts.

This is a **structural seed verifier**, not source CI, full consumer validation,
semantic review, product tests, human approval, host loading, OS isolation or runner
qualification. Existing source/legacy markers are refused. Reserved workflow,
quality-profile, navigation and dependency contract JSON files are refused even
when inactive, as is active workflow YAML: their activation and monotonic history
need a separately reviewed integration retaining stronger gates. Do not switch an
existing project to this lesser gate by deleting its installed contract markers.
No absence/seed result waives an independently required project control.

## Compare an upstream update without applying it

Keep both old and new reviewed source checkouts at their explicitly selected full
refs. The new trusted CLI invokes only the old trusted source's Git-attested
read-only descriptor. It never imports or executes project code and never trusts
project manifest hashes as executable authority.

```sh
python -I NEW_TRUSTED_SOURCE/.engineering-backbone/src/starter.py compare \
  --source-ref NEW_FULL_SHA --old-source OLD_TRUSTED_SOURCE \
  --old-ref OLD_FULL_SHA --root PROJECT
```

The JSON report distinguishes unchanged, upstream-only, local modification,
already-current, conflict, new upstream, removed upstream/conflicting removal and
ownership change. Project-owned files are always preserved. No report action writes,
removes or automatically applies an update. Actual local `.env` values are outside
the comparison plan and are neither read nor printed. A missing/altered provenance
inventory is an explicit reconciliation error, not permission to guess a base.

To obtain the exact transformed new files and new informational provenance, run
`export` from the new trusted checkout into a second empty temporary destination
with the actual project name. Review the comparison, then manually transfer only
the approved common-file changes and new provenance into the project update PR.
Preserve project-owned work and reconcile ownership/obsolete files explicitly;
copying the temporary seed wholesale would overwrite local decisions. Run the new trusted verifier and actual project checks,
then the independent review/triage/repair chain. Runtime/native/CI evidence stays
pending until actually executed. Recovery is a reviewed revert of that update;
there is no automatic update transaction or downstream application.
