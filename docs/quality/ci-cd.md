# CI/CD verification and evidence contract

Use this with the [testing contract](testing.md) and the project's adopted core,
quality and workflow contracts. It connects required verification to actual check
execution and delivery decisions. The [CI mapping template](../templates/testing/ci-mapping.md)
can record the relationship; equivalent existing project records are valid.

**Authority:** MUST identifies a Backbone-owned semantic obligation under the
adopted core. [Source notes](testing-sources.md#reference-register) distinguish public
standard scopes, recommendations and optional specifications. No external source
is asserted to require identical workflow files, a CI vendor, runner labels or
deployment for every project. Existing adopted profile duties and stronger project
controls remain binding. This document activates no workflow or permission and
does not extend the existing workflow schema or runner.

## CI-01: Applicability and ownership

The project MUST identify its actual delivery model, required verification and
decision owners. Select checks from requirements, architecture, material risks,
supported environments and adopted profiles. A documentation project, library,
desktop application and deployed service can require different pipelines. Give
each excluded area a reason and responsible owner; do not invent release or
deployment work merely to fill a diagram.

The project chooses tools, check grouping, workflow topology and appropriate
automation. Manual or hybrid verification can supply explicitly selected evidence;
it cannot silently replace an inherited required automated check. Existing active
profile selections, bindings and protected gates cannot be removed through a
new applicability note. Keep one authoritative command/configuration source and
reference it from the test strategy rather than maintaining competing commands.

Source note: Backbone applicability rule informed by T-S02, T-S03 and T-S09 in the
[source register](testing-sources.md#reference-register).

## CI-02: Bind each required claim to execution

For each required check or manual verification, the mapping MUST identify:

| Information | Minimum meaning |
| --- | --- |
| Purpose and scope | Requirement, acceptance, risk and test/design IDs; affected components and justified limits. |
| Actual check identity | Stable project check ID and authoritative command or procedure reference; identify automated, manual or hybrid execution. |
| Trigger and prerequisites | Event or decision point, trusted configuration, required inputs and start conditions. |
| Inspected subject | Actual source revision and, where relevant, test revision, build inputs and output artifact identity. |
| Environment and data | Relevant runtime/tool versions, platform, configuration, controlled data and external-service assumptions. |
| Decision criterion | Expected result or threshold, required versus advisory role and the gate affected by a missing or unsuccessful result. |
| Responsibility and bounds | Check owner, reviewer where needed, time/resource limits, access and permitted actions. |
| Evidence handling | Run/job identity or manual record, observed results and findings, accessible evidence location, access controls and retention. |

A declared check kind, shell exit code or generated report alone does not establish
its claimed behavioral coverage. Assess the command's meaning and actual results.
Mocks and fixture-based smoke checks retain their limited scope; live integration
or supported-platform claims need the corresponding evidence. The mapping does not
add fields to `workflows.json`, quality-profile JSON or the traceability CSV.

Source note: Backbone mapping informed by T-S03, T-S07 and T-S09 in the
[source register](testing-sources.md#reference-register).

## CI-03: Separate delivery events from implemented phases

Select timing from the risk and gate that the evidence protects. A required result
must be available before that gate is satisfied. This table distinguishes planning
questions from the currently implemented Backbone workflow-kit contract.

| Event or decision point | Verification question | Current kit support and boundary |
| --- | --- | --- |
| Change / PR | Do affected requirements, contracts and applicable static/security/behavior checks hold? | Phase `pr`; required kinds follow selected profiles/capabilities. |
| Configured target-branch push | Does the actual integrated source/configuration retain the necessary evidence? | The PR-check caller also uses phase `pr` for its configured target push; this is not a separate `post_merge` schema phase. |
| Periodic / maintenance | Have time-dependent inputs or broader risks changed? | Phase `maintenance` supports selected `dependency` and `container` commands, plus the workflow's separate secret prevention. General scheduled behavior, load or platform suites need project-owned integration or a separately reviewed extension. |
| Release | Is the identified deliverable ready, intact and traceable to its qualified inputs? | Selected `release` capability requires `release-integrity`, `provenance` and `signature`; `sbom` is also required when dependencies or containers are selected. Release examples remain inert until reviewed local activation. |
| Deployment | Are prerequisites, actual operation and recovery evidence sufficient for this environment? | Selected `deploy` capability requires `deployment-smoke`, `rollback` and `monitoring`. Project authorization and environment integration remain necessary. |

In the current kit, `test`, `browser`, `api`, `migration` and other ordinary quality
checks support phase `pr` only. Release phase is not a generic behavior-test runner.
An arbitrary OS/version matrix, nightly suite, release regression or merge-queue
event mapping is not installed by this documentation. Record needed project checks
or explicit gaps; do not put unsupported phase values into the closed schema or
claim that a policy table has executed them.

For an integrated revision, assess changes in source composition, build inputs and
configuration. Re-execute affected checks or justify the applicability of prior
results. Retain their actual tested revisions; do not relabel an earlier execution
as a run on an untested merge commit. Human merge and release decisions retain
their separately required approvals.

Source note: the event-to-evidence questions are Backbone choices informed by T-S02,
T-S07 and T-S09. Exact kinds and phases come from the existing Backbone implementation,
not an ISO-prescribed pipeline. See [source boundaries](testing-sources.md#reference-register).

## CI-04: Trust, execution permissions and evidence storage

The project MUST identify which configuration is trusted and which inputs execute
candidate code. Apply suitable least privilege, isolated workers and separation
between untrusted checks and privileged release/deployment actions. Review access
to credentials, networks, mutable state and other workspaces. A safe argument format
or schema-valid configuration is not an execution sandbox.

Pipeline routing conditions alone do not authenticate contributor-modified workflow
code or prove runner isolation. Record the required operator-controlled access and
environment restrictions. Permission, runner and CI configuration changes are HIGH
risk under the core. Verify relevant repository protections, exact required-check
names, reviewer eligibility and bypass controls separately from files in Git.

The Backbone source uses a local-runner and no-GitHub-artifact-upload operating
contract. Receiving projects adopting those constraints must retain them. They are
project choices, not general external norm requirements. Missing suitable runners
remain pending evidence; do not add a hosted fallback to obtain a result. Arrange
an authorized, accessible, access-controlled evidence store and retention period
instead of assuming a GitHub upload. Redact secrets and sensitive test data.
Generated local outputs under a declared ignored artifacts root are not CI
evidence and are not uploaded.

The retained optional legacy reusable consumer workflows still have their documented
hosted-runner and artifact-exchange assumptions. This semantic contract does not
convert them into a local/no-upload profile. Such projects must select or adapt
their workflow contract through reviewed changes before activating those callers.
Source CI and a consumer's CI remain distinct adoptions.

Source note: Backbone operational rules informed by T-S09 and T-S10 in the
[source register](testing-sources.md#reference-register). T-S10 addresses supply-chain
security in cloud-native DevSecOps; it is not a complete universal testing norm.

## CI-05: Preserve the identity of the delivered result

When a project produces a release or deployment artifact, its required evidence
MUST identify the actual delivered bytes or equivalent immutable product identity.
Record source/build input references, output digest or immutable version and the
verification that applies to that output. A passing source test does not qualify
a later differently built package. Rebuilding, repackaging or changing runtime
inputs requires an applicability assessment and the relevant renewed checks.

Where integrity, provenance, signature or SBOM checks are required by the adopted
contract, perform and evaluate them. Verify the expected subject, relevant trust
identity and policy; generating a file or finding a signature is insufficient.
These checks complement functional/security acceptance rather than establishing it.

SLSA is an optional, versioned supply-chain specification. A project claiming a
particular track/level must satisfy its actual requirements and substantiate that
claim; a template, hash or runner label alone establishes no level. Its adoption
does not authorize weakening the existing release capability requirements.

Source note: Backbone evidence rule informed by T-S07, T-S09 and optional T-S11 in
the [source register](testing-sources.md#reference-register).

## CI-06: Results, gates and unavailable execution

Use the testing contract's separate meanings for applicability, execution, outcome,
evidence validity and acceptance. Required missing, queued, blocked, cancelled,
skipped, failed or unevaluable checks do not satisfy the affected gate. Record tool
or infrastructure failure distinctly from an observed product failure. Advisory
results must be visibly advisory; a summary cannot turn them into mandatory proof.

The existing workflow kit requires actual success from its fixed set of required
jobs. Candidate reports cannot redefine that set. Its explicit non-applicability
handling for a security command does not waive the independently required secret
check. Preserve these implementation duties rather than interpreting this document
as permission to skip an expected job.

Keep initial failures and investigation results. A rerun requires a stated purpose,
such as a confirmed transient infrastructure problem, repaired test or changed
product input. Treat intermittent results under the flaky-test policy; repeated
unchanged runs until green do not resolve the uncertainty. Any permitted exception
retains its authority, scope, expiry and compensating evidence and cannot rewrite
the original outcome or waive a nonwaivable obligation.

Source note: Backbone gate semantics informed by T-S03, T-S07 and T-S09 in the
[source register](testing-sources.md#reference-register); exact status names and
aggregate behavior are local contracts.

## CI-07: Change, adoption and review

Changes to checks, dependencies, triggers, permissions, evidence handling or gate
logic MUST assess affected claims and trusted inputs. Review whether a candidate
could suppress a required check, substitute a harmless command, falsify evidence
or reach privileged execution. Use relevant producer/consumer and negative checks;
a valid YAML file alone does not establish those behaviors.

Apply the existing independent plan, deterministic check, frozen Full, triage,
confirmed repair and scoped Delta process. Preserve project-owned commands and
records on updates. Record missing runtime or administrative evidence explicitly;
an AI review does not supply a human signature or configure repository protections.

The source implementation guide is `docs/operations/engineering/workflows/README.md`;
legacy consumers receive `.engineering-backbone/workflow-guide.md` only when that
optional package is selected. Follow its separate reviewed seed/activation contract
and the receiving project's stronger controls. Copying this guidance or an example
neither starts CI nor approves publication, deployment or automatic downstream apply.

Source note: Backbone change/review rules informed by T-S02, T-S03 and T-S09 in the
[source register](testing-sources.md#reference-register). Record the project mapping
with [the reusable template](../templates/testing/ci-mapping.md).
