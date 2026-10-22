# Project architecture source and tool mapping

Template under the [architecture contract](../../agent-governance/architecture.md).
Complete this in the project's architecture index or equivalent authoritative home.
The information contract applies regardless of file format or vendor. This record
does not install a tool, adapter, check or approval mechanism.

## Scope, authority and responsibilities

| Field | Project value |
| --- | --- |
| Project / system boundary and mapping owner | `TBD` |
| Adopted Backbone revision and local policy authority | `TBD` |
| Architecture scope and source revision | `TBD` |
| Requirement decision owner and approval rule | `TBD` |
| Design decision owner and applicable approval rule | `TBD` |
| Independent review and quality responsibilities | `TBD` |
| Required gates and actual enforcement / manual controls | `TBD` |

Do not imply that every routine design choice needs a new human approval. Use the
project's actual delegation and approval rules. Human merge/release decisions and
existing stricter controls remain separate and mandatory where applicable.

## One authority per information item

| Information | Authoritative source / owner | Identity and revision mechanism | Derived view/export and refresh method |
| --- | --- | --- | --- |
| Requirements and acceptance criteria | `TBD` | `TBD` | `TBD` |
| Quality scenarios and proposed thresholds | `TBD` | `TBD` | `TBD` |
| Architecture description and views | `TBD` | `TBD` | `TBD` |
| Decisions and history | `TBD` | `TBD` | `TBD` |
| Requirement/design/test relations | `TBD` | `TBD` | `TBD` |
| Implementation and actual verification results | `TBD` | `TBD` | `TBD` |
| Generated tool/run outputs | `TBD` ignored root and tool/run subdirectory | `TBD` | `TBD` contents ignored, tracked README, non-authoritative, no secrets or uploads |
| Reviews, triage and project decisions | `TBD` | `TBD` | `TBD` |

Declare where to edit an item and which other representations are generated. Record
source snapshots for external systems; a mutable URL alone is insufficient to bind
a review. If sources conflict, identify the owner and resolve the conflict before
using the disputed claim. Do not maintain parallel contradictory originals.

## Identity, relationships and state semantics

| Contract concept | Project representation and mapping |
| --- | --- |
| Stable identities | `TBD`: requirement, scenario, decision, element/interface, view, check and evidence ID namespaces; aliases must resolve unambiguously |
| Provenance | `TBD`: source locator/revision, origin, owner and approval record |
| Relations | `TBD`: how drives/refines/addresses/realizes/checks/supersedes and their reverse lookup are represented |
| Requirement disposition | `TBD`: linked design, justified existing coverage, justified no architecture impact, or explicit open/deferred action |
| Requirement states | `TBD`: separate approval, implementation and verification; retain native Backbone JSON enums when that schema is used |
| Architecture state | `TBD`: distinguish proposed/accepted/superseded decisions and target/observed descriptions without equating acceptance with implementation |
| Evidence states | `TBD`: planned, not run, actual pass/fail/blocked and limits in the selected record format; do not extend existing machine enums silently |
| Change impact | `TBD`: how changed sources invalidate or flag affected claims, links and evidence for reassessment |

The existing Backbone requirement JSON has no owner/provenance/architecture relation
fields. Link companion metadata keyed by ID rather than inserting unsupported keys.
The optional quality CSV keeps its existing fields and states; see
[traceability](traceability.md). Map formats semantically, preserving unknown/open
states instead of collapsing them into success.

## Tool choices and human-readable access

| Optional arrangement | What the project must supply |
| --- | --- |
| Markdown or another document format | Stable IDs, authoritative links, revision binding and inspectable relationship/coverage records |
| Sphinx-Needs for requirements | A project-reviewed mapping of requirement IDs, provenance, approval and relationships; rendered pages retain source identity and do not become a second original |
| LikeC4 for views | A project-reviewed mapping from model elements/views to architecture and requirement/decision IDs; recorded source revision, notation and readable exports |
| Other tools or a mixed stack | The same semantic mapping, readable review access, source/derived distinction and defined behavior for missing/stale information |

These are conceptual examples, not supported configuration syntax or implemented
integrations. Neither Sphinx-Needs nor LikeC4 is required. A tool may own only part
of the contract; companion records fill the remainder without duplicate authority.
Changing tools must preserve stable identity or an explicit alias map, source and
decision history, relationship meaning and review evidence.

## Checks, access and adoption

Record actual commands and CI/manual ownership for link/ID/coverage checks, generated
view freshness and semantic review. Identify which checks are implemented and which
remain planned. The supplied Backbone validator checks its existing structural
contracts; it does not enforce all architecture obligations or assess design fitness.
Missing mandatory manual review is not cured by a documentation build.

Include the contract and declared project sources in agent/reviewer handoffs. Use
existing active navigation rules where installed; preserved native instructions may
need reviewed manual integration. A file or receipt alone does not prove the client
loaded it. Review access, immutable snapshots and actual controls must be available
before claiming the corresponding gate. Do not expose secrets or private operational
data through generated diagrams, public exports or review artifacts.
