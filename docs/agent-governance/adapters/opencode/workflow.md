# OpenCode operating contract

The canonical Backbone policy and stronger project rules govern every session.
This adapter maps the existing five Task Packet roles to native OpenCode primary
agents. It supplies the same procedures as the Copilot adapter; it adds no task
roles, authorizations, merge decisions or automatic orchestration.

| Task Packet role | Native primary | Applicable procedures after task-intake |
| --- | --- | --- |
| planner | backbone-planner | implementation-plan |
| implementer | backbone-implementer | bug-reproduction, test-and-quality, docs-traceability |
| reviewer | backbone-reviewer | implementation-plan, code-review, delta-review |
| quality_checker | backbone-quality-checker | test-and-quality |
| triage | backbone-triage | finding-triage |

Use a scoped Task Packet and actual base revision. Before non-trivial implementation,
a separate reviewer checks the frozen plan in **plan** mode using implementation-plan.
Plan review examines scope, risks, dependencies, acceptance and intended checks; it
must not require completed implementation results. After implementation and actual
deterministic checks, freeze base/head/patch for separate **Full** review. Triage
classifies findings before repairs. **Delta** reviews confirmed repairs and direct
regressions; expanded scope or trust boundaries require Full review. Preserve all
IDs, evidence, budgets and stop conditions. Never let an author certify their own
work or interpret a clean AI review as human approval.

## Installation and activation

The reference layout already contains the native files at their final paths. A
direct copy follows `docs/agent-governance/adoption.md`, preserves the inactive
companion and restrictive permissions, and supplies no runtime qualification.
The Copier selection and preservation details below describe legacy installation;
the subsequent activation and qualification gates remain binding in either layout.

`use_opencode` is optional, false by default and installation-only; missing legacy
answers mean false. Copier preserves root `AGENTS.md`, `opencode.json`,
`opencode.jsonc`, `.opencode/**` and `.engineering-backbone/opencode.json`. Integrate
managed fragments and stronger local files in a reviewed adoption/update PR.
Configuration conflicts are reported, not overwritten. Existing JSONC remains on
disk but cannot coexist with the controlled JSON configuration. Native config has
explicit local instructions, and native roles share the approved policy procedures.
Project facts retain their original exact Codex/Copilot shape; OpenCode uses its
separate versioned companion.

The companion starts with `enabled: false`. This disables Backbone OpenCode routing
and controlled-runner eligibility; **it does not prevent OpenCode directly discovering
installed configuration, roles or skills**. Do not invoke an unqualified native
session and infer safety from that flag. Complete and review the inactive seed,
activate navigation first, then change only the companion's enabled flag in a
separate reviewed activation. An installed package cannot disappear or an active
binding be disabled through an ordinary update.

## Context and handoffs

With active navigation and companion, resolve the Task Packet request using the
approved guard. Verify the complete receipt against the current snapshot, then read
every resolved document before work. The receipt hashes whole file bytes, including
anchored documents. It includes companion, root native config, explicit instructions,
operating guide, runner contract, selected native role and its relevant procedures.
A reviewer always receives implementation-plan as well as Full/Delta procedures.
A role change or narrowed delegated scope requires a new request and verified receipt.
Missing/changed required documents stop admission. A receipt is structural evidence;
it does not prove the native model read or followed its contents.

## Permissions and native boundaries

The supported native format is pinned to OpenCode **1.19.0**. Each role is primary;
preflight must confirm the exact name exists before inference because a missing or
subagent-only selection can fall back. Ordered permission maps begin with `* : deny`.
Read, glob, grep and skill may allow. Implementer edit/bash and quality-checker bash
require ask; planner, reviewer and triage deny shell and edit. Consumers can retain
stricter restrictions. These are tool defaults, **not an operating-system sandbox**;
a shell-capable check session can write and remains bound to its approved commands.

Repository validation rejects unreviewed native layers, aliases, plugins, tools,
commands and legacy mode/modes overrides, duplicate identities, symlinks and ambiguous
case. Only eight exact native SKILL.md paths are supported recursively. Ordinary
skill resources remain possible; alternate reserved skills cannot replace procedures.
Host/global/ancestor configuration, environment overrides and native session changes
still need a controlled runner and actual client verification. Never use permissive
flags, an unverified plugin hook or a role's own assertions as proof of enforcement.

## Evidence and runner qualification

Use `opencode-runner-contract.md` alongside this guide (source:
`docs/agent-governance/adapters/opencode/opencode-runner-contract.md`). The initial AO governed integration is
fresh ACP/chat, implementer, default permissions only. TUI and unsupported read-only
OpenCode isolation remain blocked. No qualification is supplied by installation.
Native CLI smoke, actual Windows execution, real-model behavior and OS isolation are
separate evidence classes. The source `docs/agent-governance/adapters/opencode/smoke-tests.md` records commands
and current limits; `docs/agent-governance/adapters/opencode/source-provenance.md` records pinned sources.

Stop on stale or missing context, failed required checks, unsafe permissions,
unsupported role/runtime/interface, unresolved owner decisions or exhausted budget.
Return exact commands/exits, executed and unexecuted checks, coverage, findings,
acceptance states and recovery. Human merge/release approval and local publication
controls remain mandatory. No automatic downstream activation is authorized.
