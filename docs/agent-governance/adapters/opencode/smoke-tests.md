# OpenCode native discovery evidence

The portable smoke runs the actual OpenCode **1.19.0** executable against a
temporary fixture and a canned localhost OpenAI-compatible provider. It sends no
request to a real model and uses no model or host credentials. Linux and Windows
are separate observations; a Linux result does not establish Windows behavior.

Run from the repository root with Python 3.12 and Git available:

```sh
python -m unittest discover -s .engineering-backbone/tst -t .engineering-backbone -p 'test_opencode_native_smoke.py' -v
python .engineering-backbone/src/opencode_native_smoke.py --report artifacts/opencode-native/report.json
```

`--archive PATH` may reuse a downloaded release archive. Its exact pinned SHA-256
is checked before extraction or execution. An arbitrary executable path is not
accepted. Native subprocesses have a 60-second default timeout (maximum 120),
bounded output and process-tree cleanup. Downloads, archive contents and local
provider requests are bounded. Extraction accepts only one regular root binary;
links, extra members and path traversal fail. The workflow runs both supported
x64 platforms and uploads the report even when the smoke fails.

## Pins and fixture

The release is `v1.19.0`, source commit
`733b2c627e5aec39cb33cc22373bdce33053ef2c` in
[anomalyco/opencode](https://github.com/anomalyco/opencode/tree/733b2c627e5aec39cb33cc22373bdce33053ef2c).
The checked archive digests are:

| Platform | Archive | SHA-256 |
| --- | --- | --- |
| Linux x64 | `opencode-linux-x64.tar.gz` | `7bb9e61ad6feacf2e89c10a6a2c1840e3de4220bb50ba1fc7110f31806076aec` |
| Windows x64 | `opencode-windows-x64.zip` | `17108e9448c4fdad48eb8714c4ed6f5dfc9cf86c2eb8f2ce5d02043fef806eb5` |

The smoke copies the actual root native configuration, all explicit instruction
files, five role files and eight skill files into a temporary Git repository.
Markdown instruction copies and the selected reviewer receive distinctive smoke
markers; JSON instructions remain unchanged. Source and fixture byte hashes are
both recorded. A nested `AGENTS.md` adds a separate marker. No candidate plugins,
hooks, package scripts or extra native configuration layers are copied.

HOME, XDG and Windows user-data directories point into temporary storage. The
environment is an allowlist of basic operating-system variables, with host
credentials, native overrides and Git overrides omitted. OpenCode runs with
`OPENCODE_PURE`, model fetching and auto-update disabled. The provider is an
explicit smoke-only configuration overlay with a localhost URL and a dummy key.
Proxy/registry restrictions reduce accidental network access; they are **not an
operating-system sandbox**. Reports contain input/command hashes and bounded
errors, rather than full native configuration or provider transcripts.

## Required native observations

1. The executable reports the exact pinned version. Native `debug agent` discovers
   all five named primary roles. Planner, reviewer and triage have bash, edit,
   write and task disabled in the native tool view.
2. Actual `run --agent backbone-reviewer` calls from root and nested working
   directories send every explicit instruction's fixture bytes plus the selected
   reviewer marker to the local provider. The nested case also carries its local
   instruction marker. Each successful observation must come from one complete
   selected-agent request, not a union of unrelated requests.
3. The canned provider requests an actual `write` tool call that was not advertised
   to the read-only reviewer. The subsequent native tool result must contain a
   refusal/error tied to that exact tool-call ID, and the protected file must be
   unchanged. An unchanged file by itself is insufficient evidence.
4. A missing-role `debug agent` preflight exits 1 without a provider inference
   request. The wrapper does not dispatch `run` after the failure. This matters
   because a direct unknown-agent run can otherwise select a default agent.

The report records actual commands, working directories, exit codes, output hashes,
duration, archive and binary hashes, source/fixture hashes, per-case evidence and
failures. The expected missing-role exit 1 is recorded as a passed negative case.
Unit tests validate that missing markers, incomplete requests, unchanged-file-only
claims, unrelated tool replies, advertised writes, timeouts and archive hazards
cannot produce a passing smoke result.

## Qualification and current evidence

This is native discovery and a narrow tool-boundary smoke. It does not establish
real-model instruction compliance, complete workflow behavior, OS confinement,
native compaction, resume or delegated-role behavior. It does not activate the
adapter or qualify any AO model/runtime/interface tuple. Those require the separate
reviewed runner qualification contract and actual evidence for every declared case.

Fresh reports and CI artifacts identify their own source inputs. Historical reports
lost during workspace cleanup do not certify reconstructed code. A platform is
pending until its actual native job completes; the presence of this workflow or a
passing unit test is not native-platform evidence.
