# Independent testing and CI/CD review

Status: pending review. Use the [testing contract](../../quality/testing.md),
[CI/CD contract](../../quality/ci-cd.md) and existing
[core review process](../../agent-governance/core.md). This checklist adds no
schema roles, approval authority or automatic reviewer integration.

## Frozen subject and requested decision

Record reviewer identity and independence from authors; review mode; objective;
actual immutable base/head or source/plan revisions; binary-patch digest where
applicable; inspected records/check results; coverage, exclusions and limits.
For Delta, include prior reviewed head, repaired head and confirmed finding IDs.
A planning review assesses proposed verification; a result review assesses actual
evidence. Neither supplies a missing product decision or human merge/release approval.

## Questions to assess

| Area | Review question |
| --- | --- |
| Sources and scope | Are requirements, architecture, acceptance, material risks and their authoritative revisions carried into the strategy? |
| Proportionality | Are methods and applicability justified without irrelevant mandatory tools, documents, test counts or coverage quotas? |
| Test design | Are inputs, prerequisites, observable expected outcomes and meaningful success/failure/boundary paths defined or referenced in test code? |
| Environments | Do actual platform, dependency, data, isolation and live/mock limits support the claimed behavior? |
| Integration | Do component successes connect to real interface and assembled-system acceptance where required? |
| States and evidence | Are execution, outcome, applicability, freshness and gate claims distinguished without unsupported JSON values? |
| Findings and retries | Are product/test/environment errors triaged, attempts preserved and flaky or unexecuted coverage visible? |
| CI/CD mapping | Do real check IDs, events, phases, permissions and evidence correspond to the claimed gate and actual delivered subject? |
| Existing obligations | Are activated profile rules, required jobs, nonwaivable duties and local hosting/upload constraints preserved? |
| Completion | Do all required criteria have current evidence or an explicit blocker; are authorized exceptions genuinely applicable? |
| Change and return | Are affected stale results, renewed checks, integration responsibility and owner/orchestrator return explicit? |

For agentic behavior, inspect the actual task/context-to-dispatch-to-worker-to-review-
to-gate-to-return chain and relevant interruption/rejection/resume paths. Fixture-only
checks cannot establish unexecuted native host/provider behavior.

## Findings and conclusion

Use existing review-evidence fields and companion records. A finding needs stable
ID, severity, location, concrete trigger/path, impact, evidence, diff causation and
minimal relevant regression. Record actual commands/observations and unreviewed
areas. Triage before confirmed repairs; Delta covers those IDs and direct regressions.

Report confirmed findings or `NO CONFIRMED IN-SCOPE FINDINGS`, limited to this
subject and coverage. Do not equate that statement with complete testing or human
approval. Source basis: original prompts informed by T-S03/T-S06 and T-S07/T-S09
in the [source register](../../quality/testing-sources.md#reference-register).
