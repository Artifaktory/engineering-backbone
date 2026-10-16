# Initial OpenCode PR remote checks

Date: 2026-10-16. Task: BB-OPENCODE-010. Responsibility: read-only remote
verification and durable evidence reporting, separate from implementation and
finding triage.

**All five CI jobs on the initial published head completed successfully. Codex
reported a new P1 finding, separately confirmed as REC-BB-REMOTE-001; its repair,
verification and independent Delta remain pending at this report's cutoff.**
Successful CI does not close that finding or establish completion of all review
gates. This record remains bound to the original published snapshot below; it is
not evidence for any later repair head.

## Immutable publication binding

- PR: [Artifaktory/engineering-backbone#16](https://github.com/Artifaktory/engineering-backbone/pull/16).
- Remote head: `f22ef07ef018f41f487450465b757b658da6b396`.
- Equivalent local head: `a821da64c3468ebafe0e8586fc669b062b408907`.
- Identical tree: `ee1db8863633bc54765b32aa15e0a03a0452f57b`.
- Base: `bf8e901ecd066e8e6d1b05f0c56a66081a473c0a`.
- Binary base-to-head patch SHA-256:
  `86fc9df30fde86df576fc8aa0e68724b2f224464b4c4f048545b31e6d5104366`.

Inspected the actual GitHub PR, workflow/job results, decoded completed-job logs,
review submission and inline thread. Rechecked the PR head/base at the end of
remote observation: unchanged, open, not merged. Independently checked both Git
commit objects' trees and base-to-head binary patch hashes locally; both match
the binding above. Distinct commit IDs are not presented as identical commits.

The visible [Codex request, comment 6213303592](https://github.com/Artifaktory/engineering-backbone/pull/16#issuecomment-6213303592)
specified this exact base, head, tree and patch digest. The bot's completed review
is attached to that head.

## Actual remote CI results

Both workflow runs completed with conclusion `success`:
[OpenCode native discovery 38886264680](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264680)
and [Backbone quality 38886264984](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264984).

| Job | Job ID | Actual conclusion and observed execution |
| --- | --- | --- |
| Native smoke, Ubuntu | [116924637655](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264680/job/116924637655) | Success; 11 smoke-runner unit tests and the actual pinned native smoke passed; report uploaded and inspected. |
| Native smoke, Windows | [116924636668](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264680/job/116924636668) | Success; 11 smoke-runner unit tests and the actual Windows native smoke passed; report uploaded and inspected. |
| Trusted base policy | [116924637691](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264984/job/116924637691) | Success; the base-owned validator reported structural PASS against the candidate. |
| Source dependencies and container | [116924638005](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264984/job/116924638005) | Success; locked source environment/input checks, actual tracked Dockerfile build and offline container checks passed, including 13 real Copier tests. |
| Foundation governance and compatibility | [116924638199](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264984/job/116924638199) | Success; source validation, four compiler checks, complete unittest discovery and committed-patch whitespace check passed. Full suite: 414 tests, 459.640 seconds, `OK`. |

The Foundation log records `python -m unittest discover -s tests -v`, not a
selected subset. Its consumer-only steps were skipped by the workflow's existing
source-mode conditions; they are not claimed as independently executed steps.
No tests, timeouts or job conditions were changed by this verification session.

The container log records these actual commands:

```sh
docker build --pull --tag backbone-tooling:check --file Dockerfile .
docker run --rm --network none backbone-tooling:check sh -eu -c '
  python scripts/validate.py
  python scripts/compile_navigation.py --check
  python scripts/compile_quality_framework.py --check
  python scripts/compile_workflow_kit.py --check
  python scripts/compile_toolchain_fingerprint.py --check
  python -m unittest tests.test_copier -v
'
```

The build produced image
`sha256:ca8487ab8774f549443b3aef268d63aa5b1da05f4b7e569e755b885f0a6b39b6`.
Offline structural/compiler checks passed; the container's real Copier suite
reported **13 tests in 50.331 seconds, OK**. This supplies the remote container
execution missing from the local environment; it is not an OS-confinement claim
for OpenCode.

## Actual native reports and provenance

Downloaded the uploaded ZIP artifacts, checked each ZIP SHA-256 against GitHub's
artifact digest, and read its actual `report.json`. Artifact metadata binds both
uploads to run 38886264680 and remote head `f22ef07...`.

| Evidence | Linux | Windows |
| --- | --- | --- |
| Uploaded artifact | [12040075105](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264680/artifacts/12040075105) | [12039618778](https://github.com/Artifaktory/engineering-backbone/actions/runs/38886264680/artifacts/12039618778) |
| ZIP SHA-256 | `29a98e19dfdf7b21b70164a8bd33c1dd8580afb09e90268ae8b09d1aaceca24d` | `140b1dcedcda964002fb0a8a7d0f94fda989e11eb863a0553cd2b5fea24efd17` |
| Original report.json SHA-256 | `a69f3ca8d4db181455d628b9bcad4e69941dcd84ff583dbf60132fb4d1484ffd` | `8d6368e9ed2f227164124b28b1a730e4027c46cbfb49012d813cbf37c0bcbc66` |
| Reported platform/architecture | Linux / x86_64 | Windows / amd64 |
| Actual runtime version | 1.19.0 | 1.19.0 |
| Native smoke duration | 21.614 seconds | 36.438 seconds |
| Recorded commands / local provider requests | 11 / 4 | 11 / 4 |
| Report status | passed | passed |

These report hashes identify the original unmodified ZIP-entry bytes, not a
reserialized JSON representation. They are distinct from the source-input and
runner hashes inside each report.

For Linux, independently compared all 22 `inputs.*.source_sha256` values and the
runner hash with SHA-256 of the **raw Git blobs** at exact remote head `f22ef07...`:
all matched. The runner hash is
`e48b6f3bbb51e489151764e5dec49eff0d7128d2f496f92e40c9edd365220376`.

For Windows, independently calculated the ordinary **LF-to-CRLF checkout
transformation of those same exact Git blobs** and then hashed the transformed
bytes. All 22 source-input hashes and the runner hash matched this transformation.
The Windows runner hash is
`d8dbee7a710b1e7ecfa7c6a396bc6404c6070aaba3f818755a89791c27ef82c0`.
This establishes the observed Windows checkout's correspondence to the published
source; it does **not** assert byte identity with the raw Git blobs or Linux
checkout. The Windows log identifies Microsoft Windows Server 2025 and actual
execution of the native `opencode.exe`; this was not a cross-compilation test.

Both reports identify the pinned OpenCode source commit
`733b2c627e5aec39cb33cc22373bdce33053ef2c` and the expected downloaded release
archive digest: Linux
`7bb9e61ad6feacf2e89c10a6a2c1840e3de4220bb50ba1fc7110f31806076aec`,
Windows
`17108e9448c4fdad48eb8714c4ed6f5dfc9cf86c2eb8f2ce5d02043fef806eb5`.

The native command was
`python scripts/opencode_native_smoke.py --report artifacts/opencode-native/report.json`.
Its actual reports establish, on each platform:

- The observed runtime version is 1.19.0 and all five named roles are primary.
- The actual canned-provider requests contain every declared instruction and the
  selected reviewer marker at project root and in the nested-directory case;
  the nested marker appears in the latter case.
- Missing-role preflight returns the expected exit 1, with zero inference requests
  and no `run` dispatch. That negative-case exit is expected evidence, not a
  successful native role resolution.
- The requested `write` tool is not advertised. The matching tool-call response
  reports the native unavailable-tool error; the target file remains unchanged.
  Unchanged target bytes alone are not used as proof of rejection.

These are instrumented temporary-fixture observations using a canned local
provider. They establish neither real-model qualification nor OS confinement,
native compaction/resume/delegation qualification, host configuration adoption or
AO's separate admission/lifecycle implementation.

## Remote review and open repair obligation

Codex submitted [review 5546404425](https://github.com/Artifaktory/engineering-backbone/pull/16#pullrequestreview-5546404425)
at 2026-10-16T10:25:03Z, state `COMMENTED`, on `f22ef07...`. The completed summary
reported findings and unresolved findings. The sole observed inline finding is
[4293569208](https://github.com/Artifaktory/engineering-backbone/pull/16#discussion_r4293569208),
priority P1, titled “Bind activation to the full reviewed seed,” at
`scripts/navigation.py:522-524`. Its thread was unresolved and not outdated at
the observation cutoff.

The reported trigger is an inactive trusted seed becoming active while native
configuration, role prompts or procedure bodies change. Companion-only equality
does not bind the other package inputs to the reviewed seed; hashing candidate
bytes in a receipt does not establish that equality.

The separate [remote finding triage](opencode-reconstruction-triage.md#remote-finding-triage--2026-10-16)
confirmed this as **REC-BB-REMOTE-001, P1**, with independent static inspection and
a bounded data-only reproduction. That triage, rather than this reporting session,
owns the classification and bounded repair requirements. The author is repairing
it separately. The earlier predecessor findings remain closed; this new finding
remains open until repair, fresh checks and independent Delta establish closure.
This report does not independently repeat or claim the triage reproduction.

## Evidence custody and limits

Raw downloaded reports, ZIPs, normalized job logs and API-result summaries remain
outside tracked files in the orchestration workspace's ignored run-evidence
directory. Durable details above omit credentials, temporary download URLs and
raw environment/configuration transcripts. The retained review JSON SHA-256 is
`0b657fe36e5367a18b4d2dcc6254bf8201170cc1d27c7fe6ece0af4569917e78`;
the retained final-state JSON SHA-256 is
`3ea668fa900626c84eeb531f4abdcd4beda0df65c13286ae9ffd85c26c2e386c`.
GitHub's uploaded native artifacts expire on 2026-10-30; original bytes were
retained locally during this verification, with their hashes recorded above.

This session inspected actual remote results and artifact contents; it did not
rerun CI, alter workflow state, reproduce the finding, repair implementation,
change acceptance metadata, submit comments, resolve the thread, commit or write
remote repository state. Only this new durable report was added to the repository.
AO checks/reviews and any later Backbone repair head require their own evidence.
No merge, release, deployment, settings change or downstream activation is
authorized or performed by this record.
