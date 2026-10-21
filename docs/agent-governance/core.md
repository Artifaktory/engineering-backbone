# Engineering Backbone: shared governance

This policy is language- and domain-independent. Project-specific rules, branches,
commands, deployment permissions and risk controls belong to the consuming project.
Existing stricter project rules remain binding. A profile or agent adapter may add
restrictions; it must not weaken this baseline or replace local policy silently.

The [quality policy](../quality/policy.md) extends this authority with versioned rule
selection, responsibilities, evidence and project quality profiles. Apply the
selected profile when adopted; legacy absence is not a quality-conformance claim.
Source catalogs and project profiles express different ownership. Keep one
reviewed rule authority and preserve stronger project requirements.

## Scope and authorization

Before a non-trivial edit, check the current branch, base revision, clean/dirty
worktree and applicable instructions. Use a scoped Task Packet recording the
objective, authorized actions, base revision, included/excluded paths, role, risk,
acceptance-to-verification mapping, budgets and stop conditions. Analysis and packet
preparation may precede that packet. No unrelated cleanup or invented requirements.

Human instructions authorize the requested work. Publishing a requested PR is not
permission to merge, release, deploy, delete data or expand access. Stop when the
scope or authorization is missing, contradictory or exceeded. Never overwrite
unrelated work, force-push, perform destructive Git cleanup or commit secrets.

## Roles and planning

The planner produces a testable plan. The implementer makes the approved scoped
changes. The quality checker records actual deterministic check results. Independent
reviewers inspect a frozen snapshot read-only. Triage classifies findings before
repair. The implementer must not certify its own changes as independently reviewed.
Do not silently switch incompatible roles within a review session.

Use a direct plan for a small PR. A feature or program plan is optional when
dependencies, multiple deliveries or risks justify it. Requirement approval,
implementation and verification are separate states. Automated, manual and hybrid
verification are valid when explicitly selected and evidenced.

For requirements, architecture and material design changes, agents and human
reviewers must read and apply the [architecture contract](architecture.md).
Carry its source requirements, decisions, views, verification plan and open gaps
in the scoped handoff. Its semantic obligations apply independently of optional
quality/navigation activation; existing navigation and stricter project gates
still apply. A template, diagram or successful document build is not design
approval or evidence of implemented behavior.

For scoped planning, decomposition and delivery handoffs, agents and human
reviewers must apply the [planning contract](planning.md). Preserve source
requirements/design authority, versioned outcomes, typed prerequisites, integration
ownership, required verification and explicit return conditions. Start readiness,
review readiness, item acceptance and release approval retain distinct meanings.
Planning records may be combined proportionally; they do not install a tracker or
orchestrator, extend Task Packet schemas or override stricter local controls.

## Checks and evidence

Run the project's relevant deterministic checks before formal review. A bug fix
needs a meaningful regression check. Contract or workflow changes need producer /
consumer and failure-path checks proportional to risk. Preserve assertions,
coverage, timeouts and gates; do not skip checks to obtain a green result.

Record exact commands, exit codes, inspected revisions, executed and unexecuted
checks, findings, limitations and acceptance coverage. A plan, test name, generated
file, schema-valid report or model output is not a PASS or proof of runtime behavior.
Redact sensitive information. Missing tools or absent evidence remain visible.

## Full, triage, repair and delta review

Freeze the same base, head and patch digest for all reviewers in one Full round.
Do not edit that snapshot between reviewers. Findings need stable IDs, severity,
location, trigger, impact, evidence and a relation to the current diff. Exclude
style preferences, new requirements and unrelated pre-existing debt.

Triage findings as confirmed, rejected or requiring a human decision. Repair only
confirmed findings. Freeze the changed repair snapshot. Delta review checks those
finding IDs and regressions directly introduced by the repairs. Scope, contract or
trust-boundary expansion requires a new Full round. An unchanged repair snapshot,
unresolved human decision or exhausted budget stops the chain.

## Control plane and downstream safety

Changes to governance, schemas, validators, templates, agent permissions and CI are
HIGH risk by default. Review them against the trusted base policy as well as the
proposed head. Test generated consumers and upgrade behavior before distribution.
Consumers pin a reviewed release/commit and adopt changes through their own PRs.
Never automatically apply or merge downstream changes.

A human must approve merge and release. An AI review is advice, even when a provider
can technically submit an approval. Do not auto-merge governance. Release, signing,
branch protection and required-check settings are separate repository controls.
Instructions and schema checks do not enforce those controls by themselves.

## Adapter boundaries

Codex, Copilot and OpenCode profiles express the same roles and baseline. Read-only profiles
are restrictive defaults, not protection against elevated runtime overrides.
Native role files do not install or activate GitHub review bots. CI verifies formats
and generated artifacts; product-specific runtime discovery must be checked
separately. Preserve stricter local instructions during installation and upgrades.

## Instruction discovery and project authority

Read the root instructions and the instructions applicable to each changed path.
More specific project rules may add restrictions, never remove the inherited
safety, quality, Git or evidence requirements. Canonical project governance is the
source of authority; Codex/Copilot/OpenCode adapters, skills and prompts must not create a
contradictory second policy. An unexpected repository override is a finding to
resolve before acting; personal host settings do not prove project compliance.
Client-specific discovery and precedence must be verified in the intended client.

Project facts select the actual target branch, validation commands and available
skills. Never copy a reference project's example branch, runner, tool permission
or domain action into a new project without checking its local contract.

## Proportional planning and specialized responsibilities

Before non-trivial implementation of a design or implementation plan, obtain an
independent read-only plan review of scope, dependencies, risks, acceptance and
verification. A trivial, narrow change can use the direct Task Packet checklist;
automation, permissions, contracts, security or governance changes are not trivial.
An approved plan authorizes only its recorded scope; it is not implementation or
test evidence. Scope changes require an explicit updated plan and review.

Use the available native profiles as hosts for bounded responsibilities. Codex
retains planner, implementer and reviewer; the Copilot package adds named
specializations that map onto the existing Task Packet roles. Record the active responsibility in the Task Packet's
objective and scope; do not invent additional schema roles. A plan reviewer,
security reviewer or test/traceability reviewer is an independent reviewer with a
specific catalog. A test/documentation worker is an implementer with a narrowed
path scope. A quality checker executes checks and records evidence without
opportunistic repairs; a triage session decides findings without editing source or
tests. Keep incompatible sessions separate. Identify the assigned orchestration owner and actual host capabilities before
delegating; honor local limits on nested agents rather than imposing an orchestrator.
Start with targeted checks, then affected suites and the broader checks required by
the project. Task configuration selects required
and optional reviewers; missing required evidence blocks the declared gate, while
optional advice never substitutes for it.

## Finding quality, coverage and bounded review

Each finding states a stable ID, severity P0-P3, category and confidence, exact
location, concrete trigger and execution path, impact, reproduction or evidence,
acceptance/contract relation, current-diff causation and a minimal regression check.
Use the existing review-evidence schema for its supported fields; preserve details
such as confidence and reproduction in the claim/evidence or companion report.
Do not add unknown JSON keys. No style preferences, equivalent alternatives,
new requirements or pre-existing debt without diff causation are defects.

Report inspected areas and unreviewed areas. If no in-scope defect is confirmed,
report `NO CONFIRMED IN-SCOPE FINDINGS`; this conclusion is limited to the recorded
snapshot, scope and coverage. It is neither human approval nor proof that every
file, client or execution path was exercised.

Record a patch digest alongside the base/head revisions in a companion review
report. Reviewers in one round see the same snapshot. After triage and repairs,
Delta uses the prior reviewed head, repaired head, confirmed IDs and direct repair
regressions. Preserve prior evidence; never silently reopen unchanged areas in a
Delta. Wider requirements or changed trust boundaries need a separately scoped
Full. Use at most two Full rounds for unchanged task scope by default; another
needs a confirmed unresolved blocker, relevant new changes or a documented human
exception. Task budgets and stricter project limits remain binding. A changed objective, risk
classification or acceptance contract also requires a new scoped Full. An unchanged
failure with no changed input is investigated, not repeatedly rerun for a green
result; retries need a stated reason such as transient infrastructure failure.

## Remote reviews and publication evidence

GitHub Codex/Copilot reviews are advisory unless a separately reviewed project
contract explicitly establishes a stronger formal gate. Supply the Task Packet,
actual base/head revisions, patch digest, Full/Delta mode, prior reviewed head for
Delta and confirmed finding IDs. Without accessible context or a fixed snapshot,
the result is explicitly advisory and lists missing/unreviewed context. Remote
findings go through the same triage; no provider automatic fix bypasses it.

Automatic PR review settings are a project choice. They do not override local
review stops, iteration limits or publication gates. Projects that prohibit review
after every push need an explicit policy migration before enabling it. A reviewer
profile is not the provider's automatic code-review bot. Review changes to
instructions against trusted-base policy, even when a provider reads head rules.

Before publication, map every acceptance criterion to actual automatic/manual
results or an explicit pending, blocked or failed state. Record documentation and
requirement impact, residual risks and safe recovery. Keep local raw transcripts
redacted and outside tracked files; durable reports carry revisions and coverage.
Existing project Publish-Go signatures, finding seals and history anchors remain
required where installed. This backbone does not implement or authenticate those
mechanisms; a structural PASS or AI review never replaces them.
