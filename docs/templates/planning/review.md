# Planning, decomposition and start-readiness review: TBD scope

Template for PLAN-07 through PLAN-09 in the
[planning contract](../../agent-governance/planning.md). These are Backbone's review
and gate rules, informed by the methods in the
[source record](../../agent-governance/planning-sources.md). A Definition of Ready is
a project policy here, not a required Scrum artifact. An independent reviewer
completes this from actual inspection; the blank form is not an approval.

## Frozen inputs and responsibility

| Field | Review value |
| --- | --- |
| Review ID / date / independent reviewer identity and session | `TBD` |
| Author and accountable plan/item owner | `TBD` |
| Requested gate and inspected items | Plan / decomposition / scoped execution start: `TBD` |
| Task Packet, approved scope, risk and acceptance IDs | `TBD` |
| Base/head or other immutable source snapshots / patch digest | `TBD` |
| Requirements, architecture, plan and item revisions | `TBD` |
| Required reviewers, controls and review budget | `TBD` |
| Full or Delta | `TBD`; Delta names prior reviewed head, repaired head and confirmed IDs |
| Applicable checks actually executed before this review | `TBD` commands, results, revisions and evidence; name unavailable checks |

Planning review can assess proposed work before implementation exists. Implementation
Full review requires the relevant deterministic checks first under the core policy.
Do not describe plan approval as passing implementation or runtime verification.

## Assessment and evidence

For each applicable row record inspected sources, a concrete conclusion, gaps and
their gate effect. A checked box alone does not explain a material judgment.

| Area | Questions |
| --- | --- |
| Authority and objective | Are scope, benefit, source revisions and decision owners known? Are assumptions and derived requirements distinguished from approved obligations? |
| Complete and proportionate work | Does every scoped requirement/risk have a treatment? Does each item have an authorized purpose? Are missing integration, test, documentation, operational or security tasks visible? Is the chosen depth justified? |
| Useful slices and technical grouping | Are results independently assessable? Is a valid intermediate state possible? Is atomic grouping or technical groundwork justified without forcing every task into a user story? |
| Dependencies and conflict sets | Are edge kinds, versions and start conditions explicit? Is the graph acyclic at execution time? Are shared files, contracts, state and environments coordinated? |
| Capacity and ownership | Are implementation, review and integration responsibility and capacity available? Do estimates expose uncertainty and external prerequisites? |
| Acceptance and quality | Are criteria observable and tied to appropriate verification, environments/data and evidence? Are security and other material quality risks considered early? |
| Integration and recovery | Is someone responsible for the assembled result and its checks? Are merge order, compatibility, failure, migration and recovery addressed where applicable? |
| Start and execution handoff | Are required decisions, accessible context, prerequisites and actual host permissions available? Is the executable scope bounded and bound to the accepted item revision? |
| Change and state meaning | Can stale sources, tracker projections and evidence be detected? Are start readiness, review readiness, implementation, acceptance, Done and release distinct? |

Deliberately inspect for missing scoped work, unjustified extra work, unresolved
contract changes, a shared resource presented as independent, mocks presented as
system evidence, or a planned check presented as passed. Report actual defects with
evidence and diff causation; do not reject a creative or equivalent solution merely
because another implementation is preferred.

## Findings, coverage and gate decision

Use stable finding IDs, severity P0-P3, category/confidence, exact location, trigger,
impact, evidence, contract/acceptance relation, current-diff causation and a minimal
regression check. Preserve details in the supported review format or companion
record. List inspected and unreviewed areas, inaccessible inputs and limitations.

| Claim | Actual conclusion / supporting evidence | Blocking gap and owner |
| --- | --- | --- |
| Plan is adequate for the requested decision | Pending | `TBD` |
| Decomposition supports the proposed assignments | Pending | `TBD` |
| Named items may start within their accepted scope | Not established | `TBD` |
| Implementation and integrated behavior satisfy acceptance | Not assessed by a planning review | `TBD` |
| Merge / release authorized | Separate project/human decision | `TBD` |

The decision owner applies the project's actual approval rules. Reviewer advice
does not impersonate human approval. If no in-scope defect is confirmed, report
`NO CONFIRMED IN-SCOPE FINDINGS` with coverage and limits. Required missing evidence
blocks the corresponding claim. Do not reinterpret packet `ready_for_review` as a
start decision or use a tracker status to bypass the existing gates.

## Triage, repair and follow-through

Link a separate triage record classifying findings as confirmed, rejected or needing
a human decision, with reasons and owners. Repair confirmed findings only. A Delta
binds the previous and repaired snapshots and checks those findings plus directly
introduced regressions. Changed scope or trust boundaries need the existing newly
scoped Full process. Update affected item/source bindings and handoffs; preserve
earlier findings and evidence instead of silently replacing their recorded outcome.
