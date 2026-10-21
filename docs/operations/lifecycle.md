# Security and operating records

Use these questions with the [core policy](../agent-governance/core.md),
[architecture contract](../agent-governance/architecture.md),
[testing contract](../quality/testing.md) and [CI/CD contract](../quality/ci-cd.md).
They make relevant lifecycle duties practical without selecting a server, database,
cloud, release cadence or support model for every project.

## Select the applicable records

| Concern and selection trigger | Reusable starting point |
| --- | --- |
| Material assets, inputs, privileges or trust boundaries | [Threat model](../templates/operations/threat-model.md) |
| A deliverable someone must start, observe, stop or recover | [Operating runbook](../templates/operations/runbook.md) |
| Security or service failures needing coordinated handling | [Incident record](../templates/operations/incident.md) |
| Data or configuration whose loss must be recoverable | [Backup and restore](../templates/operations/backup-restore.md) |
| Published artifacts, supported versions or planned retirement | [Release and support](../templates/operations/release-support.md) |
| Selected local CI workers and execution evidence | [Local CI adoption](../templates/operations/local-ci.md) |

An owner assesses applicability during architecture/planning and updates it when
the change affects the answer. Record the scope, rationale, owner and affected
gate for non-applicability or an unresolved decision. Tailoring may combine records
or refer to an existing authoritative system; it cannot silently drop a required
verification or weaken an adopted project gate. A small local tool may use one
short combined record. Requirements and design retain their existing authority.

Common blank templates remain managed guidance. Copy selected questions into
project-owned operational records or map equivalent fields in existing tools.
Keep actual commands near the [development map](development.md), actual values
under the [configuration contract](configuration.md), and scoped execution evidence
under the project's delivery records. Link owners through approved project roles;
do not insert personal credentials or secrets into a template.

## Evidence and changes

Identify the component, source and delivered revisions, environment, owner and
review state. Distinguish a proposed procedure from an executed exercise. A command
in a runbook, a scheduled backup or a completed template is not proof that recovery
works. Bind actual results, anomalies, limitations and independent review to the
tested revision and environment. Keep unresolved mandatory evidence visible at the
relevant gate; recording a risk does not authorize accepting it.

Changes to interfaces, credentials, deployment topology, persisted data, support
promises or external dependencies trigger a review of the affected records and
their previous evidence. Reconcile procedure changes with actual permissions,
rollback/forward recovery and maintained versions before use. Communication,
production access, release and destructive recovery remain separately authorized
actions; a template grants none of them.

## Basis and limits

These original Backbone questions are informed by the following official guidance,
whose public scope/status was checked on 2026-10-21:

| Source | Limited use here |
| --- | --- |
| [NIST SSDF 1.1, SP 800-218, Final February 2022](https://csrc.nist.gov/pubs/sp/800/218/final) | Security/design risks, release integrity and retained release information. |
| [NIST SP 800-61 Rev. 3, Final April 2025](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Incident preparation, detection, response, recovery and improvement within risk management. |
| [NIST SP 800-34 Rev. 1, updated November 2010](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) | Contingency priorities, recovery planning, exercises and maintenance; adapted from its federal information-system scope. |
| [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | Assets, data flows/trust boundaries, threat treatment and validation; technique remains a project choice. |

The sources inform the questions; the file shapes and obligations are Backbone
choices. They do not make every source recommendation universally mandatory or
establish full-method adoption, normative conformity, certification, legal duties
or successful operating capability. Apply the project's actual stronger obligations.
