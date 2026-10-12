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
frontend/backend metadata, selected providers and optional reviewed workflow SHA.
For a project with no trusted bundle yet, leave the workflow SHA empty and follow
the two-stage bootstrap below; an active caller in the first adoption PR fails closed.
Project metadata does not execute commands or create domain-specific app workflows.
Provider selection and initial workflow activation are installation-only choices.
An ordinary update rejects changing them before writing the consumer; use a
separate reviewed migration to change provider selection or reconcile local facts.

## Generated ownership

| Files | Owner and update behavior |
| --- | --- |
| `.engineering-backbone/core.md`, `core.json`, validator, schemas, requirements/lock and scoped `.gitattributes` | Backbone-owned, refreshed by Copier |
| `.engineering-backbone/AGENTS.fragment.md`, `Copilot.fragment.md` | Always-refreshed additions for explicit local integration |
| Root `AGENTS.md`, Copilot entrypoint and native agent profiles | Created when absent; existing files preserved |
| `.engineering-backbone/project.json` | Existing local project facts preserved |
| `.github/workflows/engineering-backbone.yml` | Optional actual-SHA caller; existing file preserved |

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
runtime evidence. See [adapter limits](agent-adapters.md).

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
