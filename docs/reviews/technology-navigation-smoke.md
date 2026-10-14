Snapshot: first repair `4722d46e220ee34fb649c787d19f75f77447ca0b`. Later source-only correction and updated-guide follow-up evidence are recorded separately.

# Repaired navigation explicit-context smoke — 2026-10-14

## Bounded result

This separate smoke covers the repaired context omission (`TNAV-B-1` / `TNAV-S-1`) and retention of approved effective check definitions (`TNAV-S-2`). It does not replace independent Delta review or establish application/native-runtime behavior.

A new `fork_turns=none` quality-checker received only candidate/base/request/receipt/tool paths and a read-only output contract, with no expected project/check answer values. It independently verified the receipt (exit 0), actually read all **28 selected documents / 129,240 bytes**, and recomputed matching byte hashes for **28/28**. Both required `.engineering-backbone/project.json` and `.engineering-backbone/core.json` were included automatically.

Guard SHA-256: `32d818cbe4acab3c94de68aa89f27c587be355689fcab6870105544d0107ffd3`.
Receipt embedded context digest: `fe2403ff298a4bdcda3030e361f34ea5411c53f6504461de10fe7bc3948bdedf`.
Receipt file SHA-256: `953a045bca8b4a18165fa2192938b053ed01523c08679e1bd3ffcce6c0413f11`.

The receiver observed project `navigation-repair-fixture`, base branch `integration`, language `Python/PostgreSQL`, backend enabled, frontend disabled, Codex enabled and Copilot disabled. It read the declared validation command `python -m unittest discover -s backend_tests -v` but did not run it. It also read and reported all seven machine-readable core invariants: human merge/release and independent review required; triage before fix; Delta after fix; local policy only strengthens; automatic downstream apply false.

## Approved effective definitions

Resolve and verify ran with the separate trusted-base fixture. The receiver independently compared all four selected receipt checks (`lint`, `migration`, `test`, `typecheck`) with base and candidate declarations. Every selected definition equals the approved base. Candidate migration differs in `argv`, `cwd` and `timeout_seconds`; the receipt retains the full approved definition.

| Field | Approved base / receipt / prepared workflow | Candidate migration |
|---|---|---|
| ID / kind | `migration` / `migration` | `migration` / `migration` |
| argv | repository `.venv/bin/python`, `-c`, `raise SystemExit(31)` | `python`, `-c`, `raise SystemExit(71)` |
| cwd | `.` | `docs` |
| timeout | 5 seconds | 19 seconds |
| phases | `pr` | `pr` |

The captured workflow tool's `prepare` command exited 0. Its complete migration definition equals both the receipt and approved base, and differs from the candidate. This prepared configuration was **not executed**. Exact command arrays and outputs are in `structural-result.json` and adjacent stdout/stderr files. Broader kind/phase abuse coverage belongs to the separate repaired regression suite, not this narrow smoke.

## Mandatory project-fact tamper

The harness copied the candidate and changed only the required project's `base_branch` to another valid string. Scripted verification and the fresh receiver's independent invocation both rejected the unchanged receipt with exit 1:

```
Quality framework: Navigation: Navigation: Handoff context differs from recomputed snapshot
```

The receiver explicitly declined using the altered context, performed no repair and did not read further context from the rejected root.

## Grounded decision and limits

The receiver grounded a hypothetical query-boundary review in actual read documents: require parameter binding, validated/documented Python boundaries, and relevant lint/typecheck/behavior/real-PostgreSQL integration/data-preserving migration evidence. It retained internal decomposition, algorithms and schema/index freedom within accepted contracts. The fixture itself authorized no implementation or application execution.

The fixture revision `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` remains a declaration, not authenticated Git identity. Quality declaration documents are placeholders, traceability is planned, and no wider acceptance PASS is implied. Native Codex/Copilot discovery remains unverified. The earlier Codex startup limitation is retained; the unchanged failed client was not rerun.

All **150** files in the previous `artifacts/navigation-smoke/` evidence set remain byte-identical, with no additions. This smoke wrote only under `artifacts/navigation-repair-smoke/`; no tracked edits or commits.

## Evidence

- `structural-result.json`: exact guard/prepare invocations, exits, hashes and full compared definitions.
- `explicit-context-result.json`: fresh receiver's actual read/hash/decision/rejection observations.
- `context.json`, `request.json`, `tooling/`: captured receipt/request and tools.
- `previous-smoke-preservation.json`: preserved previous evidence check.
- `prepare_fixture.py`, `run_guard_checks.py`: bounded repeatable fixture/check harnesses.
