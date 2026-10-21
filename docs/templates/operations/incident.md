# Incident or incident exercise record

State: blank template; identify whether the eventual record is a real event or an
exercise. No incident, notification or recovery result is asserted here. Use the
[lifecycle guide](../../operations/lifecycle.md) and established response procedures.

## Identification and responsibility

- Incident/exercise ID, scope and protected evidence location:
- Affected component, environment, artifact/configuration revisions and known impact:
- Detection time/source, current state and project severity rationale:
- Coordinator, technical owner, decision authority and approved escalation roles:
- Applicability and any known context/evidence gaps:

## Response and evidence

| Time and actor role | Observation or authorized action | Evidence reference | Result, uncertainty and next decision |
| --- | --- | --- | --- |
| Record actual events in order | | | |

- Triage: distinguish observed facts, hypotheses, affected users/data and unknown scope.
- Containment: state authority, expected benefit, possible service/data impact and stop conditions.
- Investigation: preserve relevant evidence, access restrictions, provenance and retention;
  avoid raw credentials/personal data in general logs or agent context.
- Recovery: identify the approved artifact/configuration/data state, integrity checks,
  restoration steps and the observation needed before resuming use.
- Communication: record owner, audience, approved channel, content review and actual
  delivery status. This record itself does not send messages or confer authority.

## Closure and improvement

- Actual recovery/acceptance evidence and remaining exposure or uncertainty:
- Cause and contributing factors, distinguishing demonstrated facts from hypotheses:
- Corrective actions with requirement/risk links, owner, priority and verification:
- Decision to close, responsible authority and continued monitoring:
- Improvements to detection, runbooks, tests, credential handling and response exercises:

A closed record does not erase unresolved required work. Keep access and retention
proportional to sensitive evidence and the project's actual obligations. Production
changes, notifications and destructive containment require their existing authority.

Source hint: [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
(Final April 2025) informs preparation, detection, response, recovery and improvement
within cybersecurity risk management. These prompts do not impose a universal
severity scale, notification deadline or complete CSF adoption.
