# Release, support and retirement

State: draft template; no release, promotion, support promise or retirement is
approved. Use with the [lifecycle guide](../../operations/lifecycle.md), existing
release controls and the [CI/CD contract](../../quality/ci-cd.md).

## Scope and authority

- Product/component, version, source commit and immutable artifact identity/digest:
- Intended consumers, supported platforms/runtime/dependency combinations and owner:
- Linked requirements, changes, compatibility promises and user-facing release notes:
- Required checks/reviews, release decision authority and applicability:

## Release and promotion

| Decision or evidence | Project record/reference and actual state |
| --- | --- |
| Candidate qualification | Bind actual checks/results to the tested source and deliverable; list gaps and blockers. |
| Supply-chain records | Integrity/provenance/signature and SBOM as required by the adopted profile; copying this template adds no certification. |
| Promotion | Identify exactly which qualified artifact is distributed/deployed and how its identity is verified. |
| Migration/configuration | Record compatible prior states, data effects, ordered steps, owner and verified recovery. |
| Release/rollout | State approval, authorized channels, staged rollout or equivalent selection and observation. |
| Rollback/forward recovery | Identify compatible artifacts/configuration/data, decision triggers, owner and actual evidence. |

Where the delivery contract requires promoting the tested artifact, reuse that
exact identity. A rebuild is a new candidate requiring its own applicable checks;
equal source revision alone does not establish identical bytes or evidence.
Release approval and deployment approval retain their separate project meanings.

## Support, deprecation and retirement

- Supported versions/combinations, responsible owner and actual support policy:
- Vulnerability/defect reporting route and maintenance/update process:
- Deprecation criteria, affected interfaces/consumers and migration alternative:
- Approved notice/transition arrangements and how delivery is evidenced:
- End-of-support/retirement decision, retained release information and archive access:
- Data/export/deletion, credentials, dependencies and operating resources to reconcile:

Do not promise a support duration or notification deadline without project authority.
Retirement must account for any data/consumer obligations and existing approval gates.

## Actual release record

- Released/promoted identity, time, authority and evidence of checks and distribution:
- Observed rollout/compatibility/recovery results and remaining limitations:
- Follow-up work, owner and supported/retired status:

Source hint: [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) informs
release integrity and retained release information. Versioning, promotion gates,
support promises and deprecation choices here are project/Backbone decisions;
this record does not establish SSDF conformity or authorize publication.
