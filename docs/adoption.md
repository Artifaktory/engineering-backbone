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
Project metadata does not execute commands or create domain-specific app workflows.

## Generated ownership

| Files | Owner and update behavior |
| --- | --- |
| `.engineering-backbone/core.md`, `core.json`, validator, schemas, requirements/lock | Backbone-owned, refreshed by Copier |
| `.engineering-backbone/AGENTS.fragment.md`, `Copilot.fragment.md` | Always-refreshed additions for explicit local integration |
| Root `AGENTS.md`, Copilot entrypoint and native agent profiles | Created when absent; existing files preserved |
| `.engineering-backbone/project.json` | Existing local project facts preserved |
| `.github/workflows/engineering-backbone.yml` | Optional actual-SHA caller; existing file preserved |

On an existing project, review and integrate the fragments into the existing
entrypoints. Reconcile conflicting instructions by retaining the stricter policy.
Preservation prevents overwrites but does not guarantee automatic adoption of a new
rule: changed entrypoints/role permissions need a reviewed manual refresh.

## Validate the copied bundle

```sh
python -m pip install --require-hashes -r .engineering-backbone/requirements.lock
python .engineering-backbone/validate.py --root .
```

Run the project's own tests separately. For Codex/Copilot, verify the native files
are discovered by the actual supported installed client; syntax validation is not
runtime evidence. See [adapter limits](agent-adapters.md).

## Shared workflow access

Default output is a manual workflow example. Supplying an approved 40-character
workflow SHA enables the actual caller. The central reusable workflow checks out
the caller and runs the local generated validation bundle. It needs no private
backbone checkout token, provider API key, deployment secret or write permission.

GitHub still needs the private source repository's Actions access policy to permit
the consuming repository and its caller settings to allow the shared workflow.
Those settings are separately verified by a human operator. Existing project
application workflows, privileged runners and deployment permissions remain local.

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
No universal updater bot or automatic downstream application is installed.
