# Independent Full security and governance review

Reviewer: `layout_security_review`, with read-only auxiliary inspection by
`layout_security_review/ci_security_check`. Full round 1, scoped to the
[BB-LAYOUT-011 packet](task-packet.json) and [reviewed plan](plan.md).
Neither reviewer implemented these changes. This report is advisory independent
review, not authenticated human approval or permission to merge or release.

## Frozen subject

- Base: `212608aa50ee517b3dd3107a9480da997222fd4f`.
- Head: `54501f1ed542e7f42b5aa315db8863b35e80aeed`.
- Head tree: `09f9a2dacc7943e0e7ce18a97422f801a6f686e2`.
- `git diff --binary BASE HEAD` SHA256:
  `3d55fa71f514b9e39f798920188f5186db72b03ef6ea83de576e87f4e8c090bd`.

The detached review worktree's identities and clean status were checked before
and after inspection. Reproductions used disposable copies; the frozen tree was
not edited. The [quality record](checks.md) reports 431 passing tests on
`ee4f7cee7a386edfb5fb43b2763a03596b8eabf1`; the reviewed head adds only that
record. This reviewer did not repeat or claim to have executed the full suite.

## Coverage and observations

Inspected the current and trusted-base operating policy, changed validator code,
navigation and quality guard paths, workflow-kit equality, compiler fingerprint
inputs, new copy regression cases, adoption boundaries, and CI/native/tooling
configuration changes. The auxiliary reviewer independently inspected workflow,
native-role, dependency, container and IDE changes on the same head.

- Validator source/legacy identity comes from its executing location. Candidate
  project metadata cannot select consumer mode; the CLI exposes no mode override.
  Schema authority remains in the executing bundle, and policy-floor and previous
  enabled-adapter protections remain present.
- The new historical exception is bounded to 88 exact paths and reviewed SHA256
  values embedded in the executable. Current document paths are not exempted by
  candidate mapping metadata. The reviewer independently compared all 495
  embedded relocation pairs to the reviewed inventory and all 88 historical
  hashes and destination bytes to actual base Git blobs: all matched.
- Historical Markdown links use the original context and embedded mapping, then
  require an existing target within the candidate root. New named task/review
  JSON paths retain schema checks and reviewer/implementer identity separation.
  There is no new blanket exemption for `docs/changes/`.
- The trusted-policy workflow selects either validator path only from its trusted
  base checkout, uses that checkout's lockfile, and now fails closed when neither
  trusted validator exists. The old-layout rejection is not caught, projected or
  retried with candidate code. Source-only repository restrictions remain.
- The consumer workflow adds exactly the former current digest to the approved
  previous list. Compiler fingerprinting still covers actual rendered consumer
  bytes; its source changes only retarget the root and validator paths.
- Codex permission fields are unchanged; Copilot and OpenCode role front matter
  is byte-identical. OpenCode native changes only retarget instruction paths and
  its companion stays disabled. Source-only and installed instruction lists remain
  separate. No provider, model, permission, deployment or downstream activation
  is introduced.
- Direct and locked dependency inputs remain byte-identical. Docker retains its
  immutable base, nonroot user, binary/hash-locked installation and excluded local
  artifacts. CI retains read-only contents permission and disabled checkout
  credentials. New VS Code configuration only sets final-newline behavior.

## Executed focused probes

The reviewer ran a disposable-copy harness using the isolated Python 3.12
environment and the frozen validator with `-I -B --root COPY --trusted-base HEAD`.
The entire harness exited 0. Its SHA256 is
`082a546d38a4deec3189d6f752b80698caeeef7ad0f63f2fe8490dd39a0bfe0a`.

| Probe | Validator exit | Observation |
| --- | ---: | --- |
| Unchanged direct copy | 0 | Structural contracts accepted against the frozen reference. |
| Replace candidate task schema with `{}` and add malformed new task | 1 | New task still rejected using executing-bundle schema. |
| New review evidence names its implementer as independent reviewer | 1 | Self-certification rejected at the new evidence path. |
| Modify archived bytes, candidate map and candidate validator | 1 | Frozen executable rejects changed historical bytes. |
| Disable candidate adapter flags and add broken current Markdown link | 1 | Source document still checked; metadata does not hide it through consumer mode. |

These probes supplement the recorded checks; they do not establish all runtime
paths or authenticate any review record.

## Findings and cross-review overlap

**NO ADDITIONAL CONFIRMED IN-SCOPE SECURITY FINDINGS.**

The auxiliary inspection independently reproduced the behavior review's
**LBEH-01** at `.github/workflows/opencode-native.yml:36`: the removed
`tests.test_opencode_native_smoke` module produces `ModuleNotFoundError`, stopping
the jobs before native smoke. That is the same finding, not a second issue. Its
triage and any repair/Delta belong to the shared review chain. This report does
not certify the failing native workflow as passing.

The parent also reported behavior findings LBEH-02 concerning the legacy adoption
document path and LBEH-03 concerning the relocated native smoke tool's default
repository root. This security report does not independently classify those
findings or supersede their behavior review and triage.

## Limits and remaining gate

The actual previous trusted validator's exit 1 with 34 layout/context errors is
an explicitly preserved merge blocker, not a security waiver or a passing trust
migration. The first PR may be published as an inspectable draft only within its
existing authorization; readiness remains blocked.

No Docker image, remote CI, native Windows/OpenCode client, model execution, OS
isolation, production application or copied project's operational adoption was
executed by these reviewers. Legacy compatibility execution is reported by the
quality checker; this review inspected the relevant trust preservation but did
not rerun the entire Copier matrix. Repository protection settings and human
approval were not authenticated. Coverage is limited to the frozen subject and
specified changes, with no claim of exhaustive security proof.
