# Codex managed-role identity security

The human authorized a narrow repair on 2026-10-12: protect Codex role-name
collisions and add only the remaining directly related security checks. Retain
the three profiles and current governance. No new roles or skill packages.

Base: `8d4728d92a0125452b223f2fa99226fc8fc8cd0d` (merged Copilot delivery).
See [the Task Packet](codex-security-task.json).

## Observed paths and implementation

The current validator checks three canonical filenames, while Codex identifies
standalone profiles by their trimmed, case-sensitive `name`. Release
`rust-v0.162.1`, commit `092d3acd6bec3e3a14bdc7e7a2810ab628ab759d`, sorts recursive
TOML discovery and keeps the first duplicate within a layer. Explicit `[agents.*]`
declarations precede implicit discovery; referenced files can supply a different
effective name, with an absent/blank name falling back to the declaration key.
Nested project `.codex` folders form later layers and can replace root roles.

1. Add one self-contained `codex_errors` function to the trusted validator. Keep
   the existing canonical name, field and sandbox-declaration checks inside this
   function so local checks and the compiled workflow have one contract.
2. Inspect repository-contained `.codex` folders, recursive `agents/**/*.toml`
   profiles, and `config.toml` role declarations. Reserve exactly the three
   `backbone_*` names for the root canonical files. Use native case sensitivity
   and name trimming; parse data, never import or execute it.
3. Preserve unrelated local role/config bytes. Permit an explicit managed
   declaration only when it references its corresponding canonical root file.
   Reject competing effective names, unreadable/malformed identity data,
   symlinked native paths/ancestors and uninspectable role-file references.
   Inspect references inside the snapshot, including files outside `agents/`.
   Host-global and live session settings are outside this repository contract.
   Source-mode root `artifacts/` retains its existing raw-evidence exclusion;
   consumer mode checks that directory too. Historical artifact checkouts are not
   a supported source-project execution directory.
   Structural discovery covers regular owned repository paths and inspected
   references. Generic application directory links remain local; execution beneath
   such an uninspected alias requires separate working-directory reconciliation.
4. Compile the function into the existing pinned consumer workflow, independently
   of the consumer's validator. Retain reviewed old tooling identities, add the
   merged current identity to history, and refresh the new current fingerprint.
5. Add focused source/consumer negative tests and actual workflow payload tests
   with historical tooling. Verify root/nested collisions, declaration fallback,
   path ambiguity, disabled-provider bypass, unrelated-role preservation and
   canonical references. Existing Copier/update compatibility stays required.
6. Update adapter documentation only for these ownership and permission limits.
   A role's `sandbox_mode` is a declared setting, not observed confinement: the
   inspected release preserves parent permissions when applying role overrides.
   Record the live client check as unexecuted if no intended client is available.
   Verify a governed working directory without unreviewed directory-link ancestors:
   the inspected client can preserve logical cwd paths and load external layers
   through those aliases. Do not certify arbitrary linked application trees.

## Acceptance and validation

- AC-1: Root/nested native files cannot occupy a reserved role through an alias.
- AC-2: Config declarations and referenced effective names cannot substitute it.
- AC-3: Native identity inspection fails closed on path/parse ambiguity.
- AC-4: Canonical profiles, stronger implementer defaults, unrelated valid roles
  and project runtime settings remain compatible and unchanged by validation.
- AC-5: The pinned workflow applies the same guard with approved old tooling;
  candidate imports and provider-flag changes cannot suppress it.
- AC-6: The compiler checks both guard blocks and the actual rendered digest;
  generated consumers and existing create/update tests pass.
- AC-7: Documentation distinguishes structural identity/default checks from
  actual client discovery and parent permissions.
- AC-8: Deterministic checks, independent Full/triage/repair/Delta and PR evidence.

Run `python scripts/validate.py`,
`python scripts/compile_toolchain_fingerprint.py --check`, the affected tests and
`python -m unittest discover -s tests -v`, trusted-base validation, `actionlint`,
and `git diff --check`. Capture actual command results under ignored `artifacts/`
and durable redacted summaries under `docs/reviews/`. A live Codex role spawn is
separate evidence, not simulated by parser tests.

## Review and recovery

Obtain an independent read-only plan review before implementation. Freeze
base/head/patch SHA-256 for independent behavior and security Full reviews. Triage
before repairs, then Delta the confirmed IDs and direct repair regressions. Use
at most two Full rounds and eight repair iterations; failed required checks,
unresolved confirmed findings or exceeded scope stop publication. Publish one PR;
human merge/release and downstream adoption remain separate.

Recovery is a reviewed revert/repair PR with the matching workflow fingerprint.
Do not silently permit name collisions, overwrite native files, remove historical
evidence or weaken the existing Copilot guard.

## Primary source evidence

- [Codex role discovery](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/agent-roles/src/discovery.rs)
- [Codex role loader and precedence](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/agent-roles/src/loader.rs)
- [Codex native name parsing](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/agent-roles/src/agent_role_config.rs)
- [Codex project-layer discovery](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/config/src/loader/mod.rs)
- [Codex role authority](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/core/src/agent/role.rs)
- [Codex parent-permission regression tests](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/core/src/agent/role_tests.rs)
- [Codex explicit cwd loading](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/core/src/config/mod.rs)
- [Codex logical absolute paths](https://github.com/openai/codex/blob/092d3acd6bec3e3a14bdc7e7a2810ab628ab759d/codex-rs/utils/absolute-path/src/lib.rs)
