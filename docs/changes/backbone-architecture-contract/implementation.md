# BB-ARCH-015 implementation record

## Scope delivered

The canonical architecture contract defines eight document-local rule areas:
source authority/state; requirement derivation; complete bidirectional traceability;
architecture content/views; decisions/evaluation; roles/gates; change impact/staleness;
and tool mapping/handoffs. Core policy makes it required context for scoped design
work by agents and human reviewers. Optional navigation and quality activation remain
separate, and stricter project rules remain binding.

Eight reusable documents cover the index, architecture description, decision,
quality scenario, traceability, independent review, source/tool mapping and worked
example. The example is fictional, draft, unimplemented and unverified. Open
retention/ownership/storage questions demonstrate a blocked implementation gate.
The public-source record distinguishes standards scopes from our semantic rules.

Direct-copy source files stay in their final documentation locations. Legacy Copier
includes the same content at managed Backbone paths, rewrites local links and does
not seed or overwrite product requirements/design. Existing native instructions
continue through canonical core; preserved consumer instructions require reviewed
manual integration. Four new tests exercise actual copy/update, optional-package
independence, preservation and missing-guide/template rejection.

## Responsibility and frozen subject

- Planner/integrator: `/root`.
- Independent preimplementation plan reviewer: `/root/architecture_plan_review`.
- Contract/source writer: `/root/architecture_contract_writer`.
- Template writer: `/root/architecture_template_writer`.
- Legacy distribution/test writer: `/root/architecture_compatibility`.
- Frozen implementation: `f5860b5ec6ff31457c021c8a81cc0128f62fc468`.
- Actual base: `ae317bf30576914d4ed53856be4ae496c6ed64b3`.
- Implementation tree: `d4aa8b2a9024a3cb26293fede0bb4e6e13add713`.
- Base-to-implementation binary patch SHA-256:
  `5440559beb213336e0c424cccf0b4e60ed7d48b30a789188168e27ef5996a287`.

The frozen commit is a GitHub-created object fetched before independent repaired-head
quality checks and reviews. It will remain an ancestor of the PR head, so reproducing
review does not depend on an unpublished local construction commit.

## Confirmed pre-review repair

The [initial check report](failed-checks.md) records the first frozen subject
`1dbd1d68a7a23b8b38f532ed7a9dff8488642a57`: 465 tests, five failure events across
four methods. [Separate triage](check-triage.md) confirmed `ARCH-CHECK-01` before
repair. The new direct quality-policy link broke historical quality-only adoption.
The repair states that architecture duties follow the adopted canonical core and
removes the unconditional package dependency and unnecessary wrapper rewrite.
New complete installs still require the architecture contract through core.

No test, historical fixture, schema, guard, catalog or workflow assertion was
changed. Root preflight of unchanged `test_quality_workflows.py` passed all seven
tests in 7.335 seconds, exit 0. Independent repaired-head checks and the first Full
round use the frozen subject above; the failed initial run remains visible.

## Boundaries and recovery

No schema, quality catalog, guard/validator, dependency, workflow, runtime or product
implementation was changed. The new document rules are not a semantic CI validator,
Sphinx-Needs/LikeC4 adapter, model qualification or certification. Automated checks
cover their declared structural/distribution scope; independent review assesses
content and authority. Tool selection and project-specific design remain free.

The unrelated earlier PR18 evidence/adoption corrections are excluded. Historical
records retain their bytes and original claims. Revert this scoped delivery to
recover; downstream adoption remains a separate reviewed project change. This
record does not authorize merge, release, deployment or automated downstream apply.
