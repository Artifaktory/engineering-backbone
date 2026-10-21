# Security and operations starter kit

Use this kit with the [lifecycle guide](../../operations/lifecycle.md),
[configuration guide](../../operations/configuration.md) and
[CI/CD evidence contract](../../quality/ci-cd.md). These are original prompts,
not completed project records or executable operating procedures.

| Need | Template |
| --- | --- |
| Explain assets, trust boundaries, threats and treatment | [Threat model](threat-model.md) |
| Start, observe, stop and recover a deliverable | [Runbook](runbook.md) |
| Handle an actual or exercised incident | [Incident](incident.md) |
| Protect and demonstrably restore required data | [Backup and restore](backup-restore.md) |
| Release, support, deprecate and retire versions | [Release and support](release-support.md) |
| Qualify local workers and retain actual CI evidence | [Local CI](local-ci.md) |

Select only applicable records, combine them for a small project, or link existing
authoritative equivalents. Non-applicability needs a reason and owner. An unresolved
decision needs an owner, next action and gate impact. No universal infrastructure,
fixed file count, service availability target or backup frequency is imposed.

Copy selected templates into project-owned locations such as `docs/operations/`
and repair relative links there. Preserve the common kit during updates; never put
actual incident data or operating results into managed templates. Identify source
requirements/design, component/revision, responsible roles and actual evidence.
Keep secrets, personal data and production access material out of reports.

The [local workflow example](local-ci.yml.example) is deliberately outside active
workflow paths and requires reviewed project configuration. It does not replace an
already adopted workflow kit or activate runners/checks. Filled documents and
passing syntax checks establish no human approval, restore success or live CI.
