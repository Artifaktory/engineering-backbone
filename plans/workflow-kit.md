# Shared workflow kit

## Authority, base and scope

The human approved implementation on 2026-10-12 after comparing current Microsoft,
Artifaktory and Tars workflows and NIST SSDF/OpenSSF OSPS/SLSA guidance. Deliver the
versioned kit in this repository, add meaningful checks/tests, then independent
Full, triage, repairs and Delta reviews and a PR. Merge, release, deployment,
repository protection changes and downstream adoption remain separate decisions.

Base: `1ecbb7a572b3679b422105c557cb88a8bff75dac`, merged PR 7, tree
`5cc9e9079b0958a5a15ef24c48e827c6e890c73d`. Existing stricter local policy and the
eight-file historical tooling fingerprint contract remain intact. This is HIGH
risk control-plane work. No new native agent roles or skills.

## Design

1. Add an optional, separate `.engineering-backbone/workflows.json` contract,
   schema and documented profile catalog. Keep closed `project.json` version 1
   unchanged. Legacy consumers without a kit remain valid. Initial generated kit
   configuration is explicitly inactive and contains no invented application
   commands. First adoption seeds complete reviewed config before activation.
2. Profiles cover documentation, Python, TypeScript, Go and .NET; capabilities
   select dependency, browser/API, database, container, infrastructure, release
   and deployment checks. Required check kinds follow the trusted catalog,
   rather than arbitrary candidate reporting. Checks declare stable IDs, kind,
   argument arrays, relative working directory, bounded timeout and phases.
   Runtime versions are bounded numeric inputs. Missing required checks block.
3. Use a self-contained standard-library kit guard/runner compiled into pinned
   reusable workflows from trusted source. Never import candidate Python or run
   application commands inside the governance/configuration/secret-check jobs.
   Preserve the existing eight-file fingerprint format; the new guard has its
   own compiled authority and source consistency check.
4. Read candidate and trusted configuration as regular bounded files without
   symlink ancestors or duplicate JSON keys. Existing adopted configuration,
   selected profiles/capabilities and required check IDs cannot silently disappear.
   For PR/push, execute base-approved definitions for existing check IDs against
   candidate code. Candidate additions are additionally checked. Proposed command
   changes are review material and become authoritative only after merge. Initial
   activation requires a complete already reviewed seed configuration.
5. Common PR checks comprise existing governance, configuration, quality, secret
   scanning and applicable project security checks, plus an unconditional strict
   aggregate. Expected jobs are fixed and only exact success passes. Missing,
   skipped, failed or cancelled required jobs never become PASS. Project report
   files are evidence, never authority for the GitHub aggregate.
6. Run project argv using `shell=False`, bounded timeouts and safe cwd on clean
   hosted runners, with read-only repository token, no inherited secrets, no
   persisted checkout credentials and no self-hosted selection. Set up declared
   runtimes explicitly. Commands are project-owned executable code, not proven
   safe by schema validation. CI/permission changes need semantic review.
7. Add separate scheduled maintenance using the approved default-branch config;
   do not send schedule events through the old governance workflow which does
   not support them. Dependency checks apply in PR and maintenance. Results stay
   visible; no automatic merge or repairs and no invented alert delivery.
8. Ship inactive, fail-closed release/deployment workflow examples and their
   activation contracts. They select prerequisite/integrity/SBOM/signature/smoke
   checks appropriate to configured capabilities. Concrete publishing credentials,
   environment approvals, cloud commands, rollback and monitoring remain local
   project integration; this kit does not publish or deploy a consumer.
9. Extend Copier with explicit installation choices and protected kit config and
   caller paths. Existing workflows, local facts and stronger rules remain byte
   preserved. Blank pins keep activation manual; active callers require full
   reviewed commit pins. Consumer updates happen through their own PRs.
10. Document the workflow diagram, what/how/when matrix, profile applicability,
    activation, exact required status configuration and negative red/green pilot.
    Structural tests cannot authenticate reviews, enforce host rules or establish
    runtime agent discovery. The full review chain remains required separately.

## Acceptance and verification

- AC-1: Explicit profile/capability/config contracts reject malformed, incomplete,
  unsafe and weakening proposals while legacy consumers remain valid.
- AC-2: Actual runner executes real successful/failing checks, never uses a shell,
  rejects unsafe cwd and handles timeout/no-command/tool failure truthfully.
- AC-3: Actual compiled workflow payloads enforce config and fixed aggregate,
  including historical approved consumers and candidate bypass attempts.
- AC-4: Secret prevention and conditional security/maintenance checks are real,
  with declared scanner coverage limits and no false clean scan on tool failure.
- AC-5: Copier produces usable, inactive/active reviewed callers and preserves
  existing workflows/config through creation and upgrades; all profiles render.
- AC-6: Release/deploy templates, diagrams, source provenance and activation
  instructions accurately describe capabilities and unexecuted operational gates.
- AC-7: Source and trusted-base validation, compilation consistency, all tests,
  actionlint and committed diff hygiene pass on the final reviewed snapshot.
- AC-8: Independent plan and behavior/security Full reviews, triage, required
  repair Deltas and published PR checks/review evidence are recorded honestly.

Run focused new suites, affected existing suites, then complete source suite.
Use the previous approved validator against the candidate. Test the rendered
consumers and actual workflow shell/Python payloads, not only YAML string shapes.
Negative scenarios include failing test/scanner, missing/empty command, timeout,
unsafe path/symlink, duplicate keys, invalid runtime/profile, config deletion,
required-check deletion, permission escalation, forged result reports and
advisory/skip-to-green attempts. Preserve historical fixtures unchanged.

## Review and recovery

Independent read-only plan review precedes implementation. Two independent Full
reviewers (behavior/compatibility and security) see the same frozen base/head/diff
digest. Triage each causal finding before edits. Review confirmed repairs and
direct regressions in Delta; broadened trust/scope requires a new Full. Default
limit: two Full rounds for unchanged scope, up to eight bounded repair iterations.
Required failure, unresolved confirmed finding or owner decision blocks closeout.
Remote provider review is advisory and follows the same triage contract.

Recovery is a reviewed revert of this delivery or reverting an adopted caller's
pin/config through the consumer's existing controls. No automatic downstream apply.
