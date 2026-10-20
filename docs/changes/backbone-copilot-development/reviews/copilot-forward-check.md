# Copilot skill instruction forward check

Date: 2026-10-12. This is an isolated instruction-usability experiment with a
fresh local AI session; it is **not actual Copilot client/provider execution**.

## Inputs and binding

- Skill: `.github/skills/bug-reproduction/SKILL.md`, Git blob `1d5294ab7d5335c5e90127d896e824ad2016ba75`.
- Raw fixture base: `057a0893793d8cd631f5834e92637047842d1521`; accepted README contract and scoped task packet.
- Source input:

```python
def chunk_items(items, size):
    if size <= 0:
        raise ValueError('size must be positive')
    return [items[index:index + size] for index in range(0, len(items) - size, size)]
```

Accepted behavior preserves all input elements exactly once in order, with each
chunk at most `size`, without mutating the input. Empty returns empty; nonpositive
size raises ValueError. Caller reported missing elements for some sizes.

The fresh session received the skill, raw source/contract and task packet only.
It did not receive the suspected cause, intended fix or expected reviewer output.
Implementation edits and external publishing were forbidden; test/evidence writes
in the disposable fixture were authorized.

## Actual observation

The session created boundary tests and ran
`python -m unittest discover -s tests -v` once. Exit **1**, three tests with five
failing cases: exact-size, below-size, remainder and exact-multiple inputs lose
final groups. Minimal reproducer: `chunk_items([1], 1)` returns `[]` instead of
`[[1]]`. Empty input, source input preservation and nonpositive-size cases passed.
The implementation source remained byte-identical to its fixture HEAD; no fix,
Full/Delta, commit or publication was claimed.

The outcome supports that this procedure can guide a scoped reproduction with
real failure evidence and useful regression coverage. It does not prove automatic
skill discovery, host tool permissions, reviewer independence, GitHub review or
human approval. Native client tests remain in
[the smoke checklist](../copilot/smoke-tests.md). No source-project code was changed.
