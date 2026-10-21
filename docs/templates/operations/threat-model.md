# Threat model

State: draft template; no project risks are accepted and no checks have run.
Use with the [lifecycle guide](../../operations/lifecycle.md) and the project's
authoritative architecture. Existing equivalent threat records may be referenced.

## Scope and authority

- Component/system boundary, source/design revisions and responsible owner:
- Linked requirements, data classifications and relevant quality scenarios:
- Intended users/operators, dependencies and assumptions with resolution owners:
- Required security/privacy reviewers and the decision authority for residual risk:
- Applicability, or justified non-applicability and affected gate:

## Assets and boundaries

Identify data, credentials by reference, software/artifacts and operations worth
protecting. Describe entry points, data flows, identities, privileges and boundaries
between trust levels. Link a diagram/view when useful. Include local files, client
and server boundaries, automation/agent tools and build/release paths where relevant.

| Asset or interface ID | Location/flow and trust boundary | Security property and authorized access | Assumption/dependency |
| --- | --- | --- | --- |
| Record applicable entries | | | |

## Threats, treatment and verification

| Threat ID | Concrete actor/trigger and abuse or failure path | Affected requirement/asset | Risk and rationale | Treatment/decision and owner | Check/evidence reference and state |
| --- | --- | --- | --- | --- | --- |
| Record applicable entries | | | | | |

Use the project's selected analysis technique and risk vocabulary. Include relevant
rejected-input, unauthorized-access, credential exposure, dependency and recovery
paths. Record why a threat is treated, accepted, transferred or inapplicable; only
the authorized project role can accept residual risk. Open mandatory treatment
or verification retains its gate impact and next action.

## Review and change

- Actual reviewed model revision, reviewers, findings and triage:
- Verified controls and evidence limits; unresolved risks and decision owners:
- Triggers for reassessment: changed inputs, data, privileges, dependencies or trust boundaries:

Source hint: [OWASP threat modeling guidance](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
informs asset/boundary analysis and threat treatment. This original record does
not prescribe a threat taxonomy or claim a complete named method was performed.
