# Architecture review: TBD scope and gate

Template under the [architecture contract](../../agent-governance/architecture.md).
An independent reviewer fills this from actual inspection. The template itself is
not a completed review, authorization, human signature or approval.

## Immutable inputs and responsibility

| Field | Review value |
| --- | --- |
| Review ID, date, reviewer and independent session/role | `TBD` |
| Author / responsible design owner | `TBD`; reviewer must not approve own implementation |
| Task Packet, scope, risk, acceptance IDs and requested gate | `TBD` |
| Base and head revisions / patch digest | `TBD` |
| External requirement/model source versions or immutable exports | `TBD` |
| Design target state / inspected implementation revision | `TBD`; keep distinct |
| Full or Delta | `TBD`; Delta also identifies prior reviewed head and confirmed finding IDs |
| Applicable project rules, required reviewers and budget | `TBD` |
| Deterministic checks actually run before review | `TBD`: command, result, revision and evidence |

## Assessment record

For each applicable question record inspected sources, the concrete conclusion,
gaps and effect on the requested gate. Use a justified exclusion for an inapplicable
question. A tick alone is insufficient for a material risk.

| Assessment | Questions to answer |
| --- | --- |
| Input and document completeness | Are authority, revision, ownership and scope known? Does every scoped requirement have a justified disposition? Are assumptions and derived requirements explicitly proposed or approved by the proper authority? |
| Design fitness | Do the decisions and behavior plausibly satisfy the prioritized goals? Are meaningful alternatives, negative consequences, sensitive assumptions and tradeoffs assessed? Is complexity justified? |
| Views and consistency | Do the views address stakeholder concerns with clear notation? Do element IDs, interfaces, data ownership, runtime behavior and deployment agree? Are contradictions visible? |
| Risk and failure behavior | Are material trust boundaries, failure/recovery paths and operational assumptions addressed? Which analysis, prototype or check is needed before proceeding? |
| Verification plan | Are criteria measurable or otherwise decidable, with sourced thresholds, owner, environment and method? Are planned checks clearly separated from executed results? |
| Implementation correspondence, if claimed | Does inspected implementation at the recorded revision match the relevant target? Are deviations linked, assessed and decided? |
| Verified behavior, if claimed | Were the required checks actually executed on the stated subject/environment? Do results and limitations support the exact claim? |
| Change impact and authority | Are affected sources/decisions/evidence reassessed? Are prior results kept with their original scope? Are project approval, human merge/release and stricter controls preserved? |

Check adverse cases deliberately: a missing requirement row, an unsourced threshold,
an assumption labeled approved, stale model input, a planned test labeled verified,
and a forced tool/pattern with no requirement basis. Report a defect only when the
actual inspected change exhibits it. Creative or equivalent solutions are not
defects merely because the reviewer prefers another design.

## Findings and coverage

Use stable finding IDs with severity P0-P3, category/confidence, exact location,
trigger and execution/decision path, impact, supporting evidence, requirement or
contract relation, current-diff causation and a minimal regression check. Preserve
these details in the supported review format or a companion record, not unknown
schema fields. List inspected and unreviewed areas, unavailable inputs and limits.

## Gate conclusion

| Claim under review | Conclusion and actual evidence | Blocking gaps / owner |
| --- | --- | --- |
| Description is ready for the scoped review | Pending | `TBD` |
| Design supports proceeding to the scoped implementation | Pending | `TBD` |
| Implementation matches the relevant design | Not assessed | `TBD` |
| Required behavior is verified | Not assessed | `TBD` |

Conclude only for the requested scope and available evidence. The project decision
owner applies its approval rules; reviewer advice does not impersonate that decision.
When no in-scope defect is confirmed, report `NO CONFIRMED IN-SCOPE FINDINGS` with
coverage and limitations. Missing required evidence blocks the corresponding gate.

## Triage and follow-through

Link separate triage classifying each finding as confirmed, rejected or requiring
a human decision, with reasons and owner. Authors repair confirmed findings only.
A subsequent independent Delta binds prior reviewed and repaired snapshots, confirmed
IDs and direct repair regressions. Expanded scope or trust boundaries require the
existing newly scoped Full process. Record the actual final decision and outstanding
items without rewriting the earlier review. Preserve task budgets and local gates.
