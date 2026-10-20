# Bootstrap delivery plan

Status: implementation authorized by the repository owner's request on 2026-10-12.
Base: `396737eea7cc2d69b654917dfb62e39541c7ac3a` (`main`).
Branch: `agent/bootstrap-foundation`. Risk: HIGH (shared control plane).

## Acceptance criteria

1. Shared portable policy, scoped planning/check/review formats and source provenance
   are documented without copying domain rules, branches or runner labels.
2. Native Codex and Copilot instructions plus planner/implementer/reviewer profiles
   are valid, consistent and restrict independent reviewers by default.
3. Real Copier installation and upgrade tests cover different project metadata,
   optional providers and preservation of existing local instructions.
4. Own CI validates schemas, adapters, examples, negative cases, generated consumers
   and the previous policy floor. Dependencies/actions are pinned; no release or
   downstream write permissions are needed by the checks.
5. Installation, updating, operational controls and what is not yet enforced are
   explicit. Human review/merge/release is required; no downstream rollout now.
6. Deterministic checks pass, independent frozen Full review is triaged, confirmed
   fixes receive Delta review, and one PR is published to this repository.

## Scope and exclusions

Repository baseline, policy, templates, schemas, native profiles, small validators,
tests, examples, own workflows and documentation only. Existing Tars/Artifaktory
repositories are read-only sources. Exclude product code, deployment, secrets,
automatic merges/releases, arbitrary agent orchestration and broad language profiles.

## Validation and review

Run structural validation, the complete unittest suite (including actual Copier
generation/update), whitespace checks and independent correctness/security and
test/compatibility reviews against an immutable snapshot. Findings are triaged
before edits. Runtime Codex/Copilot discovery, required-check enforcement, product
review integration and repository settings must be reported separately from tests.

## Publication authority and stop conditions

The owner explicitly requested a PR with this foundation and its own workflows.
That request is publication authority, not merge/release/deployment authority.
Stop on unresolved P0/P1, missing review evidence, failed required checks, unsafe
consumer overwrite, authorization conflict or expansion into excluded scope.

The initial base contains only README: there is no pre-existing trusted validator
or active base-branch workflow. Bootstrap cannot claim an existing enforced gate.
The PR adds testable gates; a human must configure/verify protected repository
settings before promoting a downstream-consumable release.
