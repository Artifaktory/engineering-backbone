# Technology profiles and agent decision space

Technology catalog version **1.0.0** adds selected component obligations to the
existing Backbone core/quality rules. It does not replace them. The original
quality catalog, including its inactive C++17 and IEC references, remains intact.
The extension's `cpp` profile is an organization-owned minimum; it does not
activate the older `cpp17` reference or claim a Google C++17 standard.

## Authority and selection

| Source repository | Installed consumer |
|---|---|
| `standards/technologies/sources.json` | `.engineering-backbone/standards/technologies/sources.json` |
| `standards/technologies/rules.json` | `.engineering-backbone/standards/technologies/rules.json` |
| `standards/technologies/profiles/` | `.engineering-backbone/standards/technologies/profiles/` |
| `docs/quality/technology-profiles.md` | `.engineering-backbone/technology-guide.md` |

The compiler-owned extension is distributed with the same reviewed Backbone
revision as the navigation guard. Sources record provenance; rule statements
record our selected obligations; profiles collect rules and decision guidance.
The catalog never fetches a living website during validation or a delegated task.

Projects choose profiles per component in their reviewed navigation manifest and
record exact language, runtime, framework, database, tool and target-platform
versions in that component's authoritative documents. A source's observed version
does **not** select a project's runtime. Combine applicable profiles: for example,
TypeScript + React + Next.js + Node, or Python + FastAPI + SQL + PostgreSQL.
Framework profiles complement the language profiles; they are not substitutes.
Language inference from filenames is advisory; the reviewed component inventory
and affected-path routing must account for all applicable technologies.

Every selected profile's `rules` are mandatory. `quality_profiles` names required
existing core quality selections; it does not enumerate all applicable project
quality/risk profiles. For example, the Python and FastAPI extensions require
the core `python` profile, while the TypeScript extension requires `typescript`.
Core baseline, software/risk selection and stronger local rules remain binding.
Unselected profiles impose no obligations on unrelated components. Generated or
vendor code needs an explicit documented scope decision, not a broad exclusion
that silently covers new project code.

## MUST, SHOULD and free choices

| Level | Stored in | Agent behavior |
|---|---|---|
| MUST / MUSS | Rule `statement` and `check_kind_groups` | Fulfill the selected obligation and its evidence. Do not suppress it or rename a failing check to manufacture success. |
| SHOULD / SOLL | Profile `recommendations` | Prefer the stated approach; a suitable alternative needs a rationale in normal review, not a separate routine approval. |
| FREE / FREI | Profile `free_choices` | Decide independently within requirements, architecture, authorization and mandatory rules. These are examples, not an exhaustive whitelist. |

Tool names in recommendations are examples. Choosing an equivalent approved tool
is allowed; its version/configuration and ability to establish the obligation must
be reviewed. A rule is not satisfied merely because a command has a matching name
or declares a matching check kind. Review scope, assertions, failure behavior and
actual results. Mandatory exceptions are not implemented by this extension;
change the approved contract through a separately reviewed migration when needed.
Core quality exceptions cannot waive a `TECH-*` obligation.

Do not silently adopt an entire external guide. Record the compatible selected
sections and any project style decisions in the component documents. Resolve
conflicting requirements before the affected implementation; continue independent
authorized work where possible. For C++, select one exception/error policy before
combining Google and Core Guidelines. Local style cannot override an applicable
mandatory standard, accepted interface or stronger project requirement. No fixed
class pattern, universal function-length limit or blanket coverage percentage is
introduced here.

## Initial profile inventory

Each cell in the last column lists required existing PR check kinds. A slash
inside a group means either kind may supply that group; comma-separated groups
are all required. The check must actually cover the selected component and rule.

| Profile IDs | Principal evidence | Required PR check-kind groups |
|---|---|---|
| `python` | Boundary typing, error behavior, style and public contracts | lint, typecheck, test |
| `javascript` | Runtime boundaries and asynchronous failure handling | lint, test |
| `typescript` | Strict typing, runtime validation and suppression rationale | lint, typecheck, test |
| `java`, `csharp`, `go` | Compilation, resource/error handling, runtime behavior | build, lint, test |
| `c`, `cpp` | Compiler targets, ownership, bounds and failure behavior | build, lint, test |
| `php` | Syntax/style, public interfaces and validated boundaries | lint, test |
| `html`, `css` | Semantic/rendered behavior and relevant manual accessibility checks | lint, browser/test |
| `sql` | Declared dialect, parameterization and query semantics | lint, test |
| `postgresql` | Real PostgreSQL behavior and existing-data migrations | test, migration |
| `powershell`, `bash` | Interpreter compatibility, paths, failures and cleanup | lint, test |
| `json`, `yaml` | Actual consumer parser/schema and duplicate-key handling | lint |
| `dockerfile` | Reproducible image construction and secret boundary | lint, container |
| `github-actions` | Workflow syntax and negative gate/permission cases | lint, test |
| `windows`, `linux` | Native/target-environment support evidence | test |
| `node` | Runtime behavior and dependency integrity | test, dependency |
| `dotnet`, `jvm` | Target compatibility and dependency integrity | build, test, dependency |
| `docker` | Actual image startup, readiness, shutdown and failure behavior | container, test |
| `react` | Hook/component rules and observable interaction states | lint, browser/test |
| `nextjs` | Production build, rendering boundaries and route behavior | build, browser/test |
| `fastapi` | Request/response, authorization and lifecycle behavior | api, test |

The exact statements and source IDs live in the catalog. Select only technologies
actually used. Selecting a profile makes its stated check groups mandatory even
when the current task touches only a small part of that component. A reusable
project check can satisfy more than one rule if its real coverage supports each.
Inherited component bindings cannot simply be removed in an active candidate.

### Runtime support and workflow boundaries

These profiles do not install Java, C/C++, PHP, PowerShell, PostgreSQL or other
toolchains. They do not expand the existing workflow kit's supported setup
profiles. Project owners provide reviewed runner/container environments and
commands for unsupported automatic setup. Missing tools or unavailable targets
remain explicit blockers for the corresponding required evidence.

Windows acceptance needs native Windows execution for the promised behavior.
Linux containers can establish their Linux user-space behavior; they do not
establish Windows behavior or every host/kernel integration. Document genuine
environment limits instead of relabeling a test as a different platform.

For shared build, maintenance and test automation, Python is the preferred
organization choice. PowerShell and Bash remain supported for existing scripts
and suitable platform adapters. Consider a scoped migration when substantial
shared logic becomes shell-dependent; no unsolicited rewrite is required. Both
shell profiles require actual failed-command and whitespace-path tests. PowerShell
native process exit codes are distinct from caught exceptions; Bash `set -e` alone
does not establish the required failure behavior.

PostgreSQL projects record server versions, extensions, drivers, migration history
and data-risk/recovery assumptions. Their checks run against actual PostgreSQL;
SQLite or mocks cannot establish PostgreSQL compatibility. Migrations must be
checked with prior data as well as a fresh database. The selected data-risk plan
defines when restore/forward-recovery rehearsal, concurrency tests and performance
measurements are required. A passing fresh-schema test alone is insufficient.

## Navigation, handoff and review

The project's agent entrypoint routes to the active Task Packet, core and quality
policy, project profile and navigation manifest. The resolver combines the task
type and role route with **all** affected matching components, then supplies the
relevant documents, technology profiles, exact rule versions and bound check IDs.
The installed technology guide is part of that document context so that an agent
receives its decision space along with mandatory rules.

An implementer and independent reviewer use the same frozen rule/document
identity; their responsibilities differ. The implementer applies obligations and
returns evidence. The reviewer checks semantics, justified SHOULD deviations,
coverage and actual results. Quality checkers execute the approved commands.
Delegations retain task scope, rule/document identity, required evidence and
return/stop conditions. A verified context digest demonstrates intact context,
not that a model read it, obeyed it or has the necessary runtime permissions.

An active manifest or profile is not a certification. Static navigation and
catalog tests establish routing/contract properties. Real language builds,
database runs, native client discovery and agent behavior need separate execution
and evidence. Leave unexecuted tests pending or blocked rather than treating the
installed catalog as proof.
