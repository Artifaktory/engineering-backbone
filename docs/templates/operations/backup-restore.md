# Backup and restore plan and evidence

State: draft template; no backup, restored data or recovery target is verified.
Use with the [lifecycle guide](../../operations/lifecycle.md). Select this record
when data/configuration must survive loss; otherwise record a reason and owner.

## Scope and recovery decision

- Data/configuration inventory, source of truth, dependencies and responsible owner:
- Authorized recovery objectives: acceptable data loss (RPO) and recovery time (RTO),
  rationale/requirement and decision authority; no universal values are supplied:
- Failure scenarios, integrity/consistency requirements and affected users:
- Applicability or reasoned non-applicability, open decisions and gate impact:

## Protection and recovery procedure

| Information | Project decision/procedure reference |
| --- | --- |
| Backup mechanism and schedule | Include consistent snapshots/transactions or coordinated components where needed. |
| Storage, copies and failure boundaries | Explain protection against relevant loss and separation from the affected system. |
| Access and encryption | Identify authorized roles and key references; never put key values here. |
| Retention and deletion | Define lifecycle, capacity, applicable obligations and safe disposal. |
| Restore prerequisites | Compatible software/schema, credentials by reference, required dependencies and capacity. |
| Restore procedure | Exact reviewed steps, authorization, destination, integrity checks and stop conditions. |
| Fallback/forward recovery | State constraints and actions if restore or migration cannot safely complete. |

Separate the backup from its recoverability claim. Check completeness, integrity and
application-level consistency on a suitable isolated restore target. Avoid replacing
live data during an exercise. Record the authority and safeguard for any destructive
step; no permission is granted by this template.

## Actual restore exercises

| Backup identity/time and tested revision | Restore environment and procedure revision | Observed data integrity/loss and elapsed recovery | Evidence/anomalies/limits | Owner and review |
| --- | --- | --- | --- | --- |
| No exercise recorded by this template | | | | |

Compare actual results with authorized objectives. A scheduled job or successful
backup command is not a successful restore. Record failures, untested scenarios
and changes requiring a new exercise, including schema, key, storage or dependency
changes. Retain evidence through an approved local or project channel.

Source hint: [NIST SP 800-34 Rev. 1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final)
informs contingency priorities, recovery planning, testing and maintenance. Its
federal information-system guidance is adapted here; backup tools, schedules and
recovery objectives remain project decisions.
