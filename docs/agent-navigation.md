# Agent document navigation

Navigation connects a scoped task to the documents, technology obligations and
checks that its agent must use. The canonical core and quality policies remain the
authority. `.engineering-backbone/navigation.json` is a project-owned routing
manifest; it does not grant permissions or replace the Task Packet.

## Route contract

| Input | How it selects context |
|---|---|
| Existing Task Packet | Supplies the role, authorized include/exclude scope, acceptance and stop contract |
| `task_type` | Selects `bugfix`, `implementation`, `architecture`, `review` or `documentation` documents |
| Affected `paths` | Files select containing component prefixes; directory requests also select mapped components beneath them |
| Named `components` | Supports design-level work within Task Packet scope; does not authorize an entire subtree |
| Matching components | Adds their technology profiles, documents and actual workflow check bindings |
| Core and selected quality profile | Adds inherited policy, selected catalog files and required quality documents |
| Native instructions | Adds root/ancestor `AGENTS.md`; directory/component requests include descendant instruction scopes |

Paths are relative to the repository root, use `/`, and match by complete path
segments: `src/api` matches `src/api/service.py`, never `src/api-old/service.py`.
Overlapping components combine by union. Task Packet exclusions win over includes;
an unmatched or out-of-scope concrete path fails. Task Packet `*`, `?` and character
classes match within one segment; a whole `**` segment matches zero or more
segments. Role comes from the packet, never from a replacement value in the request.
Directory/component requests walk descendant instruction scopes with a bounded
4096-directory limit and reject symlink/reparse subtrees or unreadable traversal.
Narrow oversized requests to affected paths. Reading a component context does not
broaden authorized edit scope.

The manifest maps document IDs to existing files, optionally with a supported
Markdown heading anchor. `always`, each of the five Task Packet roles and each task
type refer to those IDs. Components declare `id`, `paths`, technology `profiles`,
`documents` and `checks`. Each check binding names a selected `TECH-*` rule and
actual PR workflow `check_ids`; every required any-of check-kind group must be
covered. Independent review must assess the commands and coverage behind those
IDs. The resolver does not run them or infer missing languages from file suffixes.
With an enabled trusted workflow base, existing check IDs use that base's complete
approved definitions for coverage and receipt output, matching workflow preparation.
Genuinely new IDs retain their candidate definitions. The full candidate workflow
file is still hashed, so its changes invalidate an older receipt.

All declared document references are checked, including routes not selected by the
current request. Use exact case, nonempty regular files and repository-local paths;
symlinks, traversal, ambiguous case and unsafe portable path names fail. Anchors use
simple ATX headings with letters, digits, spaces, `_` and `-`; unsupported renderer
features are not inferred. Unexpected `AGENTS.override.md` blocks resolution for
explicit reconciliation, rather than silently replacing inherited authority.
Map relevant provider role, skill and path-instruction files explicitly into the
routes. Copilot `applyTo` matching and custom-subagent inheritance are not simulated
by this resolver; verify them in the intended client.

## Resolve and use context

Task intake and packet preparation may precede resolution. Once the packet exists,
an active navigation installation requires these steps before scoped work:

1. Discover the project's trusted instructions and approved tool checkout. Validate
   the snapshot with the normal project gates. Do not execute a candidate branch's
   modified guard as the authority for its own policy changes.
2. Create a request with the actual packet, task type, affected paths or named
   components and declared full lowercase commit SHA. Keep scope within the packet.
3. Resolve with the approved guard and read **all** returned documents. Apply their
   selected mandatory rules, documented defaults and project requirements.
4. Carry the request and complete context into each handoff, together with the Task
   Packet's acceptance, authorized actions, expected output, checks and stop/return
   conditions. The receiver recomputes and verifies before using that context.
5. Resolve a new request when role, scope, selected paths or snapshot changes.
   Delegation needs its own correctly scoped Task Packet when its role differs.
   Missing or stale mandatory context blocks the affected task until corrected.

Example request (replace the sample paths and revision with project facts):

```json
{
  "schema_version": "1",
  "task_packet": "plans/database-fix-task.json",
  "task_type": "bugfix",
  "paths": ["src/backend/query.py", "db/migrations/014_users.sql"],
  "components": [],
  "revision": "0123456789abcdef0123456789abcdef01234567"
}
```

Run from an isolated environment with the approved guard's dependencies. In this
example, `/approved-backbone` is a separately reviewed source checkout, `/project`
is the candidate project and `/approved-project-base` is its trusted base snapshot:

```sh
python /approved-backbone/scripts/quality_framework.py resolve \
  --root /project --trusted-base /approved-project-base \
  --request /evidence/navigation-request.json --output /evidence/navigation-context.json
python /approved-backbone/scripts/quality_framework.py verify \
  --root /project --trusted-base /approved-project-base \
  --request /evidence/navigation-request.json --expected /evidence/navigation-context.json
```

The distributed `.engineering-backbone/quality-guard.py` exposes the same commands;
use a separately approved tool copy, not unreviewed candidate code. Add `--source`
only when validating the Backbone source layout itself. Request/context evidence
can live outside tracked source; preserve the exact request with its receipt. Do
not add unsupported fields to the Task Packet or existing evidence schemas.

The receipt records exact document byte hashes, request and manifest digests,
Task Packet document hash, selected catalog/profile/rule identities and concrete
check definitions. `verify` recomputes the complete receipt; missing, altered or
stale fields fail. A file edit invalidates its hash even if its path stays the same.
Both layouts automatically include the existing `.engineering-backbone/project.json`.
Consumer receipts also include `.engineering-backbone/core.json`; source receipts
include `policy/core.json`. The Task Packet and applicable contribution instructions
remain additional sources of scoped task facts.
The declared revision is checked against a non-null packet head; review requires a
frozen packet head. Neither value is authenticated against Git or a provider by
this guard. Bind actual base/head/patch evidence separately for formal review.

## Adoption and updates

Copier's optional quality package installs the managed extension, guide and schemas
and seeds an **inactive** project-owned navigation manifest. Missing navigation
remains compatible with legacy consumers; it is not a navigation conformance claim.

1. Adopt active quality and workflow profiles through their own reviewed contracts.
   Select only technologies actually used by each component; satisfy their required
   quality profiles and check-kind bindings. Record runtime/tool versions and
   scoped rule choices in the quality plan and technology guide.
2. Complete the inactive manifest: document IDs, role/task routes, component paths,
   technology selections, required documents and actual check IDs. Review route
   coverage and instruction compatibility. An empty seed is not activation-ready.
3. Merge the complete inactive seed. In a separate activation PR, change only its
   `enabled` value. Supply the reviewed base to validation: activation must match
   that complete seed exactly apart from `enabled`.
4. Exercise representative successful and failing task routes and the intended
   native clients. Configure required repository gates separately. Receipt success
   is one piece of evidence, never human acceptance or semantic approval.

Copier preserves existing native files and the project-owned manifest on updates.
Refreshing managed policy or fragments does not update those native bodies: merge
approved entrypoint/role/skill routing instructions manually in the consumer PR,
preserving stronger local rules. Existing active document IDs/targets, routes, selected profiles and check bindings
cannot silently disappear, remap or weaken; a rename needs a separately reviewed
migration preserving the current controls. Managed extension bytes come
from the reviewed Backbone version; candidates cannot supply a replacement catalog.
A broader authority or migration change needs its own reviewed contract.

Technology obligations use the same policy authority. `TECH-*` rules are mandatory
when selected. Recommendations are defaults with a recorded technical rationale
for deviation; `free_choices` leave routine implementation decisions to the agent
within scope. No extra owner approval is required solely for an allowed free choice.
Technology guidance is `docs/quality/technology-profiles.md` in the source and
`.engineering-backbone/technology-guide.md` when installed. Provenance identifies
reviewed public references, not certification or proof that every runtime ran.

## Verification boundaries

| Evidence | What it establishes | What remains separate |
|---|---|---|
| Static route and handoff checks | Required paths, identities, bindings and receipt integrity for declared inputs | Document substance, actual commands, completeness of project selection |
| Explicit-context agent smoke | Behavior observed when the request and documents were supplied directly | Automatic native discovery or implicit delegation inheritance |
| Native provider discovery smoke | Observed loading and behavior in the named client/version/configuration | Other clients, settings and future versions |
| Actual project tests and independent review | Recorded execution and scoped assessment on the identified revision | Universal correctness, certification and human merge/release authorization |

Keep these evidence classes distinct in check and review records. Test representative
Python/PostgreSQL bugfix and migration routes, PowerShell/Windows maintenance,
Bash/Linux/container work, architecture, independent review and delegated tasks.
Include missing/renamed/empty documents, missing anchors, case mistakes, symlinks,
unknown profiles, unmatched/excluded paths and stale/tampered handoffs. Record
unavailable native checks as pending or blocked; an agent claiming it read the
right files is not a substitute for observed client loading and scoped behavior.
