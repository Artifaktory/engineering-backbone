# Consumer adoption and updates

## Before copying

Use a clean isolated branch and an explicitly scoped Task Packet. Inventory the
project's existing AGENTS/Copilot/Codex instructions, branch strategy and required
checks. Choose only the needed providers. Preserve stricter local policy.

The bootstrap branch is not a released foundation. After human review and verified
repository controls, a human can approve a release and record its immutable commit.
The placeholders below must be replaced with that actual approved 40-character SHA.
Do not use floating main or invent a release tag.

```sh
copier copy --vcs-ref APPROVED_COMMIT gh:Artifaktory/engineering-backbone .
```

Normal authenticated Git/Copier access to this private repository is required for
the copy/update operation. Never put a token in the URL, answers file or command.
Questions record project name, base branch, validation command, language and
frontend/backend metadata, selected providers, optional Copilot Python/frontend
instruction profiles and an optional reviewed workflow SHA. The two technical
profile choices default false; they do not infer frameworks or path layouts from
language metadata. Copilot includes three core governance/test/docs path rules.
For a project with no trusted bundle yet, leave the workflow SHA empty and follow
the two-stage bootstrap below; an active caller in the first adoption PR fails closed.
Project metadata does not execute commands or create domain-specific app workflows.
Provider/profile selection and initial workflow generation are installation-only choices.
An ordinary update rejects changing them before writing the consumer; use a
separate reviewed migration to change provider selection or reconcile local facts.

## Generated ownership

The optional [shared workflow kit](workflows/README.md) uses separate project-owned
`workflows.json`, `use_workflow_kit` and a reviewed `workflow_kit_ref`. It does not
change the descriptive `project.json` version 1 contract. Seed complete inactive
configuration first, then activate pinned callers in a separate reviewed PR.
Kit configuration, native callers and inert delivery examples are preserved on
ordinary updates; manually reconcile them in the consumer's reviewed migration.

| Files | Owner and update behavior |
| --- | --- |
| `.engineering-backbone/core.md`, `core.json`, validator, schemas, requirements/lock and scoped `.gitattributes` | Backbone-owned, refreshed by Copier |
| `.engineering-backbone/AGENTS.fragment.md`, `Copilot.fragment.md` | Always-refreshed additions for explicit local integration |
| `.engineering-backbone/copilot-guide.md` | Always-refreshed neutral operating guide, including diagram; reference only if Copilot unselected |
| Root `AGENTS.md`, Copilot entrypoint and native agent profiles | Created when absent; existing files preserved, including the original three Copilot profiles |
| Copilot `.github/skills/**` and `.github/instructions/**` | Selected missing files created; existing native files preserved for reviewed manual refresh |
| `.engineering-backbone/project.json` | Existing local project facts preserved |
| `.github/workflows/engineering-backbone.yml` | Optional actual-SHA caller; existing file preserved |
| `.engineering-backbone/workflows.json`, kit callers and delivery examples | Optional project-owned kit contract; existing files preserved |
| `.engineering-backbone/quality-policy.md` | Always-refreshed canonical quality-policy extension |
| Quality guide, guard, schema and `.engineering-backbone/standards/**` | Optional backbone-owned bundle; refreshed together with its reviewed workflow pin |
| `.engineering-backbone/quality-profile.json` and `docs/quality/{quality-plan.md,test-strategy.md,traceability.csv,exceptions.md}` | Optional project-owned seed and records; existing files preserved |

On an existing project, review and integrate the fragments into the existing
entrypoints. Reconcile conflicting instructions by retaining the stricter policy.
Preservation prevents overwrites but does not guarantee automatic adoption of a new
rule: changed entrypoints/role permissions need a reviewed manual refresh.
Inspect the complete update diff for renamed/removed upstream files as well: the
Copier overwrite-skip mechanism is not a general protection against template-path
removal. Release review and consumer PR review must catch such migrations.

## Validate the copied bundle

```sh
python -m pip install --require-hashes -r .engineering-backbone/requirements.lock
python .engineering-backbone/validate.py --root .
```

Run the project's own tests separately. For Codex/Copilot, verify the native files
are discovered by the actual supported installed client; syntax validation is not
runtime evidence. See [adapter limits](agent-adapters.md),
[Copilot client differences](copilot/clients.md) and [runtime acceptance](copilot/smoke-tests.md).

## First adoption: establish trust before activating CI

1. Copy from the human-approved immutable backbone commit with
   `backbone_workflow_ref` empty. Keep the shared workflow inactive. Review the
   generated bundle, run the local checks above plus the project's tests, and
   perform independent review. A human decides whether to merge that seed PR.
2. After the reviewed bundle exists on the project's base branch, add the pinned
   caller from `.engineering-backbone/workflow-example.md` in a separate PR.
   The shared gate now uses the already-merged bundle to validate that activation
   PR. Human review also verifies the exact workflow pin and sharing settings.

Missing or partial trusted bundles fail before any Python/dependency execution.
There is no first-adoption fallback to the candidate validator, candidate lock or
an automatically downloaded baseline. Activating a caller during the first copy
therefore cannot manufacture a trusted baseline. A manual caller migration does
not require editing Copier's installation-only saved answers.

## Shared workflow access

The central reusable workflow checks out explicit candidate and trusted consumer
revisions. Before installing or running either bundle, immutable workflow literals
attest the validator, five schemas and both dependency manifests as one coherent
SHA256 fingerprint. The base must match the current or an explicitly retained
historical fingerprint. Candidate tooling must equal that base or the workflow's
current fingerprint; mixed files, unapproved edits and historical downgrades fail.
The gate installs only the attested base's locked dependencies and runs only its
validator and schemas, in isolated Python mode, against the candidate with
`--trusted-base`. Candidate code, dependencies and project commands are never
executed. This also prevents a no-op candidate validator becoming trusted next PR.

Project facts, core policy and local instructions remain independently validated
rather than hashed: project variation and stricter local invariants are preserved.
The workflow separately enforces exact boolean provider facts and prevents
turning off a provider enabled in the base, including with older approved
validators. `source_mode` is restricted to the backbone repository. Hashes express
provenance under the reviewed workflow pin; they do not replace human approval.
The updated immutable workflow also owns the Copilot extended-asset guard: a
candidate cannot supply its own profile registry or bypass new role/skill/rule
checks with an old trusted-base validator. Legacy three-role installations remain
supported; an extended package must be complete and retains installed extended
assets across subsequent ordinary changes.
The generated `.engineering-backbone/.gitattributes` keeps only the eight tooling
files at LF line endings, so Windows checkout conversion does not change their
attestation. Application files retain their existing Git attributes.

| Trigger | Trusted consumer tooling | Committed whitespace range |
| --- | --- | --- |
| Pull request | PR base SHA | PR base SHA to PR head SHA |
| Push | Previous push SHA (`before`) | Previous SHA to current SHA |
| First push with zero `before` | No baseline: consumer gate fails closed | Empty tree to current SHA |
| Manual dispatch | Repository default branch, independently of the selected candidate | Selected commit's parent to selected commit, or empty tree for a root commit |

Dispatch validates the operator-selected candidate using the complete bundle on
the repository's default branch. Selecting an unmerged feature commit does not
make its validator or dependencies trusted. The whitespace range still covers the
selected commit's latest patch. This compares policy against the default branch,
not against the candidate's preceding commit; PR/push checks use their event bases.
Unsupported events or invalid revision contexts fail rather than falling back to a clean-worktree diff.

The workflow needs no private backbone checkout token, provider API key,
deployment secret or write permission. GitHub still needs the private source
repository's Actions access policy to permit the consuming repository and its
caller settings to allow the shared workflow. Those settings are separately
verified by a human operator. Existing application workflows, privileged runners
and deployment permissions remain local. The caller and workflow pin also need
protected review: an editable caller can remove a job, which this job cannot
prevent by itself.

## Update through a project PR

Use a clean worktree on an update branch and preserve the answers file:

```sh
copier update --answers-file .engineering-backbone/copier-answers.yml --vcs-ref APPROVED_COMMIT
```

Resolve any merge conflicts, inspect the actual diff, integrate safe fragments and
refresh native role files only after review. Do not manually modify the Copier
answers file to fake a baseline; change questions through Copier's supported options.
Validate the bundle, run project tests and follow Full/Triage/Fix/Delta before human
merge. The old project revision remains effective until the update PR is merged.

Dependabot can propose shared Workflow/Action reference changes. A reference update
does not synchronize vendored policy/schema/validator files: include the matching
Copier update and native-fragment integration in the reviewed delivery when needed.
When any of the eight tooling files changes, include the newly reviewed immutable
workflow pin in the same consumer upgrade PR. Its current fingerprint must match
the actual Copier output, and its retained previous list must contain the existing
base tooling. An unchanged approved bundle remains supported. Custom edits to
these managed tools need a centrally reviewed toolchain update; a consumer cannot
supply its own hash or allowlist. Caller changes remain manual and do not require
changing installation-only Copier answers.

Source maintainers regenerate the current workflow literal with
`python scripts/compile_toolchain_fingerprint.py --write`, review that diff and run
`python scripts/compile_toolchain_fingerprint.py --check`. Source CI verifies the
literal against actual rendered working-tree output. Previous fingerprints are
explicitly reviewed compatibility entries, never automatically extended.
No universal updater bot or automatic downstream application is installed.

## Copilot extended-package migration

The new package adds seven profiles and eight skills while retaining the original
planner, implementer and reviewer. Before upgrading a three-role consumer, inventory
its protected native files and source/path overrides. Use a clean reviewed update
PR, inspect every newly created role/skill/rule and reconcile the refreshed
Copilot fragment and guide into local native instructions. Existing files are
preserved; a common instruction change is not automatically active in them.

Include the matching reviewed reusable-workflow commit in the same tooling upgrade
PR; its previous-tooling list must accept the installed base, and its workflow-owned
Copilot guard must validate new assets even when the installed validator has only
the old three-role checks. Do not upgrade the bundle against an older unamended
workflow and call it enforced. The guard validates structure and maximum native
permissions; it cannot prove a client's instruction semantics or tool binding.

Legacy answers without `copilot_python_profile` or `copilot_frontend_profile` are
treated as false. Ordinary updates cannot change these choices. To add a technical
rule later, use a separately reviewed manual native-rule migration (which need not
alter saved Copier choices), or an explicit reviewed template-configuration
migration. Do not delete/edit the answers file to bypass installation-only guards.
GitHub bot activation, runtime client setup, hooks and downstream writes remain
separate authorized work.

### Managed Copilot name reconciliation

Managed `backbone-*` roles use canonical lowercase `.agent.md` filenames. Copilot
also supports `.md` profiles, so the workflow guard rejects alternate spellings or
case variants of those reserved role identities, including reserved frontmatter
`name` values under project-owned filenames, rather than trusting ambiguous
configuration. Both filename and header names participate in supported clients'
role discovery. Native declarations must be safely inspectable; ambiguous YAML or
linked files require explicit reconciliation. Existing local alternates remain
preserved on disk; reconcile them manually into the canonical file in the reviewed
adoption PR, keeping stronger
instructions/permissions. Never delete a local policy merely to obtain a green gate.
Unrelated project-native agents retain their own tools, metadata and body rules;
the namespace scan checks identity without imposing managed-role tool budgets.
Client filename fallbacks for an empty header also cannot resolve to a reserved
managed identity under a noncanonical filename.

## Versioned quality-profile adoption

`use_quality_framework` is an independent installation-only choice, default false.
Legacy answers with no choice remain unselected on ordinary updates; changing the
choice requires a reviewed migration. Selecting it creates an incomplete inactive
seed, never an automatically approved quality plan. The neutral quality policy
ships even without the optional bundle so the canonical-policy link remains valid.

Follow [the quality guide](quality/README.md) and [testing guide](quality/testing.md):

1. Inventory project risks, selected source editions, stronger local rules and actual
   workflow checks. Select enabled profiles and their exact versions from the
   managed catalog. Disabled C++17/IEC references cannot be activated by changing
   consumer catalog data.
2. Complete the four project-owned records and the rule/check bindings while
   `enabled` stays false. Adopt the shared workflow kit with its complete inactive
   seed and separate activation; an active quality profile needs that active kit.
   Use a reviewed immutable `backbone_ref`, independently review semantic content
   and run the copied guard with
   `python .engineering-backbone/quality-guard.py validate --root .`.
3. Merge the reviewed complete quality seed first. In a separate PR change only
   quality-profile `enabled` to true; the workflow compares it with that complete
   trusted seed. Keep the matching current governance-workflow pin in use.
4. Later changes preserve selected profiles and installed bindings. Expired
   exceptions must be removed; new exceptions cannot be introduced after activation.
   Wider adoption or a policy change requires a reviewed upstream migration, not
   silent consumer catalog edits.

The current pinned reusable workflow carries a compiled quality guard before
running the base-owned validator. It protects the new contract even when the base
validator predates it, without importing the candidate quality script or trusting
consumer catalog changes. Catalog equality compares parsed data; harmless JSON
formatting changes do not create a new rule authority. The existing eight-file
tooling fingerprint format is unchanged. Only explicitly reviewed historical
tooling identities remain allowed.

Ordinary updates refresh managed files, fragments and the neutral policy but
preserve project records and native profiles. Manually integrate new quality
context into protected native roles/skills and verify exact catalog/profile/rule
versions at each handoff in the intended Codex/Copilot client. A parsed declaration,
`verified` CSV status or approval metadata is not authenticated semantic evidence.
No live agent discovery, downstream activation or external certification is
established by these structural checks.
