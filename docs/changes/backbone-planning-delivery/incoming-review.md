# Incoming review disposition

Input: the user's post-PR21 review and independent read-only adoption/portability
audits of `main@4394763d03c1d1302b6b37cef142d0f98f848be4`, followed by the
2026-10-21 planning/standards inventory of Backbone, Artifaktory and Tars.
These observations are baseline findings, not new defects caused by PR21's
architecture documents. They are explicitly in this delivery's scoped plan.

| ID | Observation and evidence | Disposition in this PR |
| --- | --- | --- |
| CONS-01 | `apps/backend/tst/examples/request.json` with `{"value":1}` was interpreted as a governance artifact by `RepositoryValidator.artifacts()`. Baseline control passed and the product addition failed. Schema-looking product fixtures also need the ownership boundary. | Repair artifact discovery and add source/consumer positive and negative tests. Final result belongs in `checks.md`. |
| CONS-02 | Real `core.autocrlf=true` checkout changed four byte-attested files: source inventories for Artifaktory/Tars, `.engineering-backbone/core.json`, and the OpenCode predecessor manifest. Fourteen selected tests on Linux with autocrlf gave 12 passes and two failures. | Add LF attributes and verify every one of the 152 preservation entries through a real checkout. Preserve recorded historical bytes. |
| CONS-03 | `label()` used platform-native separators while the reference-layout assertion expected POSIX. The actual method reproduced the mismatch with `PureWindowsPath`; the auditor did not run a native Windows suite. | Make repository diagnostic paths portable and test that behavior. Keep native Windows runtime evidence separate. |
| CONS-04 | Adoption still called the merged layout a draft and its former old-path failure an outstanding merge blocker. | Correct the current guidance while preserving historical delivery reports. |
| CONS-05 | Active source PR/push workflows included hosted runners and native-smoke artifact uploads; an in-step repository refusal still allocated a runner. The problem extended beyond OpenCode to source dependencies/trusted-policy jobs. | Add source job admission before allocation, dedicated local runners and no source native upload; retain checks. Explain copied-workflow selection and the separate legacy workflow-kit assumptions. |
| CONS-06 | Source validation requires the historical archive and maintenance assets. `.git` history is not required; inherited records must not become current product evidence. | Retain the current validated contract and specify **open** neutral-export work in [follow-up packages](follow-up-packages.md). No claim that neutral export is implemented. |
| CONS-07 | Direct-copy updates are manual file integration. | State this accurately. Reproducible manifest/diff support is part of the follow-up; no automatic downstream update. |
| CONS-08 | Tools, schemas and catalogs remain in `.engineering-backbone/`. | Intentional separation of tooling from product files, not a confirmed defect. No new layout churn. |
| CONS-09 | No installed Sphinx-Needs/LikeC4 stack or Mastra-specific profile. | Optional project profiles, not required generic-core components. Explicit follow-up selection and acceptance. |
| CONS-10 | No shared `.agents/skills/` catalog; native host packages differ. | Separate optional discovery/distribution work. Moving directories alone cannot establish native loading or equivalent host behavior. |
| PLAN-IN-01 | Artifaktory/Tars already distinguish plans, WPs, delivery items, issues and concrete Task Packets, with dependencies/conflict sets/integration. | Generalize their newer planning semantics; keep program IDs, tools, finance/domain controls and branch/runner facts project-owned. |
| PLAN-IN-02 | Artifaktory's stored Spec-Kit task template says tests are optional unless requested, treats different files as a parallelism signal, and lists security hardening under final polish. Its stronger planning governance requires more. | Do not copy these defaults. Derive verification from behavior/risk, plan security early and assess semantic/resource conflicts. |
| PLAN-IN-03 | Backbone has a planning checklist and architecture handoff but no complete generic planning/decomposition kit. Its Task Packet forbids unknown keys and `ready_for_review` binds immutable review revisions. | Supply the kit and linked companion records; preserve existing schemas/state meanings. |

## Source snapshots for the planning inventory

- [Artifaktory planning governance](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/docs/agent-governance/planning/README.md)
  and [decomposition review](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/docs/agent-governance/review-catalogs/delivery-decomposition.md).
- [Installed Artifaktory task template](https://github.com/Artifaktory/Artifaktory/blob/981c9dbc68fdd44acbf25a5351208d9d467b4789/.specify/templates/tasks-template.md).
- [Tars decomposition contract](https://github.com/Artifaktory/Tars/blob/9e91f8c16d747d5a58890d0d16e4c3cf7078b942/docs/agent-governance/planning/30-delivery-decomposition-standard.md),
  on the inspected `feature/frontend` revision, not an assertion about default-branch adoption.

This ledger records scope and disposition, not test success. See the final delivery
checks, independent implementation reviews and closeout for observed completion.
No baseline audit result qualifies the new implementation automatically.
